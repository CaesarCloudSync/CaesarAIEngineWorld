from fastapi import UploadFile,File, status
from fastapi.responses import Response
from CaesarSQLDB.caesarcrud import CaesarCRUD
class CaesarAIModelCRUD:
    def __init__(self,caesarcrud : CaesarCRUD) -> None:
        self.caesarcrud = caesarcrud 
    async def postmodel(self,table :str,file : UploadFile = File(...)):
        filename = file.filename
        modelbytes = await file.read()
        modelhex = modelbytes.hex().encode()
        condition = f"filename = '{filename}'"
        model_exists = self.caesarcrud.check_exists(("*"),table,condition)
        if model_exists:
            return {"message":"model already exists."}
        else:
            res = self.caesarcrud.post_data(("filename",),(filename,),table)
            res = self.caesarcrud.update_blob("model",modelhex,table,condition=condition)
            if res:
                return {"message":"model was posted."}
            else:
                return {"error":"posting error"}
    def getmodel(self,table :str, filename : str):
        condition = f"filename = '{filename}'"
        model_exists = self.caesarcrud.check_exists(("*"),table,condition)
        if model_exists:
            model_json = self.caesarcrud.get_data(("filename","model"),table,condition=condition)[0]
            modelfilename = model_json["filename"]
            modelhex = model_json["model"].decode()
            model = bytes.fromhex(modelhex)
            return Response(model,
                            headers={'Content-Disposition': f'attachment; filename="{modelfilename}"'},
                            status_code=status.HTTP_200_OK)
        else:
            return {"error":"model doesn't exist."}
    def deletemodel(self,table :str, filename :str):
        condition = f"filename = '{filename}'"
        model_exists = self.caesarcrud.check_exists(("*"),table,condition)
        if model_exists:
            res = self.caesarcrud.delete_data(table,condition)
            if res:
                    return {"meesage":"model was deleted."}
            else:
                    return {"error":"error when deleting"}
        else:
            return {"error":"model doesn't exist."}
    async def updatemodel(self,table:str,filename: str,file : UploadFile = File(...)):
        newfilename = file.filename
        modelbytes = await file.read()
        modelhex = modelbytes.hex().encode()
        condition = f"filename = '{filename}'"
        model_exists = self.caesarcrud.check_exists(("*"),table,condition)
        if model_exists:
            res = self.caesarcrud.update_data(("filename",),(newfilename,),table,condition=condition)
            res = self.caesarcrud.update_blob("model",modelhex,table,condition=condition)
            if res:
                 return {"message":"model was updated."}
            else:
                return {"error":"error updating."}
        else:
            return {"message":"model does not exists."}