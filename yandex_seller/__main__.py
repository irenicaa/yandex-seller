import datetime
import os

import dotenv

from . import credentials, first_mile_shipments_confirm, request_api

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        data = first_mile_shipments_confirm.ActConfirmDataRequest(
            externalShipmentId = os.getenv('SHIPMENT_ID'),
            orderIds = []
        )
        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        act_status = first_mile_shipments_confirm.get_act_confirm(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            os.getenv('SHIPMENT_ID'),
            data,
        )
        print(act_status)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
