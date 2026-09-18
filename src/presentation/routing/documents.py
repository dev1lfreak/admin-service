from fastapi import APIRouter, Depends, File, UploadFile

from src.application.commands import (
    GetOrganizationDocumentCommand,
    ListOrganizationDocumentsCommand,
    PutOrganizationDocumentCommand,
)
from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access, require_admin_role
from src.presentation.dependencies.commands import (
    get_get_organization_document_command,
    get_list_organization_documents_command,
    get_put_organization_document_command,
    get_s3_documents_service,
)
from src.infrastructure.storage.s3_documents_service import S3DocumentsService
from src.presentation.schemas.mappers import document_to_response
from src.presentation.schemas.organization import DocumentResponse

documents_router = APIRouter(prefix='/organizations/{organization_id}/documents', tags=['documents'])


async def _document_download_url(s3: S3DocumentsService, s3_key: str | None) -> str | None:
    if not s3_key:
        return None
    return await s3.generate_presigned_download_url(key=s3_key)


@documents_router.get('', response_model=list[DocumentResponse])
async def list_documents(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListOrganizationDocumentsCommand = Depends(get_list_organization_documents_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    docs = await command(organization_id)
    result: list[DocumentResponse] = []
    for doc in docs:
        url = await _document_download_url(s3, doc.s3_key)
        result.append(document_to_response(doc, download_url=url))
    return result


async def _put_document(
    *,
    organization_id: str,
    document_type: str,
    file: UploadFile,
    command: PutOrganizationDocumentCommand,
    s3: S3DocumentsService,
) -> DocumentResponse:
    body = await file.read()
    saved = await command(
        organization_id=organization_id,
        document_type=document_type,
        file_name=file.filename or 'document',
        content_type=file.content_type or 'application/octet-stream',
        body=body,
    )
    url = await _document_download_url(s3, saved.s3_key)
    return document_to_response(saved, download_url=url)


@documents_router.put('/charter', response_model=DocumentResponse)
async def put_charter_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='charter',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.put('/inn-certificate', response_model=DocumentResponse)
async def put_inn_certificate_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='inn_certificate',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.put('/ogrn-certificate', response_model=DocumentResponse)
async def put_ogrn_certificate_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='ogrn_certificate',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.put('/bank-details', response_model=DocumentResponse)
async def put_bank_details_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='bank_details',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.put('/kyc-representative', response_model=DocumentResponse)
async def put_kyc_representative_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='kyc_representative',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.put('/power-of-attorney', response_model=DocumentResponse)
async def put_power_of_attorney_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='power_of_attorney',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.put('/other', response_model=DocumentResponse)
async def put_other_document(
    organization_id: str,
    file: UploadFile = File(...),
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: PutOrganizationDocumentCommand = Depends(get_put_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _put_document(
        organization_id=organization_id,
        document_type='other',
        file=file,
        command=command,
        s3=s3,
    )


@documents_router.get('/charter', response_model=DocumentResponse)
async def get_charter_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'charter', command, s3)


@documents_router.get('/inn-certificate', response_model=DocumentResponse)
async def get_inn_certificate_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'inn_certificate', command, s3)


@documents_router.get('/ogrn-certificate', response_model=DocumentResponse)
async def get_ogrn_certificate_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'ogrn_certificate', command, s3)


@documents_router.get('/bank-details', response_model=DocumentResponse)
async def get_bank_details_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'bank_details', command, s3)


@documents_router.get('/kyc-representative', response_model=DocumentResponse)
async def get_kyc_representative_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'kyc_representative', command, s3)


@documents_router.get('/power-of-attorney', response_model=DocumentResponse)
async def get_power_of_attorney_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'power_of_attorney', command, s3)


@documents_router.get('/other', response_model=DocumentResponse)
async def get_other_document(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationDocumentCommand = Depends(get_get_organization_document_command),
    s3: S3DocumentsService = Depends(get_s3_documents_service),
):
    return await _get_document(organization_id, 'other', command, s3)


async def _get_document(
    organization_id: str,
    document_type: str,
    command: GetOrganizationDocumentCommand,
    s3: S3DocumentsService,
) -> DocumentResponse:
    doc = await command(organization_id, document_type)
    url = await _document_download_url(s3, doc.s3_key)
    return document_to_response(doc, download_url=url)
