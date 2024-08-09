import os

from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from src.predictor import Predictor

# Configure logging
app = FastAPI()
predictor = Predictor()

USE_CACHE = os.getenv('USE_CACHE', False)
logger.info(f'USE_CACHE: {USE_CACHE}')
if USE_CACHE:
    from src.cache import PredictorCache

    cache = PredictorCache(seconds_to_invalidate_prediction=5)


@app.get('/health')
def health():
    return {'status': 'OK'}


class PredictRequest(BaseModel):
    product_id: str


@app.post('/predict')
def predict(request: PredictRequest):
    """
    Endpoint to make a prediction for a given product id
    """
    if not USE_CACHE:
        return predictor.predict(request.product_id)
    else:
        # We are using a cache
        prediction = cache.read(request.product_id)
        if prediction is not None:
            return prediction
        else:
            # Cache miss
            prediction = predictor.predict(request.product_id)
            cache.write(request.product_id, prediction)
            return prediction
