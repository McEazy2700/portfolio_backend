from typing import TYPE_CHECKING, List, Optional, Self
from graphql import GraphQLError
from sqlmodel import Field, Relationship, SQLModel, Session, col, select
from cloudinary.uploader import upload_image
from common.model_links import ImageProjectLink

from assets.types import ImageInput, ImageFilter
from common.types import TotalList, PageOptions
from common.utils.graphql import model_to_graphql

if TYPE_CHECKING:
    from projects.models import Project
    from .types import ImageType

IMAGE_FIELDS = ["id", "url", "description", "projects"]

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    description: str
    public_id: str
    projects: List["Project"] = Relationship(back_populates="images", link_model=ImageProjectLink)
    profile: Optional["Profile"] = Relationship(
            back_populates="image", sa_relationship_kwargs=dict(uselist=False))

    @classmethod
    async def new(cls, session: Session, input: ImageInput) -> Self:
        assert input.file, GraphQLError("file is required for new_image")
        assert input.description, GraphQLError("description is required for new_image")
        file = await input.file.read() #type: ignore
        res = upload_image(file, folder="vice")
        image = cls(
                url=res.url,
                description=str(input.description),
                public_id=str(res.public_id)
            )
        session.add(image)
        session.commit()
        session.refresh(image)
        return image


    @classmethod
    def get(cls, session: Session, id: int | str) -> Self:
        stmt = select(cls).where(cls.id==id)
        image = session.exec(stmt).one()
        return image


    @classmethod
    def filter(cls, session: Session, options: Optional[PageOptions[ImageFilter]]=None) -> TotalList[Self]:
        stmt = select(cls)
        total = len(session.exec(stmt).all())
        if options: stmt = stmt.limit(options.limit).offset(options.offset)
        if options and options.filter and options.filter.description:
            stmt = stmt\
                .where(col(cls.description).contains(options.filter.description))
        values = session.exec(stmt).all()
        return TotalList(total=total, values=values)

    @classmethod
    def all(cls, session: Session) -> List[Self]:
        stmt = select(cls)
        images = session.exec(stmt).all()
        return images

    def update(self, input: ImageInput|None=None) -> Self:
        if input:
            if input.file: upload_image(input.file, public_id=self.public_id)
            if input.description: self.description = input.description
        return self

    def gql(self) -> "ImageType":
        from .types import ImageType
        return model_to_graphql(ImageType, self, IMAGE_FIELDS)

from users.models import Profile
