use std::env;

pub struct Settings;

impl Settings {
    pub fn expect_env_var(name: &str) -> String {
        env::var(name).unwrap_or_else(|_| panic!("Environment Variable {} is not set", name))
    }
    pub fn ip_address() -> String {
        Settings::expect_env_var("IP_ADDRESS")
    }

    pub fn port() -> u16 {
        Settings::expect_env_var("PORT")
            .parse()
            .expect("PORT should be a valid u16")
    }
}
