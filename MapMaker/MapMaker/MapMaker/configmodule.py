"""
[ AZURE STORAGE ]
This app uses Azure Storage Tables to store maps marker data, because it is extremely cheap!

When developing, you can install the Azure Storage Emulator and leave Azure Storage Name & Key equal = None
and IS_EMULATED = True. You can install emulator here: https://azure.microsoft.com/en-gb/documentation/articles/storage-use-emulator/

Otherwise, you can use a real Azure Storage account and set config accordingly.

[ GOOGLE MAPS JAVASCRIPT API ]
This app uses Google Maps Javascript API to display the map on the maps page.

When developing, you will need to provide an API key in this config file. Obtain one here:
https://console.developers.google.com/flows/enableapi?apiid=maps_backend,geocoding_backend,directions_backend,distance_matrix_backend,elevation_backend&keyType=CLIENT_SIDE&reusekey=true

"""
class BaseConfig(object):
    AZURE_STORAGE_ACCOUNT_NAME = None
    AZURE_STORAGE_ACCOUNT_KEY = None
    AZURE_STORAGE_ACCOUNT_IS_EMULATED = True
    GOOGLE_MAPS_API_KEY = ""


class DevelopmentConfig(BaseConfig):
    AZURE_STORAGE_ACCOUNT_NAME = None
    AZURE_STORAGE_ACCOUNT_KEY = None
    AZURE_STORAGE_ACCOUNT_IS_EMULATED = True
    GOOGLE_MAPS_API_KEY = ""


class ProductionConfig(BaseConfig):
    AZURE_STORAGE_ACCOUNT_NAME = "{{ ADDED UPON DEPLOYMENT }}"
    AZURE_STORAGE_ACCOUNT_KEY = "{{ OBVIOUSLY NOT IN SOURCE CONTROL }}"
    AZURE_STORAGE_ACCOUNT_IS_EMULATED = False
    GOOGLE_MAPS_API_KEY = "{{ AGAIN, NOT IN SOURCE CONTROL }}"