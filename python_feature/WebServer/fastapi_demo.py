from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Person(BaseModel):
    name: str
    age: int
    address: str
    salary: float


@app.post('/hello')
def hello(p: Person):
    name = p.name
    age = p.age
    age += 10

    rsp = f"name: {name}, age: {age}"
    return {'success': True, 'msg': rsp}


@app.get('/query/{name}')
def query(name):
    rsp = f"you find {name}"
    return {'success': True, 'msg': rsp}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
