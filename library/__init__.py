import pymysql

__version__ = '1.0.0'
VERSION = tuple(__version__.split("."))
default_app_config = "library.apps.LibraryAppConfig"

pymysql.install_as_MySQLdb()
