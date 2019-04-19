from gapsule.settings import settings
import importlib
import gapsule.models.connection
settings['dbname'] = 'gapsule_test'
importlib.reload(gapsule.models.connection)
