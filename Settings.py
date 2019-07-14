import sqlite3
import os

class Settings():
	Data = dict()
	DBPATH = "Youtube_Recoding_Data"
	
	@classmethod
	def RegisterPath(cls):
		pathToRegister = os.path.dirname(__file__) + os.sep + "webdrivers"
		os.environ["PATH"] += os.pathsep + pathToRegister
	
	@classmethod
	def GetValue(cls, key):
		return cls.Data[key] if key in cls.Data.keys() else None
	
	@classmethod
	def RefreshData(cls):
		connection = sqlite3.connect(cls.DBPATH)
		cursor = connection.cursor()
		cursor.execute('''SELECT SettingsKey, SettingsValue FROM SettingsData''')
		cls.Data = dict()
		cls.Data["DatabasePath"] = cls.DBPATH
		for fetch_data in cursor:
			cls.Data[fetch_data[0]] = str(fetch_data[1])