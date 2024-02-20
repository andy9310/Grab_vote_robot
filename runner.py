from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time
import base64
import requests
import json
from PIL import Image
driver = webdriver.Chrome()
driver.get('https://tkglobal.melon.com/main/index.htm')
driver.maximize_window()
class Sign_in:
    def __init__(self):
        self.email = 'b10302352@ntu.edu.tw'
        self.password = 'Aa0907458007'
        self.captcha_api = 'd1cb6c919c1ffa284b58bdaef978bc2f'
        self.performance_page = '/performance/index.htm?langCd=EN&prodId=209257'
        self.date = 'Sun, Mar 24, 2024'
        self.prodid = '209257'
    def sign_in_function(self):
        driver.find_element(By.XPATH, "//a[contains(@id, 'g_login')]").click()
        driver.find_element(By.XPATH, "//input[contains(@id, 'email')]").send_keys(self.email)
        driver.find_element(By.XPATH, "//input[contains(@id, 'pwd')]").send_keys(self.password)
        driver.find_element(By.XPATH, "//a[contains(@id, 'formSubmit')]").click()
        driver.find_element(By.XPATH, f"//a[contains(@href, '{self.performance_page}')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, f"//span[ text()='{self.date}']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, f"//button[ contains(@data-prodid, '{self.prodid}')]").click()


        time.sleep(2)
        main_window = driver.current_window_handle
        for handle in driver.window_handles: 
            if handle != main_window: 
                print("hi")
                popup = handle
                driver.switch_to.window(popup)
                break
        
        
        
        
        while True:
            break
            driver.save_screenshot('./test.png')
            # element = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')
            element = driver.find_element(By.XPATH, "//img[ contains(@id, 'captchaImg')]")
            # print(element.location)
            left = element.location['x']
            right = element.location['x'] + element.size['width']
            top = element.location['y']
            bottom = element.location['y'] + element.size['height']
            img = Image.open('./test.png')
            img = img.crop((left, top, right, bottom))
            img.save('captcha.png')
            file = {'file': open('captcha.png', 'rb')}
            api_key = self.captcha_api
            payload = {'key': api_key}
            response = requests.post('http://2captcha.com/in.php', files = file, params = payload)
            print(f'response:{response.text}')
            captcha_text='hhhhhh'
            if response.ok and response.text.find('OK') > -1:
                # 擷取驗證碼ID
                captcha_id = response.text.split('|')[1]  
                # 由於 2Captcha 服務有時無法即時辨識與回應結果，所以實作一個 retry 機制
                for i in range(10):
                    # 取得辨識結果，帶入你的 api_key 跟剛剛擷取的 captcha_id
                    response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
                    # 若尚未辨識完成，休息個三秒，會在 for 開頭再跑一次
                    if response.text.find('CAPCHA_NOT_READY') > -1: 
                        time.sleep(2)
                    # 若辨識完成正確
                    elif response.text.find('OK') > -1:
                    # 擷取正確辨識結果 
                        captcha_text = response.text.split('|')[1]  
                        print(captcha_text)
                        break
                    else:
                        print('取得驗證碼發生錯誤!')
            driver.find_element(By.XPATH, "//input[ contains(@id, 'label-for-captcha')]").send_keys(captcha_text)
            driver.find_element(By.XPATH, "//a[ contains(@id, 'btnComplete')]").click()
            break
            # try:
            #     driver.find_element(By.XPATH, "//div[ contains(@id, 'errorMessage')]")
            #     driver.find_element(By.XPATH, "//input[ contains(@id, 'label-for-captcha')]").clear()
            #     continue
            # except Exception as e:
            #     break
        print("finish captcha part")
        
        ### seat selection
        time.sleep(2)
        # driver.find_element(By.XPATH, "//rect[ contains(@fill, '#baa885')]").click()
        # '//*[name()="rect"][@id="id123"]'
        ids = driver.find_elements(By.TAG_NAME,'iframe')
        for ii in ids:
            #print ii.tag_name
            print(ii.get_attribute('id'))    # id name as string
        driver.switch_to.frame(driver.find_element(By.TAG_NAME,'iframe'))
        ids = driver.find_elements(By.XPATH,"//*[name()='rect']")
        for ii in ids:
            #print ii.tag_name
            try:
                ii.click()
                print("clicked")
                break
            except Exception as e:
                continue
            # print(ii.get_attribute('x'))    # id name as string
        # driver.find_element(By.XPATH,"//*[name()='rect'][@fill='#bfa889']").click()
        # driver.find_element(By.XPATH, "//*[contains(@id,'ez_canvas') ]").click()
        driver.find_element(By.XPATH, "//a[ contains(@id, 'nextTicketSelection')]").click()
        time.sleep(2)
        select = Select(driver.find_element(By.TAG_NAME,'select'))	
        select.select_by_value("1")
        driver.find_element(By.XPATH, "//a[ contains(@id, 'nextPayment')]").click()


        # # driver.switch_to.frame(driver.find_element(By.TAG_NAME, "frame"))
        # # driver.find_element(By.TAG_NAME, "div")
        # ids = driver.find_elements(By.XPATH,'//*[@id]')
        # for ii in ids:
        #     #print ii.tag_name
        #     print(ii.get_attribute('id'))    # id name as string
        # driver.find_element(By.CLASS_NAME, "layerPop").send_keys('adtgww')
        # driver.find_element(By.CLASS_NAME, "layerPop").click()
        driver.save_screenshot('./test.png')
Sign_action = Sign_in()
Sign_action.sign_in_function()
