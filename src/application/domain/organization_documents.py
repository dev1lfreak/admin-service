from __future__ import annotations

ORGANIZATION_DOCUMENT_TYPES: tuple[str, ...] = (
    'charter',
    'inn_certificate',
    'ogrn_certificate',
    'bank_details',
    'kyc_representative',
    'power_of_attorney',
    'other',
)

DOCUMENT_TYPE_TO_COLUMN: dict[str, str] = {
    'charter': 'charter_s3_key',
    'inn_certificate': 'inn_certificate_s3_key',
    'ogrn_certificate': 'ogrn_certificate_s3_key',
    'bank_details': 'bank_details_document_s3_key',
    'kyc_representative': 'kyc_representative_s3_key',
    'power_of_attorney': 'power_of_attorney_s3_key',
    'other': 'other_document_s3_key',
}

DOCUMENT_TYPE_URL_SLUGS: dict[str, str] = {
    'charter': 'charter',
    'inn_certificate': 'inn-certificate',
    'ogrn_certificate': 'ogrn-certificate',
    'bank_details': 'bank-details',
    'kyc_representative': 'kyc-representative',
    'power_of_attorney': 'power-of-attorney',
    'other': 'other',
}

URL_SLUG_TO_DOCUMENT_TYPE: dict[str, str] = {
    slug: document_type for document_type, slug in DOCUMENT_TYPE_URL_SLUGS.items()
}
