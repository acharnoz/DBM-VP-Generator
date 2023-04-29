import requests

class WoWApi:

    def __init__(self):
        self.client_id = "cf439756d012472980bfd93654e74db5"
        self.client_pwd = "s3tw976mXyH58Um4KflY38oS9itRSdp7"
        self.region = "us"
        self.namespace = f"static-{self.region}"
        self.url = f"https://{self.region}.api.blizzard.com"
        self.lang = "en"
        self.lang_to_locale = {
            "fr": "fr_FR",
            "en": "en_US",
            "es": "es_ES",
            "de": "de_DE",
            "it": "it_IT",
        }
        self.headers = {}
        self.params = {}
        self.is_configured = False

    def configure(self):
        if not self.is_configured:
            self.set_headers()
            self.set_params()
            self.is_configured = True

    def create_access_token(self, client_id, client_secret, region):
        data = {'grant_type': 'client_credentials'}
        response = requests.post('https://%s.battle.net/oauth/token' %
                                 region, data=data, auth=(client_id, client_secret))
        return response.json()

    def get_access_token(self):
        response = self.create_access_token(
            self.client_id, self.client_pwd, self.region)
        print(response)
        access_token = response["access_token"]
        return access_token

    def set_headers(self):
        access_token = self.get_access_token()
        headers = {
            'Authorization': f"Bearer {access_token}",
        }
        print(headers)
        self.headers = headers

    def set_params(self):
        params = {
            'namespace': self.namespace,
            'locale': self.lang_to_locale[self.lang]
        }
        print(params)
        self.params = params


    # endpoint = '/data/wow/journal-expansion/499' # list shadowland raids donjons
    # endpoint = '/data/wow/journal-instance/1195' # info sur le sépulcre
    # endpoint = '/data/wow/journal-encounter/index' # liste de toutes les rencontres
    # endpoint = '/data/wow/journal-encounter/2465' # drop and spell boss
    # endpoint = '/data/wow/playable-class/2' # paladin
    # endpoint = '/data/wow/playable-specialization/65' # paladin sacré talents
    #endpoint = '/data/wow/spell/1022'
    def get_info(self, endpoint):
        response = requests.get(f"{self.url}{endpoint}",
                                params=self.params, headers=self.headers)
        return response

    def get_response(self, api, id):
        endpoint = f"/data/wow/{api}/{id}"
        response = self.get_info(endpoint)
        if response.status_code == 500:
            print(f"Error 500: api={api} id={id}")
            response = self.get_response(api, id)
        return response


    def get_journal_expansion(self, journal_expansion_id):
        self.configure()
        journal = self.get_response('journal-expansion', journal_expansion_id).json()
        return journal


    def get_journal_encounter(self, journal_encounter_id):
        self.configure()
        journal = self.get_response('journal-encounter', journal_encounter_id).json()
        return journal


    def get_journal_instance(self, journal_instance_id):
        self.configure()
        journal = self.get_response('journal-instance', journal_instance_id).json()
        return journal
