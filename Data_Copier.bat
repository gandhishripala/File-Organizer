@echo off
echo Processing Audio Recording Files.....Please Wait
set "gDriveRMPath=G:\My Drive\Rajkot Mandir"
set "gDriveULPath=%gDriveRMPath%\Audio Recordings - Upload Log"
set "gDriveARPath=%gDriveRMPath%\Audio Recordings - Dr. Pravin Doshi Saheb"
set "gDriveSWPath=%gDriveRMPath%\Audio Recordings - Software"
set "gDriveCRPath=%gDriveARPath%" REM Depricated - Resolved at Runtime from function.py
set "gDriveCRDPath=%gDriveARPath%\Current Removed Recordings"
set "gDriveDVDPath=%gDriveARPath%\DVDs"
set "gDriveBackupOFPath=%gDriveARPath%\Backup - Original Files"
set "gDriveBackupDVDPath=%gDriveARPath%\Backup - DVDs"
set "localARPath=E:\Audio Recordings\01 Dr. Saheb"
set "localULPath=E:\Audio Recordings\Upload Log"
set "localBackupOFPath=E:\00 Important Data\02 Audio Recordings\Backup - Original Files"
set "localDVDPath=E:\00 Important Data\02 Audio Recordings\DVD"
REM Upload to Current Recordings Folder
python "%gDriveSWPath%\data_specialize.py" "%localARPath%" "%gDriveCRPath%" "%localULPath%" "%gDriveCRDPath%"
echo Step 1 of 7 Completed
REM Copy data from Recording Folder to Local ORG Folder
python "%gDriveSWPath%\data_copy_and_organise.py" "%localARPath%" "%localBackupOFPath%" "%localULPath%"
echo Step 2 of 7 Completed
REM Copy data from Local ORG Folder to Drive ORG Folder
python "%gDriveSWPath%\data_replicate.py" "%localBackupOFPath%" "%gDriveBackupOFPath%" "%localULPath%" "3"
echo Step 3 of 7 Completed
REM Copy data from Source DVD Folder to Drive DVD Folder
python "%gDriveSWPath%\data_replicate.py" "%localDVDPath%" "%gDriveDVDPath%" "%localULPath%" "3"
echo Step 4 of 7 Completed
REM Copy data from Source DVD Folder to Drive Backup DVD Folder
python "%gDriveSWPath%\data_replicate.py" "%localDVDPath%" "%gDriveBackupDVDPath%" "%localULPath%" "3"
echo Step 5 of 7 Completed
python "%gDriveSWPath%\log_copy.py" "%localULPath%" "%gDriveULPath%" "%localULPath%"
echo Step 6 of 7 Completed
python "%gDriveSWPath%\log_remove.py" "%localULPath%"
echo Step 7 of 7 Completed