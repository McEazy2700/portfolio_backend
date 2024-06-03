use actix_web::{get, middleware, post, web, App, HttpResponse, HttpServer, Result};
use async_graphql::http::{graphiql_plugin_explorer, GraphiQLSource};
use async_graphql_actix_web::{GraphQLRequest, GraphQLResponse};
use dotenv::dotenv;
use migration::{Migrator, MigratorTrait};

use crate::config::{
    database::DB,
    schema::{build_schema, AppSchema},
};
pub mod config;

#[get("/")]
async fn graphiql() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok()
        .content_type("text/html; charset=utf-8")
        .body(
            GraphiQLSource::build()
                .title("Portfolio Backend")
                .plugins(&[graphiql_plugin_explorer()])
                .endpoint("/")
                .finish(),
        ))
}

#[post("/")]
async fn execute_query(
    schema: web::Data<AppSchema>,
    gql_req: GraphQLRequest,
) -> Result<GraphQLResponse> {
    Ok(schema.execute(gql_req.into_inner()).await.into())
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .with_test_writer()
        .init();
    let db_conn = DB::connect().await.expect("Database connection failed");
    Migrator::up(&db_conn, None)
        .await
        .expect("Database migration failed");
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(db_conn.clone()))
            .app_data(web::Data::new(build_schema()))
            .wrap(middleware::Logger::default())
            .service(graphiql)
            .service(execute_query)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
