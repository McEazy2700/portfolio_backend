from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Self
from graphql import GraphQLError
from sqlmodel import Field, Relationship, SQLModel, Session, col, select
from common.model_links import ImageProjectLink
from common.types import PageOptions, TotalList

from projects.types import ProjectInput
from common.utils.graphql import model_to_graphql

if TYPE_CHECKING:
    from assets.models import Image
    from .types import ProjectType

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    github: Optional[str] = Field(default=None)
    live_url: Optional[str] = Field(default=None)
    date_added: datetime = Field(default=datetime.now())
    images: List["Image"] = Relationship(back_populates="projects", link_model=ImageProjectLink)

    @classmethod
    def new(cls, session: Session, input: ProjectInput) -> Self:
        from assets.models import Image

        assert input.title, GraphQLError("title is requred to create project")
        assert input.description, GraphQLError("description is requred to create project")
        project = cls(
                title=input.title,
                github=input.github,
                live_url=input.live_url,
                description=input.description
            )
        if input.image_ids and len(input.image_ids) > 0:
            stmt = select(Image).where(col(Image.id).in_(input.image_ids))
            project.images = session.exec(stmt).all()
        session.add(project)
        session.commit()
        project.images
        session.refresh(project)
        return project

    @classmethod
    def update(cls, session: Session, input: ProjectInput) -> Self:
        if not input.id:
            raise GraphQLError("Id is required for project update")
        project = cls.get(session, id=input.id)
        for key, value in input.__dict__.items():
            if key != "image_ids" and value is not None:
                setattr(project, key, value)
        if input.image_ids and len(input.image_ids) > 0:
            stmt = select(Image).where(col(Image.id).in_(input.image_ids))
            project.images = session.exec(stmt).all()
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    @classmethod
    def filter(cls, session: Session, options: Optional[PageOptions]=None) -> TotalList[Self]:
        stmt = select(cls)
        total = len(session.exec(stmt).all())
        if options: stmt.offset(options.offset).limit(options.limit)
        projects = session.exec(stmt).all()
        return TotalList(total=total, values=projects)

    @classmethod
    def get(cls, session: Session, id: int) -> Self:
        stmt = select(cls).where(cls.id==id)
        return session.exec(stmt).one()

    def gql(self) -> "ProjectType":
        from .types import ProjectType
        fields = ["id", "title", "description", "date_added", "images"]
        return model_to_graphql(ProjectType, self, fields)

from assets.models import Image
