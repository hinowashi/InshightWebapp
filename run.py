#!/usr/bin/env python
from flaskexample import app
app.run(debug = True)
app.use("/static", express.static('./static/'));

