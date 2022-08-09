import datetime
import os

import dotenv

from . import credentials, orders_status, request_api

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        data = orders_status.SetStatusRequest(
            order = orders_status.OrderStatus(
                status = 'PROCESSING',
                substatus = 'READY_TO_SHIP',
            )
        )

        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        status = orders_status.set_order_status(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            os.getenv('ORDER_NUMBER'),
            data
        )
        print(status)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
