from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import model
import check
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")



@app.get("/",response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})





@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    try:

        contents = await file.read()
        with open("./test_images/uploaded.jpg", "wb") as f:
            f.write(contents)

        checked=check.check_face_exist('test_images/', 'uploaded.jpg')
        if checked==True:
            prediction = model.model_sprint()
            if prediction=="deepfake":
                alert_type="deepfake"
            else:
                alert_type="real"
        else:
            alert_type=None
        print(check.check_face_exist('test_images/', 'uploaded.jpg'))

        
        return templates.TemplateResponse("index.html", {"request": request,"alert_type":alert_type})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})
    finally:
        await file.close()


if __name__ == "__main__":
    uvicorn.run("fast:app", host="0.0.0.0", port=8000,log_level="debug",reload=True)











# @app.post("/upload",response_class=HTMLResponse)
# async def upload(request: Request,file: UploadFile = File(...)):
#     try:
#         contents =file.file.read()
#         with open("./test_images/uploaded.jpg", "wb") as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()
    
#     prediction=model.model_sprint()
#     print(prediction)
#     return templates.TemplateResponse("index.html", {"request": request,"predicted":"fake"})