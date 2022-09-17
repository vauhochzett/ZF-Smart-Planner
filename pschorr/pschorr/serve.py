"""Main entrypoint to start the server."""
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


@route("/")
def index():
    """Return the homepage."""
    return template("index", title="Hello", name="world")


@route("/static/<ext>/<filename>")
def serve_static(ext, filename):
    """Return arbitrary static files."""
    return static_file(filename, root=f"./static/{ext}/")


## -- API for frontend -- ##


@route("/drivers", method="POST")
def drivers():
    startpoint: str = request.forms.get("startpoint")
    destination: str = request.forms.get("destination")
    route: Route = Route(startpoint, destination)
    raise NotImplementedError()


@route("/vehicles", method="POST")
def vehicles():
    unit_length: str = request.forms.get("unit_length")
    unit_width: str = request.forms.get("unit_width")
    unit_height: str = request.forms.get("unit_height")
    unit_count: str = request.forms.get("unit_count")
    raise NotImplementedError()


run(host="localhost", port=8975)
