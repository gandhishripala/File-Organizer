script_name = 'data_compare' #Version - 2018-05-26
import function
from os import walk, makedirs, path
from shutil import copy2 as copy
import sys
folder_source_path, folder_destination_path, folder_log_path = sys.argv[1], sys.argv[2], sys.argv[3]
function.script_name, function.folder_log_path = script_name, folder_log_path
#function.executeSoftware()
function.checkFolder(folder_source_path, 'Source Folder')
function.checkFolder(folder_destination_path, 'Destination Folder')
function.checkFolder(folder_log_path, 'Log Folder')
try:
	function.writefile('Execution Start')
	function.writefile('Scanning Source')
	print('Scanning Source')
	source_files = function.filesUnderDirectory(folder_source_path)
	function.writefile('Scanning Destination')
	print('Scanning Destination')
	destination_files = function.filesUnderDirectory(folder_destination_path)
	difference = set()
	difference = difference.union(source_files.difference(destination_files))
	difference = difference.union(destination_files.difference(source_files))
	for diff in difference:
		function.writefile('Non-matching Path: ' + diff)
		print('Non-matching Path: ' + diff)
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')