#C:\Python27\Lib\site-packages\google_auth_oauthlib - Changes in flow.py
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import datetime
import json

from CustomisedWebDriver import CustomisedWebDriver
from Settings import Settings

class CustomisedYoutubeService():
	SCOPES = ['https://www.googleapis.com/auth/youtube']
	API_SERVICE_NAME = 'youtube'
	API_VERSION = 'v3'
	YOUTUBEVIDEOSUFFIX = "https://www.youtube.com/watch?v="

	def __init__(self):
		client_config = json.loads(Settings.GetValue("YoutubeSecret"))
		appFlow = InstalledAppFlow.from_client_config(client_config, CustomisedYoutubeService.SCOPES)
		urlForAuth = appFlow.run_console()
		authCode = CustomisedYoutubeService.GetAuthenticationCode(urlForAuth)
		credentialsForAuth = appFlow.run_console_rest(authCode)
		self.youtubeService = build(CustomisedYoutubeService.API_SERVICE_NAME, CustomisedYoutubeService.API_VERSION, credentials = credentialsForAuth)

	@staticmethod
	def GetAuthenticationCode(authUrl):
		webDriver = CustomisedWebDriver()
		webDriver.LaunchURL(authUrl)
		webDriver.LocateByPath("//input[@type='email']")
		webDriver.SendKeys(Settings.GetValue("GUsername"))
		webDriver.LocateByPath("//input[@type='password']")
		webDriver.SendKeys(Settings.GetValue("GPassword"))
		webDriver.LocateByPath("//*[contains(text(), '" + Settings.GetValue("YTChannelName") + "')]")
		webDriver.Click()
		webDriver.LocateByPath("//a[contains(text(), 'Advanced')]")
		webDriver.Click()
		webDriver.LocateByPath("//a[contains(text(), 'Go to python test project (unsafe)')]")
		webDriver.Click()
		webDriver.LocateByPath("//span[contains(text(), 'Allow')]")
		webDriver.Click()
		code = webDriver.GetAuthCode()
		webDriver.quit()
		return code
		
	@staticmethod
	def ConvertToISTTime(dateTimeString):
		parsedDateTime = datetime.datetime.strptime(dateTimeString, "%Y-%m-%dT%H:%M:%S.%fZ")
		parsedDateTime = parsedDateTime + datetime.timedelta(hours=5,minutes=30)
		return parsedDateTime.strftime("%Y%m%d %H%M%S")

	def UpdateVideoInformation(self, videoId = None, videoTitle = None, videoDescription = None, videoRecordingDate = None):
		videoId = self.videoYoutubeId if videoId is None else videoId
		videoTitle = self.videoTitle if videoTitle is None else videoTitle
		videoDescription = self.videoDescription if videoDescription is None else videoDescription
		videoRecordingDate = self.videoRecordingDate if videoRecordingDate is None else videoRecordingDate
		queryReturnParts = "snippet,recordingDetails"
		videoToUpdate = self.youtubeService.videos().list(
			id = videoId,
			part = queryReturnParts
		).execute()
		if not videoToUpdate[u"items"]:
			return False
		videoSnippet = videoToUpdate[u"items"][0][u"snippet"]
		videoRecordingDetails = dict()
		if videoTitle:
			videoSnippet[u"title"] = videoTitle
		if videoDescription:
			videoSnippet[u"description"] = videoDescription
		if videoRecordingDate:
			videoRecordingDetails[u"recordingDate"] = videoRecordingDate
		if u"tags" not in videoSnippet:
			videoSnippet[u"tags"] = []
		videos_update_response = self.youtubeService.videos().update(
			part = queryReturnParts,
			body = dict(
				snippet = videoSnippet,
				recordingDetails = videoRecordingDetails,
				id = videoId)
		).execute()
		print(videoId)
		print(videoTitle)
		print(videoDescription)
		print("----------------")
		return True

	def GetVideoIDs(self, searchString):
		queryReturnParts = "id,snippet"
		orderString = "date"
		queryString = searchString
		nextPageToken = ""
		responseData = []
		while True:
			response = self.youtubeService.search().list(
				part = queryReturnParts,
				channelId = Settings.GetValue("YTChannelID"),
				order = orderString,
				q = queryString,
				pageToken = nextPageToken
			).execute()
			for currentResponseItems in response["items"]:
				if u"videoId" in currentResponseItems[u"id"].keys():
					currentVideoId = currentResponseItems[u"id"][u"videoId"]
					responseData.append(currentVideoId)
			if u"nextPageToken" in response.keys():
				nextPageToken = response[u"nextPageToken"]
			else:
				break
		return responseData

	def GetVideoStartTimeDetails(self, inputList):
		queryReturnParts = "id,liveStreamingDetails"
		idToFetch = ",".join(inputList)
		responseData = []
		nextPageToken = ""
		while True:
			response = self.youtubeService.videos().list(
				part = queryReturnParts,
				id = idToFetch,
				pageToken = nextPageToken
			).execute()
			for currentResponseItems in response["items"]:
				responseData.append((str(currentResponseItems[u"id"]), (CustomisedYoutubeService.ConvertToISTTime(currentResponseItems[u"liveStreamingDetails"][u"actualStartTime"]))))
			if u"nextPageToken" in response.keys():
				nextPageToken = response[u"nextPageToken"]
			else:
				break
		return responseData	

	def SetVideoDetails(self, dataTuple, videoType):
		VideoId = videoType + str(dataTuple[0])
		VideoRecordingDate = datetime.datetime.strptime(dataTuple[2], "%Y%m%d %H%M%S").strftime("%d %B %Y")
		VideoShastraNameTitle = dataTuple[3] if dataTuple[3] is not None else "Vanchan"
		VideoShastraNameDesc = dataTuple[3] if dataTuple[3] is not None else "TBD"
		VideoPrevId = "TBD" if not dataTuple[4] else str(CustomisedYoutubeService.YOUTUBEVIDEOSUFFIX + dataTuple[4])
		VideoNextId = "TBD" if not dataTuple[5] else str(CustomisedYoutubeService.YOUTUBEVIDEOSUFFIX + dataTuple[5])
		self.videoYoutubeId = dataTuple[1]
		self.videoTitle = VideoShastraNameTitle + " || " + VideoRecordingDate + " || " + VideoId + " || Live Stream"
		self.videoDescription = "Shree Adinath Digambar Jain Mandir, Rajkot\nLive Stream\nPrevious Video Link: " + VideoPrevId + "\nShastra: " + VideoShastraNameDesc + "\nRecording Date: " + VideoRecordingDate + "\nRecording Number: " + VideoId + "\nNext Video Link: " + VideoNextId
		self.videoRecordingDate = datetime.datetime.strptime(dataTuple[2], "%Y%m%d %H%M%S").strftime("%Y-%m-%dT%H:%M:%S.%fZ")