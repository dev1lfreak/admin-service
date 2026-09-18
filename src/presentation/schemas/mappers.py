from __future__ import annotations

from src.application.domain.entities.organization import (
    LegalEntityEntity,
    OrganizationDocumentSlot,
    OrganizationWalletEntity,
    PurchaseRequestEntity,
)
from src.application.domain.entities.party_search import (
    PartySearchEntity,
)
from src.application.domain.entities.user import (
    UserEntity,
)
from src.application.domain.entities.order import (
    OrderEntity,
)
from src.presentation.schemas.user import (
    UserResponse,
)
from src.presentation.schemas.organization import (
    DocumentResponse,
    OrganizationResponse,
)
from src.presentation.schemas.entity import (
    CreateWalletsResponse,
    MnemonicResponse,
    PartySearchResponse,
    PurchaseRequestResponse,
    SecretKeyResponse,
    WalletResponse,
)
from src.presentation.schemas.order import (
    OrderResponse,
)


def organization_to_response(entity: LegalEntityEntity) -> OrganizationResponse:
    return OrganizationResponse(
        id=entity.id,
        user_id=entity.user_id,
        name=entity.name,
        short_name=entity.short_name,
        inn=entity.inn,
        ogrn=entity.ogrn,
        kpp=entity.kpp,
        legal_address=entity.legal_address,
        actual_address=entity.actual_address,
        bank_details=entity.bank_details,
        contact_person=entity.contact_person,
        contact_phone=entity.contact_phone,
        status=entity.status,
        kyc_verified=entity.kyc_verified,
        kyc_verified_at=entity.kyc_verified_at.isoformat() if entity.kyc_verified_at else None,
        has_wallets=bool(entity.encrypted_mnemonic),
        created_by=entity.created_by,
        created_at=entity.created_at.isoformat() if entity.created_at else None,
        updated_at=entity.updated_at.isoformat() if entity.updated_at else None,
    )


def party_search_to_response(entity: PartySearchEntity) -> PartySearchResponse:
    return PartySearchResponse(
        id=entity.id,
        account_type=entity.account_type,
        user_id=entity.user_id,
        email=entity.email,
        name=entity.name,
        inn=entity.inn,
        phone=entity.phone,
        status=entity.status,
        kyc_verified=entity.kyc_verified,
        created_at=entity.created_at.isoformat() if entity.created_at else None,
    )


def wallet_to_response(entity: OrganizationWalletEntity) -> WalletResponse:
    return WalletResponse(
        id=entity.id,
        chain=entity.chain,
        address=entity.address,
        derivation_path=entity.derivation_path,
        created_at=entity.created_at.isoformat() if entity.created_at else None,
    )


def create_wallets_to_response(*, wallets: list[OrganizationWalletEntity], mnemonic: str) -> CreateWalletsResponse:
    return CreateWalletsResponse(
        wallets=[wallet_to_response(w) for w in wallets],
        mnemonic=mnemonic,
    )


def mnemonic_to_response(mnemonic: str) -> MnemonicResponse:
    return MnemonicResponse(mnemonic=mnemonic)


def secret_key_to_response(
    *,
    chain: str,
    address: str,
    derivation_path: str,
    private_key: str,
) -> SecretKeyResponse:
    return SecretKeyResponse(
        chain=chain,
        address=address,
        derivation_path=derivation_path,
        private_key=private_key,
    )


def document_to_response(
    entity: OrganizationDocumentSlot,
    *,
    download_url: str | None = None,
) -> DocumentResponse:
    return DocumentResponse(
        organization_id=entity.organization_id,
        document_type=entity.document_type,
        s3_key=entity.s3_key,
        file_name=entity.file_name,
        content_type=entity.content_type,
        file_size_bytes=entity.file_size_bytes,
        download_url=download_url,
    )


def purchase_request_to_response(entity: PurchaseRequestEntity) -> PurchaseRequestResponse:
    return PurchaseRequestResponse(
        id=entity.id,
        organization_id=entity.organization_id,
        status=entity.status,
        usdt_amount=str(entity.usdt_amount),
        rub_amount=str(entity.rub_amount) if entity.rub_amount is not None else None,
        exchange_rate=str(entity.exchange_rate) if entity.exchange_rate is not None else None,
        service_fee_percent=str(entity.service_fee_percent) if entity.service_fee_percent is not None else None,
        comment=entity.comment,
        admin_comment=entity.admin_comment,
        target_wallet_chain=entity.target_wallet_chain,
        target_wallet_address=entity.target_wallet_address,
        tx_hash=entity.tx_hash,
        assigned_to=entity.assigned_to,
        created_at=entity.created_at.isoformat() if entity.created_at else None,
        updated_at=entity.updated_at.isoformat() if entity.updated_at else None,
        completed_at=entity.completed_at.isoformat() if entity.completed_at else None,
    )

def user_to_response(entity: UserEntity) -> UserResponse:
    return UserResponse(
        id=entity.id,
        email=entity.email,
        first_name=entity.first_name,
        middle_name=entity.middle_name,
        last_name=entity.last_name,
        birth_date=entity.birth_date,
        phone=entity.phone,
        passport_data=entity.passport_data,
        inn=entity.inn,
        avatar_link=entity.avatar_link,
        account_type=entity.account_type,
        kyc_verified=entity.kyc_verified,
        is_deleted=entity.is_deleted,
        created_at=entity.created_at.isoformat() if entity.created_at else None,
        updated_at=entity.updated_at.isoformat() if entity.updated_at else None,
        kyc_verified_at=entity.kyc_verified_at.isoformat() if entity.kyc_verified_at else None,
    )


def order_to_response(entity: OrderEntity) -> OrderResponse:
    return OrderResponse(
        order_id=entity.id,
        order_status=entity.status,
        usdt_amount=str(entity.usdt_amount),
        usdt_exchange_rate=str(entity.usdt_exchange_rate) if entity.usdt_exchange_rate is not None else None,
        gas_fee=str(entity.gas_fee) if entity.gas_fee is not None else None,
        total_price=str(entity.total_price) if entity.total_price is not None else None,
        service_fee=str(entity.service_fee) if entity.service_fee is not None else None,
        updated_at=entity.updated_at.isoformat() if entity.updated_at else None,
    )
