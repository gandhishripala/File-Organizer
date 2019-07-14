import sqlite3

from Settings import Settings

class CustomisedDatabase():
	def __init__(self):
		connection = sqlite3.connect(Settings.GetValue("DatabasePath"))
		self.connection = connection

	def InsertVideos(self, insertionData):
		if len(insertionData) > 0:
			cursor = self.connection.cursor()
			sortedData = sorted(insertionData, key = lambda current : current[1])
			for (insertId, insertDateTime) in sortedData:
				cursor.execute('''INSERT OR IGNORE INTO VideoRecordingData (VideoYoutubeId, VideoRecordingDate, VideoDataModified) VALUES (?,?,?)''', (str(insertId),str(insertDateTime),"Y"))
			self.connection.commit()

	def GetVideosToOrganise(self):
		cursor = self.connection.cursor()
		cursor.execute('''SELECT VideoYoutubeId, VideoRecordingDate FROM VideoRecordingData WHERE VideoShastraName is null OR VideoShastraName = '' ''')
		returnDate = [(fetch_data[0], fetch_data[1]) for fetch_data in cursor]
		sortedData = sorted(returnDate, key = lambda current : current[1])
		return sortedData

	def UpdateShastraName(self, videoId, videoShastraName):
		cursor = self.connection.cursor()
		cursor.execute('''UPDATE VideoRecordingData SET VideoShastraName = ?, VideoDataModified = ? WHERE VideoYoutubeId = ?''', (str(videoShastraName), "Y", str(videoId)))
		self.connection.commit()
		
	def UpdateInternalReferences(self):
		cursor = self.connection.cursor()
		cursor.execute('''SELECT VideoId FROM VideoRecordingData WHERE VideoDataModified = ? ''', ("Y",))
		videoIdToProcess = [fetch_data[0] for fetch_data in cursor]
		for currentVideoId in videoIdToProcess:
			cursor = self.connection.cursor()
			cursor.execute('''SELECT VideoShastraName, VideoPrevId, VideoNextId, VideoYoutubeId FROM VideoRecordingData WHERE VideoId = ?''', (str(currentVideoId),))
			fetchRecord = cursor.fetchone()
			VideoShastraName, VideoPrevId, VideoNextId, VideoYoutubeId = str(fetchRecord[0]), fetchRecord[1], fetchRecord[2], fetchRecord[3]
			#VideoPrevId
			cursor = self.connection.cursor()
			cursor.execute('''SELECT VideoYoutubeId, VideoId FROM VideoRecordingData WHERE VideoId < ? AND VideoShastraName = ? ORDER BY VideoId DESC''', (currentVideoId, VideoShastraName))
			fetchRecord = cursor.fetchone()
			if fetchRecord:
				PreviousVideoYoutubeId, PreviousVideoId = fetchRecord[0], fetchRecord[1]
				cursor = self.connection.cursor()
				cursor.execute('''UPDATE VideoRecordingData SET VideoPrevId = ?, VideoDataModified = ? WHERE VideoId = ?''', (str(PreviousVideoYoutubeId), "Y", str(currentVideoId)))
				cursor = self.connection.cursor()
				cursor.execute('''UPDATE VideoRecordingData SET VideoNextId = ?, VideoDataModified = ? WHERE VideoId = ?''', (str(VideoYoutubeId), "Y", str(PreviousVideoId)))
			#VideoNextId:
			cursor = self.connection.cursor()
			cursor.execute('''SELECT VideoYoutubeId, VideoId FROM VideoRecordingData WHERE VideoId > ? AND VideoShastraName = ? ORDER BY VideoId''', (currentVideoId, VideoShastraName))
			fetchRecord = cursor.fetchone()
			if fetchRecord:
				NextVideoYoutubeId, NextVideoId = fetchRecord[0], fetchRecord[1]
				cursor = self.connection.cursor()
				cursor.execute('''UPDATE VideoRecordingData SET VideoNextId = ?, VideoDataModified = ? WHERE VideoId = ?''', (str(NextVideoYoutubeId), "Y", str(currentVideoId)))
				cursor = self.connection.cursor()
				cursor.execute('''UPDATE VideoRecordingData SET VideoPrevId = ?, VideoDataModified = ? WHERE VideoId = ?''', (str(VideoYoutubeId), "Y", str(NextVideoId)))
		self.connection.commit()

	def FetchDataToUpdate(self):
		cursor = self.connection.cursor()
		cursor.execute('''SELECT VideoId, VideoYoutubeId, VideoRecordingDate, VideoShastraName, VideoPrevId, VideoNextId FROM VideoRecordingData WHERE VideoDataModified = "Y" ''')
		for fetch_data in cursor:
			self.updateVideoId = fetch_data[0]
			yield (fetch_data[0], fetch_data[1], fetch_data[2], fetch_data[3], fetch_data[4], fetch_data[5])

	def SetUpdateCompleted(self, updateVideoId = None):
		updateVideoId = self.updateVideoId if updateVideoId is None else updateVideoId
		cursor = self.connection.cursor()
		cursor.execute('''UPDATE VideoRecordingData SET VideoDataModified = ? WHERE VideoId = ?''', ("", updateVideoId))
		self.connection.commit()
