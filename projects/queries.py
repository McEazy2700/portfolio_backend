import strawberry
from typing import Optional
from sqlmodel import Session
from core.settings import Setting
from projects.models import Project
from common.types import PageOptions
from assets.types import PaginatedList

from projects.types import ProjectType


@strawberry.type
class ProjectQueries:
    @strawberry.field
    def project(self, id: int) -> ProjectType:
        with Session(Setting().DB_ENGINE) as session:
            return Project.get(session=session, id=id).gql()

    @strawberry.field
    def projects(self, options: Optional[PageOptions[None]]=None) -> PaginatedList[ProjectType]:
        with Session(Setting().DB_ENGINE) as session:
            projects = Project.filter(session=session, options=options)
            return PaginatedList(
                total=projects.total,
                count=len(projects.values),
                data=list(map(lambda item: item.gql(), projects.values))
            )

