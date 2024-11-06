import os

ENDPOINTS = {
    'acme': os.getenv('ACME_URL_ENDPOINT', 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'),
    'patagonia': os.getenv('PATAGONIA_URL_ENDPOINT', 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'),
    'paperflies': os.getenv('PAPERFLIES_URL_ENDPOINT', 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies')
}

DATACLASSES = {
    'acme': 'models.acme.ACMEHotel',
    'patagonia': 'models.patagonia.PatagoniaHotel',
    'paperflies': 'models.paperflies.PaperfliesHotel',
}
