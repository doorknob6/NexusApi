"""Module containing the base Api class."""
from urllib3.util.retry import Retry
from requests_toolbelt import sessions
from NexusApi.TimeoutHttpAdapter import TimeoutHttpAdapter
import math

class NexusApi():
    """This class provides the base class for API calls."""

    def __init__(self, token=None,
                 base_url=r'https://api.nexushub.co/',
                 timeout=1):
        """
        Initialize the NexusApi class and optionally attach an authentication token.

        Args:
            token (str): Authentication token the API.
            base_url (str, optional): Base URL for calls to the API.
                Defaults to r'https://api.nexushub.co/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        self.token = token
        self.http = sessions.BaseUrlSession(base_url)
        self.http.hooks['response'] = [lambda response, *args, **kwargs: response.raise_for_status()]
        retries = Retry(total=6, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = TimeoutHttpAdapter(timeout=timeout, max_retries=retries)
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def get_items_items(self, server, item_id, endpoint=r'wow-classic/v1/items/:server/:item'):
        """
        Send a GET items-items request to the API, returns the item stats.

        Args:
            server (str): server name for the which the item stats are to be found.
            item_id (str, int): item id for the item to be found.
            endpoint (str, optional): endpoint for the GET items-items request. Defaults to r'wow-classic/v1/items/:server/:item'.

        Raises:
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors.

        Returns:
            dict(JsonApiObject): JsonApi object in the form of a dict.

        """
        try:
            token = self.token
        except AttributeError:
            raise ValueError("Please initialise the Api class.")

        headers = {}

        if token is not None:
            headers.update({'Authorization' : "Bearer {}".format(token)})

        endpoint = endpoint.replace(":server", server).replace(":item", str(item_id))

        resp = self.http.get(endpoint, headers=headers)

        if resp.status_code == 200:
            cont = resp.json()
            return cont

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

class Price():

    def __init__(self, price):
        self.price = price
        self.__update__()

    def __update__(self):
        self.g = math.floor(self.price / 10000)
        self.s = math.floor((self.price % 10000) / 100)
        self.c = (self.price % 10000) % 100

    def __repr__(self):
        return f"{self.g}g {self.s}s {self.c}c"

    def __str__(self):
        return f"{self.g}g {self.s}s {self.c}c"

    def __add__(self, other):
        return self.price + other

    def __radd__(self, other):
        return other + self.price

    def __sub__(self, other):
        return self.price - other

    def __rsub__(self, other):
        return other - self.price

    def __mul__(self, other):
        return self.price * other

    def __rmul__(self, other):
        return self.price * other

    def __truediv__(self, other):
        return self.price / other

    def __rtruediv__(self, other):
        return other / self.price

    def __floordiv__(self, other):
        return self.price // other

    def __rfloordiv(self, other):
        return other // self.price

    def __mod__(self, other):
        return self.price % other

    def __rmod__(self, other):
        return other % self.price

    def __lt__(self, other):
        return self.price < other

    def __le__(self, other):
        return self.price <= other

    def __eq__(self, other):
        return self.price == other

    def __ne__(self, other):
        return self.price != other

    def __gt__(self, other):
        return self.price > other

    def __ge__(self, other):
        return self.price >= other