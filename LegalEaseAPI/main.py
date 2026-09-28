from fastapi import FastAPI

from routes import router

app = FastAPI(title="LegalEase: AI Legal Document Generator")

@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)