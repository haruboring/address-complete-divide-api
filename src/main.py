from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.routers import convert, default  # type: ignore

app = FastAPI()
app.include_router(default.router)
app.include_router(convert.router)

# # for local development
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

lambda_handler = Mangum(app)
