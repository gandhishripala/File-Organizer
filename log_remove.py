script_name = 'log_remove' #Version - 2018-03-20
import function
from os import walk, unlink, path
import datetime
import sys
folder_log_path = sys.argv[1]
function.script_name, function.folder_log_path = script_name, folder_log_path
function.executeSoftware()
function.checkFolder(folder_log_path, 'Log Folder')
try:
	function.writefile('Execution Start')
	for (dirpath, dirnames, filenames) in walk(folder_log_path):
		for file in filenames:
			if datetime.datetime.strptime(file[:-4],'%Y-%m-%d').date() < (datetime.datetime.now().date()-datetime.timedelta(days=2)):
				file_path = path.join(dirpath, file)
				unlink(file_path)
				function.writefile(file_path + ' - Removed')
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')