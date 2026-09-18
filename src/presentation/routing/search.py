from fastapi import APIRouter, Depends, Query

from src.application.commands import (
    SearchPartiesCommand,
)
from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access
from src.presentation.dependencies.commands import (
    get_search_parties_command,
)
from src.presentation.schemas.mappers import (
    party_search_to_response,
)
from src.presentation.schemas.entity import (
    PartySearchListResponse,
)

search_router = APIRouter(prefix='/search', tags=['search'])

@search_router.get('', response_model=PartySearchListResponse)
async def search_parties(
    q: str = Query(min_length=1, max_length=255),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: SearchPartiesCommand = Depends(get_search_parties_command),
):
    items, total = await command(query=q, limit=limit, offset=offset)
    return PartySearchListResponse(
        items=[party_search_to_response(x) for x in items],
        total=total,
    )