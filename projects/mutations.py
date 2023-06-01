from sqlmodel import Session
import strawberry
from common.types import Success
from core.settings import Setting
from projects.models import Project

from projects.types import ProjectInput, ProjectType


@strawberry.type
class ProjectMutations:
    @strawberry.field
    def create_update_project(self, input: ProjectInput) -> Success[ProjectType]:
        with Session(Setting().DB_ENGINE) as session:
            if input.id:
                project = Project.update(session=session, input=input).gql()
            else:
                project = Project.new(session=session, input=input).gql()
            return Success(success=True, data=project)
