#Mephistopheles
def getFromFlipkart():
    import requests
    url = "http://mobile-mapi2.nm.flipkart.com:8079/documentation/resourceList"
    payload = {"infolevel":2, "version":2, "ids":"CMKDU959Z8FPM9PQ"}
    header = {
        'User-agent': 'w3.product_service'
    }
    
    r = requests.get(url, params=payload,headers=header)
    print r.url
    print r.text

def getFSNForItemID():
    import requests
    import urllib
    url="http://w3-web1003.nm.flipkart.com:8190/productService/getItems/"
    payload = {
        "ids":"ITME3Q7Q93M77CG6"
        }
    url += urllib.urlencode(payload)
    header = {
        'User-Agent': 'w3.product_service'
    }
    r = requests.get(url, headers=header)
    print r.url
    print r.headers
    print r.text
    #print r.json()

def readAssignmentSheets():
    import gspread
    assignment_sheets = {
    "RPD": {"ID": "1xJVyHuuLhzYQiYInC5yALEBjLqqHqPodw0q8WTfmAMU", "Name": "RPD Assignment - 2015"},
    "PD": {"ID": "1uH6hIl4meFJbPCnbbWLP8jZ8HCn6wGMZYYQSnCkMzEM", "Name": "Content Team Work Assignment 2015"},
    "SEO": {"ID": "15xhg6xTBqmSYxa_5EWFsdtS7OX0vVZKifQ9xD2q0GSk", "Name": "Content Team SEO Tracker-2015"},
    "Project": {"ID": "1Ll-svw6ajsRNJyxXkSc44Nn3xMvLVH2z7FZ_qgEho2g", "Name": "Project FSN Assignment Sheet"}
    }
    google_cred =  getGoogleCredentials()
    
    


def getGoogleCredentials():
    import os
    import json
    from oauth2client.client import SignedJwtAssertionCredentials
    auth_file_name = os.path.join("Data","GoogleAuthInfo.json")
    json_key = json.load(open(auth_file_name))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    google_credentials = gspread.authorize(credentials)
    return google_credentials()