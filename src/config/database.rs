use std::env;

use sea_orm::{ConnectOptions, Database, DatabaseConnection, DbErr};

pub struct DB;

impl DB {
    pub async fn connect() -> Result<DatabaseConnection, DbErr> {
        let db_url = env::var("DATABASE_URL").expect("DATABASE_URL env variable should be set");
        let mut opts = ConnectOptions::new(db_url);
        opts.sqlx_logging(true)
            .sqlx_logging_level(log::LevelFilter::Info);
        let conn = Database::connect(opts).await?;
        Ok(conn)
    }
}
