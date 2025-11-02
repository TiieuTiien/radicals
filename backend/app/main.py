from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.main import api_router

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title="Radicals",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)