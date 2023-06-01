from typing import List, Optional
import strawberry


@strawberry.type
class ProjectType:
    id: strawberry.ID
    title: str
    github: Optional[str] = None
    live_url: Optional[str] = None
    description: str
    date_added: str
    images: Optional[List["ImageType"]] = None


@strawberry.input
class ProjectInput:
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_ids: Optional[List[int]] = None
    github: Optional[str] = None
    live_url: Optional[str] = None

from assets.types import ImageType
