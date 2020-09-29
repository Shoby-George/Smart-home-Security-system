import RPi.GPIO as GPIO
import time
import picamera
import base64
import urllib.request
from time import sleep
import smtplib,ssl  
#from picamera import PiCamera  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders

camera = picamera.PiCamera()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN) #PIR
GPIO.setup(10, GPIO.OUT) #LED
encoded=0

def cam():
    camera.capture('image.jpg', resize=(500,281))
    with open("image.jpg", "rb") as image_file:
      encoded = base64.b64encode((image_file.read()))
      print(encoded)
   

def video():
   camera.start_recording('examplevid.h264')
   time.sleep(5)
   camera.stop_recording()
    

def thingspeak():
   data=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=4JWC3O98GFI9W1PB&field1="+str(encoded)+"&field2=1")
   data.read()
   time.sleep(15)

def send_an_email():  
    toaddr = 'emailid2@gmail.com'      # To id 
    me = 'emailid1@gmail.com'          # your id
    subject = "Evidence"              # Subject
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("image.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    msg.attach(part)
    s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
    s.ehlo()  
    s.starttls()
    s.ehlo()
    s.login(user = 'emailid1@gmail.com', password = '*******')  # User id & password
    s.sendmail(me, toaddr, msg.as_string())
    print("Mail sent")
    s.quit()  
  

while True:
        #GPIO.output(10, False)
        #data=urllib.request.urlopen("https://api.thingspeak.com/update?api_key=4JWC3O98GFI9W1PB&field2=0")
        #data.read() 
        
        #sleep(15) # to stabilize sensor
        if GPIO.input(8):
            GPIO.output(10, True)
            time.sleep(2)
            print("Motion Detected...")
            cam()
            thingspeak()
            video()
            send_an_email()
            time.sleep(15) #LED turns on for 15 sec
            GPIO.output(10, False)
            time.sleep(0.5) 
            
 

             
           
        



