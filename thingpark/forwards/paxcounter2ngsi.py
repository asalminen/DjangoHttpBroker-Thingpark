import json
import logging

import requests

from broker.providers.forward import ForwardProvider

logger = logging.getLogger('runforwards')

ngsi_template = {
    "id": "000773207E3FFFFF",
    "type": "PaxcounterObserved",
    "dateObserved": "2019-03-19T04:52:52.652000+00:00Z",
    "WiFi": 14,
    "Bluetooth": 3,
    "location": {
        "coordinates": [
            24.949541,
            60.189692
        ],
        "type": "Point"
    },
    "address": {
        "addressCountry": "FI",
        "addressLocality": "Helsinki",
        "streetAddress": "Park Sinebrychoff"
    }
}


class Paxcounter2NGSIForward(ForwardProvider):
    description = 'Send data to a NGSI broker, e.g. Orion'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def forward_data(self, datalogger, data, config):
        # Copy template
        m = ngsi_template.copy()
        # Replace data with real values
        m['id'] = datalogger.devid
        m['dateObserved'] = data['time']
        if datalogger.lon and datalogger.lat:
            m['location']['coordinates'] = [datalogger.lon, datalogger.lat]
        else:
            del m['location']
        m['WiFi'] = data['data']['wifi']
        m['Bluetooth'] = data['data']['ble']
        m['address'] = {
            "addressCountry": datalogger.country,
            "addressLocality": datalogger.locality,
            "streetAddress": datalogger.street
        }
        logger.debug(json.dumps(m, indent=2))
        # POST data to an endpoint, which is defined in Forward's or DataloggerForward's config field
        # TODO: add authentication and other
        res = requests.post(config['url'], json=m)
        if 200 <= res.status_code < 300:
            logger.info(f'POST request to {config["url"]} returned success code {res.status_code}')
            return True
        else:
            logger.warning(f'POST request to {config["url"]} returned error code {res.status_code}')
            return False
