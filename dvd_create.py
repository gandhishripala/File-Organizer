script_name = 'dvd_create' #Version - 2018-03-20
import function
from os import walk, mkdir, path, rmdir, makedirs
from shutil import copy2 as copy
import datetime
import sys
folder_source_path, folder_destination_path, folder_log_path, dvd_start_date, dvd_number = sys.argv[1], sys.argv[2], sys.argv[3], datetime.datetime.strptime(sys.argv[4],'%Y-%m-%d').date(), sys.argv[5]
function.script_name, function.folder_log_path = script_name, folder_log_path
function.executeSoftware()
function.checkFolder(folder_source_path, 'Source Folder')
function.checkFolder(folder_destination_path, 'Destination Folder')
function.checkFolder(folder_log_path, 'Log Folder')
try:
	function.writefile('Execution Start')
	file_size_data, nodate_max_count, nodate_count = {}, 15, 0
	for (dirpath, dirnames, filenames) in walk(folder_source_path):
		for file in filenames:
			try:
				file_date = datetime.datetime.strptime(file[4:12],'%Y%m%d').date()
			except Exception as ex:
				file_date = datetime.datetime.strptime(file[3:7],'%m%d').date()
				file_date = file_date.replace(year=2015)
			if file_date >= dvd_start_date:
				file_date = file_date.strftime('%Y%m%d')
				file_size_data[file_date] = file_size_data.get(file_date, 0) + path.getsize(path.join(dirpath, file))
	dvd_end_date, dvd_counter_date, dvd_current_size, dvd_max_size = dvd_start_date, dvd_start_date, 0, 4.1*1024*1024*1024
	while dvd_current_size <= dvd_max_size:
		file_date_size = file_size_data.get(dvd_counter_date.strftime('%Y%m%d'), 0)
		if file_date_size == 0:
			print('No data for date:', dvd_counter_date.strftime('%Y%m%d'))
			nodate_count += 1
		else:
			nodate_count = 0
		if nodate_count > nodate_max_count:
			dvd_end_date = None
			print('No-date limit exceeds. Probably not enough data for DVD')
			function.printerror()
			function.writefile('No-date limit exceeds. Probably not enough data for DVD')
			function.writefile('Execution End - Failure')
			exit()
		if dvd_current_size + file_date_size <= dvd_max_size:
			dvd_end_date = dvd_counter_date
			dvd_counter_date += datetime.timedelta(days=1)
			dvd_current_size += file_date_size
		else:
			break
	if dvd_end_date is not None:
		dvd_folder_name = 'DVD_' + dvd_number + ' [' + dvd_start_date.strftime('%d-%b-%Y') + ' To ' + dvd_end_date.strftime('%d-%b-%Y') + ']'
		folder_destination_path = path.join(folder_destination_path, dvd_folder_name)
		if path.exists(folder_destination_path):
			print('DVD Folder already exists')
			function.printerror()
			function.writefile('DVD Folder already exists')
			function.writefile('Execution End - Failure')
			exit()
		else:
			mkdir(folder_destination_path)
		for (dirpath, dirnames, filenames) in walk(folder_source_path):
			check_path = dirpath.replace(folder_source_path, folder_destination_path)
			for file in filenames:
				try:
					file_date = datetime.datetime.strptime(file[4:12],'%Y%m%d').date()
				except Exception as ex:
					file_date = datetime.datetime.strptime(file[3:7],'%m%d').date()
					file_date = file_date.replace(year=2015)
				if (not path.exists(path.join(check_path, file))) and file_date >= dvd_start_date and file_date <= dvd_end_date:
					if not path.exists(check_path):
						makedirs(check_path)
					copy(path.join(dirpath, file), path.join(check_path, file))
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	print(ex)
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')
#python "H:\My Drive\Rajkot Mandir\Audio Recordings - Software\script_create_dvd.py" "E:\00 Important Data\02 Audio Recordings\Backup - Original Files" "E:\00 Important Data\02 Audio Recordings\DVD" "E:\Audio Recordings\Upload Log" "2018-01-20" "78"
