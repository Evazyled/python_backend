

from fastapi import APIRouter, Depends,status

from app.api.dependencies import get_task_services
from app.schemas.task import CreateTaskSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskService


router = APIRouter(prefix='/tasks')



@router.get('')
def read_tasks(task_service:TaskService = Depends(get_task_services)) -> list[TaskSchema]:
    return task_service.list_tasks()
    

@router.post('',status_code=status.HTTP_201_CREATED)

def create_task(payload : CreateTaskSchema,task_service:TaskService = Depends(get_task_services)) -> TaskSchema:
    return task_service.create_task(create_task=payload)
    
@router.patch('/{task_id}')
def update_task(task_id:str, payload:TaskUpdateSchema,task_service:TaskService = Depends(get_task_services) ):
    return task_service.update_task(task_id=task_id,task_update=payload)
    


@router.delete('/{task_id}',status_code=status.HTTP_204_NO_CONTENT,)
def delete_task(task_id:str,task_service:TaskService = Depends(get_task_services)):
    return task_service.delete_task(task_id=task_id)