from gapsule.settings import settings
import gapsule.models.connection
import importlib
settings['dbname'] = 'gapsule_test'
importlib.reload(gapsule.models.connection)
