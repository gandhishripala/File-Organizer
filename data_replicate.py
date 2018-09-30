script_name = 'data_replicate' #Version - 2018-03-20
import function
from os import walk, makedirs, path
from shutil import copy2 as copy
import sys
file_copy_limit, file_copy_count = int(sys.argv[4]), 0
folder_source_path, folder_destination_path, folder_log_path = sys.argv[1], sys.argv[2], sys.argv[3]
function.script_name, function.folder_log_path = script_name, folder_log_path
function.executeSoftware()
function.checkFolder(folder_source_path, 'Source Folder')
function.checkFolder(folder_destination_path, 'Destination Folder')
function.checkFolder(folder_log_path, 'Log Folder')
try:
	function.writefile('Execution Start')
	for (dirpath, dirnames, filenames) in walk(folder_source_path):
		check_path = dirpath.replace(folder_source_path, folder_destination_path)
		for file in filenames:
			if (not file_copy_limit == -1) and (file_copy_count >= file_copy_limit):
				break
			if not path.exists(path.join(check_path, file)):
				if not path.exists(check_path):
					makedirs(check_path)
				copy(path.join(dirpath, file), path.join(check_path, file))
				file_copy_count += 1
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')