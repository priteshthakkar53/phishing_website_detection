import pandas
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
from tld import get_tld
import datetime
from datetime import date

def scrape_alexa(website):
	data = {}
	try:
		BASE_URL = "https://www.alexa.com/siteinfo/" + website

		req = requests.get(BASE_URL)
		page = req.content

		soup = BeautifulSoup(page, "html.parser")

		#Global Rank
		global_rank = (soup.find("span", {"class": "globleRank"})).find("strong", {"class": "metrics-data align-vmiddle"}).text
		data["Global Rank"] = int(global_rank.strip())

		#Country Rank / Rank in -- country
		country = (soup.find("span", {"class": "countryRank"})).find("a").text
		country_rank = (soup.find("span", {"class": "countryRank"})).find("strong", {"class": "metrics-data align-vmiddle"}).text
		data["Rank in " + country] = int(country_rank.strip())

		#Bounce rate, Daily page views per visitor
		engagement_contents = soup.find("section", {"id": "engagement-content"}).find_all("span", {"class": "col-pad"})
		for divisions in engagement_contents:
			label = divisions.find("h4", {"class": "metrics-title"}).text.strip()
			value = divisions.find("strong", {"class": "metrics-data align-vmiddle"}).text.strip()
			data[label] = value

		#Search engine visits
		search_visit = soup.find("span", {"data-cat": "search_percent"}).find("strong", {"class": "metrics-data align-vmiddle"}).text
		data["Search Visits"] = search_visit.strip()

		#Alexa data availability
		data["Alexa Availability"] = "Yes"

	except:
		data["Alexa Availability"] = "No"
		data["Global Rank"] = "NA"
		data["Bounce Rate"] = "NA"
		data["Daily Pageviews per Visitor"] = "NA"
		data["Daily Time on Site"] = "NA"
		data["Search Visits"] = "NA"

	#print(json.dumps(data, indent = 1))
	return data	

def scrape_whois(website):
	data = {}
	data["Whois Availability"] = "No"
	data["Registration Date"] = "NA"
	data["Expiration Date"] = "NA"
	data["Updated Date"] = "NA"
	data["Whois Last Updated"] = "NA"
	try:
		BASE_URL = "https://www.whois.com/whois/" + website

		req = requests.get(BASE_URL)
		page = req.content

		# parse the html using beautiful soup and store in variable `soup`
		soup = BeautifulSoup(page, "html.parser")

		data["Registration Date"] = "0000-00-00"

		# Find the <div> of name and get its value
		info = soup.find_all("div", attrs={"class": "df-block"})
		#Domain, Registrar, Registration date, Expiration date, Updated date, etc
		for blocks in info:
			rows_info = blocks.find_all("div", attrs={"class": "df-row"})
			for row in rows_info:
				label = row.find("div",attrs={"class": "df-label"}).text.split(":")[0]
				value = row.find("div", attrs={"class": "df-value"}).text
				data[label] = value
			
		if(data["Registration Date"] == "0000-00-00"):
			info = soup.find("pre", attrs={"id": "registryData"}).text

			#Updated date
			updatedDateValue = info.split("Updated Date:")[1].split("T")[0].strip()
			data["Updated Date"] = updatedDateValue
			
			#Registration date
			registrationdateValue = info.split("Creation Date:")[1].split("T")[0].strip()
			data["Registration Date"] = registrationdateValue
			
			#Expiration date
			expirationDateValue = info.split("Registry Expiry Date:")[1].split("T")[0].strip()
			data["Expiration Date"] = expirationDateValue

		#Last updated date	
		last_updated = soup.find("span", attrs={"id": "dataAge"}).text
		data["Whois Last Updated"] = last_updated.split("Updated")[1].strip()

		#Whois data availability
		data["Whois Availability"] = "Yes"
	except:
		data["Whois Availability"] = "No"
		data["Registration Date"] = "NA"
		data["Expiration Date"] = "NA"
		data["Updated Date"] = "NA"
		data["Whois Last Updated"] = "NA"

	#print(json.dumps(data, indent = 1))
	return data

def scrape_rank2traffic(website):
	data = {}
	data["Rank2traffic Availability"] = "No"
	try:
		BASE_URL = "https://www.rank2traffic.com/" + website

		req = requests.get(BASE_URL)
		page = req.content

		soup = BeautifulSoup(page, "html.parser")
		
		info = soup.find("div", {"class": "alert alert-block alert-info"}).text
		data["Rank2traffic Availability"] = "Yes"
	except:
		data["Rank2traffic Availability"] = "No"

	#print(data["Rank2traffic Availability"])
	return data

def scrape_siterankdata(website):
	data = {}
	data["Siterankdata Availability"] = "No"
	data["Daily Unique Visitors"] = "No"
	try:
		BASE_URL = "https://www.siterankdata.com/" + website

		req = requests.get(BASE_URL)
		page = req.content

		soup = BeautifulSoup(page, "html.parser")
		
		info = soup.find("div", {"class": "col-lg-12 col-lg-offset-4"}).text
		data["Siterankdata Availability"] = "Yes"
		data["Daily Unique Visitors"] = soup.find("h3", {"class": "no-margins font-extra-bold text-success"}).text.strip() 
	except:
		data["Siterankdata Availability"] = "No"
		data["Daily Unique Visitors"] = "No"
	
	#print(data["Siterankdata Availability"])
	return data

def web_scraper(path):
	if(path == "phishing_websites_phishtank.csv"):
		df = pandas.read_csv('phishing_websites_phishtank.csv')["url"]
		df = df[0:2]
		websiteList = df.tolist()
	elif(path == "legitimate_websites.xlsx"):
		df = pandas.read_excel('legitimate_websites.xlsx', sheet_name='Sheet1')["url"]
		df = df[0:2]
		websiteList = df.tolist()
	else:
		websiteList = [path]

	list = []
	for currentWebsite in websiteList:
		row = {}
		row["Protocol"] = "NA"
		row["Path"] = "NA"
		row["IP Address"] = "NA"
		row["TLD"] = "NA"
		row["Subdomain"] = "NA"
		row["Domain"] = "NA"
		row["Suffix"] = "NA"
		row["Length"] = "NA"
		row["Dots in subdomain"] = "NA"
		row["@"] = "NA"
		row["-"] = "NA"
		row["Alexa Availability"] = "NA"
		row["Alexa Rank"] = "NA"
		row["Bounce Rate"] = "NA"
		row["Daily Pageviews per Visitor"] = "NA"
		row["Daily Time on Site"] = "NA"
		row["Search Visits"] = "NA"
		row["Whois Availability"] = "NA"
		row["Registration Date"] = "NA"
		row["Expiration Date"] = "NA"
		row["Updated Date"] = "NA"
		row["Rank2traffic Availability"] = "NA"
		row["Siterankdata Availability"] = "NA"
		row["Daily Unique Visitors"] = "NA"

		#URL Features (using urlparse)
		if('http://' in currentWebsite or 'https://' in currentWebsite):
			parsedUrl1 = urlparse(currentWebsite)
			row["Protocol"] = parsedUrl1.scheme
			if(parsedUrl1.netloc.replace(".","").isnumeric()):
				row["IP Address"] = parsedUrl1.netloc
			if(parsedUrl1.path == ""):
				row["Path"] = "NA"
			else:
				row["Path"] = parsedUrl1.path
		else:
			row["Protocol"] = "NA"
			row["Path"] = "NA"

		'''		
		domain = parsedUrl.netloc
		row["Domain"] = parsedUrl.netloc
		row["Path"] = parsedUrl.path
		row["Length"] = len(domain)
		row["Dots"] = domain.count(".")
		row["@"] = domain.count("@")
		row["-"] = domain.count("-")
		'''

		try:
			#TLD
			parsedUrl2 = get_tld(currentWebsite, as_object = True, fix_protocol = True)
			tld = parsedUrl2.tld
			row["TLD"] = tld
			subdomain = parsedUrl2.subdomain
			row["Subdomain"] = subdomain
			row["Domain"] = parsedUrl2.domain
			suffix = parsedUrl2.suffix
			row["Suffix"] = suffix
			row["Length"] = len(subdomain + tld)
			row["Dots in subdomain"] = subdomain.count(".") 
			row["@"] = subdomain.count("@") + tld.count("@")
			row["-"] = subdomain.count("-") + tld.count("-")

			#alexa.com
			alexa = scrape_alexa(tld)
			row["Alexa Availability"] = alexa["Alexa Availability"]
			#Alexa Rank
			row["Alexa Rank"] = alexa["Global Rank"]
			#Bounce Rate
			row["Bounce Rate"] = alexa["Bounce Rate"].split("%")[0]
			#Daily page views per visitor
			row["Daily Pageviews per Visitor"] = alexa["Daily Pageviews per Visitor"]
			#Daily time on site
			row["Daily Time on Site"] = alexa["Daily Time on Site"]
			#Search visits
			row["Search Visits"] = alexa["Search Visits"].split("%")[0]
			
			#whois.com
			whois = scrape_whois(tld)
			row["Whois Availability"] = whois["Whois Availability"]
			#Registration Date
			row["Registration Date"] = whois["Registration Date"]
			#Expiration Date
			row["Expiration Date"] = whois["Expiration Date"]
			#Query Website last Updation Date //Not the whois update. Its different
			row["Updated Date"] = whois["Updated Date"]

			#rank2traffic.com
			rank2traffic = scrape_rank2traffic(tld)
			row["Rank2traffic Availability"] = rank2traffic["Rank2traffic Availability"]

			#siterankdata.com
			siterankdata = scrape_siterankdata(tld)
			row["Siterankdata Availability"] = siterankdata["Siterankdata Availability"]  
			#Daily unique visitors
			row["Daily Unique Visitors"] = siterankdata["Daily Unique Visitors"]
		except:
			print("TLD error")

		list.append(row)


	columnList = ["Protocol","Path","IP Address","TLD","Subdomain","Domain","Suffix","Length","Dots in subdomain","@","-",
				"Alexa Availability", "Alexa Rank","Bounce Rate","Daily Pageviews per Visitor",
				"Daily Time on Site", "Search Visits","Whois Availability","Registration Date","Expiration Date",
				"Updated Date","Rank2traffic Availability","Siterankdata Availability", "Daily Unique Visitors"]

	if(len(list)>1):
		if(path == "phishing_websites_phishtank.csv"):
			pandas.DataFrame(list,columns=columnList).to_csv("phishing_webscraped.csv")
			#sorted_data = pandas.DataFrame(list,columns=columnList).sort_values("Domain").to_csv("sorted.csv")
		elif(path == "legitimate_websites.xlsx"):
			pandas.DataFrame(list,columns=columnList).to_csv("legitimate_webscraped.csv")
	else:
		pandas.DataFrame(list,columns=columnList).to_csv("user_query_webscraped.csv")
		
def training_setup(path):
	if(path == "phishing_webscraped.csv"):
		filedf = pandas.read_csv('phishing_webscraped.csv')
	elif(path == "legitimate_webscraped.csv"):
		filedf = pandas.read_csv('legitimate_webscraped.csv')
	else:
		filedf = pandas.read_csv('user_query_webscraped.csv')

	filedf = filedf.fillna(value = "NA")
	newdf = pandas.DataFrame(data=None, index=None, columns=None)


	#Protocol
	def protocolFunction(x):
		if(x == 'https'):
			return 1
		elif(x == 'http'):
			return 0
		else: 
			return 0
	    
	newdf['Protocol'] = filedf['Protocol'].apply(lambda x: protocolFunction(x))

	#Length
	def lengthFunction(x):
		if(x == "NA" or x == "No" or x =="NaN"):
			return -1
		if(x >= 3 and x <= 20):
			return 1
		elif(x > 20 and x < 24):
			return 0
		elif(x >= 24):
			return -1

	newdf['Length'] = filedf['Length'].apply(lambda x: lengthFunction(x))	

	#Hypen (-)
	def hyphenFunction(x):
		if(x == "NA" or x == "No" or x =="NaN"):
			return -1
		if(x == 0):
			return 1
		elif(x >= 1):
			return -1

	newdf['-'] = filedf['-'].apply(lambda x: hyphenFunction(x))	

	#atTheRate (@)
	def atTheRateFunction(x):
		if(x == "NA" or x == "No" or x =="NaN"):
			return -1
		if(x == 0):
			return 1
		elif(x >= 1):
			return -1

	newdf['@'] = filedf['@'].apply(lambda x: atTheRateFunction(x))	

	#Dots (.)
	def dotFunction(x):
		if(x == "NA" or x == "No" or x =="NaN"):
			return -1
		if(x < 1):
			return 1
		elif(x > 0):
			return -1

	newdf['Dots'] = filedf['Dots in subdomain'].apply(lambda x: dotFunction(x))

	#In Domain Https or Https
	def inDomainHttpFunction(x):
		if('http' in x):
			return -1
		else:
			return 1

	newdf['In Domain Http'] = filedf['Subdomain'].apply(lambda x: inDomainHttpFunction(x))

	#IP address format
	def isIpAddressFunction(x):
		if(x =="NA" or x == "NaN"):
			return 1
		else:
			return -1

	newdf['Is IP Address'] = filedf['IP Address'].apply(lambda x: isIpAddressFunction(x))

	#Analysed Harmful Domains [Manual]
	harmfulHosts = ["000webhostapp.com","sites////google.com","panicimis","beget.tech","libero.it",
					"www.paypal.com.cgi-bin.webscr.ikubiak////webd.pl", "jidrex.cz", "jhanjartv.com",
					"someakenya.com", "cort.as"]
	def isHarmfulHostFunction(x):
		for harm in harmfulHosts:
			if(harm in x):
				subdom = x.split("////")[0]
				tldom = x.split("////")[1]
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), 'Alexa Availability'] = "No"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), 'Alexa Rank'] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), 'Bounce Rate'] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Daily Pageviews per Visitor"] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Daily Time on Site"] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Search Visits"] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Whois Availability"] = "No"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Registration Date"] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Expiration Date"] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Updated Date"] = "NA"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Rank2traffic Availability"] = "No"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Siterankdata Availability"] = "No"
				filedf.loc[((filedf["TLD"] == tldom) & (filedf["Subdomain"] == subdom)), "Daily Unique Visitors"]	= "No"    
				return -1
			else:
				return 0
	
	newdf['Harmful Host'] = (filedf["Subdomain"]+ "////" + filedf["TLD"]).apply(lambda x: isHarmfulHostFunction(x))

	#Alexa Availability
	def alexaAvailabillityFunction(x):
		if(x == "Yes"):
			return 1
		else:
			return 0

	newdf['Alexa Availability'] = filedf["Alexa Availability"].apply(lambda x: alexaAvailabillityFunction(x))

	#Alexa Rank
	def alexaRankFunction(x):
		if(x == "NA"):
			return 0
		else:
			return 1

	newdf['Alexa Rank'] = filedf["Alexa Rank"].apply(lambda x: alexaRankFunction(x))

	#Whois Availability
	def whoisAvailabillityFunction(x):
		if(x == "Yes"):
			return 1
		else:
			return -1

	newdf['Whois Availability'] = filedf["Whois Availability"].apply(lambda x: whoisAvailabillityFunction(x))

	#Whois time difference
	def differ_days(date1, date2):
		a = date1
		b = date2
		return (a-b).days

	def timeDifferenceFunction(x):
	    x = str(x)
	    if(x=="NaN" or x=="NA"):
	        return -1
	    elif(x.replace("-","").isnumeric()):
	        D1 = int(x.split("-")[2])
	        D2 = int(x.split("-")[5])
	        M1 = int(x.split("-")[1])
	        M2 = int(x.split("-")[4])
	        Y1 = int(x.split("-")[0])
	        Y2 = int(x.split("-")[3])
	        try:
	            diff = differ_days((date(Y1,M1,D1)), date(Y2,M2,D2))
	            if(diff>90):
	                return 1
	            else:
	                return 0
	        except:
	            return 0
	    else: 
	        return 0
	
	newdf["Whois Time Difference"] = (filedf["Expiration Date"] + "-" + filedf["Registration Date"]).apply(lambda x: timeDifferenceFunction(x))

	#Rank2traffic Availability
	def rank2trafficAvailabilityFunction(x):
		if(x == "Yes"):
			return 1
		else:
			return -1

	newdf['Rank2traffic Availability'] = filedf["Rank2traffic Availability"].apply(lambda x: rank2trafficAvailabilityFunction(x))

	#
	def siterankdataAvailabilityFunction(x):
		if(x == "Yes"):
			return 1
		else:
			return -1

	newdf['Siterankdata Availability'] = filedf["Siterankdata Availability"].apply(lambda x: siterankdataAvailabilityFunction(x))

	def dailyUniqueVisitorsFunction(x):
		if(x == "No" or x == "NA"):
			return -1
		else:
			return 1

	newdf['Daily Unique Visitors'] = filedf["Daily Unique Visitors"].apply(lambda x: dailyUniqueVisitorsFunction(x))


	if(path == "phishing_webscraped.csv"):
		newdf['Result'] = -1
		newdf.to_csv('phishing_train.csv')
	elif(path == "legitimate_webscraped.csv"):
		newdf['Result'] = 1
		newdf.to_csv('legitimate_train.csv')
	else:
		newdf.to_csv('user_query_predict.csv')



#web_scraper("phishing_websites_phishtank.csv")
#web_scraper("legitimate_websites.xlsx")
	
#training_setup("phishing_webscraped.csv")
#training_setup("legitimate_webscraped.csv")

#web_scraper("sapnapavbhaji.com")
#training_setup("user_query_predict.csv")