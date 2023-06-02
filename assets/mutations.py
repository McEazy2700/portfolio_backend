from sqlmodel import Session
import strawberry
from assets.models import Image
from common.utils.authorization import login_required
from common.types import Success
from core.context import Info
from .types import ImageType

from assets.types import ImageInput
from core.settings import Setting


@strawberry.type
class AssetMutations:
    @strawberry.field
    async def new_image(self, info: Info, input: ImageInput) -> Success[ImageType]:
        login_required(info)
        with Session(Setting().DB_ENGINE) as session:
            image = await Image.new(session=session, input=input)
            return Success(success=True, data=image.gql())
