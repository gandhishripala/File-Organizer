script_name = 'data_specialize' #Version - 2018-03-20
import function
from os import walk, makedirs, rmdir, path, remove, rename
from shutil import copy2 as copy
import datetime
import sys
folder_source_path, folder_destination_path_arg, folder_log_path, folder_remove_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
function.script_name, function.folder_log_path = script_name, folder_log_path
function.executeSoftware()
folder_destination_path = function.getCurrentRecordingFolderPath(folder_destination_path_arg)
function.checkFolder(folder_source_path, 'Source Folder')
function.checkFolder(folder_destination_path, 'Destination Folder')
function.checkFolder(folder_log_path, 'Log Folder')
try:
	function.writefile('Execution Start')
	specializeEndDate = datetime.datetime.now().date()
	specializeStartDate = datetime.datetime.now().date()-datetime.timedelta(days=8)
	minFileDate = specializeEndDate
	maxFileDate = specializeStartDate
	for (dirpath, dirnames, filenames) in walk(folder_source_path):
		check_path = dirpath.replace(folder_source_path, folder_destination_path)
		for file in filenames:
			if not path.exists(path.join(check_path, file)) and (datetime.datetime.strptime(file[4:12],'%Y%m%d').date() > specializeStartDate):
				if not path.exists(check_path):
					makedirs(check_path)
				copy(path.join(dirpath, file), path.join(check_path, file))
	for (dirpath, dirnames, filenames) in walk(folder_destination_path):
		if dirpath == folder_destination_path:
			continue
		if len(filenames) == 1 and filenames[0] == "desktop.ini":
			try:
				remove(path.join(dirpath, filenames[0]))
				rmdir(dirpath)
			except OSError:
				continue
		if len(filenames) == 0:
			try:
				rmdir(dirpath)
			except OSError:
				continue
		for file in filenames:
			if (not file == "desktop.ini"):
				fileDate = datetime.datetime.strptime(file[4:12],'%Y%m%d').date()
				if (fileDate < minFileDate):
					minFileDate = fileDate
				if (fileDate > maxFileDate):
					maxFileDate = fileDate
				if (not fileDate > specializeStartDate):
					check_path = dirpath.replace(folder_destination_path, folder_remove_path)
					if not path.exists(check_path):
						makedirs(check_path)
					rename(path.join(dirpath, file), path.join(check_path, file))
					#remove(path.join(dirpath, file))
	rename(folder_destination_path, path.join(folder_destination_path_arg, "Current Recordings [" + minFileDate.strftime('%Y-%m-%d') + " To " + maxFileDate.strftime('%Y-%m-%d') + "]"))
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')