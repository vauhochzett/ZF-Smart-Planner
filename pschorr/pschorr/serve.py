"""Main entrypoint to start the server."""
from pathlib import Path
from typing import Optional

from bottle import route, run, static_file, template

# Ensure that static files are accessible
static_dir: Optional[Path] = None
for static_path in (search_dirs := ["./static", "../static", "./pschorr/static"]):
    if (the_dir := Path(static_path)).exists():
        static_dir = the_dir
if static_dir is None:
    raise IOError(f"Could not find static dir. Searched directories: {search_dirs}")


@route("/")
def index():
    """Return the homepage."""
    return template("<b>Hello, {{ name }}</b>!", name="world")


@route("/static/<ext>/<filename>")
def serve_static(ext, filename):
    """Return arbitrary static files."""
    return static_file(filename, root=f"./static/{ext}/")


run(host="localhost", port=8975)
