class Settings:
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "currency_user"
    DB_PASS: str = "0000"
    DB_NAME: str = "currency_exchange"

    @property
    def DATA_BASE_URL(self):
        # "postgresql+asyncpg://currency_user:0000@localhost:5432/currency_exchange"
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
