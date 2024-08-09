from time import sleep, time

import requests
from fire import Fire


def run(n_requests: int):
    """
    Sends n_requests to the server and logs the time it took to get a response
    """
    url = 'http://localhost:8000/predict'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {'product_id': 'ETH/EUR'}

    for _ in range(n_requests):
        # time milliseconds it takes to get a response
        start = time()
        response = requests.post(url, headers=headers, json=data)
        latency_ms = (time() - start) * 1000
        print(f'Time taken: {latency_ms:.2f}ms')
        print(response.text)

        sleep(1)


if __name__ == '__main__':
    Fire(run)
