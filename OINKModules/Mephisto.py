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