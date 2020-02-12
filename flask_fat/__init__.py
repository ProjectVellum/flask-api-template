name = "flask_fat"
from . import config_builder
# Order matters! Import this first, since other modules wants to use it.
ConfigBuilder = config_builder.ConfigBuilder

from . import blueprints
from . import baseline

Journal = blueprints.bp_base.Journal
APIBaseline = baseline.APIBaseline