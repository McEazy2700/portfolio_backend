from graphql import GraphQLError
from core.context import Info

def login_required(info: Info):
    if not info.context.user:
        raise GraphQLError("You must be authorized to perform this action")
