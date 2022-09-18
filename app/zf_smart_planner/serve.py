"""Main entrypoint to start the server."""
import datetime as dt
from collections import namedtuple
from pathlib import Path
from typing import Optional

from bottle import TEMPLATE_PATH, request, route, run, static_file, template, response
from route import Route
from datalib import zfhandler
import random
import util

# Ensure that static files are accessible
static_dir: Optional[Path] = util.load_static("static")

TEMPLATE_PATH.append(static_dir / "html")


# Globals
TITLE = "🚚 ZF Smart Planner"


@route("/static/<ext>/<filename>")
def serve_static(ext, filename):
    """Return arbitrary static files."""
    return static_file(filename, root=f"./static/{ext}/")


## -- Pages -- ##


@route("/")
def index():
    """Return the homepage."""
    return template("index", title=TITLE)


@route("/result/truck", method="POST")
def trip():
    source: str = request.forms.get("source")
    dest: str = request.forms.get("dest")
    unit_size: str = request.forms.get("unit_size")
    unit_count: str = request.forms.get("unit_count")
    delivery_from: str = request.forms.get("delivery_from")
    delivery_to: str = request.forms.get("delivery_to")

    route: Route = Route(source, dest)
    length: float = route.length()
    unit_l, unit_b, unit_w = [float(u) for u in unit_size.lower().split("x")]
    volume: float = float(unit_count) * unit_l * unit_b * unit_w
    delivery_from_dt: dt.date = dt.datetime.strptime(delivery_from, "%Y-%m-%d")
    delivery_to_dt: dt.date = dt.datetime.strptime(delivery_to, "%Y-%m-%d")

    # Return the result page (1): truck
    Vehicle = namedtuple("Vehicle", ["id", "type", "size", "health"])
    best_vehicle_ids = zfhandler.get_vehicle(
        [zfhandler.KEYS.AvgFuelConsumption_per100km], top_k=3
    )
    load = ["19L x 7W x 7H", "22L x 7.5W x 7H", "19L x 7W x 7H"]
    colors = 10 * ["green"] + 4 * ["orange"] + 3 * ["red"]
    vehicles = [
        Vehicle(
            vid,
            zfhandler.VEHICLEID2PLATE[vid],
            random.choice(load),
            random.choice(colors),
        )
        for vid in best_vehicle_ids
    ]
    return template("result-truck", title=TITLE, vehicles=vehicles,)


@route("/result/driver/<vehicle_id>")
def result_driver(vehicle_id):
    """Return the result page (2): driver."""
    Driver = namedtuple("Driver", ["name", "trips_made", "score"])
    best_driver_ids = zfhandler.get_driver(
        [zfhandler.KEYS.AvgFuelConsumption_per100km], top_k=3
    )

    return template(
        "result-driver",
        title=TITLE,
        drivers=[
            Driver("Sabrina Murray", 198, 92),
            Driver("Gabriel Gibbs", 192, 86),
            Driver("Mark Diaz II", 200, 83),
        ],
        vehicle_id=vehicle_id,
    )


@route("/result/summary/<vehicle_id>/<driver_id>")
def result_summary(vehicle_id, driver_id):
    """Return the result page (3): summary."""

    return template(
        "result-summary",
        title=TITLE,
        driver=driver_id,
        truck=vehicle_id,
        expected_fuel_savings="1.25 liters",
        expected_co2_savings="1.2 kg",
    )


run(host="localhost", port=8975)
