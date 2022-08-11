import datetime
import os

import dotenv

from . import credentials, first_mile_shipments, request_api

if __name__ == "__main__":
    dotenv.load_dotenv()
    try:
        data = first_mile_shipments.FirstMileShipmentsRequest(
            dateFrom="11-08-2022",
            dateTo="11-08-2022",
        )
        ya_credentials = credentials.Credentials(os.getenv('CLIENT_ID'), os.getenv('CLIENT_TOKEN'))

        act_id = first_mile_shipments.get_first_mile_data(
            ya_credentials,
            os.getenv('COMPANY_NUMBER'),
            data,
        )
        print(act_id)
    except request_api.HTTPError as error:
        print('ERROR', error)
        print('ERROR response_data', error.response_data)
