import sys
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import time
import ssl
import os
from selenium.webdriver.common.by import By
import imageio.v2 as imageio
import requests
import json
winKey = 8
macKey = 6
osKey = winKey
winSlash = "\\"
macSlash = "/"
osSlash = winSlash

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

ico = resource_path('alpha.ico')
ssl._create_default_https_context = ssl._create_unverified_context
chromedriver_autoinstaller.install()
main_ui = resource_path('main.ui')
login_ui = resource_path('login.ui')
loginUI = uic.loadUiType(login_ui)[0]
mainUI = uic.loadUiType(main_ui)[0]
webdriver_options = webdriver.ChromeOptions()
webdriver_options.add_argument('headless')
webdriver_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=webdriver_options)
driver.implicitly_wait(5)
# Headless option

# No Headless option
# driver = webdriver.Chrome()

class runOfficialThread(QThread):
    id_data = ""
    pwd_data = ""
    def setId(self, id_data, pwd_data):
        self.id_data = id_data
        self.pwd_data = pwd_data
    def __init__(self,parent = None):
        super().__init__(parent)
    def run(self):
        id = self.id_data
        pwd = self.pwd_data
        print("Official Loging in")
        driver.get('https://admin.sellable.kr/itstore/user/logout')
        driver.find_element(By.ID, 'userId').send_keys(id)
        driver.find_element(By.ID, 'userPw').send_keys(pwd)
        driver.find_element(By.ID, 'btnLogin').click()

class runDevThread(QThread):
    id_data = ""
    pwd_data = ""
    def setId(self, id_data, pwd_data):
        self.id_data = id_data
        self.pwd_data = pwd_data

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        print("Dev login")
        id = self.id_data
        pwd = self.pwd_data
        driver.get('https://deva.sellable.kr/itstore/user/login')
        driver.find_element(By.ID, 'userId').send_keys(id)
        driver.find_element(By.ID, 'userPw').send_keys(pwd)
        driver.find_element(By.ID, 'btnLogin').click()

class loginWindow(QDialog, loginUI) :
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('alpha.ico'))
        self.setupUi(self)
        self.officialLogin.clicked.connect(self.loginOfficial)
        self.devLogin.clicked.connect(self.loginDev)

    def loginOfficial(self):
        x = runOfficialThread(self)
        x.setId(self.idForm.text(), self.pwdForm.text())
        x.start()
        load = False
        driver.implicitly_wait(0.3)
        self.label_2.setText("Logging_in")
        self.label_2.repaint()
        while(load == False):
            try:
                print("????????? ??? ????????? ????????????")
                driver.find_element(By.CLASS_NAME,"dropdown-toggle")
                self.hide()
                self.second = mainWindow()
                self.second.exec()
                print("?????? ??????")
            except:
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                    load = True
                    print("????????? ??????")
                    self.label_2.setText("Password or ID is incorrect")
                except:
                    print("????????? x")
        driver.implicitly_wait(5)

    def loginDev(self):
        x = runDevThread(self)
        x.setId(self.idForm.text(),self.pwdForm.text())
        x.start()
        load = False
        driver.implicitly_wait(0.3)
        self.label_2.setText("Logging_in")
        self.label_2.repaint()
        while(load == False):
            try:
                print("?????? ?????? ??????")
                driver.find_element(By.CLASS_NAME,"dropdown-toggle")
                load = True
                self.hide()
                self.second = mainWindow()
                self.second.exec()
                print("?????? ?????? ??????")
            except:
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                    load = True
                    print("????????? ??????")
                    self.label_2.setText("Password or ID is incorrect")
                except:
                    print("????????? x")
        driver.implicitly_wait(5)

class mainWindow(QDialog, mainUI):
    def __init__(self):

        def dragEnterEvent(e):
            if str(e.mimeData().urls()) == "[]":
                e.ignore()
            elif e.mimeData().hasUrls:
                e.accept()
            else:
                print("?????????x")
                super(QListWidget,self.detailList).dragEnterEvent(e);

        def dropEventDetail(e):
            fullLinks = []
            urls = e.mimeData().urls()
            for url in urls:
                url = url.toString()
                fullLinks.append(url)
                #name = url.split('/')[-1]
                self.detailList.addItem(url)
            self.consoleLabel.setText("Images updated in \"?????? ??????\" list")
            self.consoleLabel.repaint()
            self.detailCheck.setChecked(True)

        def dropEventInfo(e):
            fullLinks = []
            urls = e.mimeData().urls()
            for url in urls:
                url = url.toString()
                fullLinks.append(url)
                # name = url.split('/')[-1]
                self.infoList.addItem(url)
            self.consoleLabel.setText("Images updated in \"?????? ????????????\" list")
            self.consoleLabel.repaint()
            self.infoCheck.setChecked(True)

        def dropEventThumbnail(e):
            fullLinks = []
            urls = e.mimeData().urls()
            for url in urls:
                url = url.toString()
                fullLinks.append(url)
                # name = url.split('/')[-1]
                self.thumbnailList.addItem(url)
            self.consoleLabel.setText("Images updated in \"?????? ?????????\" list")
            self.consoleLabel.repaint()
            self.thumbnailCheck.setChecked(True)
        super().__init__()
        self.setWindowIcon(QIcon('alpha.ico'))
        self.setupUi(self)
        self.detailList.setDragEnabled(True)
        self.detailList.setAcceptDrops(True);
        self.detailList.dragEnterEvent = dragEnterEvent
        self.detailList.dropEvent = dropEventDetail
        self.thumbnailList.dropEvent = dropEventThumbnail
        self.thumbnailList.dragEnterEvent = dragEnterEvent
        self.infoList.dropEvent = dropEventInfo
        self.infoList.dragEnterEvent = dragEnterEvent
        self.reloadButton.clicked.connect(self.reloadClicked)
        self.switchButton.clicked.connect(self.switchClicked)
        self.pushButton.clicked.connect(self.submitClicked)
        self.detailList.itemClicked.connect(self.showDetailIMG)
        self.thumbnailList.itemClicked.connect(self.showThumbIMG)
        self.infoList.itemClicked.connect(self.showInfoIMG)
        self.orderButton.clicked.connect(self.orderSwitch)
        if driver.current_url == "https://deva.sellable.kr/itstore/main":
            self.setWindowTitle("??????-????????? ?????????")
        else:
            self.setWindowTitle("?????? ????????? ?????????")

    def orderSwitch(self):
        items = [str(self.detailList.item(x).text()) for x in range(self.detailList.count())]
        self.detailList.clear()
        self.consoleLabel.setText("??????????????? ????????????????????????")
        self.consoleLabel.repaint()
        items.sort()
        for item in items:
            self.detailList.addItem(str(item))

    def showThumbIMG(self):
        w = self.imgLabel.width()
        h = self.imgLabel.height()
        self.imgLabel.setPixmap(QPixmap(self.thumbnailList.currentItem().text()[osKey:]).scaled(w, h))

    def showInfoIMG(self):
        w = self.imgLabel.width()
        h = self.imgLabel.height()
        self.imgLabel.setPixmap(QPixmap(self.infoList.currentItem().text()[osKey:]).scaled(w, h))

    def showDetailIMG(self):
        w = self.imgLabel.width()
        h = self.imgLabel.height()
        self.imgLabel.setPixmap(QPixmap(self.detailList.currentItem().text()[osKey:]).scaled(w, h))

    def reloadClicked(self):
        self.detailList.clear()
        self.thumbnailList.clear()
        self.infoList.clear()
        self.consoleLabel.setText("Every images cleared")

    def switchClicked(self):
        items = [str(self.detailList.item(x).text()) for x in range(self.detailList.count())]
        self.detailList.clear()
        self.consoleLabel.setText("Images reversed")

        items.reverse()
        for item in items:
            self.detailList.addItem(str(item))

    def submitClicked(self):
        run = True
        if(self.thumbnailCheck.isChecked() == False and self.infoCheck.isChecked() == False and self.detailCheck.isChecked()==False):
            self.consoleLabel.setText("No Items are Checked")
            self.consoleLabel.repaint()
            print("--No Item Selected--")
            return None
        try:
            self.consoleLabel.setText("Searching...")
            self.consoleLabel.repaint()
            targetProduct = int(self.codeForm.text())
            time.sleep(0.5)
        except:
            self.consoleLabel.setText("Please enter \"????????????\" properly")
            return None
        driver.switch_to.default_content()
        ul = driver.find_element(By.CLASS_NAME, "pcoded-left-item")
        lis = ul.find_elements(By.CLASS_NAME, "pcoded-hasmenu")
        li = lis[2]
        lis[2].click()
        driver.find_element(By.XPATH, "//a[@href='/itstore/product/list']").click()
        frame = driver.find_element(By.ID, "mainContent")
        driver.switch_to.frame(frame)
        time.sleep(0.4)
        # COUNT PAGES
        page = driver.find_element(By.CLASS_NAME, "pagination")
        li = page.find_elements(By.TAG_NAME, "li")
        pages = int(li[len(li) - 2].find_element(By.TAG_NAME, "a").get_attribute("innerHTML"))

        skip = True
        while (skip):
            for i in range(1, pages + 1):
                # Table Load & Pagination Load
                page = driver.find_element(By.CLASS_NAME, "pagination")
                li = page.find_elements(By.TAG_NAME, "li")
                table = driver.find_element(By.ID, "mainDataTable")
                tbody = table.find_elements(By.TAG_NAME, "tbody")
                tr = table.find_elements(By.TAG_NAME, "tr")
                for j in range(1, len(tr)):
                    vect = tr[j].find_element(By.CLASS_NAME, "text-center")
                    if (targetProduct == int(vect.find_element(By.TAG_NAME, "a").get_attribute("text"))):
                        skip = False
                        self.consoleLabel.setText(str(targetProduct) + " has been found")
                        vect.click()
                        break
                if (not skip):
                    break
                li[len(li) - 1].click()
                time.sleep(0.8)
                if (pages == i):
                    skip = False
                    run = False
                    self.consoleLabel.setText(str(targetProduct) + " cannot be found")

        def runImgAdd():
            driver.find_element(By.LINK_TEXT, "??????????????????").click()
            order = 1
            detail_files = [str(self.detailList.item(x).text()) for x in range(self.detailList.count())]
            thumb_files = [str(self.thumbnailList.item(x).text()) for x in range(self.thumbnailList.count())]
            info_files = [str(self.infoList.item(x).text()) for x in range(self.infoList.count())]
            thumbCount = self.thumbnailList.count()
            infoCount = self.infoList.count()
            detailCount = self.detailList.count()
            s = requests.Session()
            selenium_user_agent = driver.execute_script("return navigator.userAgent;")
            s.headers.update({"user-agent": selenium_user_agent})
            for cookie in driver.get_cookies():
                s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
            payload = {"productNo": str(self.codeForm.text()),
                       "txId": "MODIFY",
                       "fileTypeCd": "image",
                       "fileMainClassCd": "product",
                       "productImagesDT_length": 10,
                       "commonFileNo": "",
                       "fileClassCd": "",
                       "sortNum": ""}
            if("https://deva" == driver.current_url[0:12]):
                payloadUrl = "https://deva.sellable.kr/itstore/product/images?productNo="+str(self.codeForm.text())+"&txId=MODIFY&fileTypeCd=image&fileMainClassCd=product&productImagesDT_length=10&commonFileNo=&fileClassCd=&sortNum="
            else:
                payloadUrl = "https://admin.sellable.kr/itstore/product/images?productNo="+str(self.codeForm.text())+"&txId=MODIFY&fileTypeCd=image&fileMainClassCd=product&productImagesDT_length=10&commonFileNo=&fileClassCd=&sortNum="
            r = s.get(payloadUrl, data=payload)
            r = r.text.encode('utf-8')
            a = r.decode('unicode-escape')
            a = json.loads(str(a))
            jsonData = a["data"]["contents"]
            print(jsonData)
            #????????????
            if self.detailCheck.isChecked() == True and detailCount != 0:
                if(jsonData != []):
                    for Data1 in jsonData:
                        if(Data1["fileClassCd"] == "mainImg"):
                            payloadDelete = {
                                "productNo" : str(Data1["productNo"]),
                                "txId": "DELETE_PROD_IMAGE",
                                "fileTypeCd": str(Data1["fileTypeCd"]),
                                "fileMainClassCd": str(Data1["fileMainClassCd"]),
                                "productImagesDT_length": str(a["reqParameter"]["productImagesDT_length"]),
                                "commonFileNo": str(Data1["commonFileNo"]),
                                "fileClassCd": str(Data1["fileClassCd"]),
                                "sortNum" : str(Data1["sortNum"]),
                                "inputFile":"",
                            }
                            if ("https://deva" == driver.current_url[0:12]):
                                url = "https://deva.sellable.kr/itstore/common/file/product"
                            else:
                                url = "https://admin.sellable.kr/itstore/common/file/product"
                            s.post(url,payloadDelete)
                self.consoleLabel.setText("Now inserting \"?????? ??????\" images")
                self.consoleLabel.repaint()
                time.sleep(0.5)



                for i in detail_files:
                    # ?????????
                    driver.find_element(By.ID, "sortNum").send_keys(Keys.BACKSPACE)
                    driver.find_element(By.ID, "sortNum").send_keys(str(order))
                    # ????????? ?????? selection
                    select = Select(driver.find_element(By.ID, "fileClassCd"))
                    select.select_by_visible_text("????????????")
                    # image send
                    print("Now sending key -> "+i[osKey:])
                    driver.find_element(By.ID, "productImgObject").send_keys(i[osKey:])
                    driver.find_element(By.ID, "ru_prod_images").click()
                    # ?????????
                    time.sleep(1)
                    Alert(driver).accept()
                    order = order + 1

            #thumbnail
            order = 1
            if self.thumbnailCheck.isChecked() == True and thumbCount == 1:
                if (jsonData != []):
                    for Data1 in jsonData:
                        if (Data1["fileClassCd"] == "thumbnail"):
                            payloadDelete = {
                                "productNo": str(Data1["productNo"]),
                                "txId": "DELETE_PROD_IMAGE",
                                "fileTypeCd": str(Data1["fileTypeCd"]),
                                "fileMainClassCd": str(Data1["fileMainClassCd"]),
                                "productImagesDT_length": str(a["reqParameter"]["productImagesDT_length"]),
                                "commonFileNo": str(Data1["commonFileNo"]),
                                "fileClassCd": str(Data1["fileClassCd"]),
                                "sortNum": str(Data1["sortNum"]),
                                "inputFile": "",
                            }
                            if ("https://deva" == driver.current_url[0:12]):
                                url = "https://deva.sellable.kr/itstore/common/file/product"
                            else:
                                url = "https://admin.sellable.kr/itstore/common/file/product"
                            s.post(url,payloadDelete)
                self.consoleLabel.setText("Now inserting \"?????? ?????????\" images")
                self.consoleLabel.repaint()
                # ????????? ?????? selection
                select = Select(driver.find_element(By.ID, "fileClassCd"))
                select.select_by_visible_text("???????????????")
                # image send
                driver.find_element(By.ID, "productImgObject").send_keys(thumb_files[0][osKey:])
                driver.find_element(By.ID, "ru_prod_images").click()
                # ?????????
                time.sleep(1)
                Alert(driver).accept()
                time.sleep(0.3)
            elif self.thumbnailCheck.isChecked() == True and thumbCount >= 1:
                if (jsonData != []):
                    for Data1 in jsonData:
                        if (Data1["fileClassCd"] == "thumbnail"):
                            payloadDelete = {
                                "productNo": str(Data1["productNo"]),
                                "txId": "DELETE_PROD_IMAGE",
                                "fileTypeCd": str(Data1["fileTypeCd"]),
                                "fileMainClassCd": str(Data1["fileMainClassCd"]),
                                "productImagesDT_length": str(a["reqParameter"]["productImagesDT_length"]),
                                "commonFileNo": str(Data1["commonFileNo"]),
                                "fileClassCd": str(Data1["fileClassCd"]),
                                "sortNum": str(Data1["sortNum"]),
                                "inputFile": "",
                            }
                            if ("https://deva" == driver.current_url[0:12]):
                                url = "https://deva.sellable.kr/itstore/common/file/product"
                            else:
                                url = "https://admin.sellable.kr/itstore/common/file/product"
                            s.post(url,payloadDelete)
                images = []
                for filename in thumb_files:
                    images.append(imageio.imread(filename[osKey:]))
                imageio.mimsave('movie.gif', images, format='GIF', fps=1)
                # ????????????
                self.consoleLabel.setText("Now inserting \"?????? ?????????\" images as GIF")
                self.consoleLabel.repaint()
                # ????????? ?????? selection
                select = Select(driver.find_element(By.ID, "fileClassCd"))
                select.select_by_visible_text("???????????????")
                # image send
                driver.find_element(By.ID, "productImgObject").send_keys(os.getcwd() + osSlash+"movie.gif")
                driver.find_element(By.ID, "ru_prod_images").click()
                # ?????????
                time.sleep(1)
                Alert(driver).accept()
                time.sleep(0.3)

            order = 1
            # info
            if self.infoCheck.isChecked() == True and infoCount != 0:
                if (jsonData != []):
                    for Data1 in jsonData:
                        if (Data1["fileClassCd"] == "prodNotice"):
                            payloadDelete = {
                                "productNo": str(Data1["productNo"]),
                                "txId": "DELETE_PROD_IMAGE",
                                "fileTypeCd": str(Data1["fileTypeCd"]),
                                "fileMainClassCd": str(Data1["fileMainClassCd"]),
                                "productImagesDT_length": str(a["reqParameter"]["productImagesDT_length"]),
                                "commonFileNo": str(Data1["commonFileNo"]),
                                "fileClassCd": str(Data1["fileClassCd"]),
                                "sortNum": str(Data1["sortNum"]),
                                "inputFile": "",
                            }
                            if ("https://deva" == driver.current_url[0:12]):
                                url = "https://deva.sellable.kr/itstore/common/file/product"
                            else:
                                url = "https://admin.sellable.kr/itstore/common/file/product"
                            s.post(url,payloadDelete)
                self.consoleLabel.setText("Now inserting \"?????? ????????????\" images")
                self.consoleLabel.repaint()                # ????????? ?????? selection
                select = Select(driver.find_element(By.ID, "fileClassCd"))
                select.select_by_visible_text("??????????????????")
                # image send
                driver.find_element(By.ID, "productImgObject").send_keys(info_files[0][osKey:])
                driver.find_element(By.ID, "ru_prod_images").click()
                # ?????????
                time.sleep(1)
                Alert(driver).accept()
                time.sleep(0.8)
        if(run):
            runImgAdd()
            self.consoleLabel.setText("Insertion Complete")
            self.consoleLabel.repaint()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = loginWindow()
    myWindow.show()
    app.exec_()