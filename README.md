# dropbox-update-notifier
A python app to check for hourly updates in a dropbox folder. The application connects to the users' dropbox account and  
monitors a specified folder for any updates for the following file types: .txt, .doc, .docx. It provides alerts (in real-time) 
when such files are created/updated/deleted in that folder in the last hour.

# How to run:
1.) Double click on Notifier.py and wait for the application to open

2.) Enter the details:
	- app key
	- app secret
	- a folder name ( ex: /cloud )
	  Note: You can enter a folder name which is already present
	  in your dropbox account. If not present a new folder with
	  the entered name will be created.

3.) Click on submit. A url will be displayed on the application. Go to
this url and click allow.

4.) Click on Authorize and start service. An alert box notifies to which
dropbox account the application is now linked to.

5.) Now the application is up and running!. Any changes made to files (only .txt/.doc/.docx files)
in the given folder in the past hour will be notified with an alert box. The application keeps on 
running and any updates made as above will be notified with an alert box.
