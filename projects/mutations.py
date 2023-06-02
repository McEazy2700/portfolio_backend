from sqlmodel import Session
import strawberry
from common.types import Success
from core.context import Info
from core.settings import Setting
from projects.models import Project

from projects.types import ProjectInput, ProjectType
from common.utils.authorization import login_required


@strawberry.type
class ProjectMutations:
    @strawberry.field
    def create_update_project(self, info: Info, input: ProjectInput) -> Success[ProjectType]:
        login_required(info)
        with Session(Setting().DB_ENGINE) as session:
            if input.id:
                project = Project.update(session=session, input=input).gql()
            else:
                project = Project.new(session=session, input=input).gql()
            return Success(success=True, data=project)
