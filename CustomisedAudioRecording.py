from SpecializeFileOperations import SpecializeFileOperations
from Settings import Settings
from Functions import Functions

class CustomisedAudioRecording():
	def __init__(self, pathSuffix):
		self.LocalMainPath = Settings.GetValue(pathSuffix + "LocalMainPath")
		self.GDriveMainPath = Settings.GetValue(pathSuffix + "GDriveMainPath")
		self.CurrentRecordings = "Current Recordings"
		self.GDriveRemovePath = Settings.GetValue(pathSuffix + "GDriveRemovePath")
		self.LocalBackupPath = Settings.GetValue(pathSuffix + "LocalBackupPath")
		self.GDriveBackupPath = Settings.GetValue(pathSuffix + "GDriveBackupPath")
		self.SourceFiles = Functions.ScanAllFiles(self.LocalMainPath, False)
	
	def PerformOperations(self):
		organiseData = SpecializeFileOperations()
		organiseSpecializeFolder = Functions.GetFolderPath(self.GDriveMainPath, self.CurrentRecordings)
		if organiseSpecializeFolder:
			organiseData.PerformSpecializeOperations(self.SourceFiles, self.LocalMainPath, organiseSpecializeFolder, self.GDriveRemovePath)
		organiseData.ModifyFilesDataToOrganise(self.SourceFiles)
		organiseData.OrganiseFiles(self.LocalMainPath, self.LocalBackupPath)
		organiseData.OrganiseFiles(self.LocalMainPath, self.GDriveBackupPath)
	
	def GetFiles(self):
		return self.SourceFiles