from fastapi import FastAPI


app = FastAPI(
    title="VK tz"
)


@app.get("/")
def home():
    return {"status": "success"}
