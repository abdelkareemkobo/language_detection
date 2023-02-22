from fastapi import FastAPI ,Request
from pydantic import BaseModel 
from model.model import predict_pipeline
from model.model import __version__ as model_version 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates")

class TextIn(BaseModel):
    text: str

class PredictionOut(BaseModel):
    language: str 
@app.get("/")
def home():
    return {"health_check":"OK","model_version":model_version}

@app.get("/items/{id}",response_class=HTMLResponse)
async def read_item(request:Request,id:str):
    return templates.TemplateResponse("base.html",{"request":request,"id":id})

# @app.post("/predict",response_model=PredictionOut)
# def predict(payload:TextIn):
#     language = predict_pipeline(payload.text)
#     return {"language":language}    

@app.post("/predict",response_class=HTMLResponse)
async def predict(request:Request,payload:TextIn):
    language = predict_pipeline(payload.text)
    # return {"language":language}    
    return templates.TemplateResponse("base.html",{"request":request,"language":language})