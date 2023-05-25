from sqlmodel import Session
import strawberry
from assets.models import Image
from common.types import Success
from .types import ImageType

from assets.types import ImageInput
from core.settings import Setting


@strawberry.type
class AssetMutations:
    @strawberry.field
    async def new_image(self, input: ImageInput) -> Success[ImageType]:
        with Session(Setting().DB_ENGINE) as session:
            image = await Image.new(session=session, input=input)
            return Success(success=True, data=image.gql())
