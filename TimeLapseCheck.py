import ftplib
import getpass
import smtplib
import keyring

from email.mime.text import MIMEText

filename = "log.txt" #This text file contains the last file count

pswd = keyring.get_password('service','username') #The keyring safely stores passwords on my raspberry pi

ftp = ftplib.FTP("ftpserver.com")
ftp.login("username", pswd)

data = []

ftp.dir("ConstructionPhotos",data.append) #Adds the contents of the FTP directory to an array

ftp.quit()

numberOfFiles = int(len(data)) #The length of this array is the number of files in the FTP folder

print "Number of files:", numberOfFiles

stringToPrint = str(numberOfFiles)

target = open(filename, 'r')

lastCount = int(target.readline()) #This text file contains the last file count

print "Last time we had", lastCount

target.close()

target = open(filename, 'w')

target.write(stringToPrint) #Save the current file count to a text file for later comparison
target.close()

if lastCount >= numberOfFiles: #If the count hasn't changed, or if it's gone down since we last checked, there is a problem. Alert user.
  print "No new files since last check!"
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  gpass = keyring.get_password('Gmail','email')
  server.login("email@gmail.com", gpass)

  msg = "No new files! Last time we had " + str(lastCount)
  server.sendmail("email@gmail.com","email@gmail.com",msg) # Send message from myself, to myself.
  server.quit()

elif lastCount < numberOfFiles: #This occurs if everything is ok. If system is found to be reliable, these updates should be changed from daily to weekly.
  print "Timelapse is working normally"
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls() 
  gpass = keyring.get_password('Gmail','email') # This should be put into a function
  server.login("email@gmail.com", gpass)

  msg = "Timelapse is working! We got " + str(numberOfFiles - lastCount) + " more files since last time for a total of " + str(numberOfFiles)
  server.sendmail("email@gmail.com","email@gmail.com",msg)
  server.quit()
