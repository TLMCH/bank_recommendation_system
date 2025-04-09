import logging

from recommendations import Recommendations
from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

logger = logging.getLogger("uvicorn.error")
rec_store = Recommendations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    logger.info("Starting")
    rec_store.load()

    yield
    # этот код выполнится только один раз при остановке сервиса
    logger.info("Stopping")
    rec_store.stats()
    

# создаём приложение FastAPI
app = FastAPI(title="recommendations", lifespan=lifespan)
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


app_personal_recommendation_count = Counter(
    "app_personal_recommendation_count",
    "Personal recommendation counter"
)

app_default_recommendation_count = Counter(
    "app_default_recommendation_count",
    "Default recommendation counter"
)

app_error_recommendation_count = Counter(
    "app_error_recommendation_count",
    "Error counter"
)


@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 5):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """
    response = rec_store.get(user_id, k)
    recs = [response[1]]

    if response[0] == 'personal':
        app_personal_recommendation_count.inc()
    elif response[0] == 'default':
        app_default_recommendation_count.inc()
    else:
        app_error_recommendation_count.inc()

    return {"recs": recs}