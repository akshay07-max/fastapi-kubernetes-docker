from fastapi import FastAPI, websockets

app = FastAPI()

@app.get("/")
def root():
    return {
            "message": "app started successfully"
            }