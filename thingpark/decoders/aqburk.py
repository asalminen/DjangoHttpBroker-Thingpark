from broker.providers.decoder import DecoderProvider
from thingpark.parsers import parse_aqburk


class AQBurkDecoder(DecoderProvider):
    description = 'Decode AQBurk payload'

    def decode_payload(self, hex_payload):
        data = parse_aqburk(hex_payload)
        return data