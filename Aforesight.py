from flaskwebgui import FlaskUI  # get the FlaskUI class
from requests import get
from requests.packages import urllib3
# import requests
from flask import Flask, request, render_template, jsonify
import socket
from getmac import get_mac_address
from platform import platform, system, release
from getpass import getuser
import uuid
import os.path

import config
# for windows 10
import Printer_Latest_Remove_Latency_win10
import test_fetch_mail_win10
import diskCleanup
import json
# for windows 8
import Printer_Latest_Remove_Latency_for_8
import test_fetch_mail_for_8
import sys
# for windows 7
import Printer_Latest_Remove_Latency_for_7
import test_fetch_mail_for_7
import configparser

# for software installation
import install_automate
import tkinter, tkinter.messagebox
def MessageBox(title, text):
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title, text)
    root.destroy()
        
    
# os.environ['PYTHONWARNINGS']="ignore:Unverified HTTPS request"
urllib3.disable_warnings()
def run():
    config.logger.info('App starts running')
    
    config1 = configparser.ConfigParser()
    config1.read('config_test.ini')
    url_fg = config1['DEFAULT']['URL']
    logo_fg = config1['DEFAULT']['logo']
    config1 = dict()
    config1['DEFAULT']=dict()

    config1['DEFAULT']['URL'] = url_fg
    config1['DEFAULT']['logo'] = logo_fg
    try:
        config_data = get(config1['DEFAULT']['URL'] + '/configdata',verify=False)
    except:
        print("server not working.")
        MessageBox("Warning","Server not responding.")
        sys.exit()
    config_data = config_data.json()
    config1['DEFAULT']['Incoming Server'] = config_data['inserver']
    config1['DEFAULT']['Outgoing Server'] = config_data['outserver']
    config1['DEFAULT']['it policy url'] = config_data['policy_url']
    config1["DEFAULT"]["IT helpdesk"] = config_data['it_help']
    config1["DEFAULT"]["myhostname"] = config_data['myhostname']
    config1["DEFAULT"]["myusername"] = config_data['myusername']
    config1["DEFAULT"]["pem_file"] = config_data['pem_file']
    config1["DEFAULT"]["software_password"] = config_data['software_password']
    config1["DEFAULT"]["software upload link"] = config_data['software upload link']
    # file1 = open('software_afs.pem','w')
    with open('software_afs.pem','w') as file1:
        file1.write(config1["DEFAULT"]["pem_file"])
    file1.close()
    
    # creating new id
    config.logger.info("New id not required: "+str(os.path.isfile('static/ids.txt')))
    if(os.path.isfile('static/ids.txt')):
        global ids
        ids = open('static/ids.txt')
        ids = ids.read()
        ids = ids.replace('\n', '')
        all_id = get(config1['DEFAULT']['URL']+'/getalluniqueid',verify = False)
        all_id = all_id.json()
        all_id = all_id['MAC_ID']
        flag = 0
        for i in range(0, len(all_id)):
            if str(ids) == all_id[str(i)]:
                flag += 1
        if flag > 0:
            config.logger.info('Id found')
            pass
        else:
            token = True
            while token:
                config.logger.info('Id Not found generating new id')
                ids = uuid.uuid1()
                ids = str(ids)
                ids = ids.replace('-', '')
                all_id = get(config1['DEFAULT']['URL']+'/getalluniqueid',verify=False)
                all_id = all_id.json()
                all_id = all_id['MAC_ID']
                flag = 0
                for i in range(0, len(all_id)):
                    if ids == all_id[str(i)]:
                        flag += 1
                    else:
                        pass
                if flag == 0:
                    config.logger.info('Writing new id in static file')
                    with open('static/ids.txt', 'w') as file:
                        file.write(str(ids))
                    url = config1['DEFAULT']['URL']+'/userdetails/new/1/1/' + \
                        str(ids)+'/1/1/1/'+config1['DEFAULT']['Incoming Server']+'/'+config1['DEFAULT']['Outgoing Server']+'/1/1'
                    res = get(url,verify = False)
                    token = False
    else:
        token = True
        while token:
            ids = uuid.uuid1()
            ids = str(ids)
            ids = ids.replace('-', '')
            all_id = get(config1['DEFAULT']['URL']+'/getalluniqueid',verify=False)
            all_id = all_id.json()
            all_id = all_id['MAC_ID']
            flag = 0
            for i in range(0, len(all_id)):
                if ids == all_id[str(i)]:
                    flag += 1
                else:
                    config.logger.info('Id found')
                    pass
            if flag == 0:
                config.logger.info('writing new id in static ')
                with open('static/ids.txt', 'w') as file:
                    file.write(str(ids))
                url = config1['DEFAULT']['URL']+'/userdetails/new/1/1/' + \
                        str(ids)+'/1/1/1/'+config1['DEFAULT']['Incoming Server']+'/'+config1['DEFAULT']['Outgoing Server']+'/1/1'
                res = get(url,verify=False)
                token = False
    
    rel = release()
    
    app = Flask(__name__)
    if FlaskUI.find_chrome_win('self') != None:
        ui = FlaskUI(app,width = 436, height = 610)
    else:
        ui = FlaskUI(app,browser_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",width = 436, height = 580)
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    # macid = get_mac_address()
    OS_v = platform()
    username = getuser()
    sernum = '12345'
    lap_desk = 'desk'
    config.logger.info('Starting up GUI ')
    # url = config1['DEFAULT']['URL']+'/inoutserver/'+str(ids)
    config.logger.info('Getting user information ')
    print('------------')
    # print(url)
    # res = get(url,verify = False)
    # res = res.json()
    config.logger.info('Get request successfull')
    inser, outser = config1['DEFAULT']['Incoming Server'], config1['DEFAULT']['Outgoing Server']
    dprint = '2'
    
    # creating new user
    # storing tid
    def storetid(t):
        global tid
        tid = t
        return tid
    
    url = config1['DEFAULT']['URL']+'/userdetails/old/'+hostname+'/'+IP+'/' + \
        str(ids)+'/'+sernum+'/'+OS_v+'/'+lap_desk + \
        '/'+inser+'/'+outser+'/'+dprint+'/'+username
    config.logger.info('Setting up inserver and outserver for user')
    s1=get(url,verify = False)
    config.logger.info('Request returned'+s1.text)
    def logging_sync():
        line_num = 0
        if(os.path.isfile('static/logger.txt')):
            f1 = open('static/logger.txt')
            line_num = f1.read()
            line_num = line_num.replace('\n', '')
            line_num = int(line_num)
        else:
            with open('static/logger.txt', 'w') as file:
                file.write(str(line_num))
        try:
            file1 = open('script.log','r')
            Lines = file1.readlines()
            cnt=0
            s = ''
            for line in Lines[line_num:]:
                cnt+=1
                s += line
                s += '\n'
            d = dict()
            d['logs_new'] = s
            check = get(config1['DEFAULT']['URL'] + '/synclogs/'+str(ids), data = json.dumps(d),verify = False)
            with open('static/logger.txt', 'w') as file:
                file.write(str(line_num + cnt))
        except Exception as e:
            return
    logging_sync()
    @app.route('/feedback',methods=['GET','POST'])
    def feedback():
        config.logger.info('Feedback route called ')
        feed = request.args.get('con1')
        feed = feed.replace(' ','_')
        url = config1['DEFAULT']['URL']+'/feedback/'+feed+'/'+str(tid)+'/'+str(ids)
        res = get(url,verify = False)
        config.logger.info('Feedback request returned '+res.text)
        return res.text
    
    @app.route('/emailadd',methods=['GET','POST'])
    def emailadd():
        config.logger.info('Email add route called ')
        feed = request.args.get('em')
        feed = feed.replace(' ','_')
        url = config1['DEFAULT']['URL']+'/emailadd/'+feed+'/'+str(ids)
        config.logger.info('Email routed on server hitting')
        res = get(url,verify = False)
        config.logger.info('Request returned '+ res.text)
        config.logger.info('Email added successfully ')
        return "hello"
    
    @app.route('/itpolicies', methods=['GET', 'POST'])
    def itpolicies():
        config.logger.info('Called IT policies route ')
        return '''
                <p class="speech-bubble btn-primary" style="height: 20%;">
                                    Please open the following link in a new tab to know about our IT policies<br>
                                    <br><h1 style="color:white;"><a target="_blank" href = "''' + str(config1['DEFAULT']['it policy url']) + '''"> IT POLICIES</a>
                                    <br>
                                                            
            </p>
                '''
    @app.route('/helpdesk', methods=['GET', 'POST'])
    def helpdesk():
        config.logger.info('Called HelpDesk route ')
        return'''
                <p class="speech-bubble btn-primary" style="padding-right:3%;height: 20%;">
                    You can contact IT Helpdesk on '''+config1["DEFAULT"]["IT helpdesk"]+''' from 10am-5pm.
                </p>
                '''
    
    @app.route('/', methods=['GET', 'POST'])
    def login():
        config.logger.info('Setting up screen for GUI')
        return render_template('index.html', User=username.title(), img = config1["DEFAULT"]['logo'])
    
    @app.route('/pr', methods=['GET', 'POST'])
    def pr():
        config.logger.info('Printer setup route called')
        manufac_name = request.args.get('manuname')
        mdelname = request.args.get('model')
        printer_ip = request.args.get('printer_ip')
        url = config1['DEFAULT']['URL']+'/newt/Printer_to_be_configured/Printer_to_be_configured/' + \
            str(ids)
        config.logger.info('Get request for Printer configuration')
        res = get(url,verify = False)
        if res:
            config.logger.info('Request returned '+ res.text)
            storetid(res.text)
            if rel == '8.1':
                config.logger.info('Script for windows-8 called')
                out = Printer_Latest_Remove_Latency_for_8.printerConfig(
                    manufac_name, mdelname,printer_ip)
                # out = 'success'
                if out == 'Success':
                    config.logger.info('Automation completed Successfully ')
                    url = config1['DEFAULT']['URL']+'/upt/'+res.text+'/'+str(ids)
                    res1 = get(url,verify = False)
                    config.logger.info('Request returned '+ res.text)
                    return '''
                <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
                else:
                    #Assing to department
                    config.logger.info('Automation failed ')
                    url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                    config.logger.info('Get request to assign')
                    res = get(url,verify = False)
                    config.logger.info('Request returned is ' + res.text)
                    return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
            elif rel == '7':
                config.logger.info('Script for windows 7 called ')
                out = Printer_Latest_Remove_Latency_for_7.printerConfig(
                    manufac_name, mdelname,printer_ip)
                if out == 'Success':
                    config.logger.info('Automation Successful ')
                    url = config1['DEFAULT']['URL']+'/upt/'+res.text+'/'+str(ids)
                    config.logger.ingo('Get request to upload feedback')
                    res = get(url,verify = False)
                    config.logger.info('Request returned is ' + res.text)
                    return '''
                
                <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
                else:
                    #Assing to department
                    config.logger.info('Automation Failed ')
                    url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is ' + res.text)
                    return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
                    
            else:
                config.logger.info('Script Called for windows 7')
                
                print(printer_ip)
                out = Printer_Latest_Remove_Latency_win10.printerConfig(
                    manufac_name, mdelname,printer_ip)
                print(out)
                # out = 'Fail'
                if out == 'Success':
                    config.logger.info('Automation Successful ')
                    url = config1['DEFAULT']['URL']+'/upt/'+res.text+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    return '''
                <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
                else:
                    #Assing to department
                    config.logger.info('Automation failed ')
                    url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
        else:
             return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Could not connect to ITSM Tool.
                    </p>'''
    
    
    @app.route('/emailconfig', methods=['GET', 'POST'])
    def em():
        config.logger.info('Enail configuration called ')
        username = request.args.get('username')
        email_ss = request.args.get('email_s')
        password_s = request.args.get('password_s')
        url = config1['DEFAULT']['URL']+'/newt/Email_to_be_configured/Email_to_be_configured/' + \
            str(ids)
        config.logger.info('Get request for email tp be configured')
        res = get(url,verify = False)
        if res:
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Routed for email to server')
            storetid(res.text)
            if rel == '8.1':
                config.logger.info('Email Script for windows 8.1 called!!')
                out = test_fetch_mail_win10.mailConfig(
                    username, inser, outser, email_ss, password_s)
                if out == 'Success':
                    config.logger.info('Automation Successfull, email configured')
                    url = config1['DEFAULT']['URL']+'/upt/'+str(res.text)+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    return '''
                <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
                else:
                    #Assing to department
                    config.logger.info('Automation failed, assigning to department')
                    rurl = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
            elif rel == '7':
                config.logger.info('Email Script for windows 7 called')
                out = test_fetch_mail_win10.mailConfig(
                    username, inser, outser, email_ss, password_s)
                if out == 'Success':
                    config.logger.info('Automation Successfull, email configured')
                    url = config1['DEFAULT']['URL']+'/upt/'+res.text+'/'+str(ids)
                    return '''
                <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback" required>
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
                else:
                    config.logger.info('Automation failed, assigning to expert')
                    #Assing to department
                    url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
            else:
                config.logger.info('Email Script for windows 10 called')
                out = test_fetch_mail_win10.mailConfig(
                    username, inser, outser, email_ss, password_s)
                # out = 'success'
                print(out)
                if out == 'Success':
                    config.logger.info('Automation Successfull, email configured')
                    url = config1['DEFAULT']['URL']+'/upt/'+str(tid)+'/'+str(ids)
                    # print(url)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    # print(res.text)
                    return '''
                <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback" required>
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
                else:
                    config.logger.info('Automation failed, assigning to expert')
                    #Assing to department
                    url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                    res = get(url,verify = False)
                    config.logger.info('Request returned is '+ res.text)
                    return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
        else: 
            return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Could not connect to ITSM server
                                                           
                    </p>'''
    

    @app.route('/diskclean', methods=['GET', 'POST'])
    def dc():
        config.logger.info('Routed for Disk Cleanup Script')
        url = config1['DEFAULT']['URL']+'/newt/Disk_full_disk_clean_to_be_configured/disk_full_disk_clean_to_be_configured/' + \
            str(ids)
        res = get(url,verify = False)
        if res:
            storetid(res.text)
            config.logger.info('Disk Cleanup Started')
            out = diskCleanup.startCleanup()
            if out == 'Success':
                config.logger.info('Disk Cleanup Successfull !!')
                url = config1['DEFAULT']['URL']+'/upt/'+ res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                        Automation Done Successfully
                                                           
                    </p>
                    <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                    Please Give Feedback
                                    <br>
                                    <br>
                                            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
                                    <br>
                                            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
                    '''
            else:
                #Assing to department
                config.logger.info('DIsk Cleanup Failed, assigned to expert !!')
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Automation Failed Due to unknown Issue!!! ''' + res.text + '''
                                                           
                    </p>'''
        else:
                return '''<p class="speech-bubble btn-primary" style="height: 20%;padding-right: 3%;">
                        Could not connect to ITSM Server.
                                                           
                    </p>'''
    
    # @app.route('/sft', methods=['GET', 'POST'])
    # def sft():
    #     config.logger.info('Routed for software')
    #     return 'Yet to implement'
    
    # flow start for new request
    
    
    @app.route('/newrequest', methods=['GET', 'POST'])
    def newreq():
        config.logger.info('Routed to new request function')
        return '''
        <p class="speech-bubble btn-primary" style="height: 25%;">
            Please verify the below details to continue with Aforesight
           <br>
           <br>
            Your IP : '''+str(IP)+'''
           <br>
           Your Username : '''+str(username.title())+'''
           </p>
        <p class="speech-bubble btn-primary" style="height: 30%;padding-right: 3%;">
        <br>
                                Please enter your email
                                <br>
                                <br>
                                        <input type="email" id="user_email" class="form-control" placeholder="Email" required>
                                                      
        </p>
        '''
        
    @app.route('/confirmnew', methods=['GET', 'POST'])
    def connew():
        config.logger.info('Routed to confirm function')
        arg = request.args.get('con1')
        if arg == 'confirm':
            config.logger.info('Routed to menu of available services')
            return '''
        <p class="speech-bubble btn-primary" style="height: 75%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="sft2install()">Software Installation</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="sysrelated()">System Related</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="apprelated()">Application Related</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="osrelated()">OS Related</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="printerrelated()">Printer Related</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="networkrelated()">Network Related</button>
                                                
        </p>
        '''
        # elif arg == 'proceed':
        elif arg == 'sftcon':
            config.logger.info('Routed to software install page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 55%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="msoffice()">MS Office</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="adobe()">Adobe Reader</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="java()">Java </button>
                                <br>
                                        <button class="btn btn-secondary" onclick="otherssft()">Others</button>
                                                
        </p>
            '''
        elif arg == 'msoffice':
            config.logger.info('Routed to MS Office Page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 50%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="msoffice_10_32()">MS Office 10 32bit</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="msoffice_13_32()">MS Office 13 32bit</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="msoffice_13_64()">MS Office 13 64bit </button>
                                <br>
                                                
        </p>
            '''
        elif arg == 'msoffice_10_32':
            config.logger.info('Routed to MS Office 10 32b installation page')
            url = config1['DEFAULT']['URL']+'/newt/MS_office_10_32_installation/MS_office_10_32_installation/' + str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Contacting server for MS_office_10_32 installation')
            storetid(res.text)
            out = install_automate.software_fetch("msoffice_10_32",config1["DEFAULT"]["myhostname"],config1["DEFAULT"]["myusername"],config1["DEFAULT"]["software upload link"],config1["DEFAULT"]["pem_file"],config1["DEFAULT"]["software_password"])
            # out = "success"
            if out == "success":
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Download Complete.
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Download Failed. ''' + res.text + '''
                                                       
                </p>'''
        elif arg == 'msoffice_10_32_install':
            out = install_automate.software_install("msoffice_10_32")
            if out == "success":
                url = config1['DEFAULT']['URL']+'/upt/'+ tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Automation Done Successfully
                                                               
            </p>
            <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
            Please Give Feedback
            <br>
            <br>
            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
            <br>
            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Installation Failed. ''' + res.text + '''
                                                       
                </p>'''
            
        elif arg == 'msoffice_13_32':
            config.logger.info('Routed to MS Office 13 32b installation page')
            url = config1['DEFAULT']['URL']+'/newt/MS_office_13_32_installation/MS_office_13_32_installation/' + str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Contacting server for MS_office_10_32 installation')
            storetid(res.text)
            out = install_automate.software_fetch("msoffice_13_32",config1["DEFAULT"]["myhostname"],config1["DEFAULT"]["myusername"],config1["DEFAULT"]["software upload link"],config1["DEFAULT"]["pem_file"],config1["DEFAULT"]["software_password"])
            # out = "success"
            if out == "success":
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Download Complete.
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Download Failed. ''' + res.text + '''
                                                       
                </p>'''
        elif arg == 'msoffice_13_32_install':
            out = install_automate.software_install("msoffice_13_32")
            if out == "success":
                url = config1['DEFAULT']['URL']+'/upt/'+ tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Automation Done Successfully
                                                               
            </p>
            <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
            Please Give Feedback
            <br>
            <br>
            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
            <br>
            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Installation Failed. ''' + res.text + '''
                                                       
                </p>'''
            
        elif arg == 'msoffice_13_64':
            config.logger.info('Routed to MS Office 13 64b installation page')
            url = config1['DEFAULT']['URL']+'/newt/MS_office_13_64_installation/MS_office_13_64_installation/' + str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Contacting server for MS_office_10_32 installation')
            storetid(res.text)
            out = install_automate.software_fetch("msoffice_13_64",config1["DEFAULT"]["myhostname"],config1["DEFAULT"]["myusername"],config1["DEFAULT"]["software upload link"],config1["DEFAULT"]["pem_file"],config1["DEFAULT"]["software_password"])
            # out = "success"
            if out == "success":
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Download Complete.
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Download Failed. ''' + res.text + '''
                                                       
                </p>'''
        elif arg == 'msoffice_13_64_install':
            out = install_automate.software_install("msoffice_13_64")
            if out == "success":
                url = config1['DEFAULT']['URL']+'/upt/'+ tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Automation Done Successfully
                                                               
            </p>
            <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
            Please Give Feedback
            <br>
            <br>
            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
            <br>
            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Installation Failed. ''' + res.text + '''
                                                       
                </p>'''
            
        
        elif arg == 'adobe':
            config.logger.info('Routed to adobe installation page')
            url = config1['DEFAULT']['URL']+'/newt/adobe_installation/adobe_installation/' + str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Contacting server for adobe installation')
            storetid(res.text)
            out = install_automate.software_fetch("adobe",config1["DEFAULT"]["myhostname"],config1["DEFAULT"]["myusername"],config1["DEFAULT"]["software upload link"],config1["DEFAULT"]["pem_file"],config1["DEFAULT"]["software_password"])
            # out = "success"
            if out == "success":
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Download Complete.
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Download Failed. ''' + res.text + '''
                                                       
                </p>'''
        elif arg == 'install_adobe':
            out = install_automate.software_install("adobe")
            if out == "success":
                url = config1['DEFAULT']['URL']+'/upt/'+ tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Automation Done Successfully
                                                               
            </p>
            <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
            Please Give Feedback
            <br>
            <br>
            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
            <br>
            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Installation Failed. ''' + res.text + '''
                                                       
                </p>'''
                
                
        elif arg == 'java':
            config.logger.info('Routed to Java installation page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 35%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="java32()">JAVA 32bit</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="java64()">JAVA 64bit</button>
                                <br>                                                
        </p>
            '''
        elif arg == 'java32':
            config.logger.info('Routed to java32 installation page')
            url = config1['DEFAULT']['URL']+'/newt/java32/java32/' + str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Contacting server for adobe installation')
            storetid(res.text)
            out = install_automate.software_fetch("Java_32b",config1["DEFAULT"]["myhostname"],config1["DEFAULT"]["myusername"],config1["DEFAULT"]["software upload link"],config1["DEFAULT"]["pem_file"],config1["DEFAULT"]["software_password"])
            # out = "success"
            if out == "success":
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Download Complete.
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Download Failed. ''' + res.text + '''
                                                       
                </p>'''
        elif arg == 'install_java32':
            out = install_automate.software_install("java_32b")
            if out == "success":
                url = config1['DEFAULT']['URL']+'/upt/'+ tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Automation Done Successfully
                                                               
            </p>
            <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
            Please Give Feedback
            <br>
            <br>
            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
            <br>
            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Installation Failed. ''' + res.text + '''
                                                       
                </p>'''
                
        elif arg == 'java64':
            config.logger.info('Routed to java64 installation page')
            url = config1['DEFAULT']['URL']+'/newt/java64/java64/' + str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            config.logger.info('Contacting server for adobe installation')
            storetid(res.text)
            out = install_automate.software_fetch("Java_64b",config1["DEFAULT"]["myhostname"],config1["DEFAULT"]["myusername"],config1["DEFAULT"]["software upload link"],config1["DEFAULT"]["pem_file"],config1["DEFAULT"]["software_password"])
            # out = "success"
            if out == "success":
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Download Complete.
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Download Failed. ''' + res.text + '''
                                                       
                </p>'''
        elif arg == 'install_java64':
            out = install_automate.software_install("java_64b")
            if out == "success":
                url = config1['DEFAULT']['URL']+'/upt/'+ tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''
            <p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
            Automation Done Successfully
                                                               
            </p>
            <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
            Please Give Feedback
            <br>
            <br>
            <input type="text" id="feedback" class="form-control" placeholder = "Feedback">
            <br>
            <button class="btn btn-secondary" onclick="feedback()">Proceed</button>                        
            </p>
            '''
            else:
                #Assing to department
                url = config1['DEFAULT']['URL']+'/assign/'+tid+'/'+str(ids)
                res = get(url,verify = False)
                return '''<p class="speech-bubble btn-primary" style="height: 10%;padding-right: 3%;">
                    Installation Failed. ''' + res.text + '''
                                                       
                </p>'''
                
        elif arg == 'otherssft':
            config.logger.info('Routed for other software installation page')
            
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="sftsymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="sftdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="sftothernew()">Proceed</button>                        
        </p>
                '''
        elif arg == 'newt':
            config.logger.info('Routed to new ticket page')
            
            symp = request.args.get('symptom')
            des = request.args.get('des')
            if len(symp) >= 10 and len(des) >= 10:
                config.logger.info('Length of symptom and description is greater than 10')
                
                url = config1['DEFAULT']['URL']+'/newt/'+symp+'/'+des+'/' + str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                ticket = res.text
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                return '''
                    <p class="speech-bubble btn-primary" style="height: 7%;">
                    Ticket ID : '''+ticket+''' '''+res.text+'''
                    </p>
                    '''
            else:
                config.logger.info('Length of symptom and description is less than 10')
                
                
                return '''
                    <p class="speech-bubble btn-primary" style="height: 10%;">
                    Symptom and Description should not be less than 10 characters
                    </p>
                    '''
        elif arg == 'msoff':
            config.logger.info('Routed to Issue page')
            
                
            return '''
            <p class="speech-bubble btn-primary" style="padding-right:3%;">
                                Please describe the issue
            </p>
            <div class="md-form" style="">
                <textarea id="textms" class="form-control md-textarea" length="120" rows="3" style="width:70%;color:white;" placeholder="Description"></textarea>
            </div>
            <button class="btn btn-secondary" onclick="conms()">Confirm</button>
            
            '''
        elif arg == 'conms':
            config.logger.info('Routed to  Confirm Issue page')
            arg2 = request.args.get('text')
            return '''
            <p class="speech-bubble btn-light" style="padding-right:3%;height: 11%;">Description Added : <br>'''+arg2+'''</p>'''
        elif arg == 'other':
            config.logger.info('Routed to Others page')
            return '''
            <p class="speech-bubble btn-primary" style="padding-right:3%;height: 10%;">
                Which software you want to install/configure
            </p>
            '''
        elif arg == 'othercon':
            config.logger.info('Routed to confirm CON page')
            arg2 = request.args.get('text')
            return '''
            <br><p class="speech-bubble btn-light" style="padding-right:3%;height: 10%;">Description Added : <br>'''+arg2+'''</p>
            '''
        elif arg == 'no':
            config.logger.info('Routed to Other ticket and IT helpdesk Page')
            return'''
            <p class="speech-bubble btn-primary" style="padding-right:3%;height: 10%;">
                Please contact IT Helpdesk on '''+config1["DEFAULT"]["IT helpdesk"]+''' to raise ticket on behalf of others…
            </p>
            '''
    
    
    @app.route('/sysrelated', methods=['GET', 'POST'])
    def sysrelated():
        config.logger.info('Routed to system related page')
        arg = request.args.get('con1')
        if arg == 'sysrelated':
            config.logger.info('Routed to system related menu page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 77%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="performance()">Performance Issue/System Slow</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="disk()">Disk full/No Space</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="autoshutres()">Auto shutdown/restart</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="forgetpsw()">Forget login password</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="unablelog()">Unable to login</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="sysother()">Other</button>                
        </p>
            '''
        elif arg == 'autoshut':
            config.logger.info('Routed to Auto shutdown page')
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="sftsymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="sftdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="sftothernew()">Proceed</button>                        
        </p>
                '''
            # url = config1['DEFAULT']['URL']+'/newt/auto_shutdown_restart/auto_shutdown_restart/' + \
            #     str(ids)
            # config.logger.info('Raising new ticket for auto shutdown')
            # res = get(url,verify = False)
            # ticket = res.text
            # config.logger.info('Assigning ticket')
            # url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            # res = get(url,verify = False)
            # config.logger.info('Request returned is '+ res.text)
            # return '''
            # <p class="speech-bubble btn-primary" style="height: 7%;">
            # Ticket ID : '''+ticket+''' '''+res.text+'''
            # </p>
            # '''
        elif arg == 'unlog':
            config.logger.info('Routed to Unable to login page')
            url = config1['DEFAULT']['URL']+'/newt/unable_to_login/unable_to_login/' + \
                str(ids)
            config.logger.info('Raising new ticket for unable to login')
            res = get(url,verify = False)
            ticket = res.text
            
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning ticket')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'sysother':
            config.logger.info('Routing to system other issue')
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="syssymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="sysdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="sysothernew()">Proceed</button>                        
        </p>
                '''
        elif arg == 'newt':
            config.logger.info('New ticket route')
            symp = request.args.get('symptom')
            des = request.args.get('des')
            if len(symp) >= 10 and len(des) >= 10:
                config.logger.info('Symptom and description lenght OK')
                url = config1['DEFAULT']['URL']+'/newt/'+symp+'/'+des+'/' + str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                ticket = res.text
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''
                <p class="speech-bubble btn-primary" style="height: 7%;">
                Ticket ID : '''+ticket+''' '''+res.text+'''
                </p>
                '''
            else:
                config.logger.info('Lenght is less than 10')
                return '''
                    <p class="speech-bubble btn-primary" style="height: 10%;">
                    Symptom and Description should not be less than 10 characters
                    </p>
                    '''
        elif arg == 'psw':
            config.logger.info('Routed to password page')
            url = config1['DEFAULT']['URL']+'/newt/password_has_to_be_reset/password_has_to_be_reset/' + \
                str(ids)
            config.logger.info('Raising new ticket for password reset')
            res = get(url,verify = False)
            ticket = res.text
            config.logger.info('Assigning ticket')
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'ps1':
            config.logger.info('Routed to password page')
            url = config1['DEFAULT']['URL']+'/newt/password_has_to_be_changed/password_has_to_be_changed/' + \
                str(ids)
            config.logger.info('Raising new ticket for password reset')
            res = get(url,verify = False)
            ticket = res.text
            config.logger.info('Assigning ticket')
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
    
    
    @app.route('/apprelated', methods=['GET', 'POST'])
    def apprelated():
        config.logger.info('Routed to App related page')
        arg = request.args.get('con1')
        if arg == 'apprelated':
            config.logger.info('Routed to main App related page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 84%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="outlook()">Outlook related issue</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="exc_el()">Excel not responding</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="sap()">SAP not working</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="emailconf()">Email Configuration</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="ieconf()">IE Configuration</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="vpnconf()">VPN Configuration</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="appother()">Other</button>                        
        </p>
            '''
        elif arg == 'outlook':
            config.logger.info('Routed to Outlook related page Page')
            url = config1['DEFAULT']['URL']+'/newt/outlook_related_issue/outlook_related_issue/' + \
                str(ids)
            config.logger.info('Raising ticket related to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'excel':
            config.logger.info('Routed to excel issue page Page')
            url = config1['DEFAULT']['URL']+'/newt/excel_not_responding/excel_not_responding/' + \
                str(ids)
            config.logger.info('Rasing ticket related to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'sap':
            config.logger.info('Routed to sap not responding Page')
            url = config1['DEFAULT']['URL']+'/newt/sap_not_responding/sap_not_responding/' + \
                str(ids)
            config.logger.info('Rasing ticket related to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'ie':
            config.logger.info('Routed to ie configuration Page')
            url = config1['DEFAULT']['URL']+'/newt/ie_configuration/ie_configuration/' + \
                str(ids)
            config.logger.info('Rasing ticket related to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'vpn':
            config.logger.info('Routed to VPN configuration Page')
            url = config1['DEFAULT']['URL']+'/newt/vpn_configuration/vpn_configuration/' + \
                str(ids)
            config.logger.info('Rasing ticket related to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'appother':
            config.logger.info('Routed to other app related issue')
            
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="appsymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="appdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="appothernew()">Proceed</button>                        
        </p>
                '''
        elif arg == 'newt':
            config.logger.info('Routed to new ticket page')
            
            symp = request.args.get('symptom')
            des = request.args.get('des')
            symp = symp.replace(' ', '_')
            des = des.replace(' ', '_')
            if len(symp) >= 10 and len(des) >= 10:
                config.logger.info('Description and symptom length OK')
            
                url = config1['DEFAULT']['URL']+'/newt/'+symp+'/'+des+'/' + str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                ticket = res.text
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''
                <p class="speech-bubble btn-primary" style="height: 7%;">
                Ticket ID : '''+ticket+''' '''+res.text+'''
                </p>
                '''
            else:
                config.logger.info('Description and symptom length less than 10')
                return '''
                    <p class="speech-bubble btn-primary" style="height: 10%;">
                    Symptom and Description should not be less than 10 characters
                    </p>
                    '''
        elif arg == 'email':
            config.logger.info('Routed to email configuration form')
            return '''
            <p class="speech-bubble btn-primary" style="height: 54%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="username" class="form-control" placeholder="UserName">
                                <br>
                                        <input type="text" id="useremail" class="form-control" placeholder = "Email">
                                <br>
                                        <input type="password" id="password" class="form-control" placeholder = "Password">
                                <br>
                                        <button class="btn btn-secondary" onclick="email_reg()">Proceed</button>                        
        </p>
            '''
    
    
    @app.route('/osrelated', methods=['GET', 'POST'])
    def osrelated():
        config.logger.info('Routed to OS related Issue')
            
        arg = request.args.get('con1')
        if arg == 'osrelated':
            config.logger.info('Routed to email configuration form')
            
            return '''
            <p class="speech-bubble btn-primary" style="height: 42%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="addpcdomain()">Add PC with Domain</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="osnotbooting()">OS not booting</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="osother()">Other</button>                        
        </p>
            '''
        elif arg == 'addpc':
            config.logger.info('Routed to add pc issue')
            url = config1['DEFAULT']['URL']+'/newt/add_pc_with_domain/add_pc_with_domain/' + \
                str(ids)
            config.logger.info('Ticket raised realted to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigned to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'osnot':
            config.logger.info('Routed to OS not booting issue')
            url = config1['DEFAULT']['URL']+'/newt/os_not_booting/os_not_booting/' + \
                str(ids)
            config.logger.info('Ticket raised realted to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigned to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'osother':
            config.logger.info('Routed to OS other issue')
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="ossymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="osdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="osothernew()">Proceed</button>                        
        </p>
                '''
        elif arg == 'newt':
            config.logger.info('Routed to new ticket issue issue')
            symp = request.args.get('symptom')
            des = request.args.get('des')
            symp = symp.replace(' ', '_')
            des = des.replace(' ', '_')
            if len(symp) >= 10 and len(des) >= 10:
                config.logger.info('Desc and Symptom length is OK')
                url = config1['DEFAULT']['URL']+'/newt/'+symp+'/'+des+'/' + str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                ticket = res.text
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''
                <p class="speech-bubble btn-primary" style="height: 7%;">
                Ticket ID : '''+ticket+''' '''+res.text+'''
                </p>
                '''
            else:
                config.logger.info('Desc and Symptom length is less than 10')
                return '''
                    <p class="speech-bubble btn-primary" style="height: 10%;">
                    Symptom and Description should not be less than 10 characters
                    </p>
                    '''
    
    
    @app.route('/printerrelated', methods=['GET', 'POST'])
    def printerrelated():
        config.logger.info('Routed to printer related issue')
        arg = request.args.get('con1')
        if arg == 'printerrelated':
            config.logger.info('Routed to printer related menu page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 56%;width:75%">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="newprinter()">Printer - New configuration</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="printernotworking()">Printer not working</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="printernotproper()">Printout not proper</button>                        
                                <br>
                                        <button class="btn btn-secondary" onclick="printerother()">Other</button>        
        </p>
            '''
        elif arg == 'newprinter':
            config.logger.info('Routed to new printer page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 54%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="manuname" class="form-control" placeholder="Manufaturer Name">
                                <br>
                                        <input type="text" id="model" class="form-control" placeholder = "Model Name">
                                <br>
                                        <input type="text" id="printerip" class="form-control" placeholder = "Printer config IP">
                                <br>
                                        <button class="btn btn-secondary" onclick="new_print()">Proceed</button>                        
        </p>
            '''
        elif arg == 'notprinter':
            config.logger.info('Routed to no printer page')
            url = config1['DEFAULT']['URL']+'/newt/Printer_Not_working/Printer_Not_working/' + \
                str(ids)
            config.logger.info('Raising ticket related to this issue')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'notproper':
            config.logger.info('Routed to not proper printer page')
            url = config1['DEFAULT']['URL']+'/newt/Printer_not_proper/Printer_Not_proper/' + \
                str(ids)
            config.logger.info('Raising ticket related to this issue')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'otherprint':
            config.logger.info('Routed to other printer related issue')
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="printsymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="printdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="printother()">Proceed</button>                        
        </p>
                '''
        elif arg == 'newt':
            config.logger.info('Routed to new ticket page')
            symp = request.args.get('symptom')
            des = request.args.get('des')
            symp = symp.replace(' ', '_')
            des = des.replace(' ', '_')
            if len(symp) >= 10 and len(des) >= 10:
                config.logger.info('Desc and symtom length is OK')
                url = config1['DEFAULT']['URL']+'/newt/'+symp+'/'+des+'/' + str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                ticket = res.text
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''
                <p class="speech-bubble btn-primary" style="height: 7%;">
                Ticket ID : '''+ticket+''' '''+res.text+'''
                </p>
                '''
            else:
                config.logger.info('Desc and symtom length is less than 10')
                return '''
                    <p class="speech-bubble btn-primary" style="height: 10%;">
                    Symptom and Description should not be less than 10 characters
                    </p>
                    '''
    
    
    @app.route('/networkrelated', methods=['GET', 'POST'])
    def networkrelated():
        config.logger.info('Routed to new network related page')
        arg = request.args.get('con1')
        if arg == 'networkrelated':
            config.logger.info('Routed to network related menu page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 63%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="IEnotworking()">Internet not working</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="noacessserver()">Unable to access server</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="ipchange()">IP Address - Change</button>                        
                                <br>
                                        <button class="btn btn-secondary" onclick="wificonf()">Wi-Fi Configuration</button>                        
                                <br>
                                        <button class="btn btn-secondary" onclick="networkother()">Other</button>        
        </p>
            '''
        elif arg == 'ie':
            config.logger.info('Routed to not IE not working page')
            url = config1['DEFAULT']['URL']+'/newt/Internet_explorer_not_working/Internet_explorer_not_working/' + \
                str(ids)
            config.logger.info('Ticket raising related to the issue')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assgining to the expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
                <p class="speech-bubble btn-primary" style="height: 7%;">
                Ticket ID : '''+ticket+''' '''+res.text+'''
                </p>
                '''
        elif arg == 'noaccess':
            config.logger.info('Routed to NO Access page')
            url = config1['DEFAULT']['URL']+'/newt/Unable_to_access_server/Unable_to_access_server/' + \
                str(ids)
            config.logger.info('Ticket raising related to the issue')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assgining to the expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'ipchange':
            config.logger.info('Routed to IP change page')
            url = config1['DEFAULT']['URL']+'/newt/IP_address_change/IP_address_change/' + \
                str(ids)
            config.logger.info('Ticket raising related to the issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to the expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'wifi':
            config.logger.info('Routed to wifi configuration page')
            url = config1['DEFAULT']['URL']+'/newt/wi_fi_configuration/wi_fi_configuration/' + \
                str(ids)
            config.logger.info('Ticket raised related to this issue')
            res = get(url,verify = False)
            ticket = res.text
            url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
            config.logger.info('Assigning to the expert')
            res = get(url,verify = False)
            config.logger.info('Request returned is '+ res.text)
            return '''
            <p class="speech-bubble btn-primary" style="height: 7%;">
            Ticket ID : '''+ticket+''' '''+res.text+'''
            </p>
            '''
        elif arg == 'other':
            config.logger.info('Routed to Other issue page')
            return '''
                <p class="speech-bubble btn-primary" style="height: 43%;padding-right: 3%;">
                                All fields are mandatory
                                <br>
                                <br>
                                        <input type="text" id="netsymptom" class="form-control" placeholder="Symptom">
                                <br>
                                        <input type="text" id="netdes" class="form-control" placeholder = "Description">
                                <br>
                                        <button class="btn btn-secondary" onclick="netother()">Proceed</button>                        
        </p>
                '''
        elif arg == 'newt':
            config.logger.info('Routed to new ticket page')
            symp = request.args.get('symptom')
            des = request.args.get('des')
            symp = symp.replace(' ', '_')
            des = des.replace(' ', '_')
            if len(symp) >= 10 and len(des) >= 10:
                config.logger.info('Desc and symptom length is OK')
                url = config1['DEFAULT']['URL']+'/newt/'+symp+'/'+des+'/' + str(ids)
                res = get(url,verify = False)
                ticket = res.text
                url = config1['DEFAULT']['URL']+'/assign/'+res.text+'/'+str(ids)
                res = get(url,verify = False)
                config.logger.info('Request returned is '+ res.text)
                return '''
                        <p class="speech-bubble btn-primary" style="height: 7%;">
                        Ticket ID : '''+ticket+''' '''+res.text+'''
                        </p>
                        '''
            else:
                config.logger.info('Desc and symptom length is less than 10')
                return '''
                        <p class="speech-bubble btn-primary" style="height: 10%;">
                        Symptom and Description should not be less than 10 characters
                        </p>
                        '''
    # flow end for new request
    
    # flow know your ticket
    @app.route('/knowticket', methods=['GET', 'POST'])
    def knowticket():
        config.logger.info('Routed to know ticket page')
        arg = request.args.get('con1')
        if arg == 'know':
            url = config1['DEFAULT']['URL']+'/know/'+str(ids)
            config.logger.info('Requesting server database for all recent tickets')
            res = get(url,verify = False)
            
            res = res.json()
            ticket_id = res['Incident ID']
            status = res['Status']
            issue = res['Issue_Class']
            description = res['Description']
            print(ticket_id, status, issue, description)
            ht = '''<p class="speech-bubble btn-light" style="padding-right:3%;">Select one from your previous tickets : <br></p><table class="table" style="background-color: #eec0c6;background-image: linear-gradient(315deg, #eec0c6 0%, #7ee8fa 74%);"><thead class="black white-text"><tr><th scope="col">Ticket ID</th><th scope="col">Status</th><th scope="col">Issue</th><th scope="col">Description</th></tr></thead><tbody>'''
            for i in range(0, len(ticket_id)):
                ht = ht + '''<tr><td>'''+str(ticket_id[str(i)])+'''</td><td>'''+str(status[str(i)])+'''</td><td>'''+str(
                    issue[str(i)])+'''</td><td>'''+str(description[str(i)])+'''</td></tr>'''
            ht = ht + '''</tbody></table>'''
            return ht
    
        elif arg == 'newr':
            config.logger.info('Routed to Details page')
            return '''
        <p class="speech-bubble btn-primary" style="height: 25%;">
            Please verify the below details to continue with Aforesight
           <br>
           <br>
            Your IP : '''+str(IP)+'''
           <br>
           Your Hostname : '''+str(username.title())+'''
        </p>
        '''
        elif arg == 'proceed':
            config.logger.info('Routed to proceed route')
            tid = request.args.get('id')
            url = config1['DEFAULT']['URL']+'/oldt/'+str(tid)
            msg = get(url,verify = False)
            config.logger.info('Request returned is '+ msg.text)
            return msg.text
    # flow new query
    @app.route('/newquery', methods=['GET', 'POST'])
    def newquery():
        config.logger.info('Routed to new query page')
        arg = request.args.get('con1')
        if arg == 'newq':
            config.logger.info('Routed to new query menu page')
            return '''
            <p class="speech-bubble btn-primary" style="height: 42%;">
                                Please select desired option…
                                <br>
                                <br>
                                        <button class="btn btn-secondary" onclick="itpolicies()">Know your IT Policies</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="helpdesk()">Contact of IT Helpdesk</button>
                                <br>
                                        <button class="btn btn-secondary" onclick="asset()">Know your IT Asset</button>                        
        </p>
            '''
        elif arg == 'asset':
            config.logger.info('Routed to IT Assets page')
            return '''
        <p class="speech-bubble btn-primary" style="height: 42%;">
                Below are your details: <br>
                <br>
                Your Hostname : '''+str(username.title())+''' <br>
                <br>
                Aforeserve Unique id: ''' + str(ids) + '''<br>
                <br>
                Your System IP: ''' + str(IP) + '''
            </p>
        '''
    
    ui.run()
run()
