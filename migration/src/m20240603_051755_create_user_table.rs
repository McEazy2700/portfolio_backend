use chrono::Utc;
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(User::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(User::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(User::Email).string().not_null())
                    .col(ColumnDef::new(User::PasswordHash).string())
                    .col(
                        ColumnDef::new(User::DateAdded)
                            .date_time()
                            .default(Value::ChronoDateTimeUtc(Some(Box::new(Utc::now())))),
                    )
                    .col(
                        ColumnDef::new(User::LastUpdated)
                            .date_time()
                            .default(Value::ChronoDateTimeUtc(Some(Box::new(Utc::now())))),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().if_exists().table(User::Table).to_owned())
            .await
    }
}

#[derive(DeriveIden)]
pub enum User {
    Table,
    Id,
    Email,
    PasswordHash,
    DateAdded,
    LastUpdated,
}
