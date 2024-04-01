from fastapi import FastAPI
from database.database import Base, engine, create_unique_id_sequence
from routes import auth_routes, client_routes, user_routes, metal_routes, order_routes, banner_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://akhzamov.github.io/metally-prod",
    "https://metally-60745.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    with engine.connect() as conn:
        conn.execute(create_unique_id_sequence)


app.include_router(auth_routes.router)
app.include_router(client_routes.router)
app.include_router(user_routes.router)
app.include_router(metal_routes.router)
app.include_router(order_routes.router)
app.include_router(banner_routes.router)

