from sqlalchemy.orm import Session

from app.cache.redis import RedisCacheBackend
from app.core.config import get_settings
from app.repositpries.task import TaskRepositories
from app.schemas.task import TaskSchema,TaskUpdateSchema,CreateTaskSchema


settings = get_settings()


class TaskService:
    def __init__(self,db:Session):
        self.db = db
        self.task_repository = TaskRepositories(db)
        self.cache = RedisCacheBackend(settings.redis_url,settings.cache_ttl_seconds)
        



    def list_tasks(self)->TaskSchema:
        # шаг 1 . проверить , есть ли данные в redis
        cached_tasks = self.cache.get(settings.cache_tasks_key)
        if cached_tasks:
            return cached_tasks

        tasks_orm = self.task_repository.get_all() #шаг 2 .идем в бд ,если данных нет в кеше
        
        tasks_read =  [TaskSchema.model_validate(task) for task in tasks_orm]  
        #преобразуем модель базы к питон словарю \model_dump()

        tasks_for_cache = [task.model_dump() for task in tasks_read]
        #шаг 3 сохранить данные в кеш, если данных в кеше нет
        self.cache.set(settings.cache_tasks_key,tasks_for_cache)

        return tasks_read #шаг 4 . вернуть результат
       


    def create_task(self, create_task:CreateTaskSchema)->TaskSchema:
        #Инвалидировать кеш (чтобы он был актуальным)
        self.cache.delete(settings.cache_tasks_key) #очищаем кеш перед манипуляциями, чтобы не было не акутуального списка
        task_orm = self.task_repository.create(title = create_task.title)
        self.db.commit()
        self.db.refresh(task_orm)
        return TaskSchema.model_validate(task_orm)  


    def update_task(self,task_id,task_update:TaskUpdateSchema)->TaskSchema:
        self.cache.delete(settings.cache_tasks_key)
        """task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if task_update.title:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed"""
        self.task_repository.update(task_id=task_id,task_update=task_update)
        self.db.commit()        

    def delete_task(self,task_id: str)->TaskSchema:
        self.cache.delete(settings.cache_tasks_key)
        task_for_delete = self.task_repository.get_by_id(task_id)
        self.task_repository.delete(task_for_delete)
        self.db.commit()

