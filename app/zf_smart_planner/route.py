"""Calculate arbitrary routes."""

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
        nominatim_r_str = requests.get(_NOMINATIM_BASE_URL + f"q={search_string}")
        nominatim_r = nominatim_r_str.json()
        latitude: str = nominatim_r["lat"]
        longitude: str = nominatim_r["lon"]
        return _CAR_ROUTER.findNode(latitude, longitude)

    def length(self):
        return 200
