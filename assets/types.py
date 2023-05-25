from typing import Generic, List, Optional, TypeVar
import strawberry
from strawberry.file_uploads import Upload

T = TypeVar("T")

@strawberry.type
class ImageType:
    url: str
    description: str
    id: strawberry.ID
    projects: Optional[List["ProjectType"]] = None


@strawberry.input
class ImageFilter:
    description: Optional[str] = None


@strawberry.type
class PaginatedList(Generic[T]):
    total: int = strawberry.field(description="the total number of reccords available")
    count: int = strawberry.field(description="the total number of reccords returned")
    data: List[T] = strawberry.field(description="the list of reccords")


@strawberry.input
class ImageInput:
    id: Optional[int] = None
    file: Optional[Upload] = None
    description: Optional[str] = None


from projects.types import ProjectType
