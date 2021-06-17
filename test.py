from sitec.sitec_api.models import SitecApi

api = SitecApi()

# api.login('18212170', 'jajatujefa42')
api.is_connected = True

print(api.retrieve_panel_data())