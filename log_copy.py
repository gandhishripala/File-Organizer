script_name = 'log_copy' #Version - 2018-03-20
import function
from os import walk, path
from shutil import copy2 as copy
import datetime
import sys
folder_source_path, folder_destination_path, folder_log_path = sys.argv[1], sys.argv[2], sys.argv[3]
function.script_name, function.folder_log_path = script_name, folder_log_path
function.executeSoftware()
function.checkFolder(folder_source_path, 'Source Folder')
function.checkFolder(folder_destination_path, 'Destination Folder')
try:
	for (dirpath, dirnames, filenames) in walk(folder_source_path):
		for file in filenames:
			if datetime.datetime.strptime(file[:-4],'%Y-%m-%d').date() <= (datetime.datetime.now().date()):
				check_path = dirpath.replace(folder_source_path, folder_destination_path)
				copy(path.join(dirpath, file), path.join(check_path, file))
	function.printsuccess()
except Exception as ex:
	function.writefile(ex)
	function.writefile('Execution End - Failure')
	function.printerror()