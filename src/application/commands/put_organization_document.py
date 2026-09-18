from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import OrganizationDocumentSlot
from src.application.domain.exceptions import ApplicationException
from src.application.domain.organization_documents import ORGANIZATION_DOCUMENT_TYPES
from src.infrastructure.database.decorators import transactional
from src.infrastructure.storage.s3_documents_service import S3DocumentsService


class PutOrganizationDocumentCommand:
    def __init__(
        self,
        unit_of_work: IUnitOfWork,
        s3_service: S3DocumentsService,
        logger: ILogger,
    ):
        self._unit_of_work = unit_of_work
        self._s3 = s3_service
        self._logger = logger

    @transactional
    async def __call__(
        self,
        *,
        organization_id: str,
        document_type: str,
        file_name: str,
        content_type: str,
        body: bytes,
    ) -> OrganizationDocumentSlot:
        if document_type not in ORGANIZATION_DOCUMENT_TYPES:
            raise ApplicationException(status_code=400, message='Invalid document type')

        if not body:
            raise ApplicationException(status_code=400, message='File is empty')

        await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        old_s3_key = await self._unit_of_work.legal_entity_repository.get_document_s3_key(
            organization_id,
            document_type,
        )

        new_s3_key = self._s3.build_object_key(organization_id, document_type, file_name)
        await self._s3.upload_bytes(key=new_s3_key, body=body, content_type=content_type)

        try:
            await self._unit_of_work.legal_entity_repository.set_document_s3_key(
                organization_id,
                document_type,
                new_s3_key,
            )
            await self._unit_of_work.commit()
        except Exception:
            await self._unit_of_work.rollback()
            await self._s3.delete_object(key=new_s3_key)
            raise

        if old_s3_key and old_s3_key != new_s3_key:
            await self._s3.delete_object(key=old_s3_key)

        self._logger.info(
            f'Document uploaded org={organization_id} type={document_type} key={new_s3_key}'
        )
        return OrganizationDocumentSlot(
            organization_id=organization_id,
            document_type=document_type,
            s3_key=new_s3_key,
            file_name=self._s3.file_name_from_key(new_s3_key),
            content_type=content_type,
            file_size_bytes=len(body),
        )
