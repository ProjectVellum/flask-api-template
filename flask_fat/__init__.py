name = "flask_fat"
from . import blueprints
from . import baseline

Journal = blueprints.bp_base.Journal
APIBaseline = baseline.APIBaseline

# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.startswith('__')]

# name = "flask_fat"
# from os.path import dirname, basename, isfile
# import glob
# modules = glob.glob(dirname(__file__)+"/*.py")

# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.startswith('__')]
# __all__.append('blueprints')

# Journal = blueprints.bp_base.Journal
# APIBaseline = baseline.APIBaseline