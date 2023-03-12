import requests


class Service:
    def __init__(
            self,
            name: str,
            address: str,
            catalog: str,
            token: str = None
    ):
        if address is None:
            return
        self._service_name = name
        self._service_catalog = catalog
        self._service_address = address
        self._service_token = token
        self.service_register()

    def service_register(self):
        response = requests.post(f"{self._service_catalog}/register", params={
            "name": self._service_name,
            "endpoint": self._service_address,
            "token": self._service_token
        })
        pass

    def service_unregister(self):
        requests.delete(f"{self._service_catalog}/unregister", params={
            "name": self._service_name,
            "token": self._service_token
        })
