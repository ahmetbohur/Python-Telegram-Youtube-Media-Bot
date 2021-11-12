# This project created by urhoba
# www.urhoba.net

from pytube import YouTube
from pytube import Search
import ssl

import os
import os.path
import re

from LogManager import LogManager
from Settings import DownloadSettings
import ColoredPrint

#region SSL Settings
ssl._create_default_https_context = ssl._create_stdlib_context
#endregion

class YouTubeManager:
#region Init    
    def __init__(self) -> None:
        self.logManager = LogManager("YouTubeManagerLog")
#endregion

#region Search Modules    
    def SearchVideo(self, searchQuery):
        try:
            search = Search(searchQuery)
            return search.results
        except:
            self.logManager.AddLog(f"Video aranırken bir sorun meydana geldi! \nArama sorgusu : {searchQuery}")
            ColoredPrint.RedPrint(f"Video aranırken bir sorun meydana geldi! \nArama sorgusu : {searchQuery}")

#endregion

#region File Modules
    def FileCheck(self, file):
        if os.path.isfile(file) and os.access(file, os.R_OK):
            return True
        else:
            return False

    def DeleteFile(self, file):
        os.remove(file)

    def FileNameFormatter(self, name):
        validFileName = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        return validFileName
#endregion

#region Download Modules
    def DownloadVideo(self, videoURL):
        try:
            youtube = YouTube(f"https://www.youtube.com/watch?v={videoURL}")
            videoTitle = youtube.title
            fileName = self.FileNameFormatter(videoTitle) + ".mp4"
            if self.FileCheck(DownloadSettings.videoFolder+"/"+fileName) == False:
                youtube.streams.get_highest_resolution().download(output_path=DownloadSettings.videoFolder, filename=fileName)
            return videoTitle, videoURL, DownloadSettings.videoFolder + "/" + fileName
        except:
            self.logManager.AddLog(f"Video indirilirken bir sorun meydana geldi! \nVideo bağlantısı : {videoURL}")
            ColoredPrint.RedPrint(f"Video indirilirken bir sorun meydana geldi! \nVideo bağlantısı : {videoURL}")
            return False

    def DownloadAudio(self, songURL):
        try:
            youtube = YouTube(f"https://www.youtube.com/watch?v={songURL}")
            songTitle = youtube.title
            fileName = self.FileNameFormatter(songTitle) + ".mp4"
            if self.FileCheck(DownloadSettings.musicFolder+"/"+fileName) == False:
                youtube.streams.get_audio_only().download(output_path=DownloadSettings.musicFolder, filename=fileName)
            return songTitle, songURL,DownloadSettings.musicFolder + "/" + fileName
        except:
            self.logManager.AddLog(f"Ses indirilirken bir sorun meydana geldi! \nSes bağlantısı : {songURL}")
            ColoredPrint.RedPrint(f"Ses indirilirken bir sorun meydana geldi! \nSes bağlantısı : {songURL}")
            return False
#endregion