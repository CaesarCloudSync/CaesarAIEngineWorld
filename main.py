import os
import io
import json
import base64
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
        filename = file.filename
        modelbytes = await file.read()
        modelhex = modelbytes.hex().encode()
        condition = f"filename = '{filename}'"
        model_exists = caesarcrud.check_exists(("*"),table,condition)
        if model_exists:
            return {"message":"model already exists."}
        else:
            res = caesarcrud.post_data(("filename",),(filename,),table)
            res = caesarcrud.update_blob("model",modelhex,table,condition=condition)
            if res:
                return {"message":"model was posted."}
            else:
                return {"error":"posting error"}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}


@app.get('/getmodel')# GET # allow all origins all methods.
async def getmodel(filename):
        try:
            condition = f"filename = '{filename}'"
            model_exists = caesarcrud.check_exists(("*"),table,condition)
            if model_exists:
                model_json = caesarcrud.get_data(("filename","model"),table,condition=condition)[0]
                modelfilename = model_json["filename"]
                modelhex = model_json["model"].decode()
                model = bytes.fromhex(modelhex)
                return Response(model,
                                headers={'Content-Disposition': f'attachment; filename="{modelfilename}"'},
                                status_code=status.HTTP_200_OK)
            else:
                return {"error":"model doesn't exist."}
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.get('/getallmodelnames')# GET # allow all origins all methods.
async def getallmodelnames():
        try:
            filenames = caesarcrud.get_data(("filename",),table)
            if filenames:
                return {"modelnames":filenames}
            else:
                return {"error":"no models exist"}
                 
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.delete('/deletemodel')# GET # allow all origins all methods.
async def deletemodel(filename):
        try:
            condition = f"filename = '{filename}'"
            model_exists = caesarcrud.check_exists(("*"),table,condition)
            if model_exists:
                res = caesarcrud.delete_data(table,condition)
                if res:
                        return {"meesage":"model was deleted."}
                else:
                        return {"error":"error when deleting"}
            else:
                return {"error":"model doesn't exist."}
        except Exception as ex:
            return {"error":f"{type(ex)},{ex}"}
@app.put('/updatemodel')# GET # allow all origins all methods.
async def updatemodel(filename=Form(...),file: UploadFile = File(...)):
    try:
        newfilename = file.filename
        modelbytes = await file.read()
        modelhex = modelbytes.hex().encode()
        condition = f"filename = '{filename}'"
        model_exists = caesarcrud.check_exists(("*"),table,condition)
        if model_exists:
            res = caesarcrud.update_data(("filename",),(newfilename,),table,condition=condition)
            res = caesarcrud.update_blob("model",modelhex,table,condition=condition)
            if res:
                 return {"message":"model was updated."}
            else:
                return {"error":"error updating."}
        else:
            return {"message":"model does not exists."}
            

    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.post('/createqrcode')# GET # allow all origins all methods.
async def createqrcode(data : JSONStructure = None):
    try:
        data = dict(data)
        if data.get("help"):
            return {"url":"<url>","version":3,"box_size":10,"border":10,"usebase64":"true"}
        url = data["url"]
        version = data.get("version") if data.get("version") else 3
        box_size = data.get("box_size") if data.get("box_size") else 5
        border = data.get("border") if data.get("border") else 10
        # Create a QR code object with a larger size and higher error correction
        qr = qrcode.QRCode(version=version, box_size=box_size, border=border, error_correction=qrcode.constants.ERROR_CORRECT_H)

        # Define the data to be encoded in the QR code
        

        # Add the data to the QR code object
        qr.add_data(url)

        # Make the QR code
        qr.make(fit=True)

        # Create an image from the QR code with a black fill color and white background
        img = qr.make_image(fill_color="black", back_color="white")
        imgstream = io.BytesIO()
        # Save the QR code image    
        img.save(imgstream)
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
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())