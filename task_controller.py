"""Import Libs"""
import os
import tensorflow as tf
from tensorflow import keras
from fastapi import APIRouter, HTTPException, status
from starlette.responses import RedirectResponse
from models import Task

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

router = APIRouter()
tasks_list = []

@router.get('/')
def get_home():
    """Get Task List"""
    response = RedirectResponse(url='/docs')
    return response

@router.get('/taskslist')
def get_taskslist():
    """Get Task List"""
    return tasks_list

@router.get('/tasks')
def get_tasks():
    """Get Task"""
    if len(tasks_list) > 0:

        for task_item in tasks_list:

            if task_item["id"]==len(tasks_list):

                model_path = 'DMSNR_Curve_model.h5'

                # Load Tensorflow model
                model = keras.models.load_model(model_path)

                start = int(task_item["start"])
                end = int(task_item["end"])
                iter_num = int(task_item["iter_num"])

                padded = tf.linspace(start, end, iter_num)

                msj = (model.predict(padded)).tolist()

                break
        else:
            msj = HTTPException(status_code=404,detail="Task not found")

    else:
        msj = HTTPException(status_code=404,detail="Task empty")

    return msj

@router.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_tasks(task_object: Task):
    """Insert Task"""   

    start = int(task_object.start)
    end = int(task_object.end)
    iter_num = int(task_object.iter_num)

    new_task = {"id": len(tasks_list)+1, "start": start, "end": end, "iter_num": iter_num}

    tasks_list.append(new_task)

    return {"message": "Task created successfully"}

@router.put('/tasks/{task_id}', status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
def update_tasks(task_id:int, task_object: Task):
    """Update Task"""
    for task_item in tasks_list:

        if task_item["id"]==task_id:

            task_item["start"] = task_object.start
            task_item["end"] = task_object.end
            task_item["iter_num"] = task_object.iter_num

            msj = {"message": "Task updated successfully"}

            break
    else:
        msj = HTTPException(status_code=404,detail="Task not found")

    return msj

@router.delete('/tasks/{task_id}', status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
def delete_tasks(task_id:int):
    """Delete Task"""
    for task_item in tasks_list.copy():

        if task_item["id"]==task_id:

            tasks_list.remove(task_item)

            msj = {"message": "Task deleted successfully"}

            contador = 0

            for item in tasks_list:

                contador = contador + 1
                item["id"] = contador

            break

    else:
        msj = HTTPException(status_code=404,detail="Task not found")

    return msj
