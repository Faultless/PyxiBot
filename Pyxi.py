# coding: utf-8
import telegram
import urllib
import os
import time
from bs4 import BeautifulSoup
import requests
import shutil

bot = telegram.Bot("Your_Bot_s_Token")

try:
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
except IndexError:
    LAST_UPDATE_ID = None

def echo():
    global LAST_UPDATE_ID

    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID <= update.update_id:
            try:
                statement = update.message.text.split()
                chat_id = update.message.chat_id
                pass
            except:
                LAST_UPDATE_ID = update.update_id + 1
                pass
            if statement.__len__() < 2:
                LAST_UPDATE_ID = update.update_id + 1
                break
            cmd = statement[0]
            chapter = statement[1]
            url = "http://mangapark.me"
            for i in xrange(2, statement.__len__()):
                if i>2:
                    url += "+"+statement[i]
                    pass
                else:
                    url += "/search?q="+statement[i]
            if cmd=="/manga":
                try:
                    reqq = requests.get(url) #search for the manga
                    pass
                except:
                    bot.sendMessage(chat_id, "No manga found.")
                    LAST_UPDATE_ID = update.update_id + 1
                    pass
                page = reqq.text
                soup = BeautifulSoup(page, 'html5lib')
                result = [a.attrs.get('href') for a in soup.select('a[href^=/manga/]')] #scrape (pick) to the most relevant result.
                if not result:
                    bot.sendMessage(chat_id, "No manga found.")
                    LAST_UPDATE_ID = update.update_id + 1
                    pass
                url = "http://mangapark.me"+result[1]
                try:
                    reqq = requests.get(url)
                    pass
                except:
                    bot.sendMessage(chat_id, "No manga found.")
                    LAST_UPDATE_ID = update.update_id + 1
                    pass
                page = reqq.text
                soup = BeautifulSoup(page, 'html5lib')
                result = [a.attrs.get('href') for a in soup.select('span > a[href*=/c'+chapter+'/]')] #scrape to the designated chapter.
                if not result:
                    bot.sendMessage(chat_id, "No chapter found.")
                    LAST_UPDATE_ID = update.update_id + 1
                    pass
                url = "http://mangapark.me"+result[1]
                url = url.replace("/1", "")
                try:
                    reqq = requests.get(url)
                    pass
                except:
                    bot.sendMessage(chat_id, "No chapter found.")
                    LAST_UPDATE_ID = update.update_id + 1
                    pass
                page = reqq.text
                soup = BeautifulSoup(page, 'html5lib')
                result = [a.attrs.get('src') for a in soup.select('a > img[src*=.jpg]')]
                for i in xrange(0, result.__len__()):
                    pass
                    urllib.urlretrieve(result[i], "/app/manga/" + i.__str__() + ".jpg") #download the needed images to the server (or locally).
                    print result[i]
                shutil.make_archive("/app/chapter" + chapter.__str__(), "zip", "/app/manga") #create a zip file containing all the images.
                zipfile = "/app/chapter" + chapter.__str__() + ".zip"
                bot.sendDocument(chat_id, document=open(zipfile, 'rb')) #send the zipfile.
            else:
                LAST_UPDATE_ID = update.update_id + 1
            folder = '/app/manga'
            for the_file in os.listdir(folder): #empty the manga directory once zipped and sent.
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, e:
                    print e
            os.unlink(zipfile)
            LAST_UPDATE_ID = update.update_id + 1



if __name__ == '__main__':
    while True:
        try:
            echo()
            pass
        except:
            print "Check your connection"
            pass
        time.sleep(1)
