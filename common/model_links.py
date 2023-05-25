from typing import Optional
from sqlmodel import SQLModel, Field

class ImageProjectLink(SQLModel, table=True):
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    image_id: Optional[int] = Field(default=None, foreign_key="image.id", primary_key=True)
