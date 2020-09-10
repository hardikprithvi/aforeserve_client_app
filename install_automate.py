import pysftp    
import os   
from stat import S_ISDIR, S_ISREG
import subprocess


def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):
    for entry in sftp.listdir_attr(remotedir):
        remotepath = remotedir + "/" + entry.filename
        localpath = os.path.join(localdir, entry.filename)
        mode = entry.st_mode
        if S_ISDIR(mode):
            try:
                os.mkdir(localpath)
            except OSError:     
                pass
            get_r_portable(sftp, remotepath, localpath, preserve_mtime)
        elif S_ISREG(mode):
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

def software_fetch(soft_name, myHostname, myUsername,software_link, pem_file, software_password):
    kwargs = dict()
    if len(software_password) != 0:
        kwargs['password']=software_password
    if len(pem_file)!=0:
        kwargs['private_key'] = 'software_afs.pem'
    print(kwargs)
    # checking if folder exists or not and if not creating one
    try:
        os.system('cmd /c "cd\ && IF exist Software_Aforesight ( cd Software_Aforesight && echo exists ) ELSE ( mkdir Software_Aforesight && cd Software_Aforesight && echo created)"')
        print("folder created")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  
        with pysftp.Connection(host=myHostname, username=myUsername,cnopts=cnopts,**kwargs) as sftp:
            print("conection success")
            if soft_name == "Java_32b":
                # download software
                print("Software downloading")
                get_r_portable(sftp, software_link+"Java_32B", r"C:\Software_Aforesight", preserve_mtime=False)
            
            
            elif soft_name == "Java_64b":
            
                # download software
                print("software Download")
                get_r_portable(sftp, software_link+"Java_64B", r"C:\Software_Aforesight", preserve_mtime=False)
            
            
            elif soft_name == "adobe":
            
                # download software
                print("software Download")
                get_r_portable(sftp, software_link+"Adobe_Reader", r"C:\Software_Aforesight", preserve_mtime=False)
            
            elif soft_name == "msoffice_10_32":
            
                # download software
                print("software Download")
                get_r_portable(sftp, software_link+"MS_Office_2010_32B", r"C:\Software_Aforesight", preserve_mtime=False)
            
            elif soft_name == "msoffice_13_32":
            
                # download software
                print("software download")
                get_r_portable(sftp, software_link+"MS_Office_2013_32B", r"C:\Software_Aforesight", preserve_mtime=False)
            
            
            elif soft_name == "msoffice_13_64":
            
                # download software
                print("software Download")
                get_r_portable(sftp, software_link+"MS_Office_2013_64B", r"C:\Software_Aforesight", preserve_mtime=False)
            else: return "fail"
    except:
        return "fail"
            
    return "success"
       
def software_install(soft_name):
    
    if soft_name == "adobe":
        print("software installation")
        result = subprocess.Popen('cmd /c "cd\ && cd c:\Software_Aforesight\Adobe_Reader && AcroRdrDC2001220041_en_US.exe /sPB"', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,error = result.communicate()
        if error == b"":
            return "success"
        else:
            return "fail"
    if soft_name == "java_32b":
        print("software installation")
        result = subprocess.Popen('cmd /c "cd\ && cd c:\Software_Aforesight\Java_32B && jre-8u261-windows-i586.exe /s"', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,error = result.communicate()
        if error == b"":
            return "success"
        else:
            return "fail"
    
    if soft_name == "java_64b":
        print("software installation")
        result = subprocess.Popen('cmd /c "cd\ && cd c:\Software_Aforesight\Java_64B && jre-8u261-windows-x64.exe /s"', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,error = result.communicate()
        if error == b"":
            return "success"
        else:
            return "fail"
    
    if soft_name == "msoffice_10_32":
       print("software installation")
       result = subprocess.Popen('cmd /c "cd\ && cd c:\Software_Aforesight\MS_Office_2010_32B && setup.exe /config config.xml"', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       output,error = result.communicate()
       if error == b"":
           return "success"
       else:
           return "fail"
        
    if soft_name == "msoffice_13_32":
       print("software installation")
       result = subprocess.Popen('cmd /c "cd\ && cd c:\Software_Aforesight\MS_Office_2013_32B && setup.exe /config config.xml"', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       output,error = result.communicate()
       if error == b"":
           return "success"
       else:
           return "fail"
        
    if soft_name == "msoffice_13_64":
       print("software installation")
       result = subprocess.Popen('cmd /c "cd\ && cd c:\Software_Aforesight\MS_Office_2013_64B && setup.exe /config config.xml"', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       output,error = result.communicate()
       if error == b"":
           return "success"
       else:
           return "fail"
        
# software_fetch("adobe", myHostname = "3.135.61.122", myUsername = "ubuntu")




