from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#import chromedriver_binary
import time

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import ssl,os

import psycopg2

# Seleniumをあらゆる環境で起動させるChromeオプション

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


def sendMail(day,mail):
    account = "retasubot.sendonly@gmail.com"
    password = "djtralajkkyuzgpa"
    TEXT = day+'の予約に空きができました！'+'\n\nhttps://webrsv01.dia-koukyou.jp/sayama/web/ から予約できます'
    msg = MIMEText(TEXT,'plain', 'utf-8')
    msg['Subject'] = day+'の予約に空きができました！'
    msg['From'] = account
    msg['To'] = mail
    msg['Date'] = formatdate()
    server = smtplib.SMTP("smtp.gmail.com", port= 587)
    server.ehlo()
    server.starttls()
    server.login(account, password)
    server.sendmail(account, mail, msg.as_string())
    server.close()

def sendMail_(day):
    mail_list = ['natsukaze2525@gmail.com','namiwa@softbank.ne.jp','hiroaki.nagase@g.softbank.co.jp']
    for m in mail_list:
        sendMail(day,m)
# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

#DRIVER_PATH = '/chromedriver'
#DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

#driver = webdriver.Chrome(executable_path="C:\driver\chromedriver.exe",chrome_options=options)

def dbcheck(day,text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')

    for row in cur:
        if day in row:
            return row[1]

    cur.execute("insert into db values('{day}','{text}')".format(day=dya,text=text))
    conn.commit()
    return text

def seve(day,text):
    #ID=送られた側 ID2=送った側
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            if day in row:
                cur.execute("UPDATE db SET text = '{text}' WHERE day='{day}';".format(text=text,day=day))
                conn.commit()
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{day}','{text}')".format(day=day,text=text))
        conn.commit()
        return
    except Exception as e:
        print (str(e))
        return

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
            if '空き' in alt:
                text_ = dbcheck(d.text,alt)
                if alt != text_:
                    sendMail_(d.text)
                    seve(d.text,alt)
            else:
                seve(d.text,alt)
            #text_list.append(d.text+alt)
    driver.find_element_by_xpath("//*[@alt='次の月']").click()
    class_ = driver.find_elements_by_class_name('m_akitablelist_sat')
    for c in class_:
        day = c.find_elements_by_tag_name('strong')
        for d in day:
            alt = c.find_element_by_tag_name("img").get_attribute("alt")
            if '空き' in alt:
                text_ = dbcheck(d.text,alt)
                if alt != text_:
                    sendMail_(d.text)
                    seve(d.text,alt)
            else:
                seve(d.text,alt)
    driver.quit()

if __name__ == "__main__":
    check()
