from datetime import datetime, timezone
from time import sleep

from pydantic import BaseModel


# a pydantic class with 2 fields
# - timestamp: datetime
# - predicted_price: float
class Prediction(BaseModel):
    timestamp: str
    timestamp_sec: int
    product_id: str
    predicted_price: float

    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'timestamp_sec': self.timestamp_sec,
            'product_id': self.product_id,
            'predicted_price': self.predicted_price,
        }


class Predictor:
    def predict(self, product_id: str) -> Prediction:
        """
        Simulate a prediction by sleeping for 1 second and the returning a prediction

        Args:
            product_id (str): the product id for which we want to make a prediction

        Returns:
            Prediction: the prediction object
        """
        # sleep for 1 second to simulate the time it takes to make a prediction
        # This is a blocking operation
        sleep(1)

        # get the current time in utc format using datetime
        current_time = datetime.now(timezone.utc)
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        timestamp_sec = int(current_time.timestamp())

        return Prediction(
            timestamp=timestamp,
            timestamp_sec=timestamp_sec,
            product_id=product_id,
            predicted_price=42.0,
        )
