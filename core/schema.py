import asyncio
from typing import AsyncGenerator
import strawberry
from assets.mutations import AssetMutations
from assets.queries import AssetQueries
from projects.mutations import ProjectMutations

from projects.queries import ProjectQueries
from users.mutations import UserMutations
from users.queries import UserQueries

@strawberry.type
class Query(ProjectQueries, AssetQueries, UserQueries):
    pass


@strawberry.type
class Mutation(ProjectMutations, AssetMutations, UserMutations):
    pass

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
