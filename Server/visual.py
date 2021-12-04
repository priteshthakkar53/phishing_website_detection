
from bs4 import BeautifulSoup
from googlesearch import search
import requests
from tld import get_tld
from urllib.parse import urlparse

from skimage.measure import _structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB):
	# compute the mean squared error and structural similarity
	m = mse(imageA, imageB)
	print("MSE : %.2f " %(m))
	if(m<6000):
		return 1
	else:	
		return 0

def convertIcotoPng():
	try:
		from PIL import Image
		filename = r'images/img_data1.ico'
		img = Image.open(filename)
		icon_sizes = [(16,16)]
		img = img.resize((16,16), Image.ANTIALIAS)
		img.save('images/img_data1.png', sizes=icon_sizes)
		return 1
	except:
		print("Ico to Png convert errror")
		return 0

def load_image(domain1, domain2):
	try:
		url1 = domain1
		url2 = "http://www.google.com/s2/favicons?domain=" + domain2

		try:
			img_data1 = requests.get(url1).content
			with open('images/img_data1.ico', 'wb') as handler:
			    handler.write(img_data1)
			res = convertIcotoPng()
			if(res == 0):
				return 0

			image1 = cv2.imread("images/img_data1.png")
			image2 = cv2.imread("images/notAvailableIcon.jpg")

			# convert the images to grayscale
			image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
			image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
			print(compare_images(image1, image2))
			if(compare_images(image1, image2) == 1):
				return 0
		except:
			return 0

		img_data2 = requests.get(url2).content
		with open('images/img_data2.png', 'wb') as handler:
		    handler.write(img_data2)
			
		image1 = cv2.imread("images/img_data1.png")
		image2 = cv2.imread("images/img_data2.png")

		# convert the images to grayscale
		image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
		image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
		# compare the images
		return compare_images(image1, image2)
	except:
		return 0

def parseURL(currentWebsite):
    try:
        parsedUrl = get_tld(currentWebsite, as_object = True, fix_protocol = True)
        if(parsedUrl.subdomain == ""):
            return parsedUrl.tld
        else:
            return parsedUrl.tld 	#parsedUrl.subdomain + "." + 
    except:
        if('http://' in currentWebsite or 'https://' in currentWebsite):
            parsedUrl1 = urlparse(currentWebsite)
            if(parsedUrl1.netloc.split("/")[0].replace(".","").isnumeric()):
                return parsedUrl1.netloc.split("/")[0]
        else:
            return currentWebsite.split("/")[0]

def search_google_query(query):
	indexingList = []
	print(query)
	for j in search(query, tld="co.in", num=5, stop=1, pause=2):
		indexingList.append(j)

	return indexingList

def title_indexing(BASE_URL):
	try:
		req = requests.get(BASE_URL)
		page = req.content

		soup = BeautifulSoup(page, "html.parser")

		try:
			title = soup.find("title").text
			indexingList = search_google_query(title)
			print(indexingList)
		except:
			indexingList = 0

		try: 
			fav = soup.find("link", {"rel": "shortcut icon"})
			faviconLink =  fav["href"]
		except:
			try:
				faviconLink = "http://www.google.com/s2/favicons?domain=" +BASE_URL
			except:
				faviconLink = 0

		return indexingList, faviconLink
	except: 
		print("Error retrieving the website")
		return 0, 0

def url_indexing(BASE_URL):
	try:
		indexingList = search_google_query(parseURL(BASE_URL))
		print(indexingList)
		return indexingList
	except:
		print("Error retrieving google url indexing list")
		return 0

def visual_action(BASE_URL):
	score1 = 0
	score2 = 0
	score3 = 0
	score4 = 0
	faviconLink = 0
	phishfound = 0

	title_list, faviconLink = title_indexing(BASE_URL)
	print("Favicon Link - " +  str(faviconLink))
	url_list = url_indexing(BASE_URL)

	if(title_list == 0):
		score1 = 0
		score3 = 0

	if(title_list != 0):
		for currentWebsite in title_list:
			if(parseURL(BASE_URL) == parseURL(currentWebsite)):
				score1 = 1
				break
			elif(faviconLink != 0):
				score1 = 0
				if(score3 == 0):
					score3 = load_image(faviconLink, currentWebsite)
				else:
					break

	if(url_list != 0):	
		for currentWebsite in url_list:
			if(parseURL(BASE_URL) == parseURL(currentWebsite)):
				score2 = 1
				break
			elif(faviconLink != 0):
				score2 = 0
				if(score4 == 0):
					score4 = load_image(faviconLink, currentWebsite)
				else:
					break

	print(score1)
	print(score2)
	print(score3)
	print(score4)

	if(score1 == 1 and score2 == 1 and score3 == 0 and score4 == 0 ):
		return 1

	if(score1 == 0 and score2 == 1 and score3 == 0 and score4 == 0 ):
		return 1
		
	if(score1 == 1 and score2 == 0 and score3 == 0 and score4 == 0 ):
		return 1	

	if(score1 == 0 and score2 == 0 and score3 == 1 and score4 == 1 ):
		return -1

	if(score1 == 0 and score2 == 0 and score3 == 1 and score4 == 0 ):
		return -1

	if(score1 == 0 and score2 == 0 and score3 == 0 and score4 == 1 ):
		return -1

	if(score1 == 0 and score2 == 0 and score3 == 0 and score4 == 0 ):
		return -1



#BASE_URL = "http://secure-support-paypl.com/V4/myaccount/websc_login/?country.x=IN&locale.x=en_IN"
#BASE_URL = "http://www.sapnapavbhaji.com"

#print("visual result - " + str(visual_action(BASE_URL)))

#print(parseURL("https://www.airbnb.co.in/help/article/380/how-do-i-book-a-place-on-airbnb"))

#print(load_image("https://www.jggjjgon.ico", BASE_URL))


#BASE_URL = "https://www.google.com"
"""
req = requests.get(BASE_URL)
page = req.content

soup = BeautifulSoup(page, "html.parser")

title = soup.find("title").text
print(title + "\n")

fav = soup.find("link", {"rel": "shortcut icon"})
print(fav["href"])
"""
