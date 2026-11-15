from fastapi import FastAPI

app = FastAPI(title="Truyen AI Backend")

@app.get("/")
def read_root():
    return {"status": "Bộ não đang chạy!", "service": "Truyen AI Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
