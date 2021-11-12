# This project created by urhoba
# www.urhoba.net

from logging import info
from telegram import *
from telegram.ext import *

from LogManager import LogManager
from Settings import TelegramSettings
from Base import UrhobA

import ColoredPrint

#region Start Command
def StartCommand(update, context):
    text = f'''\
Merhaba, <b>{update.message.from_user.first_name}</b>!
YouTube da aradığın o videoyu veya şarkıyı bulmana yardım edecek ve sana dosya olarak göndereceğim.
<b>Sadece aramak istediğin video veya şarkı adını gir.</b> 😉 

⚠️ Nasıl kullanacağını öğrenmek için
/help komutunu kullanabilirsin.
    '''
    urhoba = UrhobA()
    urhoba.CreateUser(update.message.from_user.id, update.message.from_user.username)
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
#endregion

#region Help 
def HelpCommand(update, context):
    text = f'''\
Merhaba, <b>{update.message.from_user.first_name}</b>.
Görüyorum ki yardıma ihtiyacım var, hadi sana yardım edelim.

Bulmak istediğin video veya şarkının adını girmen yeterli olacaktır.

Çıkan sonuçlar arasından;
🎬 Butonu video indirmeni sağlar. 
🎧 Butonu ses indirmeni sağlar.

<a href="https://www.urhoba.net/">🔗</a> Butonu seni internet sitemize yönlendirecektir.
    '''
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)

#endregion

#region UrhobA
def UrhobACommand(update, context):
    text = f"""
Merhaba, <b>{update.message.from_user.first_name}</b>.
Aşağıdaki bağlantıya tıklayıp internet sitemize gidebilirsin.

<a href="https://www.urhoba.net/">🔗 <b>UrhobA</b></a>
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
#endregion

#region Stats Command
def StatsCommand(update, context):
    urhoba = UrhobA()
    statDatas = urhoba.GetBotDatas()
    text = f'''\
📊 <b>İstatistikler</b> 📊
🔍 Yapılan arama : {statDatas[3]}
🎬 Video indirme : {statDatas[2]}
🎧 Ses İndirme : {statDatas[1]}
😁 Kullanıcı sayısı : {statDatas[4]}

<a href="https://www.urhoba.net/">🔗 <b>UrhobA</b></a>     
    '''
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)

#endregion

#region Search Modules
def SearchCommand(update, context):
    searchText = update.message.text.split("/search")[1].strip()
    Search(update, context, searchText)

def Search(update, context, query = None):
    text = "<b>Hemen buluyorum</b>. 🔍🔍"
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
    urhoba = UrhobA()
    if query == None:
        searchText = update.message.text
    else:
        searchText = query

    searchResult = urhoba.SearchVideo(searchText)
    try:
        if len(searchResult) > 0:
            buttons = []
            for video in searchResult:
                buttonOne = [InlineKeyboardButton(text=f'{video.title}', callback_data='none')]
                buttonTwo = [InlineKeyboardButton(text=f'🎬', callback_data=f'videourhoba{video.video_id}'),
                    InlineKeyboardButton(text=f'🔗', url="https://www.urhoba.net"),
                        InlineKeyboardButton(text=f'🎧', callback_data=f'audiourhoba{video.video_id}')]
                buttons.append(buttonOne)
                buttons.append(buttonTwo)
            replyMarkup = InlineKeyboardMarkup(buttons)
            context.bot.send_message(chat_id=update.message.chat_id, text=f"<b>Arama sonucu:</b>\n{searchText}",
                                    parse_mode=ParseMode.HTML, reply_markup=replyMarkup)
        else:
            text = "Aradığın şeyi bulamadım. 😢"
            context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
        urhoba.SearchCountUpdateUser(update.message.from_user.id, update.message.from_user.username)
    except:
        text = "İstediğin şeyi ararken bir sorun meydana geldi! 😢\nBunun ile en kısa süre içerisinde ilgileneceğiz."
        context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)
        logManager = LogManager("TelegramLog")
        logManager.AddLog(f'Telegram (YouTube) arama yaparken bir sorun meydana geldi!\n Search Text : {searchText} \n Search result : {searchResult}')
#endregion

#region Button Call Back Modules (Download & Search Result)
def ButtonCallBack(update: Update, context: CallbackQueryHandler):
    query = update.callback_query
    query.answer()
    queryData = query.data.split("urhoba")
    urhoba = UrhobA()
    text = 'Sitemizi ziyaret etmeyi unutmayın. 🥰 \n<a href="https://www.urhoba.net/">🔗 <b>UrhobA</b></a>'
    if queryData[0] == "video":
        query.edit_message_text(text=f"⏳ Video dosyası hazırlanıyor.\n⚠️ Videoların gönderim süresi ses dosyalarına göre daha uzundur, lütfen sabırlı olun.", parse_mode=ParseMode.HTML)
        urhoba.VideoDownloadCountUpdateUser(update.callback_query.from_user.id, update.callback_query.from_user.username)
        videoFolder = urhoba.DownloadVideo(queryData[1])
        if videoFolder == False:
            query.message.reply_text(text='Video dosyası hazırlanırken bir sorun meydana geldi! 😢\nBunun ile en kısa süre içerisinde ilgileneceğiz.', parse_mode=ParseMode.HTML)
        else:
            try:
                query.message.reply_video(video=open(videoFolder, 'rb'), supports_streaming=True, timeout=10000)
                query.message.reply_text(text=text,parse_mode=ParseMode.HTML)
            except:
                query.message.reply_text(text='Video dosyası gönderilirken bir sorun meydana geldi! 😢\nBunun ile en kısa süre içerisinde ilgileneceğiz.', parse_mode=ParseMode.HTML)
            finally:
                urhoba.DeleteFile(videoFolder)
    elif queryData[0] == "audio":
        query.edit_message_text(text=f"⏳ Ses dosyası hazırlanıyor.", parse_mode=ParseMode.HTML)
        urhoba.AudioDownloadCountUpdateUser(update.callback_query.from_user.id, update.callback_query.from_user.username)
        audioFolder = urhoba.DownloadAudio(queryData[1])
        if audioFolder == False:
            query.message.reply_text(text='Ses dosyası hazırlanırken bir sorun meydana geldi! 😢\nBunun ile en kısa süre içerisinde ilgileneceğiz.', parse_mode=ParseMode.HTML)
        else:
            try:
                query.message.reply_audio(audio=open(audioFolder, 'rb'))
                query.message.reply_text(text=text,parse_mode=ParseMode.HTML)
            except:
                query.message.reply_text(text='Ses dosyası gönderilirken bir sorun meydana geldi! 😢\nBunun ile en kısa süre içerisinde ilgileneceğiz.', parse_mode=ParseMode.HTML)
            finally:
                urhoba.DeleteFile(audioFolder)
    else:
        text = "⚠️ Lütfen sadece 🎬 veya 🎧 butonlarını kullanın."
        query.message.reply_text(text=text,parse_mode=ParseMode.HTML)


#endregion

#region Legal Info
def LegalInfoCommand(update, context):
    returnedMessage = """\
We built UrhobABot with the idea that a legal stream recording tool for the internet that was clean, easy, and not spammy needed to exist. 
According to the EFF.org "The law is clear that simply providing the public with a tool for copying digital media does not give rise to copyright liability".    
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=returnedMessage, parse_mode=ParseMode.HTML)
#endregion

#region Error Handler
def ErrorExcept(update, context):
    logManager = LogManager("TelegramLog")
    logManager.AddLog(f"Telegram bot hatası : Update {update} caused error {context.error}")
#endregion

#region Main
def main():
    updater = Updater(TelegramSettings.telegramAPI, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", StartCommand))
    dp.add_handler(CommandHandler("legal", LegalInfoCommand))
    dp.add_handler(CommandHandler("help", HelpCommand))
    dp.add_handler(CommandHandler("stats", StatsCommand))
    dp.add_handler(CommandHandler("urhoba", UrhobACommand))

    dp.add_handler(CommandHandler("search", SearchCommand))


    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, Search))

    dp.add_handler(CallbackQueryHandler(ButtonCallBack))


    dp.add_error_handler(ErrorExcept)
    updater.start_polling(1)
    updater.idle()
#endregion

ColoredPrint.GreenPrint("Bot başlatıldı!")
main()
