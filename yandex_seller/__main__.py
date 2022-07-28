import datetime
import os

import dotenv

from . import credentials, orders, request_api

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        data = orders.OrdersRequest(
            campaignId=os.getenv('COMPANY_NUMBER'),
            status="PROCESSING",
            substatus="STARTED",
            page=1,
        )

        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        orders_data = orders.get_orders(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            data,
        )
        print(orders_data)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
