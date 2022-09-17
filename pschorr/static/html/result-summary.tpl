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
          <h1 class="mt-3">📌 Trip Summary</h1>
          <div class="card mt-3">
            <div class="card-body">
              🚚 Truck: {{ truck }}
            </div>
          </div>
          <div class="card mt-3">
            <div class="card-body">
              👤 Driver: {{ driver }}
            </div>
          </div>
          <div class="card mt-3">
            <div class="card-body">
              💲 Expected fuel savings: {{ expected_fuel_savings }}
            </div>
          </div>
          <div class="card mt-3">
            <div class="card-body">
              🌍 Expected CO2 savings: {{ expected_co2_savings }}
            </div>
          </div>
        </div>
        <div class="col-xl-2"></div>
      </div>
    </div>
  </body>
</html>
