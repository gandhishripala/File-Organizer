import datetime
from os import walk, path, sep, makedirs, rename
from shutil import copy2 as copy

from CustomisedFileOperations import CustomisedFileOperations
from Functions import Functions

class SpecializeFileOperations(CustomisedFileOperations):
	def GetFiles(self, allFiles):
		startDate = datetime.datetime.now().date()-datetime.timedelta(days=9)
		specializeFiles = []
		[specializeFiles.append(files) for files in allFiles if datetime.datetime.strptime(files.split(sep)[-1][4:12],'%Y%m%d').date() > startDate]
		sortedSpecializeFiles = sorted(specializeFiles, key = lambda current : current.split(sep)[-1][4:12])
		self.specializeFiles = sortedSpecializeFiles
		self.GetDates()
	
	def GetDates(self):
		self.specializeMinDate = None
		self.specializeMaxDate = None
		if len(self.specializeFiles) > 0:
			self.specializeMinDate = datetime.datetime.strptime(self.specializeFiles[0].split(sep)[-1][4:12],'%Y%m%d').strftime('%Y-%m-%d')
			self.specializeMaxDate = datetime.datetime.strptime(self.specializeFiles[(len(self.specializeFiles)-1)].split(sep)[-1][4:12],'%Y%m%d').strftime('%Y-%m-%d')
	
	def AddData(self, sourcePath, destinationPath):
		for file in self.specializeFiles:
			completeSourceFilePath = path.join(sourcePath, file)
			completeDestinationFilePath = path.join(destinationPath, file)
			if not path.exists(completeDestinationFilePath):
				folderPathToCheck = completeDestinationFilePath.split(sep)
				fileName = folderPathToCheck.pop()
				folderPath = sep.join(folderPathToCheck)
				if not path.exists(folderPath):
					makedirs(folderPath)
				copy(completeSourceFilePath, completeDestinationFilePath)
	
	def MoveData(self, destinationPath, movePath):
		currentFileContents = Functions.ScanAllFiles(destinationPath, False)
		dataToRemove = [file for file in currentFileContents if file not in self.specializeFiles]
		if len(dataToRemove) > 0:
			for file in dataToRemove:
				completeDestinationFilePath = path.join(destinationPath, file)
				completeMoveFilePath = path.join(movePath, file)
				folderPathToCheck = completeMoveFilePath.split(sep)
				fileName = folderPathToCheck.pop()
				folderPath = sep.join(folderPathToCheck)
				if not path.exists(folderPath):
					makedirs(folderPath)
				rename(completeDestinationFilePath, completeMoveFilePath)
	
	def UpdateFolderName(self, destinationPath, specializeString):
		destinationFolderPath = destinationPath.split(sep)
		destinationFolderPath.pop()
		if self.specializeMinDate and self.specializeMaxDate:
			destinationFolderPath.append(specializeString + " [" + self.specializeMinDate + " To " + self.specializeMaxDate + "]")
		else:
			destinationFolderPath.append(specializeString)
		specializationPath = sep.join(destinationFolderPath)
		rename(destinationPath, specializationPath)
		
	def PerformSpecializeOperations(self, allFiles, sourcePath, specializeFolder, movePath):
		self.GetFiles(allFiles)
		self.AddData(sourcePath, specializeFolder)
		self.MoveData(specializeFolder, movePath)
		Functions.DeleteEmptyFolders(specializeFolder)
		self.UpdateFolderName(specializeFolder, "Current Recordings")