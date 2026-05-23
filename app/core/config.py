from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config= SettingsConfigDict(
        env_file= ".env",
        extra= "ignore"
    )
    APPNAME: str = "Books Store"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_DAYS:int

    DATABASE_URL:str
    SUPABASE_DATA_API_URL:str
    SUPABASE_ANON_KEY:str
    SUPABASE_SERVICE_ROLE_KEY:str

@lru_cache()
def get_settings() -> Settings:
    return Settings() # type: ignore
settings = get_settings()
