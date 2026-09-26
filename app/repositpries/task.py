
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskORM

class TaskRepositories:
    def __init__(self,db:Session):
        self.db=db

    def get_all(self)->None:
        return self.db.scalars(select(TaskORM)).all()


    def get_by_id(self,task_id:str)->TaskORM:
        return self.db.get(TaskORM,task_id)

    def create(self,title:str)->TaskORM:
        new_task = TaskORM(title=title, completed = False)
        self.db.add(new_task)
        
        return new_task

    def update(self,task_id,task_update)->TaskORM:
        task_for_update = self.db.get_one(TaskORM,task_id)
        if task_update.title:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        return task_for_update
    
    def delete(self, TaskORM):
        self.db.delete(TaskORM)
        


  