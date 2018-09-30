# File-Organizer
File Organizer for Audio Recording Data (Rajkot Mandir - Religious Place)

Custom File Organized developed to handle the requirement to handle Audio Recording data.

* [Data_Copier.bat](https://github.com/gandhishripala/File-Organizer/blob/master/Data_Copier.bat) is scheduled to execute on Hourly basis, which will call all the python scripts to do their specified tasks.

* [data_specialize.py](https://github.com/gandhishripala/File-Organizer/blob/master/data_specialize.py) looks at the Audio files that are in created in the custom date range and places it under a special folder on Google Drive. Folder name also gets updated to have the custom data range in the name of the folder.

* [data_copy_and_organise.py](https://github.com/gandhishripala/File-Organizer/blob/master/data_copy_and_organise.py) will organise the data in the yearly archieve folder format (for example: 2018 > 05 May 2018 > Shashtra Name > Audio File). Folders that don't exist are created.

* [data_replicate.py](https://github.com/gandhishripala/File-Organizer/blob/master/data_replicate.py) will replicate the data maintaining the folder structure of the Source Folder.

* [data_compare.py](https://github.com/gandhishripala/File-Organizer/blob/master/data_compare.py) compares the directory structure between the source the destination directories.

* [dvd_create.py](https://github.com/gandhishripala/File-Organizer/blob/master/dvd_create.py) will create DVD using the start date. It will fill the content of DVD upto 4.1 GB, if found.

* [dvd_rename.py](https://github.com/gandhishripala/File-Organizer/blob/master/dvd_rename.py) will rename the file inside the DVD created to have a consistent file naming inside all the DVDs.

* [log_copy.py](https://github.com/gandhishripala/File-Organizer/blob/master/log_copy.py) will copy the log generated during the execution of the script so that they can be analyzed at a later stage.

* [log_remove.py](https://github.com/gandhishripala/File-Organizer/blob/master/log_remove.py) will remove the local copy of the log after certain time frame.

* [function.py](https://github.com/gandhishripala/File-Organizer/blob/master/function.py) contains the shared library of the functions that are used across these files.

* [ExecutionTime.txt](https://github.com/gandhishripala/File-Organizer/blob/master/ExecutionTime.txt) contains the last time the code is executed. This is to check if the System Time gets reset to the default date. If so, it will prevent the script execution.
