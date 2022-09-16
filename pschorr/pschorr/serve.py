"""Main entrypoint to start the server."""
from bottle import route, run, template


@route("/")
def index():
    """Returns the homepage."""
    return template("<b>Hello, {{ name }}</b>!", name="world")


run(host="localhost", port=8975)
