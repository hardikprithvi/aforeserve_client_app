# todo
# working but need to be checked and improved
import sys
from requests import get
import pyautogui
import pywinauto
import time
from pywinauto.controls.win32_controls import ButtonWrapper
from pywinauto.keyboard import send_keys, KeySequenceError
import config
import configparser
import tkinter, tkinter.messagebox
def MessageBox(title, text):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title, text)
    root.destroy()
    
config1 = configparser.ConfigParser()
config1.read('config_test.ini')
try:
    config_data = get(config1['DEFAULT']['URL'] + '/configdata',verify = False)
except:
    print("server not working")
    MessageBox("Warning","Not able to communicate with server")
    sys.exit()
config_data = config_data.json()
# print(config_data)
flag=0
if config_data["smtp_auth"] == "True":
    smtp_auth = True
else:
    smtp_auth = False
incoming_server_port = config_data["incoming_server_port"]
outgoing_server_port = config_data["outgoing_server_port"]
type_of_encrypted_connection = config_data["type_of_encrypted_connection"]
if config_data["requires_SSL_connection"] == "True":
    requires_SSL_connection = True
else:
    requires_SSL_connection = False
    
    
def mailConfig(username,inser,outser,email_ss,password_s):
    try:
        global flag
        
        config.logger.info('opening control panel for email configuration ')
        control_panel=pywinauto.Application(backend='uia').start(r'C:\Windows\System32\control.exe',timeout=50)
                
        time.sleep(2)
        
        pyautogui.hotkey('win','up')
        
        #time.sleep(2)
        
        window=None
        
        def checkForWindowExistence(window_title):
            
            print(window_title)
            global window
            #print('WINDOW IS ',window)
            config.logger.info('Searching for '+str(window_title)+' via infinite loop')
            cnt=0
            while True:
                print('In Loop part')
                if(cnt==200):
                    return 1/0
                cnt+=1
                try:
                    window=pywinauto.findwindows.find_windows(best_match=window_title)
                except:
                    window=None
                if window:
                    break
            print('Out of Loop part',window)
            ""
            return window
        
        try:  
            config.logger.info('Searching for All Control Panel Items window')
            control_panel_window=pywinauto.findwindows.find_windows(best_match=u'All Control Panel Items')
        except:
            control_panel_window=checkForWindowExistence(u'All Control Panel Items')
        print(control_panel_window)
        
        if control_panel_window:
            
            mail=control_panel.window_(handle=control_panel_window[0])
            
            mail.set_focus()
            try:
                
                mail.child_window(title="Category").click()
                time.sleep(2)
                pyautogui.press('down',presses=2)
                pyautogui.press('enter')
                
            except Exception as e:
                
                pass
                #print(e)
                
            #click mail icon on control panel   
            try:
                config.logger.info('Searching for Mail (Microsoft Outlook 2016) icon')
                mail.child_window(title="Mail").wait('visible', timeout=3, retry_interval=0.5).click_input()
                print('Code in try block')
            except Exception as e:
                config.logger.info('Searching for Mail icon')
                try:
                    mail.child_window(title="Mail (Outlook 2016)", auto_id="name").wait('visible', timeout=3, retry_interval=0.5).click_input()
                    print('Code in except block')
                except  Exception as e:
                    mail.child_window(title="Mail (Microsoft Outlook 2016)", auto_id="name").wait('visible', timeout=3, retry_interval=0.5).click_input()
                    print('Code in except block')
                time.sleep(2)
            mail_setup_outlook_found=False
            mail_setup_outlook = True
            try:
                
                config.logger.info('Searching for Mail Setup - Outlook window')
                mail_setup_outlook=pywinauto.findwindows.find_windows(best_match='Mail Setup - Outlook')
                mail_setup_outlook_found = True
            except:
                try:
                    mail_setup_outlook=checkForWindowExistence(u'Mail Setup - Outlook')
                    mail_setup_outlook_found = True
                except:
                    try:
                        mail_setup_outlook=checkForWindowExistence(u'Mail Setup - AFS')
                        mail_setup_outlook_found = True
                    except:
                        mail_setup_new =pywinauto.findwindows.find_windows(best_match='Mail')
                        mail_setup_new=control_panel.window_(handle=mail_setup_new[0])
                        mail_setup_new.set_focus()
                        
                        config.logger.info('Searching for Add... Button')
                        mail_setup_new.child_window(title_re="Add...",control_type="Button").wait('visible', timeout=2, retry_interval=0.5).click()
                        try:
                            config.logger.info('Searching for Mail Setup - New Profile window')
                            new_profile = pywinauto.findwindows.find_windows(best_match='New Profile')
                        except:
                            new_profile = checkForWindowExistence(u'New Profile')
                        new_profile = control_panel.window_(handle=new_profile[0])
                        new_profile.set_focus()
                        new_profile.child_window(title='Profile Name:', control_type='Edit').type_keys('Outlook')
                        pyautogui.press('enter')
                    

                    
            
            if mail_setup_outlook:
                        if(mail_setup_outlook_found):
                            mail_setup_outlook=control_panel.window_(handle=mail_setup_outlook[0])
                            mail_setup_outlook.set_focus()
                            #mail_setup_outlook.
                            #mail_setup_outlook.child_window(title_re="Email Accounts",control_type="Button").click()
                            #print(mail_setup_outlook)
                            try:
                                config.logger.info('Searching for E-mail Accounts button')
                                mail_setup_outlook.child_window(title_re="Email Accounts...",control_type="Button").wait('visible', timeout=2, retry_interval=0.5).click()
                            except:
                                mail_setup_outlook.child_window(title_re="E-mail Accounts...",control_type="Button").wait('visible', timeout=10, retry_interval=0.5).click()
                                
                            time.sleep(2)
                            
                            try:
                                config.logger.info('Searching for Account Settings window')
                                print("in try account settings")
                                account_settings=pywinauto.findwindows.find_windows(best_match ='Account Settings')
                            except:
                                print("in except account settings")
                                account_settings=checkForWindowExistence(u'Account Settings')
                                print("settings window:",account_settings)
                            if account_settings:
                                account_settings=control_panel.window_(handle=account_settings[0])
                                account_settings.set_focus()
                                #try:
                                config.logger.info('Clicking on Email and New button in Account Settings window')
                                    #account_settings.child_window(title="Email").wait('visible', timeout=120, retry_interval=0.5).click_input()
                                account_settings.child_window(title="New...", control_type="Button").wait('visible', timeout=120, retry_interval=0.5).click()
                                #print('In try')
                                #except:
                                #   account_settings.child_window(title="New...", control_type="Button").wait('visible', timeout=120, retry_interval=0.5).click()
                                    #print('In Except')
                                
                                
                                #time.sleep(2)
                        try:
                                    config.logger.info('Searching for Add Account window for clicking on Manual Setup radio button')
                                    add_account=pywinauto.findwindows.find_windows(best_match='Add Account')
                        except:
                                    add_account=checkForWindowExistence(u'Add Account')
                            
                        if add_account:
                                add_account=control_panel.window_(handle=add_account[0])
                                add_account.set_focus()
                                try:
                                    add_account.child_window(title="Manual setup or additional server types",control_type="RadioButton").wait('visible', timeout=2, retry_interval=0.5).click()
                                except:
                                    add_account.child_window(title="Manually configure server settings or additional server types",control_type="RadioButton").wait('visible', timeout=5, retry_interval=0.5).click()
                                add_account.child_window(title="Next >",control_type="Button").wait('visible', timeout=120, retry_interval=0.5).click()
                                
                                #time.sleep(2)
                                
                                try:
                                    config.logger.info('Searching for Add Account window for clicking on POP or IMAP radio button')
                                    add_account=pywinauto.findwindows.find_windows(best_match='Add Account')
                                
                                except:
                                    add_account=checkForWindowExistence(u'Add Account')
                                
                                if add_account:
                                    add_account=control_panel.window_(handle=add_account[0])
                                    add_account.set_focus()
                                    try:
                                        add_account.child_window(title="POP or IMAP",control_type="RadioButton").wait('visible', timeout=2, retry_interval=0.5).click()
                                    except:
                                        add_account.child_window(title="Internet E-mail",control_type="RadioButton").wait('visible', timeout=2, retry_interval=0.5).click()
                                    add_account.child_window(title="Next >",control_type="Button").wait('visible', timeout=120, retry_interval=0.5).click()
                                    
                                    
                                    #time.sleep(2)
                                    
                                    try:
                                        config.logger.info('Searching for Add Account window for entering user details recevied via chatbot')
                                        add_account=pywinauto.findwindows.find_windows(best_match='Add Account')
                                    
                                    except:
                                        add_account=checkForWindowExistence(u'Add Account')
                                        
                                    if add_account:
                                        add_account=control_panel.window_(handle=add_account[0])
                                        add_account.set_focus()
                                        
                                        
                                        #user_details=pd.read_csv('http://127.0.0.1:8000/input.csv').columns
                                        
                                        user_details=[username,inser,outser,email_ss,password_s]
                                        
                                        add_account["Your Name:Edit"].type_keys(user_details[0])    
                                        
                                        add_account["Email Address:Edit"].type_keys(user_details[3])
                                        
                                        add_account["Incoming mail server:Edit"].type_keys(inser)
                                        
                                        add_account["Outgoing mail server (SMTP):Edit"].type_keys(outser)
                                        
                                        add_account["User Name:Edit"].type_keys('^a{BACKSPACE}')
                                        #add_account["User Name:Edit"].Edit.set_edit_text(u'')
                                        
                                        add_account["Password:Edit"].type_keys(user_details[4])
                                        
                                        add_account["User Name:Edit"].type_keys(user_details[3])
                                        
                                        add_account.child_window(title="More Settings ...").wait('visible', timeout=120, retry_interval=0.5).click()
                                        
                                        #time.sleep(2)
                                        
                                        try:
                                            config.logger.info('Searching for Internet Email Settings for entering Incoming and Outgoing port details')
                                            internet_email_settings=pywinauto.findwindows.find_windows(best_match='Internet Email Settings')
                                        
                                        except:
                                            internet_email_settings=checkForWindowExistence(u'Internet Email Settings')
                                        
                                        if internet_email_settings:
                                            
                                            internet_email_settings=control_panel.window_(handle=internet_email_settings[0])
                                            
                                            internet_email_settings.set_focus()
                                        
                                            internet_email_settings.child_window(title="Outgoing Server").wait('visible', timeout=120, retry_interval=0.5).click_input()
                                            
                                            #send_keys('some text{TAB 2}')
                                            #send_keys('some text{SPACE}')
                                            if(smtp_auth):
                                                #internet_email_settings.child_window(title="My outgoing server (SMTP) requires authentication",control_type="RadioButton").wait('visible', timeout=120, retry_interval=0.5).click()
                                                send_keys('some text{TAB 2}')
                                                send_keys('some text{SPACE}')
                                            internet_email_settings.child_window(title="Advanced").wait('visible', timeout=120, retry_interval=0.5).click_input()
                                            
                                            internet_email_settings.child_window(title="Incoming server (POP3):",control_type="Edit").type_keys('^a{BACKSPACE}')
                                            
                                            internet_email_settings.child_window(title="Incoming server (POP3):",control_type="Edit").type_keys(incoming_server_port)
                                            if(requires_SSL_connection):

                                                pyautogui.press('tab')
                                                pyautogui.press('tab')
                                                pyautogui.press('space')
                                    
                                            internet_email_settings.child_window(title="Outgoing server (SMTP):",control_type="Edit").type_keys('^a{BACKSPACE}')
                                            
                                            internet_email_settings.child_window(title="Outgoing server (SMTP):",control_type="Edit").type_keys(outgoing_server_port)
                                            
                                        
                                            
        
                                            try:
                                                internet_email_settings.child_window(title="Use the following type of encrypted connection:",control_type="ComboBox").select(type_of_encrypted_connection)
                                            
                                            except:
                                                pass
                                            
                                            
                                            #pyautogui.press('enter')
                                            internet_email_settings.child_window(title="OK",control_type="Button").wait('visible', timeout=120, retry_interval=0.5).click()
                                            
                                            add_account.child_window(title="Next >",control_type="Button").wait('visible', timeout=120, retry_interval=0.5).click()
    
                                            
                                            time.sleep(2)
                                            test_account=pywinauto.findwindows.find_windows(best_match='Test Account Settings')
                                            test_account=control_panel.window_(handle=test_account[0])
                                            test_account.set_focus()
                                            while(True):
                                                try:
                                                    test_account.child_window(title='Close',control_type="Button").wait('visible',timeout=5, retry_interval=0.5).click()
                                                    break
                                                except:
                                                    try:
                                                        try:
                                                            print('test1')
                                                            invalid_password = pywinauto.findwindows.find_windows(title ='Internet Email - '+str(user_details[3]))
                                                            invalid_password=control_panel.window_(handle=invalid_password[0])
                                                        except:
                                                            print('in except')
                                                            invalid_password = pywinauto.findwindows.find_windows(title ='Internet E-mail - '+str(user_details[3]))
                                                            invalid_password=control_panel.window_(handle=invalid_password[0])
                                                        print('test2')
                                                        invalid_password.set_focus()
                                                        print(invalid_password)
                                                        if invalid_password:
                                                                send_keys('"%{F4}"')
                                                            
                                                                send_keys('"%{F4}"')
                                                                
                                                                send_keys('"%{F4}"')
                                                            
                                                                send_keys('"%{F4}"')
                                                            # time.sleep(1)
                                                                send_keys('"%{F4}"')
                                                            # time.sleep(1)
                                                                send_keys('"%{F4}"')
                                                            # time.sleep(1)
                                                                send_keys('"%{F4}"')
                                                            # time.sleep(1)
                                                                send_keys('"%{F4}"')

                                                                return ("Invalid Credentials")
                                                    except:
                                                        print("Both windows not found")

                                            #time.sleep(2)
                                            add_account.child_window(title="Finish", control_type="Button").click()
                                            #time.sleep(2)
                                            #add_account.child_window(title="Cancel", control_type="Button").click()
                                            #time.sleep(2)
                                            
                                            #account_settings.child_window(t"itle='Close',control_type="Button").wait('visible',timeout=120, retry_interval=0.5).click()
                                            #account_settings.child_window(title="Close", control_type="Button").click()
                                            send_keys('"%{F4}"')
                                            
                                            time.sleep(2)
                                            send_keys('"%{F4}"')
                                            #mail_setup_outlook.child_window(title="Close", control_type="Button").click()
                                            
                                            time.sleep(2)
                                            send_keys('"%{F4}"')
                                            
                                            flag=1
        
        
        return "Success"
    except Exception as e:
        print(str(e))
        return "Failed"

# val = mailConfig('hardik','outlook.office365.com','smtp.office365.com','sunny.singh@algo8.ai',"SS@algo8")
# print(val)
