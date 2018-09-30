script_name = 'function' #Version - 2018-03-20
from colorama import init #pip install colorama
from termcolor import colored #pip install termcolor
from os import path, walk
import datetime
init()
def executeSoftware():
	Execute = False
	with open('G:\My Drive\Rajkot Mandir\Audio Recordings - Software\ExecutionTime.txt', 'r') as output_file:
		lastExecutionDate = datetime.datetime.strptime(output_file.read(),'%Y_%m_%d_%H_%M_%S_%f')
		if lastExecutionDate < datetime.datetime.now():
			Execute = True
	if Execute is True:
		with open('G:\My Drive\Rajkot Mandir\Audio Recordings - Software\ExecutionTime.txt', 'w') as output_file:
			output_file.write(str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')))
	else:
		printerror()
		writefile('Software Execution End - Failure')
		exit()
def writefile(string):
	with open(path.join(folder_log_path, str(datetime.datetime.now().date()) + '.log'), 'a') as output_file:
		output_file.write(str(datetime.datetime.now()) + '\t' + str(script_name) + '\t' + str(string) + '\n')
def printerror():
	print(colored('Error Occured during execution. Check log file for more details.', 'yellow'))
def printsuccess():
	print(colored('Success.', 'green'))
def checkFolder(folder_path, folder_type):
	if not path.exists(folder_path):
		printerror()
		writefile(folder_type + ' - ' + folder_path + ' - Not Found')
		writefile('Execution End - Failure')
		exit()
	else:
		writefile(folder_type + ' - ' + folder_path + ' - Found')
def filesUnderDirectory(directoryPath):
	directory_files = set()
	for (dirpath, dirnames, filenames) in walk(directoryPath):
		directory_path_relative = dirpath.replace(directoryPath, '')
		for dir in dirnames:
			directory_files.add(path.join(directory_path_relative, dir))
		for file in filenames:
			if file == "desktop.ini":
				continue
			directory_files.add(path.join(directory_path_relative, file))
	return directory_files
def getCurrentRecordingFolderPath(directoryPath):
	for (dirpath, dirnames, filenames) in walk(directoryPath):
		for dir in dirnames:
			if dir.startswith("Current Recordings"):
				return path.join(dirpath, dir)