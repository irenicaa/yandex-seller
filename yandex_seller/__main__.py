import datetime
import os

import dotenv

from . import credentials, request_api, stats_skus

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        data = stats_skus.StatsSkusRequest(
            shopSkus=["0008"],
        )
        print(data.to_json())

        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        stats = stats_skus.get_stats_skus(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            data,
        )
        print(stats)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
