import time
import requests
import json
import os.path
from os import path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

opts = Options()
name = input("ENTER ONLY THE ACCOUNT NAME (@logitech)")
opts.add_argument("user-agent=Googlebot")
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome("D:\Chromedriver 2\chromedriver.exe", desired_capabilities=caps, options=opts)
driver.get("https://www.tiktok.com/" + str(name) + "?lang=en")
#driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': events[0]["params"]["requestId"]})

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
time.sleep(1)
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


browser_log = driver.get_log('performance')
events = [process_browser_log_entry(entry) for entry in browser_log]
driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': events[0]["params"]["requestId"]})
scroll = []


if path.exists(name):
    print("folder exists")
else:
    print("creating folder")
    os.mkdir(name)
    
for i in range(0, len(events)):
    try:
        asd = events[i]["params"]["request"]["url"]
        if asd.find("m.tiktok.com/api/item_list/?count=30") > 0:
            print(asd)
            scroll.append(asd)
    except:
        pass
print(scroll)
for i in scroll:
    page = requests.get(i, headers={'User-Agent':'Googlebot'})
    time.sleep(2)
    html = page.text
    try:
        for j in range(0, 30):
                video = json.loads(html)["items"][j]["video"]["downloadAddr"]
                id = json.loads(html)["items"][j]["id"]
                if os.path.isfile(name + "/" + str(id) + ".mp4"):
                    pass
                    print("video already exists wiht id: " + str(id))
                else:
                    r = requests.get(video)
                    open(name + "/" + str(id) + ".mp4", 'wb').write(r.content)
                    print("downloading " + video + " with id: " + str(id))
    except:
        print("error")
        
print("FINISHED")
    
    
    
