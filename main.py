import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import argparse
from notes.main import notes_router

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=8000, type=int)
args = parser.parse_args()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI()

# Adding the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)

@app.get("/", status_code=200)
async def Home(request: Request):
    return 'Welcome to the Notes App'

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=args.port, reload=True)
