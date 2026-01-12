from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, users, uploads, reports, public, notifications

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Insights Portal")

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://gleaming-fudge-1e4b0c.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(uploads.router)
app.include_router(reports.router)
app.include_router(notifications.router)
app.include_router(public.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Customer Insights API"}
