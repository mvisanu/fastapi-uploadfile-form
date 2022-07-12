from fastapi import FastAPI, Body, Request, File, UploadFile, Form, Depends, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
#from typing import List

app = FastAPI()

list_of_usernames = list()
templates = Jinja2Templates(directory="htmldirectory")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
  print(form_data)
  return {"access_token": form_data.username, "token_type":"bearer"}

@app.post("/users/profilepic")
async def profile_pic(token: str = Depends(oauth_scheme)):
  print(token)
  return {
    "user": "visanu",
    "profile_pic": "my_face"
  }

class NameValues(BaseModel):
  name: str = None
  country: str
  age: int
  base_salary: float
   
@app.get("/home/{user_name}", response_class=HTMLResponse)
def write_home(request: Request, user_name: str):
  return templates.TemplateResponse("home.html", {"request": request, "username": user_name})

@app.post("/submitform")
async def handel_form(modelname: str = Form(...), model_file: UploadFile = File(...)):
  print(modelname)
  content_model = await model_file.read()
  print(content_model)
  return {
    "modelname": modelname,
    "model_file": model_file.filename
  }


# #http://127.0.0.1:8000/home/jack?query=password
# @app.get("/home/{user_name}")
# def home(user_name: str, query):
#   return {
#     "Name": user_name,
#     "Age": 24,
#     "Query": query
#   }


  
@app.post("/postData")
def post_data(name_value: NameValues, marital_status: str = Body(...)):
  print(name_value)  
  return {
    "name": name_value.name,
  }
  
def handle_email_background(email: str, data:str):
  print(email)
  print(data)
  for i in range(100):
    print(email)
    time.sleep(0.1)
  
@app.get("/users/email")  
async def handle_emal(email: str, background_task: BackgroundTasks):
  print(email)
  background_task.add_task(handle_email_background, email, "this is a sample background task manager")
  return {"email": email, "message": "Mail sent"}
  

    
    
    
    
    
# @app.put("/user_name/{user_name}")
# def put_data(user_name: str):
#   print(user_name)
#   list_of_usernames.append(user_name)
#   return {
#     "username": user_name
#   }

  
# @app.delete("/deleteData/{user_name}")
# def delete_data(user_name: str):
#   list_of_usernames.remove(user_name)
#   return {
#     "username": list_of_usernames
#   }
  
# @app.api_route("/homedata", methods=['GET', 'POST', 'PUT', 'DELETE'])
# def handle_homedata(user_name: str):
#   print(user_name)  
#   return {
#     "username": list_of_usernames
#   }