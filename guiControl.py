from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import time
import ssl
import os
from selenium.webdriver.common.by import By



webdriver_options = webdriver.ChromeOptions()
webdriver_options.add_argument('headless')
webdriver_options.add_argument("--window-size=1920,1080")
#접속 & 로그
officialOption = input("--보기중 선택 후 정수 입력--\n(1) Official Website \n(2) Test Website [Developer]\n입력: ")
id = input("\nsellable admin ID 입력: ")
pwd = input("sellable admin Password 입력: ")

def skull(officialOption):
    targetProduct = int(input("\n상품코드 입력 [정수] {0으로 종료}: "))
    if(targetProduct == 0):
        quit()
    run = True
    ssl._create_default_https_context = ssl._create_unverified_context
    chromedriver_autoinstaller.install()
    #Headless option
    driver = webdriver.Chrome(options=webdriver_options)
    #No Headless option
    #driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    if officialOption == str(1):
        driver.get('https://admin.sellable.kr/itstore/user/logout')
    if officialOption == str(2):
        driver.get('https://deva.sellable.kr/itstore/user/login')
    else:
        exit()

    driver.find_element(By.ID,'userId').send_keys(id)
    driver.find_element(By.ID,'userPw').send_keys(pwd)
    driver.find_element(By.ID,'btnLogin').click()
    time.sleep(3)
    #

    ul = driver.find_element(By.CLASS_NAME,"pcoded-left-item")
    lis = ul.find_elements(By.CLASS_NAME,"pcoded-hasmenu")
    li = lis[2]
    lis[2].click()
    driver.find_element(By.XPATH,"//a[@href='/itstore/product/list']").click()

    frame = driver.find_element(By.ID,"mainContent")
    driver.switch_to.frame(frame)
    #COUNT PAGES
    page = driver.find_element(By.CLASS_NAME,"pagination")
    li = page.find_elements(By.TAG_NAME,"li")
    pages = int(li[len(li)-2].find_element(By.TAG_NAME,"a").get_attribute("innerHTML"))

    def runImgAdd():
        driver.find_element(By.LINK_TEXT, "상품상세정보").click()
        directory = os.getcwd() + "/datas/details/"

        order = 1
        detail_files = os.listdir(directory)
        detail_files = sorted(detail_files)
        thumbCount = len(os.listdir(os.getcwd() + "/datas/thumbnails/"))
        infoCount = len(os.listdir(os.getcwd() + "/datas/info/"))

        # 상품상세
        for i in detail_files:
            # 정렬순
            driver.find_element(By.ID, "sortNum").send_keys(Keys.BACKSPACE)
            driver.find_element(By.ID, "sortNum").send_keys(str(order))
            # 이미지 구분 selection
            select = Select(driver.find_element(By.ID, "fileClassCd"))
            select.select_by_visible_text("상품상세")
            # image send
            driver.find_element(By.ID, "productImgObject").send_keys(os.getcwd() + "/datas/details/" + i)
            driver.find_element(By.ID, "ru_prod_images").click()
            # 알러트
            time.sleep(1)
            Alert(driver).accept()
            order = order + 1

        # thumbnail
        order = 1
        if thumbCount == 1:
            # 이미지 구분 selection
            select = Select(driver.find_element(By.ID, "fileClassCd"))
            select.select_by_visible_text("상품썸네일")
            # image send
            driver.find_element(By.ID, "productImgObject").send_keys(
                os.getcwd() + "/datas/thumbnails/" + os.listdir(os.getcwd() + "/datas/thumbnails/")[0])
            driver.find_element(By.ID, "ru_prod_images").click()
            # 알러트
            time.sleep(1)
            Alert(driver).accept()
            time.sleep(0.3)
        order = 1
        # info
        if infoCount == 1:
            # 이미지 구분 selection
            select = Select(driver.find_element(By.ID, "fileClassCd"))
            select.select_by_visible_text("상품정보고시")
            # image send
            driver.find_element(By.ID, "productImgObject").send_keys(
                os.getcwd() + "/datas/info/" + os.listdir(os.getcwd() + "/datas/info/")[0])
            driver.find_element(By.ID, "ru_prod_images").click()
            # 알러트
            time.sleep(1)
            Alert(driver).accept()
            time.sleep(0.8)



    #COUNT PAGES

    skip = True
    while(skip):
        for i in range(1,pages+1):
            #Table Load & Pagination Load
            page = driver.find_element(By.CLASS_NAME,"pagination")
            li = page.find_elements(By.TAG_NAME,"li")
            table = driver.find_element(By.ID,"mainDataTable")
            tbody = table.find_elements(By.TAG_NAME,"tbody")
            tr = table.find_elements(By.TAG_NAME,"tr")
            for j in range(1,len(tr)):
                vect = tr[j].find_element(By.CLASS_NAME,"text-center")
                if(targetProduct == int(vect.find_element(By.TAG_NAME,"a").get_attribute("text"))):
                    skip = False
                    print(str(targetProduct)+" found")
                    print("Now inserting Images...")
                    vect.click()
                    break
            if(not skip):
                break
            li[len(li)-1].click()
            time.sleep(0.8)
            if(pages == i):
                skip = False
                run= False
                print("Failed to find Target")
    if(run):
        runImgAdd()
        print("----사진 추가됨----")
while(True):
    skull(officialOption)
