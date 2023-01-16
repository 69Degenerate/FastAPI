from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
from bson.json_util import dumps,loads

app = FastAPI()
cli=pymongo.MongoClient("mongodb://mongo:hKkb23G8NtWIezPQe4Cg@containers-us-west-197.railway.app:7613")
db=cli.workdb.emp
project=cli.portfolio.project
cert=cli.portfolio.certificates
feed=cli.portfolio.feedback

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}



@app.get("/read")
def read():
    s=db.find({"deptno": 30},{'_id':False})
    print(s)
    di = loads(dumps(list(s)))
    return di


@app.get("/readone/{deptno}")
async def readone(deptno):
    n=int(deptno)
    return loads(dumps(list(db.find({"deptno": n},{'_id':False}))))


@app.get('/readname/{ename}')
def readname(ename):
    return loads(dumps(list(db.find({"ename":{'$regex': ename,'$options': 'i'}},{'_id':False}))))


@app.post("/items/")
def insert():
    data={
    "empno": 7499,
    "ename": "allen",
    "job": "salesman",
    "mgr": 7698,
    "hiredate": "20-02-81",
    "sal": 1600,
    "comm": 300,
    "deptno": 30
  }
    db.insert_one(data)
    return dict(data)

@app.delete('/delete/{name}')
def delete(name):
    db.delete_many({"ename":name})
    s=db.find({"deptno": name},{'_id':False})
    return loads(dumps(list(s)))


@app.put('/update/')
def update(name,newname):
    myquery = { "ename": { "$regex": name } }
    newvalues = { "$set": { "ename": newname } }
    x = db.update_many(myquery, newvalues)
    print(x.modified_count, "documents updated.")
    s=db.find({"ename": newname},{'_id':False})
    print(s)
    return loads(dumps(list(s)))


# --------------------------------------------------------------------------------------------
@app.get('/port/prj')
def proj():
    return loads(dumps(list(project.find({},{'_id':False}))))

@app.get('/port/ctr')
def ctr():
    return loads(dumps(list(cert.find({},{'_id':False}))))
