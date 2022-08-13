import datetime
import os

import dotenv

from . import credentials, get_act, request_api

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        act = get_act.get_reception_transfer_act(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            os.getenv('SHIPMENT_ID'),
        )
        with open('act.pdf', 'wb') as f:
            f.write(act)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
