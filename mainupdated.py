import os
import xlrd
import csv
import time
import tldextract
from tkinter import *
from tkinter import filedialog
from datetime import datetime
from twilio.rest import Client
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class google:
    # starting a new web driver with the details
    def __init__(self, user_name, pass_word, site, recovery_mail, business_name,
                 address, city, state, zip_code, p_num, catagory):
        opts = ChromeOptions()
        opts.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(options=opts)
        self.user_name = user_name
        self.pass_word = pass_word
        self.site = site
        self.recovery_mail = recovery_mail
        self.business_name = business_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.p_num = p_num
        self.catagory = catagory
        try:
            self.login()
        except Exception as e:
            print("login Eroor" + str(e) + '\n')
        try:
            self.change_re_mail()
        except Exception as e:
            print("change recovery Eroor" + str(e) + '\n')
        try:
            self.add_business()
        except Exception as e:
            print("add business error" + str(e) + '\n')

    # log in + entering recovery mail
    def login(self):
        def check_exists_by_xpath(xpath):
            try:
                self.driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                return False
            return True

        self.driver.get("https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27")
        time.sleep(3)
        self.find_xp('//*[@id="openid-buttons"]/button[1]').click()
        self.find_xp('//input[@type="email"]').send_keys(self.user_name)
        self.find_xp('//*[@id="identifierNext"]').click()
        time.sleep(3)
        self.find_xp('//input[@type="password"]').send_keys(self.pass_word)
        self.find_xp('//*[@id="passwordNext"]').click()
        time.sleep(6)
        # entering recovery mail if there is
        if check_exists_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/'
                                 'span/section/div/div/div/ul/li[1]/div/div[2]') is True:
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/'
                    'span/section/div/div/div/ul/li[1]/div/div[2]').click()
                time.sleep(5)
                self.driver.find_element(By.ID, "knowledge-preregistered-email-response").click()
                time.sleep(5)
                self.driver.find_element(By.ID, "knowledge-preregistered-email-response").send_keys(self.recovery_mail)
                time.sleep(5)
                self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-RLmnJb").click()
                time.sleep(5)
            except:
                pass
        # phone recovering
        try:
            if check_exists_by_xpath('//*[@id="knowledge-preregistered-email-response"]') is True:
                self.driver.find_element_by_xpath(
                    '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/'
                    'span/section/div/div/div/ul/li[1]/div/div[2]').click()
                time.sleep(5)
                self.driver.find_element(By.ID, "knowledge-preregistered-email-response").click()
                time.sleep(5)
                self.driver.find_element(By.ID, "knowledge-preregistered-email-response") \
                    .send_keys(phone_num_make_numbers(self.recovery_mail))
                time.sleep(5)
                self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-RLmnJb").click()
                time.sleep(5)
        except:
            pass
        try:
            # sending phone num to verify
            if check_exists_by_xpath('//*[@id="phoneNumberId"]') is True:
                self.find_xp('//*[@id="phoneNumberId"]').click()
                self.find_xp('//*[@id="phoneNumberId"]').send_keys(phone_num_make_numbers(self.p_num))
                self.find_xp('//*[@id="phoneNumberId"]').send_keys(Keys.ENTER)
        except:
            pass
        # idk
        if check_exists_by_xpath('//*[@id="yDmH0d"]/form/div/span/div/div[3]/div/div/span/span') is True:
            self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/form/div/span/div/div[3]/div/div/span/span').click()
        else:
            pass
        time.sleep(5)

    # create the new recovery mail
    def create_new_recovery(self):
        return "info@" + tldextract.extract(self.site).domain + "." + tldextract.extract(self.site).suffix

    # changing recovery mail to info@domain
    def change_re_mail(self):  # DONE
        recovery_link = "https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmyaccount.google" \
                        ".com" \
                        "%2Frecovery%2Femail%3Fcontinue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Femail&service" \
                        "=accountsettings&osid=1&rart" \
                        "=ANgoxcfl2Af1D0s6rgaJMCaJ3yFYnrlrJiyK2vUTt0aPs3xjslqVmHfYRCDOpVq0RsG" \
                        "-iBidaPeYgofXTjYcUiUigKrvf0t_eA&TL" \
                        "=AM3QAYZLI5YUMQJmqKd5XQEfltcr02ZTr3573MbCXnN5fXMxAVj5JUkXJEoakMpD&flowName=GlifWebSignIn&cid=1" \
                        "&flowEntry=ServiceLogin "

        recovery_new_mail = self.create_new_recovery()
        self.driver.get(recovery_link)
        # sent password
        time.sleep(5)
        self.driver.find_element(By.NAME, "password").send_keys(self.pass_word)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe-OWXEXe-k8QpJ > .VfPpkd-RLmnJb").click()
        time.sleep(5)
        # pencil button
        try:
            self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[3]/c-wiz/div/div[3]/div[1]/div/div['
                                              '2]/span/span/span').click()
        except:
            pass
        time.sleep(5)
        try:
            mail_box = self.driver.find_element(By.CSS_SELECTOR, ".whsOnd")
        except:
            def check_exists_by_xpath(xpath):
                try:
                    self.driver.find_element_by_xpath(xpath)
                except NoSuchElementException:
                    return False
                return True

            # if need to put to update recovery mail
            if check_exists_by_xpath('//*[@id="i3"]') is True:
                mail_box = self.driver.find_element_by_xpath('//*[@id="i3"]')
                '''
                self.driver.find_element_by_xpath('//*[@id="i3"]').click()
                self.driver.find_element_by_xpath('//*[@id="i3"]').send_keys(self.create_new_recovery())

                '''

        mail_box.click()
        mail_box.clear()
        time.sleep(5)
        mail_box.send_keys(recovery_new_mail)
        mail_box.send_keys(Keys.ENTER)
        try:
            self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[3]/c-wiz/div/div[2]/div/div[2]/div['
                                              '2]/div[2]/div/div/button/div[2]').click()
        except:
            pass
        time.sleep(5)

    # finding xpath of element
    def find_xp(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    # add business and location
    def add_business(self):
        def check_exists_by_xpath(xpath):
            try:
                self.driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                return False
            return True

        self.driver.get("https://www.google.com/business/")
        time.sleep(2)
        self.driver.set_window_size(1114, 952)
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Sign in").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").send_keys(self.business_name)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").send_keys(Keys.ENTER)
        # click add your buissness name
        try:
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").send_keys(Keys.ENTER)
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".UxubU .RveJvd").click()
        except:
            pass
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").send_keys(self.catagory)
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/c-wiz/div/div/div[3]/div[1]/span/span').click()
        # yes add location
        time.sleep(2)
        self.driver.find_element(By.ID, "c1").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".UxubU .RveJvd").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "qjD4af-4-1").click()
        time.sleep(4)
        # location - array down, enter
        self.driver.find_element(By.ID, "qjD4af-4-1").send_keys(self.address + " " + self.city)
        time.sleep(2)
        self.driver.find_element(By.ID, "qjD4af-4-1").send_keys(Keys.DOWN)
        time.sleep(2)
        self.driver.find_element(By.ID, "qjD4af-4-1").send_keys(Keys.ENTER)
        time.sleep(2)
        # next
        self.driver.find_element(By.CSS_SELECTOR, ".UxubU .RveJvd").click()
        time.sleep(4)
        # workink!!!

        # if the business is exist is that your business?  - dont
        if check_exists_by_xpath('//*[@id="c6"]') is True:
            try:
                self.driver.find_element_by_xpath('//*[@id="c6"]').click()
                time.sleep(2)
                self.driver.find_element_by_xpath(
                    '//*[@id="yDmH0d"]/c-wiz/c-wiz/div/div/div[3]/div[1]/span/span').click()
                time.sleep(3)
            except:
                pass
        # no i dont todo
        if check_exists_by_xpath('//*[@id="c9"]') is True:
            self.find_xp('//*[@id="c9"]').click()
        time.sleep(4)
        try:
            self.driver.find_element(By.ID, "c7").click()
        except:
            pass
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('//*[@id="c36"]').click()
            'xpth://*[@id="c21"]'
            'selector #c21'
        except:
            pass
        time.sleep(3)
        try:
            self.find_xp('//*[@id="c9"]').click()
        except:
            pass
        time.sleep(1)
        # next
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#yDmH0d > c-wiz > c-wiz > div > div > div.HN8ojc.Gg5APe > '
                                                      'div.U26fgb.O0WRkf.oG5Srb.UxubU.C0oVfc.B580Hc.JvxUib.wTAsbd.M9Bg4d '
                                                      '> span > span').click()
        except:
            pass
        time.sleep(2)
        # phone call click
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").click()
        time.sleep(2)
        # phone call number
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(2) .whsOnd").send_keys(
            phone_num_make_numbers(self.p_num))
        time.sleep(2)
        # site
        self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(1) .whsOnd").click()
        time.sleep(1)
        # site
        # self.driver.find_element(By.CSS_SELECTOR, ".rFrNMe:nth-child(1) .whsOnd").send_keys(self.site)
        time.sleep(2)
        # next
        self.driver.find_element(By.CSS_SELECTOR, ".UxubU .RveJvd").click()
        # would u upadtes TODO

        # finish
        time.sleep(5)
        print(" ")
        self.driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/c-wiz/div/div/div[3]/div[1]/span/span').click()
        time.sleep(11)

        # chack for call btn
        # mail_txt_box = '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/c-wiz/div/div/div/div/div/div[1]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input'
        # if check_exists_by_xpath(mail_txt_box) is True:
        #    print("txtbox mail")
        #    self.driver.close()
        # else:
        #    print("call btn")


# split the pattarn of the phone numbers to flixebility with the site
def phone_num_make_numbers(phone_number):
    number_spliten = []
    x1 = phone_number.split(" ")
    x11 = x1[0].split("(")
    x3 = x11[1].split(")")
    cnum1 = x3[0]
    x2 = x1[1].split("-")
    cnum2 = (x2[0] + x2[1])
    number_spliten.append(cnum1)
    number_spliten.append(cnum2)
    return number_spliten


# browse file
def browse_files():
    global file, folder_path, file_full_path, file_name_without_end, file_new_name, file_new_name_and_path
    try:
        file_full_path = filedialog.askopenfilename(initialdir="/",
                                                    title="Select a File",
                                                    filetypes=(("csv files",
                                                                "*.csv"),
                                                               ("all files",
                                                                "*.*")))
    except:
        pass
    head_tail = os.path.split(file_full_path)
    folder_path = head_tail[0]
    file = head_tail[1]
    file_name_without_end = file.split(".")[0]
    ent1.insert(END, file_full_path)
    send_msg_to_tk("FILE: {0} ADDED\n".format(file_name_without_end))
    file_new_name = "{0}NEW{1}.csv".format(file_name_without_end, datetime.now().strftime("%m%d-%H%M"))
    file_new_name_and_path = folder_path + '/' + file_new_name
    send_msg_to_tk("Will save at FOLDER: {0} \nas: {1}\n if you choose google bot dont pay attantion\n"
                   .format(folder_path, file_new_name))


# browse multiple files for domains bot
def browse_multiple_files():
    global filez
    filez = filedialog.askopenfilenames(filetypes=(("xlsx files",
                                                    "*.xlsx"), ("csv files",
                                                                "*.csv"),
                                                   ("all files",
                                                    "*.*")), title='Choose a go daddy .xlsx files or csv')


# numberbarn function
def num_web(phone_num):
    global driver
    cnum = phone_num_make_numbers(phone_num)
    driver = webdriver.Chrome()
    driver.get("https://www.numberbarn.com/")
    num1 = driver.find_element_by_xpath('//*[@id="local-search"]/input[1]')
    num1.send_keys(cnum[0])
    num2 = driver.find_element_by_xpath('//*[@id="local-search"]/input[2]')
    num2.send_keys(cnum[1])
    go_btn = driver.find_element_by_xpath('//*[@id="local-search"]/input[3]')
    ActionChains(driver).click(go_btn).perform()
    ele = driver.find_element_by_xpath(
        '/html/body/app-root/app-public/app-search/section[1]/div[1]/pagination[2]/div/span')
    if len(ele.text) > 0:
        result = True
    else:
        result = False
    driver.close()
    return result


# remove blank sites BOT
def remove_blank_domains_and_phone():
    global file, folder_path, file_full_path, file_new_name, file_new_name_and_path
    try:
        with open(file_full_path, 'r') as inp, open(file_new_name_and_path, 'w', newline='') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                pnum = row[6]
                web = row[7]
                if len(web) > 0 and len(pnum) > 0:
                    writer.writerow(row)
                else:
                    pass
        send_msg_to_tk("BOT REMOVE BLANK DOMAINS DONE!\nNew File: {0} \nSaved IN: {1}\n".format(file_new_name,
                                                                                                folder_path))
    except Exception as e:
        send_msg_to_tk("error in REMOVE blank and domains bot:" + str(e) + "\n")


# using api of twillio
def twilio_number_chacker(phone_num_twilio):
    # create the format for twilio
    def phone_num_make_numbers_to_twilio(phone_number):
        number_splitten = []
        x1 = phone_number.split(" ")
        x11 = x1[0].split("(")
        x3 = x11[1].split(")")
        cnum1 = x3[0]
        x2 = x1[1].split("-")
        cnum2 = (x2[0] + x2[1])
        number_splitten.append(cnum1)
        number_splitten.append(cnum2)
        return number_splitten

    account_sid = 'AC75d990c870ef580f594da910d944697e'
    auth_token = 'e680c44933e9d178dea66038d9e7a6cf'
    client = Client(account_sid, auth_token)
    p = phone_num_make_numbers_to_twilio(phone_num_twilio)

    local = client.available_phone_numbers('US').local.list(
        area_code=p[0],
        contains=p[1])
    try:
        if len(local[0].friendly_name) > 0:
            return True
    except:
        return False
        pass


# number_barn BOT to do
def numbers_check():
    global file, folder_path, file_full_path, file_new_name, file_new_name_and_path
    try:
        with open(file_full_path, 'r') as inp, open(file_new_name_and_path, 'w', newline='') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                phone_num1 = row[6]
                if len(phone_num1) > 0:
                    try:
                        if num_web(phone_num1) is True:
                            writer.writerow(row)
                        else:
                            if twilio_number_chacker(phone_num1) is True:
                                writer.writerow(row)
                    except Exception as e:
                        send_msg_to_tk("error in numbers bot:" + str(e) + "\n")
        send_msg_to_tk("BOT numbers check DONE!\nNew File: {0}\nSaved AT: {1}\n".format(file_new_name, folder_path))
    except Exception as e:
        send_msg_to_tk("error in numbers bot:" + str(e) + "\n")


# google bot
def google_bot():
    with open(file_full_path, 'r') as inp:
        for row in csv.reader(inp):
            try:
                google(user_name=row[9], pass_word=row[10], recovery_mail=row[11], business_name=row[0], address=row[1],
                       city=row[2], state=row[3], zip_code=row[4], p_num=row[6], site=row[7], catagory=row[8])
                send_msg_to_tk("BOT google for {0} DONE!\n".format(row[9]))
            except Exception as e:
                send_msg_to_tk("Google Error:" + str(e) + '\n')


# Send massages to txt_box in UI
def send_msg_to_tk(string):
    txt.insert(END, str(string + '\n'))
    with open("log.txt", "a") as fd:
        fd.write(string + '\n')


#  Create the design of the program
def design():
    global ent1, btn1, lbl1, lbl2, txt, ent2, btn3, btn4, btn5, txt, btn2, btn6, btn7, window
    window = Tk()
    window.title('Bot Dashboard - godaddy-google-numburn-twillio-csv-xlxs -ByBar')
    window.geometry("900x780")
    window.resizable(True, True)

    #   choose file
    btn1 = Button(window, text="Browse file", command=browse_files, state='normal', width=10,
                  height=2,
                  font=('david', 15, 'bold'))
    btn1.place(x=450, y=30)
    lbl1 = Label(window, text="File:", font=('david', 15, 'bold'))
    lbl1.place(x=15, y=50)
    ent1 = Entry(window, width="37")
    ent1.place(x=70, y=50)

    # available numbers bot > to add bot
    btn3 = Button(window, text="Available number", command=numbers_check, state='normal',
                  width=15, height=1, fg='black', font=('david', 15, 'bold'))
    btn3.place(x=170, y=170)

    # excel remove webs >
    btn6 = Button(window, text="Remove empty web&phones", command=remove_blank_domains_and_phone, state='normal',
                  width=20, height=1, fg='black', font=('david', 15, 'bold'))
    btn6.place(x=350, y=170)

    # google business >
    btn7 = Button(window, text="Google bot", command=google_bot, state='normal',
                  width=12, height=1, fg='black', font=('david', 15, 'bold'))
    btn7.place(x=15, y=170)

    # start button
    btn4 = Button(window, text="Start", command=start, state='normal',
                  width=7, height=1, fg='green', font=('david', 15, 'bold'))
    btn4.place(x=15, y=250)

    # exit btn
    btn5 = Button(window, text="Exit", command=quit, state='normal', width=7, height=1,
                  fg='red', font=('david', 15, 'bold'))
    btn5.place(x=600, y=600)

    # log txt box
    txt = Text(window, font=('david', 15, 'bold'), width='52')
    txt.place(x=15, y=300)
    # domains bot
    btn2 = Button(window, text="GoDaddy Bot", command=go_daddy, state='normal', width=10, height=1,
                  fg='red', font=('david', 15, 'bold'))
    btn2.place(x=600, y=100)

    # choose files to create new xlxs files
    btn8 = Button(window, text="Browse multiple", command=browse_multiple_files, state='normal', width=15, height=1,
                  fg='red', font=('david', 15, 'bold'))
    btn8.place(x=600, y=200)
    # go daddy after file select btn
    btn9 = Button(window, text="Go daddy files(xlxs)", command=csv_from_xlxs_multi, state='normal', width=15,
                  height=1,
                  fg='red', font=('david', 15, 'bold'))
    btn9.place(x=600, y=300)
    # complete_rows_btn
    btn10 = Button(window, text="complete rows after multiple", command=complete_rows_btn, state='normal', width=20,
                   height=1,
                   fg='red', font=('david', 15, 'bold'))
    btn10.place(x=600, y=400)
    send_msg_to_tk("Click Start.\n")
    window.mainloop()


# RESTARTING THE PROGRAM
def start():
    global file, folder_path, file_full_path
    folder_path = None
    file = None
    file_full_path = None
    btn1.configure(state='normal')
    btn3.configure(state='normal')
    btn7.configure(state='normal')
    btn6.configure(state='normal')
    ent1.delete(0, END)
    send_msg_to_tk("NEW SESSION STARTED AT {0}\n"
                   .format(datetime.now().strftime("%d/%m/%Y %H:%M:")))


# function to return domain from the tables
def return_only_domain(site):
    return tldextract.extract(site).domain + "." + tldextract.extract(site).suffix


# godaddy bot to check free websites
def go_daddy():
    # godaddy bot
    global folder_path, file_name_without_end, file_full_path, file_new_name, file_new_name_and_path, download_names
    download_names = []

    # FOlder to move the new tables
    new_path = '{0}/{1}_split-to-500-{2}'.format(folder_path, file_name_without_end,
                                                 datetime.now().strftime("%d%m%Y%H%M"))
    os.mkdir(new_path)

    # insert to godaddy the domains and downloading the file from godaddy
    def go_daddy_run(file500pth):
        driver_go = webdriver.Chrome()
        driver_go.get('https://www.godaddy.com/domains/bulk-domain-search/')
        txt_xpath_domains = '//*[@id="txt-search"]'
        driver_go.find_element_by_xpath(txt_xpath_domains).click()
        with open(file500pth, 'r') as fd:
            for row in csv.reader(fd):
                driver_go.find_element_by_xpath(txt_xpath_domains).send_keys(row)
                driver_go.find_element_by_xpath(txt_xpath_domains).send_keys(Keys.ENTER)
        sum_btn_xpath = '//*[@id="btn-submit"]'
        driver_go.find_element_by_xpath(sum_btn_xpath).click()
        time.sleep(7)
        # export btn
        export_btn = '//*[@id="btn_export"]'
        driver_go.find_element_by_xpath(export_btn).click()
        time.sleep(1)
        # click on download link
        export_all_btn = '//*[@id="btn_export_all"]'
        driver_go.find_element_by_xpath(export_all_btn).click()
        # waiting to download file
        time.sleep(10)
        driver_go.close()

    def split_csv_to_500(filehandler, delimiter=',', row_limit=499,
                         output_name_template='500_%s.csv', output_path=new_path, keep_headers=True):
        # define the name of the directory to be created
        reader = csv.reader(filehandler, delimiter=delimiter)
        current_piece = 1
        current_out_path = os.path.join(
            output_path,
            output_name_template % current_piece
        )
        current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
        current_limit = row_limit
        if keep_headers:
            headers = next(reader)
            current_out_writer.writerow(headers)
        for i, row in enumerate(reader):
            if i + 1 > current_limit:
                current_piece += 1
                current_limit = row_limit * current_piece
                current_out_path = os.path.join(
                    output_path,
                    output_name_template % current_piece
                )
                current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
                if keep_headers:
                    current_out_writer.writerow(headers)
            current_out_writer.writerow(row)

    # filtering the file to new file with only domains
    file_new_name = "{0}-DomainsOnly-{1}.csv".format(file_name_without_end, datetime.now().strftime("%m%d-%H%M"))
    file_new_name_and_path = new_path + '/' + file_new_name
    with open(file_full_path, 'r') as inp, open(file_new_name_and_path, 'a', newline='') as out:
        for row in csv.reader(inp):
            domain = return_only_domain(row[13])
            out.write(domain)
            out.write("\n")
    send_msg_to_tk("Domains-only table created, now Splitting.... \n")

    # splitting the file to files with 500 rows
    split_csv_to_500(open(file_new_name_and_path, 'r'))

    # run over the 500 files in the new folder
    for filename_with_500 in os.listdir(new_path):
        if filename_with_500.startswith('500'):
            go_daddy_run(os.path.join(new_path, filename_with_500))
    send_msg_to_tk('GoDaddy bot done!, now pick the downloaded files from multiple browser to change them to csv.\n')


# command to btn to create the new files
# method to get go daddy files and create new files in direction with the values to fill
def csv_from_xlxs_multi():
    global filez, new_path_for_unfilled_csv
    head_tail = os.path.split(filez[0])
    folder_path_xlsx = head_tail[0]
    # FOlder to move the new tables
    new_path_for_unfilled_csv = '{0}/csv_with_unfilled_rows{1}'.format(folder_path_xlsx,
                                                                       datetime.now().strftime("%d%m%Y%H%M"))
    os.mkdir(new_path_for_unfilled_csv)
    for i in filez:
        csv_from_excel(i)
    send_msg_to_tk('Unfilled csv files saved on:{0}\n '
                   'Now choose the files and fill them by the btn complete rows\n'.format(new_path_for_unfilled_csv))


# method to get go daddy one file and create new file to direction with the values to fill
def csv_from_excel(xlxs_file):
    global new_path_for_unfilled_csv, new_path_for_the_file, file_name_xlsx_without_end, file_name_xlsx
    head_tail = os.path.split(xlxs_file)
    file_name_xlsx = head_tail[1]
    file_name_xlsx_without_end = file_name_xlsx.split(".")[0]
    new_path_for_the_file = '{0}/{1}.csv'.format(new_path_for_unfilled_csv, file_name_xlsx_without_end)

    try:
        wb = xlrd.open_workbook(xlxs_file)
        sh = wb.sheet_by_name('all')
        your_csv_file = open(new_path_for_the_file, 'w', newline='')
        wr = csv.writer(your_csv_file)
        for row_num in range(sh.nrows):
            wr.writerow(sh.row_values(row_num))
        your_csv_file.close()
    except:
        pass
    send_msg_to_tk('Xlxs to csv done for:{0}\n'.format(xlxs_file))


# take two cvs files and fill by the domain
def csv_complete_rows(cvs_file_with_only_domains, full_cvs_file_to_compare):
    global new_path_for_unfilled_csv
    new_path_for_unfilled_csv = os.path.split(cvs_file_with_only_domains)[0]
    file_with_all_rows_filled = '{0}/done!.csv'.format(new_path_for_unfilled_csv)
    list_domains = []
    with open(cvs_file_with_only_domains, 'r') as inp1, open(full_cvs_file_to_compare, 'r') as inp2, \
            open(file_with_all_rows_filled, 'a', newline='') as out:
        writer = csv.writer(out)
        for row1 in csv.reader(inp1):
            list_domains.append(row1[0])
        i = 0
        for row2 in csv.reader(inp2):
            domain = row2[7]
            if return_only_domain(domain) == list_domains[i]:
                writer.writerow(row2)
                i = i + 1
                if i == len(list_domains):
                    i = 0


# command to btn to create the new files to
def complete_rows_btn():
    global filez, new_path_for_unfilled_csv
    fulled_file_to_compare = filedialog.askopenfilename(initialdir="/",
                                                        title="Select a csv fulled File",
                                                        filetypes=(("csv files",
                                                                    "*.csv"),
                                                                   ("all files",
                                                                    "*.*")))
    for i in filez:
        csv_complete_rows(i, fulled_file_to_compare)
    send_msg_to_tk('Complete bot done!.csv new file done! at:\n{0}'.format(new_path_for_unfilled_csv))


design()
