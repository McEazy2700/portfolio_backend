from typing import List, Optional
from sqlmodel import Session
import strawberry
from common.types import PageOptions
from core.settings import Setting
from projects.models import Project

from projects.types import ProjectType


@strawberry.type
class ProjectQueries:
    @strawberry.field
    def project(self, id: int) -> ProjectType:
        with Session(Setting().DB_ENGINE) as session:
            return Project.get(session=session, id=id).gql()

    def projects(self, options: Optional[PageOptions]=None) -> List[ProjectType]:
        with Session(Setting().DB_ENGINE) as session:
            return list(map(lambda item: item.gql(), Project.filter(session=session, options=options)))

