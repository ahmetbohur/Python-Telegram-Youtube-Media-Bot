# This project created by urhoba
# www.urhoba.net

from datetime import date, datetime
import locale
import os
import ColoredPrint
from MailManager import MailManager

#region Locale Settings
locale.setlocale(locale.LC_ALL, '')
#endregion

class LogManager:
#region Init    
    def __init__(self, logFileName) -> None:
        self._logFileName = logFileName
        self.mailManager = MailManager()
#endregion

#region Add Log
    def AddLog(self, errorText):
        _nowTime = datetime.now()
        _nowTime = datetime.strftime(_nowTime, "%c")
        logFile = open(os.getcwd()+"/logs/"+self._logFileName + ".txt", "a")
        try:
            with logFile as f:
                f.write(f"\nDate : {_nowTime}\nError: {errorText}\n")
            ColoredPrint.RedPrint(f'Date : {_nowTime}\nError: {errorText}\n')
            self.mailManager.SendMail("Bir hata tespit edildi! (UrhobA - Telegram Bot)", f'{errorText}', 'ahmetbohur@icloud.com')
        except:
            ColoredPrint.RedPrint("Log oluşturulurken bir sorun meydana geldi!")
        finally:
            logFile.close()
#endregion