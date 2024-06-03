use async_graphql::{EmptyMutation, EmptySubscription, MergedObject, Object, Schema};

#[derive(Default)]
struct RootQuery;

#[Object]
impl RootQuery {
    async fn version(&self) -> String {
        String::from("0.0.1")
    }
}

#[derive(MergedObject, Default)]
pub struct Query(RootQuery);

pub type AppSchema = Schema<Query, EmptyMutation, EmptySubscription>;

pub fn build_schema() -> AppSchema {
    AppSchema::build(Query::default(), EmptyMutation, EmptySubscription).finish()
}
