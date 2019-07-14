from os import walk, path, sep
import datetime

class Functions():
	@staticmethod
	def GetFolderPath(directoryPath, specializeString):
		specializeFolderPath = None
		for (dirpath, dirnames, filenames) in walk(directoryPath):
			for dir in dirnames:
				if dir.startswith(specializeString):
					specializeFolderPath = path.join(dirpath, dir)
		return specializeFolderPath

	@staticmethod
	def DeleteEmptyFolders(destinationPath):
		for (dirpath, dirnames, filenames) in walk(destinationPath):
			if dirpath == destinationPath:
				continue
			if len(filenames) == 1 and filenames[0] == "desktop.ini":
				print("DeleteEmptyFolders1")
				try:
					remove(path.join(dirpath, filenames[0]))
					rmdir(dirpath)
				except OSError:
					continue
			if len(filenames) == 0:
				print("DeleteEmptyFolders0")
				try:
					rmdir(dirpath)
				except OSError:
					continue
	
	@staticmethod
	def ScanAllFiles(directoryPath, includeFolder = True):
		files = []
		for (dirpath, dirnames, filenames) in walk(directoryPath):
			directory_path_relative = path.relpath(dirpath, directoryPath)
			if includeFolder:
				[files.append(path.join(directory_path_relative, dir)) for dir in dirnames]
			[files.append(path.join(directory_path_relative, file)) for file in filenames if file != "desktop.ini"]
		return files
	
	@staticmethod
	def GenerateFileOrganisePath(fileRelativePath):
		monthFolder = { 1 : '01 JAN', 2 : '02 FEB', 3 : '03 MAR', 4 : '04 APR', 5 : '05 MAY', 6 : '06 JUN', 7 : '07 JUL', 8 : '08 AUG', 9 : '09 SEP', 10 : '10 OCT', 11 : '11 NOV', 12 : '12 DEC' }
		fileData = fileRelativePath.split(sep)
		folderShastraName, fileName = fileData[0], fileData[1]
		fileRecDate = datetime.datetime.strptime(fileName[4:12],'%Y%m%d').date()
		folderYear = str(fileRecDate.year) + '-01 To ' + str(fileRecDate.year) + '-12'
		folderMon = monthFolder.get(fileRecDate.month, '00 MON') + '-' + str(fileRecDate.year)
		return path.join(folderYear, folderMon, folderShastraName, fileName)
	
	@staticmethod
	def GetShastraName(videoStartDate, filesData):
		videoDate = videoStartDate.split(' ')
		organise_file_date = videoDate[0]
		organise_file_time = int(videoDate[1])
		probable_source_file = []
		for source_file in filesData:
			if '.mp3' not in source_file:
				continue
			source_file_name = source_file.split(sep)[-1]
			source_file_date = source_file_name[4:12]
			source_file_time = int(source_file_name[13:19])
			if((organise_file_date == source_file_date) and (abs(source_file_time - organise_file_time) <  (5 * 60))):
				probable_source_file.append(source_file)
		if len(probable_source_file) == 1:
			source_file_path = probable_source_file[0]
			if not source_file_path.find(sep) == -1:
				return source_file_path[:source_file_path.index(sep)]
		return None