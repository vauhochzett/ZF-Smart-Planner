<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="/static/css/bootstrap.min.css" />
    <title>{{title}}</title>
  </head>
  <body>
    <nav class="navbar bg-light">
      <div class="container-fluid text-center">
        <span class="navbar-brand mb-0 h1">{{ title }}</span>
      </div>
    </nav>
    <div class="container text-center">
      <div class="row">
        <div class="col-xl-2"></div>
        <div class="col-xl-8">
          <h1 class="mt-3">Top Vehicles for Trip</h1>
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col"># Trips Made</th>
                <th scope="col">Score</th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              % for driver in drivers:
              <tr>
                <td>{{ driver.name }}</td>
                <td>{{ driver.trips_made }}</td>
                <td>{{ driver.score }}</td>
                <td><a href="/result/summary" class="btn btn-primary" role="button">Select Driver</a></td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
        <div class="col-xl-2"></div>
      </div>
    </div>
  </body>
</html>
