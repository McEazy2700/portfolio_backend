from typing import Optional
from sqlmodel import Session
import strawberry
from assets.models import Image

from assets.types import ImageType, ImageFilter, PaginatedList
from common.types import PageOptions
from core.settings import Setting


@strawberry.type
class AssetQueries:
    @strawberry.field
    def images(self, options: Optional[PageOptions[ImageFilter]]=None) -> PaginatedList[ImageType]:
        with Session(Setting().DB_ENGINE) as session:
            images = Image.filter(session=session, options=options)
            page = PaginatedList(
                total=images.total,
                count=len(images.values),
                data=list(map(lambda x: x.gql(), images.values))
            )
            return page
