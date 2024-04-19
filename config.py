from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    DB_HOST: str
    DB_NAME: str
    DB_PASS: str
    DB_PORT: int
    DB_USER: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DATABASE_URL(self):
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property 
    def REDIS_URL(self): 
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    class ConfigDict:
        env_file = ".env"


settings = Settings()
