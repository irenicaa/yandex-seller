import datetime
import os

import dotenv

from . import credentials, orders_delivery_labels, request_api

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        pdf = orders_delivery_labels.get_campaigns_orders(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            os.getenv('ORDER_NUMBER'),
        )
        with open('test.pdf', 'wb') as f:
            f.write(pdf)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
