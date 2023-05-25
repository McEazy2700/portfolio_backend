from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import  GraphQLRouter
from core.context import get_context
from core.schema import schema
from core.settings import Setting

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=Setting().CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
app.include_router(graphql_app, prefix="/graphql")
