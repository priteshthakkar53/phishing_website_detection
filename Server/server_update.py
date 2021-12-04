import urllib.request
import time
import os
import data_preprocessing

def download():
	app_key = 'c1ad036f76191835f68ccff17f3a29f84ef565dc237b80de699735d869f14402';   #Phishtank Application Key
	url = "http://data.phishtank.com/data/"+ app_key + "/online-valid.csv"
	
	print("Processing new file download")

	with urllib.request.urlopen(url) as temporary_data, open('phishing_websites_phishtank.csv', 'w') as permanent_data:
		permanent_data.write(temporary_data.read().decode())

	print("File download complete")

def delete_file():
	os.remove("phishing_websites_phishtank.csv")
	print("-->phishing_websites_phishtank.csv file removed")  
	print()  

def run_update():
	sleep_time = 1 * 60  # in seconds
	while(True):
		download()
		

		# wait for sleep_time seconds
		time.sleep(sleep_time) 
		delete_file()

#run_update()

data_preprocessing.web_scraper("phishing_websites_phishtank.csv")
data_preprocessing.web_scraper("legitimate_websites.xlsx")

data_preprocessing.training_setup("phishing_webscraped.csv")
data_preprocessing.training_setup("legitimate_webscraped.csv")

