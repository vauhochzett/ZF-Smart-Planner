"""Calculate arbitrary routes."""

import itertools
from enum import Enum
from typing import Tuple

import requests
from pyroutelib3 import Router

_CAR_ROUTER = Router("car")
_NOMINATIM_BASE_URL: str = (
    "https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&"
)


class RouteStatus(Enum):
    SUCCESS = "success"
    NO_ROUTE = "no_route"
    GAVE_UP = "gave_up"


class Route:
    def __init__(self, startpoint: str, destination: str):
        """Calculate a route based on free-text startpoint and destination."""
        start_node = Route._resolve_query(startpoint)
        dest_node = Route._resolve_query(destination)
        r_status: str
        r_status, r_route = _CAR_ROUTER.doRoute(start_node, dest_node)

        # set instance attributes
        self.status: RouteStatus = RouteStatus(r_status)
        self.node_ids_list: Tuple = r_route

    @staticmethod
    def _resolve_query(search_string: str):
        """Resolve search string to routing node."""
        api_response = requests.get(_NOMINATIM_BASE_URL + f"q={search_string}")
        response_data = api_response.json()
        latitude: float = float(response_data[0]["lat"])
        longitude: float = float(response_data[0]["lon"])
        return _CAR_ROUTER.findNode(latitude, longitude)

    def length(self):
        length: float = 0.0
        for node, next_node in itertools.pairwise(self.node_ids_list):
            length += next_node - node
        return length
