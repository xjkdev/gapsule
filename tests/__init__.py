from gapsule.settings import settings
import gapsule.models.connection
settings['dbname'] = 'gapsule_test'
gapsule.models.connection._connection = gapsule.models.connection._create_instance()
