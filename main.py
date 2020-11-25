import requests,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_binary
import time

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl


# Seleniumをあらゆる環境で起動させるChromeオプション

class SlackDriver:

    def __init__(self, _token):
        self._token = _token  # api_token
        self._headers = {'Content-Type': 'application/json'}

    def send_message(self, message, channel):
        params = {"token": self._token, "channel": channel, "text": message}

        r = requests.post('https://slack.com/api/chat.postMessage',
                          headers=self._headers,
                          params=params)
        print("return ", r.json())
'''
def sendMail(text,mail):
    account = "retasubot.sendonly@gmail.com"
    password = "djtralajkkyuzgpa"
    TEXT = 'ただ今の予約状況は以下の通りです\n'+text+'\n\nhttps://webrsv01.dia-koukyou.jp/sayama/web/ から予約できます'
    msg = MIMEText(TEXT,'plain', 'utf-8')
    msg['Subject'] = '智光山キャンプ場:予約確認状況'
    msg['From'] = account
    msg['To'] = mail
    msg['Date'] = formatdate()
    server = smtplib.SMTP("smtp.gmail.com", port= 587)
    server.ehlo()
    server.starttls()
    server.login(account, password)
    server.sendmail(account, mail, msg.as_string())
    server.close()'''

def sendMail_(text):
    token = os.environ["token"]
    slack = SlackDriver(token)
    slack.send_message('ただ今の予約状況は以下の通りです\n'+text+'\n\nhttps://webrsv01.dia-koukyou.jp/sayama/web/ から予約できます', "#定期通知")
#    mail_list = ['natsukaze2525@gmail.com']
#    for m in mail_list:
#        sendMail(text,m)
# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

#DRIVER_PATH = '/chromedriver'
#DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

#driver = webdriver.Chrome(executable_path="C:\driver\chromedriver.exe",chrome_options=options)


def check():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');
    driver = webdriver.Chrome(options=options)
    url = 'https://webrsv01.dia-koukyou.jp/sayama/web/'
    driver.get(url)
    driver.find_element_by_xpath("//*[@alt='施設の空き状況']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@alt='地域から']").click()
    time.sleep(1)
    driver.find_element_by_link_text(u"狭山市").click()
    time.sleep(1)
    driver.find_element_by_link_text(u"智光山公園キャンプ場").click()
    class_ = driver.find_elements_by_class_name('m_akitablelist_sat')
    text_list = []
    for c in class_:
        day = c.find_elements_by_tag_name('strong')
        for d in day:
            alt = c.find_element_by_tag_name("img").get_attribute("alt")
            text_list.append(d.text+alt)
    driver.find_element_by_xpath("//*[@alt='次の月']").click()
    class_ = driver.find_elements_by_class_name('m_akitablelist_sat')
    for c in class_:
        day = c.find_elements_by_tag_name('strong')
        for d in day:
            alt = c.find_element_by_tag_name("img").get_attribute("alt")
            text_list.append(d.text+alt)
    driver.find_element_by_xpath("//*[@alt='次の月']").click()
    class_ = driver.find_elements_by_class_name('m_akitablelist_sat')
    for c in class_:
        day = c.find_elements_by_tag_name('strong')
        for d in day:
            alt = c.find_element_by_tag_name("img").get_attribute("alt")
            text_list.append(d.text+alt)
    driver.find_element_by_xpath("//*[@alt='次の月']").click()
    class_ = driver.find_elements_by_class_name('m_akitablelist_sat')
    for c in class_:
        day = c.find_elements_by_tag_name('strong')
        for d in day:
            alt = c.find_element_by_tag_name("img").get_attribute("alt")
            text_list.append(d.text+alt)
    driver.find_element_by_xpath("//*[@alt='次の月']").click()
    class_ = driver.find_elements_by_class_name('m_akitablelist_sat')
    for c in class_:
        day = c.find_elements_by_tag_name('strong')
        for d in day:
            alt = c.find_element_by_tag_name("img").get_attribute("alt")
            text_list.append(d.text+alt)
    text = '\n\n'.join(text_list)
    sendMail_(text)
    driver.quit()

if __name__ == "__main__":
    check()
