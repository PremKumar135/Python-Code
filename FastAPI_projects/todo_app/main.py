########################## Without Pydantic Validations & Exceptions ##########################

# from fastapi import FastAPI

# app = FastAPI()

# todo_list = [{'todo_id':1, 'todo_name':'WakeUP', 'todo_description':'Wake up in the morning'},
#             {'todo_id':2, 'todo_name':'getReady', 'todo_description':'Getready '},
#             {'todo_id':3, 'todo_name':'Breakfast', 'todo_description':'Have Breakfast'},
#             {'todo_id':4, 'todo_name':'Lunch', 'todo_description':'Have Lunch'},
#             {'todo_id':5, 'todo_name':'Dinner', 'todo_description':'Have Dinner'}
#             ]

# @app.get('/')
# def index_page():
#     return "hello world"

# # get all the todos
# @app.get('/get_all_todos')
# def get_all_todos():
#     return todo_list

# # get a specific todo
# @app.get('/get_todo/{todo_id}')
# def get_todo(todo_id:int):
#     for i in todo_list:
#         if i['todo_id']==todo_id:
#             return {'messages':i}
#     return "todo id not available"

# # add the new todo
# @app.post('/add_new_todo')
# def add_new_todo(new_todo_dict:dict):
#     new_todo_id = len(todo_list) + 1
#     new_todo = {'todo_id':new_todo_id, 
#                 'todo_name':new_todo_dict['todo_name'], 
#                 'todo_description':new_todo_dict['todo_description']
#                 }
#     todo_list.append(new_todo)
#     return {'updated_list':todo_list}


# # edit any existing todo
# @app.put('/edit_todo')
# def edit_todo(todo_id:int, new_todo:dict):
#     for i in todo_list:
#         if i['todo_id'] == todo_id:
#             i['todo_name'] = new_todo['todo_name']
#             i['todo_description'] = new_todo['todo_description']
#     return {'edited_list':todo_list}

# # delete the todo
# @app.delete('/delete_todo')
# def delete_todo(todo_id:int):
#     for idx, i in enumerate(todo_list):
#         if i['todo_id']==todo_id:
#             todo_list.pop(idx)
#     return todo_list


########################## With Pydantic Validations & Exceptions ##########################
from typing import List, Optional, Dict, Any
from enum import IntEnum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

## todo base
class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name:str = Field(..., description = 'Name of the todo')
    todo_description:str = Field(..., description = 'Description of the todo')
    priority : Priority = Field(default=Priority.LOW, description='priority of the todo')

class CreateTodo(TodoBase):
    todo_id : int = Field(..., description = 'Unique identifier for todo')
    

class EditTodo(BaseModel):
    todo_name : Optional[str] = Field(None, description='Name of the todo')
    todo_description : Optional[str] = Field(None, description='Description of the todo')
    priority : Optional[Priority] = Field(None, description='Priority of todo')

    
todo_list = [CreateTodo(todo_id=1, todo_name='Wakeup', todo_description='Wake up in the morning', priority=Priority.HIGH),
            CreateTodo(todo_id=2, todo_name='getReady', todo_description='Getready ', priority=Priority.MEDIUM),
            CreateTodo(todo_id=3, todo_name='Breakfast', todo_description='Have Breakfast', priority=Priority.LOW),
            CreateTodo(todo_id=4, todo_name='Lunch', todo_description='Have Lunch', priority=Priority.HIGH),
            CreateTodo(todo_id=5, todo_name='Dinner', todo_description='Have Dinner', priority=Priority.HIGH)
            ]


app = FastAPI()

@app.get('/get_all_todos', response_model=List[CreateTodo])
def get_all_todos():
    return todo_list

# get a specific todo
@app.get('/get_todo/{todo_id}', response_model=CreateTodo)
def get_todo(todo_id:int):
    for i in todo_list:
        if i.todo_id==todo_id:
            return i
    raise HTTPException(status_code=404, detail='todo_id not found')

# add the new todo 
@app.post('/add_new_todo', response_model=CreateTodo)
def add_new_todo(new_todo_dict:TodoBase):
    new_todo_id = len(todo_list) + 1
    new_todo = CreateTodo(todo_id=new_todo_id, 
                        todo_name=new_todo_dict.todo_name, 
                        todo_description=new_todo_dict.todo_description,
                        priority = new_todo_dict.priority
                        )
    todo_list.append(new_todo)
    return new_todo


# edit any existing todo a.k.a update
@app.put('/edit_todo', response_model=CreateTodo)
def edit_todo(todo_id:int, edited_todo:EditTodo):
    for i in todo_list:
        if i.todo_id==todo_id:
            if edited_todo.todo_name is not None:
                i.todo_name = edited_todo.todo_name,
            
            if edited_todo.todo_description is not None:
                i.todo_description = edited_todo.todo_description
            
            if edited_todo.priority is not None:
                i.priority = edited_todo.priority
            return i

    raise HTTPException(status_code=404, detail='todo_id not found')

# delete the todo
@app.delete('/delete_todo', response_model=List[CreateTodo])
def delete_todo(todo_id:int):
    for idx, i in enumerate(todo_list):
        if i.todo_id==todo_id:
            deleted_todo = todo_list.pop(idx)
            return deleted_todo

    raise HTTPException(status_code=404, detail='todo_id not found')
