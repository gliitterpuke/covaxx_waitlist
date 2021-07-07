import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter
from re import search

urls = ["https://wapps.mmh.org.tw/webhealthnumber/EMWAITdefault.aspx?HOSP=1WAIT", "https://www.csh.com.tw/index-3-1.php", "https://docs.google.com/forms/d/e/1FAIpQLSfpTN57Y0t2l-AKf8aRSngd-HzGA0tjbDBfIpRzhQxVWNELEQ/closedform"]
# target URL
# url = "http://redcap.ntuh.gov.tw/surveys/?__dashboard=9NTNTRYKXXH", "https://www6.vghtpe.gov.tw/reg/c19vaccLine.do"
# act like a browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

prev_ver = dict.fromkeys(urls, "")
FirstRun = True

while True:

  for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    webhook = Webhook.from_url("https://discord.com/api/webhooks/861509429785395200/uBAHiEm5XN7-rzSAOL8xGCzldpaBANQFrdtv-kRl2rhjvZF1fAkoZR3UuvtwCIrFTv-4", adapter=RequestsWebhookAdapter())

    for script in soup(["script", "style"]):
        script.extract() 
    soup = soup.get_text()

    # compare the page text to the previous version
    if soup not in prev_ver.values():
        # launch, memorize page
        if FirstRun == True:
            prev_ver[url] = soup
            FirstRun = False
            print ("Start Monitoring "+url+ ""+ str(datetime.now()))
        else:
          OldPage = prev_ver[url].splitlines()
          NewPage = soup.splitlines()
          # fill values of subsequent urls
          if prev_ver[url] == "":
            prev_ver[url] = soup
            print('URL filled')
          elif "已額滿" not in soup:
            # print ("Changes detected at: "+ str(datetime.now()))
            print('Open')
            OldPage = NewPage
            prev_ver[url] = soup
            #send msg in waitlist-notifications channel
            webhook.send("Possible opening @" + url + "!")
          else:
            print('Full')
            OldPage = NewPage
            prev_ver[url] = soup
            webhook.send('Change in waitlist sit (full?) @' + url)
    else:
        print( "No Changes "+ str(datetime.now()))
    time.sleep(5)
    continue