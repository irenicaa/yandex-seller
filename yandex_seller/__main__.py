import datetime
import os

import dotenv

from . import credentials, request_api, stocks

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        data = stocks.StocksRequest(
            warehouseId=141722,
            skus=["0008", "alisa-wall-lite-black"],
        )
        print(data.to_json())

        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        stocks = stocks.get_stocks(ya_credentials, data)
        print(stocks)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
