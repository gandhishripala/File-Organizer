#pip install google-api-python-client
#pip install google_auth_oauthlib
from collections import OrderedDict
import datetime
from os import path, walk, sep

from CustomisedYoutubeService import CustomisedYoutubeService
from CustomisedDatabase import CustomisedDatabase
from CustomisedAudioRecording import CustomisedAudioRecording
from Settings import Settings
from Functions import Functions

try:
	Settings.RegisterPath()
	Settings.RefreshData()
	print("Organising Local Data...")
	print("Organising Audio Recordings...")
	print("Organising Folder Alpha...")
	alphaData = CustomisedAudioRecording("Alpha")
	alphaData.PerformOperations()
	alphaSourceFiles = alphaData.GetFiles()
	print("Organising Folder Beta...")
	betaData = CustomisedAudioRecording("Beta")
	betaData.PerformOperations()
	betaSourceFiles = betaData.GetFiles()
	print("Organising Folder Gamma...")
	gammaData = CustomisedAudioRecording("Gamma")
	gammaData.PerformOperations()
	gammaSourceFiles = gammaData.GetFiles()
	print("Connecting to different services...")
	database = CustomisedDatabase()
	youtube = CustomisedYoutubeService()
	print("Fetching new Videos...")
	videoList = youtube.GetVideoIDs("Streaming")
	videoDetails = youtube.GetVideoStartTimeDetails(videoList)
	print("Adding new Videos...")
	database.InsertVideos(videoDetails)
	print("Processing Videos...")
	videoDataToProcess = database.GetVideosToOrganise()
	print("Updating Shastra Name for Videos...")
	for (videoId, videoStartDate) in videoDataToProcess:
		shastraName = Functions.GetShastraName(videoStartDate, alphaSourceFiles)
		if shastraName:
			database.UpdateShastraName(videoId, shastraName)
	print("Updating Links for Videos...")
	database.UpdateInternalReferences()
	print("Updating Video Data on Youtube...")
	for updateData in database.FetchDataToUpdate():
		youtube.SetVideoDetails(updateData, "L")
		isUpdateSuccess = youtube.UpdateVideoInformation()
		if isUpdateSuccess:
			database.SetUpdateCompleted()
except Exception as exp:
	print ('An error occurred: ')
	print (exp)