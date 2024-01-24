import os
import io
import json
import base64
import segno
import hashlib
import asyncio 
import uvicorn
import qrcode
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarAIModelCRUD.caesaraimodelcrud import CaesarAIModelCRUD
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesarcrud = CaesarCRUD()
caesaraimodelcrud = CaesarAIModelCRUD(caesarcrud)
maturityjwt = CaesarJWT(caesarcrud)
caesarcreatetables = CaesarCreateTables()
caesarcreatetables.create(caesarcrud)
JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
table = "caesaraiworldmodels"


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIWorld!"
@app.post('/postmodel')# GET # allow all origins all methods.
async def postmodel(file: UploadFile = File(...)):
    try:
        return await caesaraimodelcrud.postmodel("caesaraiworldmodels",file)
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}


@app.get('/getmodel')# GET # allow all origins all methods.
async def getmodel(filename):
        try:
            return caesaraimodelcrud.getmodel("caesaraiworldmodels",filename)
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"},400
@app.get('/getallmodelnames')# GET # allow all origins all methods.
async def getallmodelnames():
        try:
            filenames = caesarcrud.get_data(("filename",),"caesaraiworldmodels")
            if filenames:
                return {"modelnames":filenames}
            else:
                return {"error":"no models exist"}
                 
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.delete('/deletemodel')# GET # allow all origins all methods.
async def deletemodel(filename):
        try:
            return caesaraimodelcrud.deletemodel("caesaraiworldmodels",filename)
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.put('/updatemodel')# GET # allow all origins all methods.
async def updatemodel(filename=Form(...),file: UploadFile = File(...)):
    try:

        return await caesaraimodelcrud.updatemodel("caesaraiworldmodels",filename,file)    

    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
    
@app.post('/postarmodel')# GET # allow all origins all methods.
async def postarmodel(file: UploadFile = File(...)):
    try:
        if "obj" in file.filename:
            return await caesaraimodelcrud.postmodel("caesaraiarmodels",file)
        else:
             return {"message":"file needs to be a .obj file."}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}


@app.get('/getarmodel')# GET # allow all origins all methods.
async def getarmodel(filename):
        try:
            return caesaraimodelcrud.getmodel("caesaraiarmodels",filename)
  
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/getallarmodelnames')# GET # allow all origins all methods.
async def getallarmodelnames():
        try:
            filenames = caesarcrud.get_data(("filename",),"caesaraiarmodels")
            if filenames:
                return {"modelnames":filenames}
            else:
                return {"error":"no models exist"}
                 
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.delete('/deletearmodel')# GET # allow all origins all methods.
async def deletearmodel(filename):
        try:
            return caesaraimodelcrud.deletemodel("caesaraiarmodels",filename)
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.put('/updatearmodel')# GET # allow all origins all methods.
async def updatearmodel(filename=Form(...),file: UploadFile = File(...)):
    try:

        return await caesaraimodelcrud.updatemodel("caesaraiarmodels",filename,file)    

    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.post('/createqrcode')# GET # allow all origins all methods.
async def createqrcode(data : JSONStructure = None):
    try:
        data = dict(data)
        if data.get("help"):
            return {"url":"<url>","version":3,"box_size":10,"border":10,"usebase64":"true"}
        url = data["url"]
        box_size = data.get("box_size") if data.get("box_size") else 5

        # Create a QR code object with a larger size and higher error correction
        

        light = data.get("light") if data.get("light") else "white"
        dark = data.get("dark") if data.get("dark") else "black"

        imgstream = io.BytesIO()
        video = segno.make(url)
        video.save(imgstream, kind="png", dark=dark, light=light, scale=box_size)
        imgstream.seek(0)
        imgbytes = imgstream.read()
        if data.get("usebase64"):
            imgbas64 = "data:image/png;base64,"+ base64.b64encode(imgbytes).decode()
            return {"qrcode":imgbas64}
             
        else:
            return Response(imgbytes,
                        headers={'Content-Disposition': f'attachment; filename="new_qr_code.png"'},
                        status_code=status.HTTP_200_OK)
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}


if __name__ == "__main__":
    #video = segno.make('https://www.youtube.com/channel/UCNhFxpk6hGt5uMCKXq0Jl8A')
    #video.save('Video.png', dark="yellow", light="#323524", scale=5)
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())