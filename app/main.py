from fastapi import BackgroundTasks, FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.database.session import create_db_tables
from contextlib import asynccontextmanager
from app.api.router import master_router
from app.services.notification import NotificationService


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(
    lifespan=lifespan_handler,
)

app.include_router(master_router)


@app.get("/mail")
async def send_test_mail(task: BackgroundTasks):
    task.add_task(
        NotificationService().send_email,
        subject="Test Email",
        recipients=[
            "rahiseli@outlook.com",
        ],
        body="This is a test email from FastAPI application.",
    )
    return {"detail": "Test email sent."}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
