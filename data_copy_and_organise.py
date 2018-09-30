script_name = 'data_copy_and_organise' #Version - 2018-03-20
import function
from os import walk, makedirs, path
from shutil import copy2 as copy
import datetime
import sys
file_copy_limit, file_copy_count = 0, 0
folder_source_path, folder_destination_path, folder_log_path = sys.argv[1], sys.argv[2], sys.argv[3]
function.script_name, function.folder_log_path = script_name, folder_log_path
function.executeSoftware()
function.checkFolder(folder_source_path, 'Source Folder')
function.checkFolder(folder_destination_path, 'Destination Folder')
function.checkFolder(folder_log_path, 'Log Folder')
month_folder = { 1 : '01 JAN', 2 : '02 FEB', 3 : '03 MAR', 4 : '04 APR', 5 : '05 MAY', 6 : '06 JUN', 7 : '07 JUL', 8 : '08 AUG', 9 : '09 SEP', 10 : '10 OCT', 11 : '11 NOV', 12 : '12 DEC' }
try:
	function.writefile('Execution Start')
	for (dirpath, dirnames, filenames) in walk(folder_source_path):
		for file in filenames:
			if (not file_copy_limit == 0) and (file_copy_count > file_copy_limit):
				break
			file_date = datetime.datetime.strptime(file[4:12],'%Y%m%d').date()
			folder_year_name = str(file_date.year) + '-01 To ' + str(file_date.year) + '-12'
			folder_month_name = month_folder.get(file_date.month, '00 MON') + '-' + str(file_date.year)
			folder_shastra_name = dirpath[len(folder_source_path)+1:]
			create_folder = path.join(folder_destination_path, folder_year_name, folder_month_name)
			if not path.exists(path.join(create_folder, folder_shastra_name)):
				makedirs(path.join(create_folder, folder_shastra_name))
			file_path = path.join(dirpath.replace(folder_source_path, create_folder), file)
			if not path.exists(file_path):
				copy(path.join(dirpath, file), file_path)
				file_copy_count += 1
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')