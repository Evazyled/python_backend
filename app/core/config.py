


from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL:str
    redis_url : str
    cors_allowed_origin:list[str]
    cache_ttl_seconds : int
    cache_tasks_key :str

def get_settings():
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:admin@postgres:5432/postgres",#если локально. то postgres->localhost
        redis_url = "redis://redis:6379/0",#если локально. то redis->localhost
        cors_allowed_origin=["http://localhost:3000"],
        cache_ttl_seconds= 3600,
        cache_tasks_key = 'cache:tasks_list'
    )