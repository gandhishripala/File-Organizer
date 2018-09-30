#python "H:\My Drive\Rajkot Mandir\Audio Recordings - Software\dvd_rename.py" "E:\00 Important Data\02 Audio Recordings\DVD\DVD_78 [20-Jan-2018 To 13-Mar-2018]" "E:\Audio Recordings\Upload Log" "2017" "12" "2016" "68"
script_name = 'dvd_rename' #Version - 2018-03-20
import function
from os import walk, rename, path
import datetime
import sys
import re
folder_destination_path, folder_log_path, default_year, for_month, apply_year, dvd_no = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
function.script_name, function.folder_log_path = script_name, folder_log_path
#function.executeSoftware()
function.checkFolder(folder_destination_path, 'Destination Folder')
function.checkFolder(folder_log_path, 'Log Folder')
def format_name(file_name):
	name = {
		'Ashtapahud' : 'Ashtapahud',
		'Bahenshri na Vachnamrut' : 'BahenshriNaVachnamrut',
		'Bahenshri ni Sadhana Ane Vani' : 'BahenshriNiSadhanaAneVani',
		'Bruhad Dravyasangrah' : 'BruhadDravyasangrah',
		'Gurudevshri na Vachnamrut' : 'GurudevshriNaVachnamrut',
		'Mokshmarg Prakashak' : 'MokshmargPrakashak',
		'Panchadhyayi Parimal' : 'PanchadhyayiParimal',
		'Pravachansar' : 'Pravachansar',
		'Nay nu Swarup (Pravachansar)' : 'NayNuSwarup',
		'Purusharthsiddhi Upay' : 'PurusharthsiddhiUpay',
		'Samaysarji' : 'Samaysarji',
		'47 Shakti' : '47Shakti',
		'Jain Tatva Darshan' : 'JainTatvaDarshan',
		'Niyamsarji' : 'Niyamsarji',
		'Panchadhyayi' : 'Panchadhyayi',
		'Panchastikaya' : 'Panchastikaya',
		'Paramatma Prakash' : 'ParamatmaPrakash',
		'Samaysar Kalash Tika' : 'SamaysarKalashTika',
		'Adhikar (Samaysarji)' : 'Adhikar',
		'Nav Tatva nu Swarup (Samaysarji)' : 'NavTatvaNuSwarup',
		'Nay Tatva Pragnapan (Pravachansar)' : 'NayTatvaPragnapan',
		'Extra' : 'Extra',
		'Ratnakarandak Shravakachar' : 'RatnakarandakShravakachar',
		'Swami Kartikay Anupreksha' : 'SwamiKartikayAnupreksha',
		'Moksh Shastra' : 'MokshShastra',
	}
	return name.get(file_name,'Check')

def format_string(input, out_len):
	output = input
	if out_len > len(output):
		output = ('0' * (out_len - len(output))) + output
	return output

try:
	function.writefile('Execution Start')
	for (dirpath, dirnames, filenames) in walk(folder_destination_path):
		shastra_name = format_name(dirpath[len(folder_destination_path)+1:])
		for file in filenames:
			if not (file[:1].isdigit()) and not (file == "desktop.ini"):
				try:
					file_date = datetime.datetime.strptime(file[4:12],'%Y%m%d').date()
				except Exception as ex:
					file_date = datetime.datetime.strptime(file[3:7],'%m%d').date()
					if file_date.month == for_month:
						file_date = file_date.replace(year=apply_year)
					else:
						file_date = file_date.replace(year=default_year)
				new_name = format_string(str(file_date.year), 4) + format_string(str(file_date.month), 2) + format_string(str(file_date.day), 2) + '_' + shastra_name + '_' + format_string(str(dvd_no), 3) + '.mp3'
				print(file, new_name)
				#rename(path.join(dirpath, file), path.join(dirpath, new_name))
	function.writefile('Execution End - Success')
	function.printsuccess()
except Exception as ex:
	print(ex)
	function.printerror()
	function.writefile(ex)
	function.writefile('Execution End - Failure')