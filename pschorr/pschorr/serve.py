"""Main entrypoint to start the server."""
import datetime as dt
from collections import namedtuple
from pathlib import Path
from typing import Optional

from bottle import TEMPLATE_PATH, request, route, run, static_file, template
from route import Route

# Ensure that static files are accessible
static_dir: Optional[Path] = None
for static_path in (search_dirs := ["./static", "../static", "./pschorr/static"]):
    if (the_dir := Path(static_path)).exists():
        static_dir = the_dir
if static_dir is None:
    raise IOError(f"Could not find static dir. Searched directories: {search_dirs}")

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

    # route: Route = Route(source, dest)
    # unit_l, unit_b, unit_w = [float(u) for u in unit_size.lower().split("x")]
    # volume: float = float(unit_count) * unit_l * unit_b * unit_w
    # delivery_from_dt: dt.date = dt.datetime.strptime(delivery_from, "%Y-%m-%d")
    # delivery_to_dt: dt.date = dt.datetime.strptime(delivery_to, "%Y-%m-%d")

    # Return the result page (1): truck
    Vehicle = namedtuple("Vehicle", ["id", "type", "size", "health"])
    return template(
        "result-truck",
        title=TITLE,
        vehicles=[
            Vehicle("5HJW078", "BigManCar", "19L x 7W x 7H", "green"),
            Vehicle("702-TSS", "Taurus232", "22L x 7.5W x 7H", "green"),
            Vehicle("PES 193", "TataMotors365", "19L x 7W x 7H", "orange"),
        ],
    )


@route("/result/driver")
def result_driver():
    """Return the result page (2): driver."""
    Driver = namedtuple("Driver", ["name", "trips_made", "score"])
    return template(
        "result-driver",
        title=TITLE,
        drivers=[
            Driver("Sabrina Murray", 198, 92),
            Driver("Gabriel Gibbs", 192, 86),
            Driver("Mark Diaz II", 200, 83),
        ],
    )


@route("/result/summary")
def result_summary():
    """Return the result page (3): summary."""
    return template(
        "result-summary",
        title=TITLE,
        driver="Sabrina Murray",
        truck="PES 193",
        expected_fuel_savings="1.25 liters",
        expected_co2_savings="1.2 kg",
    )


## -- API for frontend -- ##


@route("/vehicles", method="POST")
def vehicles():
    unit_length: str = request.forms.get("unit_length")
    unit_width: str = request.forms.get("unit_width")
    unit_height: str = request.forms.get("unit_height")
    unit_count: str = request.forms.get("unit_count")
    raise NotImplementedError()


run(host="localhost", port=8975)
