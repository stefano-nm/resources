from .catalog import CatalogBase
from .utils import Service, get


class Resources(CatalogBase, Service):
    def __init__(
            self,
            service_name: str,
            service_address: str,
            service_token: str,
            catalog: str,
            supabase_endpoint: str,
            supabase_token: str,
            supabase_email: str,
            supabase_password: str,
            deletion_period: float = 60 * 60 * 24 * 7,
            debug: bool = False
    ):
        CatalogBase.__init__(
            self,
            supabase_endpoint=supabase_endpoint,
            supabase_token=supabase_token,
            supabase_email=supabase_email,
            supabase_password=supabase_password,
            supabase_table="resources",
            object_name="Resources",
            deletion_period=deletion_period,
            debug=debug
        )
        Service.__init__(
            self,
            name=service_name,
            address=service_address,
            token=service_token,
            catalog=catalog
        )

    @get
    def resources(self, **kwargs):
        return self._catalog(**kwargs)

    @get
    def resource(self, name: str, **kwargs):
        return self._object(name, **kwargs)
