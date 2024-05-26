from . import base
from . import webi
from .webi.app import app

app.run('0.0.0.0', 80)