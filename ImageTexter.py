import requests, sys

import twilio
from twilio.rest import Client

from SimpleCV import Image, Camera




# Gets the contents of an image file to be sent to the
# machine learning model for classifying
def getImageFileData(locationOfImageFile):
    with open(locationOfImageFile, "rb") as fi:
        data = fi.read()
        if sys.version_info[0] < 3:
            # Python 2 approach to handling bytes
            return data.encode("base64")
        else:
            # Python 3 approach to handling bytes
            import base64
            return base64.b64encode(data).decode()



# Send image to the machine learning model, returns class with highest confidence

def classify(img):
    key = "a936c340-b31e-11e9-a7ba-f3abb34237d23b90be36-27c6-4058-8ab4-8ca68fd6279c"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : getImageFileData(img) })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


# Let's take a photo using the Webcam!

cam = Camera()
img = cam.getImage()
img.save("InsertImageNameHere.jpg")


# Change this to the name of your image file!
res = classify("InsertImageNameHere.jpg")

categoryClass = res["class_name"]

confidence = res["confidence"]

print ("The result is : '%s' with %d%% confidence" % (categoryClass, confidence))


# Now, let's use Twilio to send an SMS /if/ it is in the correct category!!

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

account_sid = 'ACXXXXXXXXXXXXXXX'

auth_token = 'XXXXXXXXXXXX'

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hey Person! Input your SMS message here, whatever is written in this line will send out as a text message. \
                         This text was triggered by an image of me/my '%s' with %d%% confidence" % (categoryClass, confidence),
                     from_='+1XXXXXXXXXX', # your twilio SMS number
                     to='+1XXXXXXXXXX' # Recipient of your SMS text
                 )

print(message.sid)

