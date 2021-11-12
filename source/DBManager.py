# This project created by urhoba
# www.urhoba.net

import sqlite3
from sqlite3.dbapi2 import Cursor
from LogManager import LogManager
from Settings import DBSettings
import ColoredPrint

class DBManager:
#region Init    
    def __init__(self) -> None:
        self._CreateVideoDB()
        self._CreateAudioDB()
        self._CreateUserDB()
        self._CreateBotStatsDB()
        self.logManager = LogManager("DBManagerLog")
#endregion

#region Connect
    def _Connect(self):
        self.db = sqlite3.connect(DBSettings.sqliteDB)
        ColoredPrint.GreenPrint("Veri tabanına bağlanıldı.")
#endregion

#region Create DB Modules
    def _CreateVideoDB(self):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "CREATE TABLE IF NOT EXISTS videos (videoTitle, videoID, videoFile, videoDownloadCount)"
            cursor.execute(sqlQuery)
            ColoredPrint.GreenPrint("Video veri tabanı oluşturuldu.")
        except:
            self.logManager.AddLog("Video veri tabanı oluşturulurken bir hata meydana geldi!")
            ColoredPrint.RedPrint("Video veri tabanı oluşturulurken bir hata meydana geldi!")
        finally:
            self.db.close()

    def _CreateAudioDB(self):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "CREATE TABLE IF NOT EXISTS audios (audioTitle, audioID, audioFile, audioDownloadCount)"
            cursor.execute(sqlQuery)
            ColoredPrint.GreenPrint("Ses veri tabanı oluşturuldu.")
        except:
            self.logManager.AddLog("Ses veri tabanı oluşturulurken bir hata meydana geldi!")
            ColoredPrint.RedPrint("Ses veri tabanı oluşturulurken bir hata meydana geldi!")
        finally:
            self.db.close()   

    def _CreateUserDB(self):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "CREATE TABLE IF NOT EXISTS users (userID, userName, userVideoDownloadCount, userAudioDownloadCount, userSearchCount)"
            cursor.execute(sqlQuery)
            ColoredPrint.GreenPrint("Kullanıcı veri tabanı oluşturuldu.")
        except:
            self.logManager.AddLog("Kullanıcı veri tabanı oluşturulurken bir hata meydana geldi!")
            ColoredPrint.RedPrint("Kullanıcı veri tabanı oluşturulurken bir hata meydana geldi!")
        finally:
            self.db.close()

    def _CreateBotStatsDB(self):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "CREATE TABLE IF NOT EXISTS stats (botID, audioDownloadCount, videoDownloadCount, searchCount, userCount)"
            cursor.execute(sqlQuery)
            ColoredPrint.GreenPrint("İstatistik veri tabanı oluşturuldu.")
        except:
            self.logManager.AddLog("İstatistik veri tabanı oluşturulurken bir hata meydana geldi!")
            ColoredPrint.RedPrint("İstatistik veri tabanı oluşturulurken bir hata meydana geldi!")
        finally:
            self.db.close()        
         
#endregion

#region Add Modules
    def AddVideo(self, videoTitle, videoID, videoFile):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "INSERT INTO videos (videoTitle, videoID, videoFile, videoDownloadCount) VALUES (?,?,?,?)"
            sqlValues = (videoTitle, videoID, videoFile, 1)
            cursor.execute(sqlQuery, sqlValues)
            self.db.commit()
            ColoredPrint.GreenPrint(f"Video eklendi. \nVideo Başlığı : {videoTitle} \nVideo ID : {videoID}")
        except:
            self.logManager.AddLog(f"Veri tabanına video eklenirken bir hata meydana geldi! \nVideo Title : {videoTitle} \nVideo ID : {videoID}\nVideo File : {videoFile}")
            ColoredPrint.RedPrint(f"Veri tabanına video eklenirken bir hata meydana geldi! \nVideo Title : {videoTitle} \nVideo ID : {videoID}\nVideo File : {videoFile}")
        finally:
            self.db.close()

    def AddAudio(self, audioTitle, audioID, audioFile):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "INSERT INTO audios (audioTitle, audioID, audioFile, audioDownloadCount) VALUES (?,?,?,?)"
            sqlValues = (audioTitle, audioID, audioFile, 1)
            cursor.execute(sqlQuery, sqlValues)
            self.db.commit()
            ColoredPrint.GreenPrint(f"Ses eklendi. \nSes Başlığı : {audioTitle} \nSes ID : {audioID}")
        except:
            self.logManager.AddLog(f"Veri tabanına ses eklenirken bir hata meydana geldi! \nAudio Title : {audioTitle} \nAudio ID : {audioID}\nAudio File : {audioFile}")
            ColoredPrint.RedPrint(f"Veri tabanına ses eklenirken bir hata meydana geldi! \nAudio Title : {audioTitle} \nAudio ID : {audioID}\nAudio File : {audioFile}")
        finally:
            self.db.close()

    def AddUser(self, userID, userName):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "INSERT INTO users (userID, userName, userVideoDownloadCount, userAudioDownloadCount, userSearchCount) VALUES (?,?,?,?,?)"
            sqlValues = (userID, userName, 0, 0, 0)
            cursor.execute(sqlQuery, sqlValues)
            self.db.commit()
            ColoredPrint.GreenPrint(f"Kullanıcı eklendi. \nKullanıcı adı : {userName}\nKullanıcı ID : {userID}")
        except:
            self.logManager.AddLog(f"Veri tabanına kullanıcı eklenirken bir hata meydana geldi! \nKullanıcı ID : {userID}\nKullanıcı adı : {userName}")
            ColoredPrint.RedPrint(f"Veri tabanına kullanıcı eklenirken bir hata meydana geldi! \nKullanıcı ID : {userID}\nKullanıcı adı : {userName}")
        finally:
            self.db.close()

    def AddBot(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "INSERT INTO stats (botID, audioDownloadCount, videoDownloadCount, searchCount, userCount) VALUES (?,?,?,?,?)"
            sqlValues = (botID, 0, 0, 0, 0)
            cursor.execute(sqlQuery, sqlValues)
            self.db.commit()
            ColoredPrint.GreenPrint(f"Bot eklendi. \nBot ID : {botID}")
        except:
            self.logManager.AddLog(f"Veri tabanına bot eklenirken bir hata meydana geldi! \nBot ID : {botID}")
            ColoredPrint.RedPrint(f"Veri tabanına bot eklenirken bir hata meydana geldi! \nBot ID : {botID}")
        finally:
            self.db.close()        
#endregion
  
#region Check Modules  
    def CheckVideoWithVideoID(self, videoID):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "SELECT * FROM videos WHERE videoID = '%s'" % videoID
            check = cursor.execute(sqlQuery).fetchall()
            if len(check) > 0:
                return True
            else:
                return False
        except:
            self.logManager.AddLog(f"Veri tabanında video doğrulanırken bir sorun meydana geldi! \nvideo ID : {videoID}")
            ColoredPrint.RedPrint(f"Veri tabanında video doğrulanırken bir sorun meydana geldi! \nvideo ID : {videoID}")
            return False
        finally:
            self.db.close()

    def CheckAudioWithAudioID(self, audioID):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "SELECT * FROM audios WHERE audioID = '%s'" % audioID
            check = cursor.execute(sqlQuery).fetchall()
            if len(check) > 0:
                return True
            else:
                return False
        except:
            self.logManager.AddLog(f"Veri tabanında ses doğrulanırken bir sorun meydana geldi! \nAudio ID : {audioID}")
            ColoredPrint.RedPrint(f"Veri tabanında ses doğrulanırken bir sorun meydana geldi! \nAudio ID : {audioID}")
            return False
        finally:
            self.db.close()
   
    def CheckUserWithID(self, userID):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "SELECT * FROM users WHERE userID = %s" % userID
            check = cursor.execute(sqlQuery).fetchall()
            if len(check) > 0:
                return True
            else:
                return False
        except:
            self.logManager.AddLog(f"Veri tabanında kullanıcı doğrulanırken bir sorun meydana geldi! \nUser ID : {userID}")
            ColoredPrint.RedPrint(f"Veri tabanında kullanıcı doğrulanırken bir sorun meydana geldi! \nUser ID : {userID}")
            return False
        finally:
            self.db.close()

    def CheckBotStatsWithID(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "SELECT * FROM stats WHERE botID = %s" % botID
            check = cursor.execute(sqlQuery).fetchall()
            if len(check) > 0:
                return True
            else:
                return False
        except:
            self.logManager.AddLog(f"Veri tabanında bot doğrulanırken bir sorun meydana geldi! \nBot ID : {botID}")
            ColoredPrint.RedPrint(f"Veri tabanında bot doğrulanırken bir sorun meydana geldi! \nBot ID : {botID}")
            return False
        finally:
            self.db.close()        
#endregion

#region Download & Search Count Update Modules
    def AudioDownloadCountUpdate(self, audioID):
        try: 
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = " UPDATE audios SET audioDownloadCount = audioDownloadCount + 1 WHERE audioID = '%s'" % audioID
            cursor.execute(sqlQuery)
            self.db.commit()
            return True
        except:
            self.logManager.AddLog(f"Veri tabanında ses indirme sayısı arttırılırken bir sorun meydana geldi! \nAudio ID : {audioID}")
            ColoredPrint.RedPrint(f"Veri tabanında ses indirme sayısı arttırılırken bir sorun meydana geldi! \nAudio ID : {audioID}")
            return False
        finally:
            self.db.close()
    
    def VideoDownloadCountUpdate(self, videoID):
        try: 
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = " UPDATE videos SET videoDownloadCount = videoDownloadCount + 1 WHERE videoID = '%s'" % videoID
            cursor.execute(sqlQuery)
            self.db.commit()
            return True
        except:
            self.logManager.AddLog(f"Veri tabanında video indirme sayısı arttırılırken bir sorun meydana geldi! \nVideo ID : {videoID}")
            ColoredPrint.RedPrint(f"Veri tabanında video indirme sayısı arttırılırken bir sorun meydana geldi! \nVideo ID : {videoID}")
            return False
        finally:
            self.db.close()
    
    def UserVideoDownloadCountUpdate(self, userID):
        try: 
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = " UPDATE users SET userVideoDownloadCount = userVideoDownloadCount + 1 WHERE userID = %s" % userID
            cursor.execute(sqlQuery)
            self.db.commit()
            return True
        except:
            self.logManager.AddLog(f"Veri tabanında kullanıcı video indirme sayısı arttırılırken bir sorun meydana geldi! \nUser ID : {userID}")
            ColoredPrint.RedPrint(f"Veri tabanında kullanıcı video indirme sayısı arttırılırken bir sorun meydana geldi! \nUser ID : {userID}")
            return False
        finally:
            self.db.close()

    def UserAudioDownloadCountUpdate(self, userID):
        try: 
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = " UPDATE users SET userAudioDownloadCount = userAudioDownloadCount + 1 WHERE userID = %s" % userID
            cursor.execute(sqlQuery)
            self.db.commit()
            return True
        except:
            self.logManager.AddLog(f"Veri tabanında kullanıcı ses indirme sayısı arttırılırken bir sorun meydana geldi! \nUser ID : {userID}")
            ColoredPrint.RedPrint(f"Veri tabanında kullanıcı ses indirme sayısı arttırılırken bir sorun meydana geldi! \nUser ID : {userID}")
            return False
        finally:
            self.db.close()

    def UserSearchCountUpdate(self, userID):
        try: 
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = " UPDATE users SET userSearchCount = userSearchCount + 1 WHERE userID = %s" % userID
            cursor.execute(sqlQuery)
            self.db.commit()
            return True
        except:
            self.logManager.AddLog(f"Veri tabanında kullanıcı arama sayısı arttırılırken bir sorun meydana geldi! \nUser ID : {userID}")
            ColoredPrint.RedPrint(f"Veri tabanında kullanıcı arama sayısı arttırılırken bir sorun meydana geldi! \nUser ID : {userID}")
            return False
        finally:
            self.db.close()

    def BotAudioCountUpdate(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "UPDATE stats SET audioDownloadCount = audioDownloadCount + 1 WHERE botID = %s" % botID
            cursor.execute(sqlQuery)
            self.db.commit()
        except:
            self.logManager.AddLog(f"Veri tabanında ses sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
            ColoredPrint.RedPrint(f"Veri tabanında ses sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
        finally:
            self.db.close()
            
    def BotVideoCountUpdate(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "UPDATE stats SET videoDownloadCount = videoDownloadCount + 1 WHERE botID = %s" % botID
            cursor.execute(sqlQuery)
            self.db.commit()
        except:
            self.logManager.AddLog(f"Veri tabanında video sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
            ColoredPrint.RedPrint(f"Veri tabanında video sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
        finally:
            self.db.close()

    def BotSearchCountUpdate(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "UPDATE stats SET searchCount = searchCount + 1 WHERE botID = %s" % botID
            cursor.execute(sqlQuery)
            self.db.commit()
        except:
            self.logManager.AddLog(f"Veri tabanında sorgu sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
            ColoredPrint.RedPrint(f"Veri tabanında sorgu sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
        finally:
            self.db.close()

    def BotUserCountUpdate(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "UPDATE stats SET userCount = userCount + 1 WHERE botID = %s" % botID
            cursor.execute(sqlQuery)
            self.db.commit()
        except:
            self.logManager.AddLog(f"Veri tabanında kullanıcı sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
            ColoredPrint.RedPrint(f"Veri tabanında kullanıcı sayısı arttırılırken bir sorun meydana geldi! \nBot ID : {botID} ")
        finally:
            self.db.close()

#endregion

#region Get Data Modules
    def BotDataGet(self, botID = 1):
        try:
            self._Connect()
            cursor = self.db.cursor()
            sqlQuery = "SELECT * FROM stats WHERE botID = %s" %botID
            datas = cursor.execute(sqlQuery).fetchone()
            return datas
        except:
            self.logManager.AddLog(f"Veri tabanından bot verileri çekilirken bir sorun meydana geldi! \nBot ID : {botID}")
            ColoredPrint.RedPrint(f"Veri tabanından bot verileri çekilirken bir sorun meydana geldi! \nBot ID : {botID}")
        finally:
            self.db.close()
#endregion
