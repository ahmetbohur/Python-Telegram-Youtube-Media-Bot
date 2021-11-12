# This project created by urhoba
# www.urhoba.net

from telegram import user
from YouTubeManager import YouTubeManager
from DBManager import DBManager

class UrhobA:
#region Init    
    def __init__(self) -> None:
        self.yt = YouTubeManager()
        self.dbMan = DBManager()
        if self.dbMan.CheckBotStatsWithID() == False:
            self.dbMan.AddBot()
#endregion

#region User Modules
    def CreateUser(self, userID, userName):
        if self.dbMan.CheckUserWithID(userID) == False:
            self.dbMan.AddUser(userID, userName)
            self.dbMan.BotUserCountUpdate()
#endregion

#region File Modules
    def DeleteFile(self, fileFolder):
        self.yt.DeleteFile(fileFolder)
#endregion

#region Counter Update Modules
    def SearchCountUpdateUser(self, userID, userName):
        if self.dbMan.CheckUserWithID(userID) == True:
            self.dbMan.UserSearchCountUpdate(userID)
            self.dbMan.BotSearchCountUpdate()
        else:
            self.CreateUser(userID, userName)
    
    def VideoDownloadCountUpdateUser(self, userID, userName):
        if self.dbMan.CheckUserWithID(userID) == True:
            self.dbMan.UserVideoDownloadCountUpdate(userID)
            self.dbMan.BotVideoCountUpdate()
        else:
            self.CreateUser(userID, userName)

    def AudioDownloadCountUpdateUser(self, userID, userName):
        if self.dbMan.CheckUserWithID(userID) == True:
            self.dbMan.UserAudioDownloadCountUpdate(userID)
            self.dbMan.BotAudioCountUpdate()
        else:
            self.CreateUser(userID, userName)
#endregion

#region Search Modules    
    def SearchVideo(self, searchQuery):
        result = self.yt.SearchVideo(searchQuery)
        return result
#endregion

#region Download Modules
    def DownloadVideo(self, video_id):
        result = self.yt.DownloadVideo(video_id)
        if result == False:
            return False
        else:
            if self.dbMan.CheckVideoWithVideoID(video_id):
                self.dbMan.VideoDownloadCountUpdate(video_id)
            else:
                self.dbMan.AddVideo(result[0], result[1], result[2])
        return result[2]

    def DownloadAudio(self, video_id):
        result = self.yt.DownloadAudio(video_id)
        if result == False:
            return False
        else:
            if self.dbMan.CheckAudioWithAudioID(video_id):
                self.dbMan.AudioDownloadCountUpdate(video_id)
            else:
                self.dbMan.AddAudio(result[0], result[1], result[2])
        return result[2]
#endregion

#region Get Stats Modules
    def GetBotDatas(self, botID = 1):
        if self.dbMan.CheckBotStatsWithID() == True:
            datas = self.dbMan.BotDataGet()
        return datas
#endregion
