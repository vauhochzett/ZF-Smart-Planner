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
          <h1 class="mt-3">Trip Details</h1>
          <form>
            <div class="mb-3">
              <label for="source" class="form-label">Source</label>
              <input type="text" placeholder="Munich" class="form-control" name="source" id="source">
            </div>
            <div class="mb-3">
              <label for="dest" class="form-label">Destination</label>
              <input type="text" placeholder="Zurich" class="form-control" name="dest" id="dest">
            </div>
            <div class="mb-3">
              <label for="unit_size" class="form-label">Unit Size (m)</label>
              <input type="text" placeholder="LxBxW" class="form-control" name="unit_size" id="unit_size">
            </div>
            <div class="mb-3">
              <label for="unit_count" class="form-label">Unit Count</label>
              <input type="number" placeholder="100" class="form-control" name="unit_count" id="unit_count">
            </div>
            <div class="mb-3">
              <label for="delivery_from" class="form-label">Earliest Delivery</label>
              <input type="date" class="form-control" name="delivery_from" id="delivery_from">
            </div>
            <div class="mb-3">
              <label for="delivery_to" class="form-label">Latest Delivery</label>
              <input type="date" class="form-control" name="delivery_to" id="delivery_to">
            </div>
            <button type="submit" class="btn btn-primary">Plan Optimal Trip</button>
          </form>
        </div>
        <div class="col-xl-2"></div>
      </div>
    </div>
  </body>
</html>
