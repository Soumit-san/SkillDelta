from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
@app.get("/skills/{skill_id:int}")
def get_int(skill_id: int):
    return {"int": skill_id}

@app.get("/skills/roles")
def get_string():
    return {"str": "roles"}

client = TestClient(app)
print(client.get("/skills/123").json())
print(client.get("/skills/roles").json())
