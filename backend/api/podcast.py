from fastapi import APIRouter
from core.user import UserFinancialProfile
from core.podcast import PodcastService, PodcastResponse

router = APIRouter(prefix="/podcasts", tags=["podcasts"])


@router.post("/podcast", response_model=PodcastResponse)
async def generate_podcast(context: UserFinancialProfile):
    podcast_service = PodcastService()
    return await podcast_service.generate_podcast(context)
