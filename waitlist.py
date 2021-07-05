import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter
from re import search

# urls = ["https://wapps.mmh.org.tw/webhealthnumber/EMWAITdefault.aspx?HOSP=1WAIT", "https://www6.vghtpe.gov.tw/reg/c19vaccLine.do", "https://reg.cgh.org.tw/tw/booking/CovRemain.jsp", "https://www.csh.com.tw/Register/RegisterVaccine.aspx" (register for cs), "https://www.csh.com.tw/index-3-1.php"]
# target URL
url = "http://redcap.ntuh.gov.tw/surveys/?__dashboard=9NTNTRYKXXH"
# act like a browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

PrevVersion = ""
FirstRun = True
while True:

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    webhook = Webhook.from_url("https://discord.com/api/webhooks/861509429785395200/uBAHiEm5XN7-rzSAOL8xGCzldpaBANQFrdtv-kRl2rhjvZF1fAkoZR3UuvtwCIrFTv-4", adapter=RequestsWebhookAdapter())

    for script in soup(["script", "style"]):
        script.extract() 
    soup = soup.get_text()

    # compare the page text to the previous version
    if PrevVersion != soup:
        # launch, memorize page
        if FirstRun == True:
            PrevVersion = soup
            FirstRun = False
            print ("Start Monitoring "+url+ ""+ str(datetime.now()))
        else:
          OldPage = PrevVersion.splitlines()
          NewPage = soup.splitlines()
          if "已額滿" not in soup:
            # print ("Changes detected at: "+ str(datetime.now()))
            print('Possible opening @')
            OldPage = NewPage
            PrevVersion = soup
            #send msg in waitlist-notifications channel
            webhook.send("Hello World")
          else:
            print('Full!')
            OldPage = NewPage
            PrevVersion = soup
            webhook.send("Full")
    else:
        print( "No Changes "+ str(datetime.now()), soup)
    time.sleep(10)
    continue