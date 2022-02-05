from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time 
from threading import Thread
import var
import shutil
from pyautogui import alert, write, press

class Scraper():
    def __init__(self):
        self.email = var.email
        self.password = var.password
        Thread(target=self.stop, daemon=True).start()

    def run(self):
        try:
            # login handle
            """ There was three case in total here.
            1. Remember me : true
            2. Remember me : true different account
            3. Remember me : false """

            if var.remember_me:
                chrome_options = Options()
                chrome_options.binary_location ="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                chrome_options.add_argument("user-data-dir=selenium")

                if self.email == var.cookies_of:
                    self.driver = webdriver.Chrome(
                        executable_path='chromedriver.exe', chrome_options=chrome_options)
                    # changed this line from => executable_path='chromedriver', chrome_options=chrome_options)
                    self.driver.get(var.primary_link)
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located(
                                (By.ID, "global-typeahead-search-input")))
                        self.driver.find_element_by_id("global-typeahead-search-input")
                    except:
                        print("Logging in....")
                        self.login()

                else:
                    try:
                        shutil.rmtree("selenium")
                    except:
                        print("Can't delete")
                    chrome_options = Options()
                    chrome_options.binary_location ="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                    self.driver = webdriver.Chrome(
                        executable_path='chromedriver', chrome_options=chrome_options)
                    self.login()

                var.cookies_of = self.email

            else:
                chrome_options = Options()
                chrome_options.binary_location ="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                self.driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
                # changed this line from => self.driver = webdriver.Chrome(executable_path='chromedriver')
                self.login()

            var.driver = self.driver
            # wait till start button is pushed
            # while var.status == True:
            #     sleep(1)

            # var.status = True
            # self.scrap()
            print("Login Done ...")
        except Exception as e:
            print("Exeception occured at scraper init :{}".format(e))
            var.status = False
            var.stop = True

        # finally:
        #     print("closing the thread")


    def login(self):
        self.driver.get(var.primary_link)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body")))
        # WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.ID, "username")))
        # write(self.email)
        # press('tab')
        # write(self.password)
        # press('enter')
        self.driver.find_element_by_tag_name("body").send_keys(
            Keys.TAB + self.email + Keys.TAB + self.password + Keys.ENTER)
        time.sleep(1)

    def scrap(self):
        links = []
        print("starting to scrape....")
        # start_time = time()
        limit = var.page_number
        profile_count = 0
        var.profile_count = profile_count
        step = var.scrolling_step
        try_count = var.try_count
        delay_time = var.delay
        count = 0
        try:
            # elem = self.driver.find_elements_by_class_name("search-results__result-item")
            # looping through every page
            for count3 in range(0,limit):
                if var.stop == True:
                    break

                for i in range(try_count):
                    count = count + step
                    self.driver.execute_script("document.querySelector('#content-main > div > div.full-width > div.p4._vertical-scroll-results_1igybl').scrollTop={}".format(count))
                    time.sleep(0.5)

                try:
                        count = 0
                        temp = list()
                        elem = self.driver.find_elements_by_css_selector('a[data-anonymize="company-name"]')  
                    
                        # time.sleep(3)
                        # lists = driver.find_elements_by_css_selector('a[data-anonymize="person-name"]')
                        # while count1<try_count and var.stop != True:
                         
                        for item in elem:
                                if var.stop == True:
                                    break
                                link = item.get_attribute("href")
                                links.append(link)
                                
                
                                # print (count3 , j)
                except Exception as e:
                            print("can't get links")
            

                if(count3<(limit-1)):
                    
                    try: 
                        next_btn = self.driver.find_element_by_css_selector('button[aria-label="Next"]')
                        next_btn.click()
                    except Exception as e:
                            print("no more page exist")
                            break
                time.sleep(4)
                
            #looping through each elements in One item
            # print(links)

            for link in links:
                                if var.stop == True:
                                  break
                                self.driver.get(link)

                                profile_count += 1
                                var.profile_count = profile_count
                                var.remaining_page = (len(links) - profile_count)

                                time.sleep(delay_time)

                                try:
                                    try:
                                        name = self.driver.find_element_by_css_selector('div[data-anonymize="company-name"]').get_attribute('innerHTML').strip()
                                    except Exception as e:
                                        name = "not available"

                                    try:   
                                        job_title = self.driver.find_element_by_css_selector('span[data-anonymize="industry"]').get_attribute('innerHTML').strip()
                                    except Exception as e:
                                        job_title = "not available"

                                    # try:
                                    #     company_name = self.driver.find_element_by_css_selector('a[data-anonymize="company-name"]').get_attribute('innerHTML').strip()
                                    # except Exception as e:
                                    #     company_name = "not available"

                                    try:   
                                        location = self.driver.find_element_by_css_selector('div[data-anonymize="location"]').text
                                    except Exception as e:
                                        location = "not available"

                                    time.sleep(2)
                                    # try:
                                    #     prfile_open = self.driver.find_element_by_css_selector('li[data-test-badge="open-link"]')
                                    #     profile = "open"
                                    # except Exception as e:
                                    #     profile= 'close'
                                    
                                    # try:
                                    #     click_more_btn = self.driver.find_element_by_class_name("right-actions-overflow-menu-trigger")
                                    #     click_more_btn.click()
                                    #     time.sleep(2)

                                    #     copy_btn = self.driver.find_element_by_css_selector('div[data-control-name="copy_linkedin"]')
                                    #     copy_btn.click()
                                    #     time.sleep(2)
                                    #     linkedin_profile_link = clipboard.paste()
                                    # except Exception as e:
                                    #     linkedin_profile_link = 'not available'

                                    try:
                                        website_link_div = self.driver.find_element_by_css_selector('a[data-control-name="visit_company_website"]')
                                        website_link = website_link_div.get_attribute("href")
                                    except:
                                        website_link = "not available"

                                    try:
                                        try:
                                            employee_count = self.driver.find_element_by_css_selector('span[data-anonymize="company-size"]').text
                                        except:
                                            employee_count = self.driver.find_element_by_css_selector('a[data-control-name="decision_makers_search_link"]').text
                                    except:
                                        employee_count = "not available"

                                    tempDict = {
                                                "Comapany": name,
                                                "Industry": job_title,
                                                "Headquater": location,
                                                "Website": website_link,
                                                "Employee_Count": employee_count
                                            }
                                    temp.append(tempDict.copy())
                                    elem.remove(item)
                                except Exception as e:
                                    # print("error at getting profile")
                                    pass
            #                 print("----- {}".format(count1))
            #                 print(len(driver.find_elements_by_class_name("search-results__result-item")))
            #                 print(len(temp))
                            # if len(temp) == 25:
                            #     break

                        # except Exception as e:
                        #     print("error at scrolling {}".format(e))
                        #     continue

                    # if var.stop == True:
                    #     break
                    # sleep(1+var.delay)

                    # # going to next page
                    
                    # self.driver.find_element_by_class_name("search-results__pagination-next-button").click()
           #             self.driver.find_element_by_class_name("search-results__pagination-previous-button").click()
                    # WebDriverWait(self.driver, 10).until(
                    #     EC.visibility_of_element_located((By.CLASS_NAME, "search-results__result-item")))
                    # except Exception as e:
                    #             print("next button not found {}".format(e))
                    #             for i in range(0,10):
                    #                 if var.stop == True:
                    #                     break
                    #                 try:
                    #                     self.driver.find_element_by_class_name("error-action").click()
                    #                     WebDriverWait(self.driver, 10).until(
                    #                         EC.visibility_of_element_located((By.CLASS_NAME, "search-results__result-item")))
                    #                     self.driver.find_element_by_class_name("search-results__result-item")
                    #                     break
                    #                 except:
                    #                     continue

            for item in temp:
                        var.scrap_data.append(item)

            # profile_count += len(temp)

            var.remaining_page = limit - (count3+1)
            var.profile_count = profile_count

            print("  Page Count : {} \n  Profile Count : {} ".format(count3+1, len(temp)))

            # time_taken = (time() - start_time)/60
            alert(text='Total Profile : {}'.format(profile_count), title='', button='OK')
            # alert(text='Time taken : {:.2f} min\nTotal Profile : {}'.format(
            #             time_taken, profile_count), title='', button='OK')

        except Exception as e:
            print("Exeception occured at scrap : {} ".format(e))
            var.status = False
            var.stop = True

        finally:
            var.scarp_start = False
            print("scrap func finished")

    def stop(self):
        while True:
            time.sleep(1)
            if var.stop == True:
                try:
                    var.status = False
                    self.driver.quit()
                    print("Process : Closing the browser")
                except Exception as e:
                    print("Exeception occured at stop : {} ".format(e))
                finally:
                    break
def run():
    scraper = Scraper()
    scraper.run()
    while var.status == True:
        time.sleep(1)
        if var.scarp_start == True:
            scraper.scrap()
            print("out of scrap func")
    var.status = False
    var.scarp_start = False
    print("Closing the thread")
# def scrap():
#     scraper = Scraper()
#     scraper.scrap()

if __name__ == "__main__":
    pass