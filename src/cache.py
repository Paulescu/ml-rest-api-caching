import os
from typing import Optional

import redis
from loguru import logger

from src.predictor import Prediction

# REDIS_HOST = os.environ['REDIS_HOST']
# REDIS_PORT = os.environ['REDIS_PORT']

class PredictorCache:

    def __init__(
        self,
        redis_host: Optional[str] = os.getenv('REDIS_HOST'),
        redis_port: Optional[int] = os.getenv('REDIS_PORT'),
        seconds_to_invalidate_prediction: Optional[int] = 60,    
    ):  
        self._client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.seconds_to_invalidate_prediction = seconds_to_invalidate_prediction

    def read(self, product_id: str) -> Prediction | None:
        """
        Read the prediction from the cache
        """
        key = product_id
        try:
            # get the value from the cache
            value = self._client.hgetall(key)

            # dict -> Prediction            
            prediction = Prediction(**value)

            # check the value is not too old
            from datetime import datetime, timezone
            current_timestamp_sec = datetime.now(timezone.utc).timestamp()
            if current_timestamp_sec - prediction.timestamp_sec > self.seconds_to_invalidate_prediction:
                return None
                        
            if value:
                logger.info(f"Data retrieved: {key} -> {value}")
                return Prediction(**value)
            else:
                logger.info(f"Key '{key}' not found.")
                return None
        except redis.RedisError as e:
            logger.info(f"Failed to read data: {e}")
            return None

    def write(self, product_id: str, prediction: Prediction):
        """
        Write the prediction to the cache
        """
        key = product_id
        try:
            self._client.hset(key, mapping=prediction.to_dict())
            logger.info(f"Data saved: {key} -> {prediction.to_dict()}")
        except redis.RedisError as e:
            logger.info(f"Failed to save data: {e}")    

    def flushdb(self):
        """
        Flush the cache
        """
        try:
            self._client.flushdb()
            logger.info("Cache flushed")
        except redis.RedisError as e:
            logger.info(f"Failed to flush cache: {e}")

if __name__ == '__main__':

    # Test the cache
    cache = PredictorCache(
        redis_host="localhost",
        redis_port=6379,
        max_seconds_stale_prediction=60,
    )
    cache.flushdb()