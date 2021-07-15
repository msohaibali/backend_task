import json
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient


try:
    fl = open("config.json", "r", encoding="utf-8")
    config_file = json.loads(fl.read())
    print('[+]  Config File Read Successfully')
except Exception as ex:
    print('[!]  Issue while Reading Config File  ::  ', str(ex))
    exit(0)


class TODO(BaseModel):
    title: str
    description: str

app = FastAPI()


class MONGO_DB():
    __instance__ = None

    def __init__(self, db_host, db_port,db_name,coll_name,db_authentication=False, auth_username='', auth_password=''):
        db_client = MongoClient(db_host, db_port)
        db = db_client[db_name]
        if db_authentication:
            try:
                db.authenticate(auth_username, auth_password)
                print('[+]  Database Authentication Successfull')
            except Exception as ex:
                print('[-]  Issue while Authentication  ::  ', str(ex))
                exit(0)

        self.coll = db[coll_name]

        if MONGO_DB.__instance__ is None:  
           MONGO_DB.__instance__ = self
        

mongo_obj = MONGO_DB (   
                        db_host=config_file['MONGO_DB'].get('HOST'),
                        db_port=config_file['MONGO_DB'].get('PORT'),
                        db_name=config_file['MONGO_DB'].get('DB_NAME'),
                        coll_name=config_file['MONGO_DB'].get('COLL_NAME'),
                        db_authentication=config_file['MONGO_DB'].get('AUTHENTICATION'),
                        auth_username=config_file['MONGO_DB'].get('DB_USERNAME'),
                        auth_password=config_file['MONGO_DB'].get('DB_PASSWORD'))

mongo_coll = mongo_obj.coll


@app.get("/api/todo")
async def get_all_tasks():
    try:
        curr = mongo_coll.find({})

        all_tasks = []
        for single_task in curr:
            del single_task['_id']
            all_tasks.append(single_task)

        return {'status':200, 'data':all_tasks}
    except:
        return {'status':400, 'data':[]}

@app.post("/api/todo/")
async def create_task(item: TODO):
    data_dict = item.dict()
    try:
        mongo_coll.insert_one(data_dict)
        return {'status':200, 'message':'Data Inserted Successfully'}
    except Exception as ex:
        return {'status':400, 'message':'Data not Inserted Successfully', 'error': str(ex)}


@app.put("/api/todo/")
async def update_task(item: TODO):
    data_dict = item.dict()
    query = {"title": data_dict.get('title')}
    try:
        mongo_coll.update_one(query, {"$set":data_dict})
        return {'status':200, 'message':'Task Updated Successfully'}
    except Exception as ex:
        return {'status':400, 'message':'Not able to Update Task', 'error':str(ex)}


@app.get("/api/todo/{title}")
async def get_tasks(title: str):
    curr = mongo_coll.find({"title":title})
    all_tasks = []
    for single_item in curr:
        del single_item['_id']
        all_tasks.append(single_item)

    if all_tasks:
        return {'status':200, 'data':all_tasks[0]}
    
    return {'status':404, 'data':{}}


@app.delete("/api/todo/{title}")
async def delete_tasks(title: str):
    try:
        mongo_coll.delete_one({"title":title})
        return {'status':200, 'message':'Task Deleted Successfully'}
    except:
        return {'status':404, 'message':'No taks with title  ::  ' + title}

