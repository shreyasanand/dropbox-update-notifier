'''
@author: Shreyas Anand
@course no: CSE 6331
@lab no: Programming Assignment 1

'''
import dropbox
import requests
import json
import Tkinter
import tkMessageBox
from pytz import timezone
from datetime import datetime, timedelta
from Tkinter import *


def login():
    
    # Get the users app key and secret
    app_key=appkey.get()
    app_secret=appsecret.get()
	
	# Authorizing the user
    session = dropbox.session.DropboxSession(app_key,app_secret)
    req_token = session.obtain_request_token()
    authorize_url= session.build_authorize_url(req_token)
    
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    url_label = Label(view,text = "Go to this url and click allow").grid(row=14,column=1)
    var = StringVar()
    var.set(authorize_url)
    url = Entry(view,textvariable = var).grid(row=14,column=2)

    def auth():
        access_token = session.obtain_access_token(req_token)
        client = dropbox.client.DropboxClient(session)
        print 'Linked account: ', client.account_info()
        account = client.account_info()['email']
        acc_var = StringVar()
        acc_var.set(account)
        tkMessageBox.showinfo("Account info","Connected to %s" % account)
        
        # Getting the current local time
        local_time = datetime.now()
        
        # Subtracting 1 hour from the current local time
        temp_time = local_time - timedelta(hours=1)
        
        # Setting the local timezone to the above time
        local_timezone = timezone('US/Central')
        lasthour = local_timezone.localize(temp_time)
        print "Local current time minus 1 hour :", lasthour
        
        # Get the user entered folder path
        folderPath = folder_path.get()
        
        # Checking if the folder is already present
        for folders in client.metadata('/')['contents']:
            if folders['path'] == folderPath:
                print "Folder %s already present" % folderPath
                found = 1
                break
            else:
                found = 0
                continue
        
        # If folder is not present create the folder
        if not found:
            result = client.file_create_folder(folderPath)
            message = "Folder %s not present. Created a new folder" % folderPath
            print message
            tkMessageBox.showinfo("Notification",message)
        
        cursor = None
        while True:
            delta_result = client.delta(cursor,folderPath)
            print 'Delta result: ', delta_result
            cursor = delta_result['cursor']
            if delta_result['reset']:
                print 'RESET'

            for path, metadata in delta_result['entries']:
            
                    # Checking if the files are of type .docx or .txt or .doc
                    if ".txt" in path or ".docx" in path or ".doc" in path:
                        
                            if metadata is not None:
                                # Extracting the last modified time of the file in the python datetime format
                                last_modified_time = datetime.strptime(metadata['modified'],'%a, %d %b %Y %H:%M:%S +0000')
                                
                                # Setting the timezone to 'Europe/London' and then converting it to 'US/Central'
                                local_tz = timezone('Europe/London')
                                last_modified = local_tz.localize(last_modified_time)
                                modified_time = last_modified.astimezone(timezone('US/Central'))
                                
                                print "File: ", path
                                print "Last modified time: ", modified_time
                                
                                # Checking if any of the files have been modified in the previous hour
                                if modified_time > lasthour:
                                    message = path+' was created/updated'
                                    print message
                                    tkMessageBox.showinfo("Notification",message)
                                    
                            else:
                                message = path+' was deleted'
                                print message
                                tkMessageBox.showinfo("Notification",message)

            # if has_more is true, call delta again immediately
            if not delta_result['has_more']:

                changes = False
                # poll until there are changes
                while not changes:
                    response = requests.get('https://api-notify.dropbox.com/1/longpoll_delta',
                        params={
                            'cursor': cursor,  # latest cursor from delta call
                            'timeout': 200     # default is 30 seconds
                        })

                    result = response.content
                    data = json.loads(result)
                    changes = data['changes']
                    if not changes:
                        print 'Timeout, polling again...'

        return
    
    auth_button = Button(view,text = "Authorize and start service", command = auth).grid(row=16,column=2)
    return

# Designing the UI
view = Tkinter.Tk()

appkey=StringVar()
appsecret=StringVar()
folder_path=StringVar()

view.title("Dropbox Notifier")
view.geometry("500x500")

head_label = Label(view,text='Dropbox update notifier').grid(row=1,column=2)

appkey_label=Label(view,text='Enter the app key: ').grid(row=4,column=1)
appkey_entry=Entry(view,textvar=appkey).grid(row=4,column=2)

appsecret_label=Label(view,text='Enter the app secret: ').grid(row=8,column=1)
appsecret_entry= Entry(view,textvar=appsecret).grid(row=8,column=2)

folderPath_label=Label(view,text='Enter a folder name: ').grid(row=9,column=1)
folderPath_entry=Entry(view,textvar=folder_path).grid(row=9,column=2)

login_button = Button(view,text ="Submit", command = login).grid(row=12,column=2)

#start the event loop
view.mainloop()
