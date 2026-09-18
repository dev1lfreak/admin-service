from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import OrganizationDocumentSlot
from src.application.domain.exceptions import ApplicationException
from src.application.domain.organization_documents import ORGANIZATION_DOCUMENT_TYPES
from src.infrastructure.database.decorators import transactional
from src.infrastructure.storage.s3_documents_service import S3DocumentsService


class ListOrganizationDocumentsCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str) -> list[OrganizationDocumentSlot]:
        org = await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        slots: list[OrganizationDocumentSlot] = []
        for document_type in ORGANIZATION_DOCUMENT_TYPES:
            s3_key = org.document_s3_keys.get(document_type)
            slots.append(
                OrganizationDocumentSlot(
                    organization_id=organization_id,
                    document_type=document_type,
                    s3_key=s3_key,
                    file_name=S3DocumentsService.file_name_from_key(s3_key) if s3_key else None,
                )
            )
        return slots


class GetOrganizationDocumentCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str, document_type: str) -> OrganizationDocumentSlot:
        if document_type not in ORGANIZATION_DOCUMENT_TYPES:
            raise ApplicationException(status_code=400, message='Invalid document type')

        org = await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        s3_key = org.document_s3_keys.get(document_type)
        if not s3_key:
            raise ApplicationException(status_code=404, message='Document not uploaded')

        return OrganizationDocumentSlot(
            organization_id=organization_id,
            document_type=document_type,
            s3_key=s3_key,
            file_name=S3DocumentsService.file_name_from_key(s3_key),
        )
