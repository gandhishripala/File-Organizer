from os import path, sep, makedirs
from shutil import copy2 as copy

from Functions import Functions

class CustomisedFileOperations():
	def ModifyFilesDataToOrganise(self, allFiles):
		allFilesToOrganise = []
		[allFilesToOrganise.append((files, Functions.GenerateFileOrganisePath(files))) for files in allFiles]
		self.fileData = allFilesToOrganise
	
	def OrganiseFiles(self, sourcePath, destinationPath):
		organiseFiles = [(sourceFile, destFile) for (sourceFile, destFile) in self.fileData if not path.exists(path.join(destinationPath, destFile))]
		for (sourceFile, destFilePath) in organiseFiles:
			completeSourceFilePath = path.join(sourcePath, sourceFile)
			completeDestinationFilePath = path.join(destinationPath, destFilePath)
			destFileData = destFilePath.split(sep)
			destFileName = destFileData.pop()
			destFolderPath = path.join(destinationPath, sep.join(destFileData))
			if not path.exists(destFolderPath):
				makedirs(destFolderPath)
			copy(completeSourceFilePath, completeDestinationFilePath)