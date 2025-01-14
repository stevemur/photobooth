# remoterequests.py

# My version of the Photo Booth posts to a back-end Internet service I created called popsee.com, 
# which lets users review the photos taken, get a download link via SMS, and allows admins 
# to create a big-screen slideshow of the photos "favorited" by the admin. 
# 
# At this writing, I'm not making popsee.com available for public use, but if you've got a special use-case, 
# jot me a note. Jot me a note at @stevemur on Twitter. 

# Change the functions here to post to YOUR own endpoint(s). You could upload to Google Photos or 
# tweet out the photos via Twitter for instance. 

import requests
import os
import aiohttp
import json 
from threading import Thread
import urllib.request # requires Python 3.x

# secret.py includes back-end support variables
# The file "secret.py" is not in the GitHub repo, and simply holds the value for these variables, 
# which relate to POSTing an image to a remote server: 
# 
# albumCode:    the "shortcode" for the popsee album to post to
# postImageUrl: the URL to POST images to 
# statusUrl:    the URL to POST text status updates to (the server then rebroadcasts them)
from secret import *

# Post an image to the server 
def send_data_to_server(image_path):
    try:
        image_filename = os.path.basename(image_path)
        multipart_form_data = {'file': (image_filename, open(image_path, 'rb'))}
        response = requests.post(postImageUrl, files=multipart_form_data)
        print(response.text)
        print(response.status_code)
        update_status(albumCode, "Uploaded with status code "+str(response.status_code))
        
        print("response code from server is:")
        print(json_response)
        return response.text 
    except:
        #update_status(albumCode, "An exception occurred in upload!")
        print("An exception occurred in upload")
        #parsed = json.loads(response.content)
        #print (parsed)
        return "Error"

# On startup, the photo booth calls out to the server to get 
# configuration information, primarily the "albumCode" to use for posting images 
# and status information, as well as the homescreen JPG. 
# The homescreen JPG is downloaded at startup, 
# and stored in the program's home directory as "homescreen-image.jpg"
# This allows for the photo booth to change homescreens from party to party
# by tweaking settings at the popsee API. 

def get_current_config(path_to_save_homescreen):
    print("Getting current configuration from popsee server...")
    global albumCode 
    try:
        response = requests.get(configUrl, verify=False)
        print(response.status_code)
        parsed = json.loads(response.content)
        print("homeScreenJPGUrl: "+ parsed["homeScreenJPGUrl"])
        print("albumCode: "+parsed["albumCode"])

        download_image(parsed["homeScreenJPGUrl"], "homescreen-image.jpg")
        return ""
    except:
        print("An exception occurred in getting configuration data")
        return "Error"

def download_image(url, image_filename):
    #try:
        urllib.request.urlretrieve(url, image_filename)
        return image_filename
    #except:

     #   return ""


# Post status information to the server. (Popsee currently uses SignalR to broadcast these messages to current viewers of the album.)
def update_status(code, message):
    try:
        response = requests.post(statusUrl, json={"code": code, "message":message })
        print(response.text)
        print(response.status_code)
        return response.text 
    except:
        print("An exception occurred in posting status")
        #return "Error"
        

# Async example
def send_data_to_server_async(image_path):
    t = Thread(target=send_data_to_server, args=(image_path,))
    t.start()
    return "Queued"

async def send_file(image_path):
   url = postImageUrl
   async with aiohttp.ClientSession() as session:
      _url = postImageUrl
      async with  session.post(url, data ={
            'url': postImageUrl,
            'file': open(image_path, 'rb')
      }) as response:
            data = await response.text()
            print (data)
