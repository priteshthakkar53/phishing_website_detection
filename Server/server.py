import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
from tld import get_tld
import algorithm
import data_preprocessing
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from urllib.parse import urlparse
import visual

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')

    def on_message(self, message):
        print('message received:  %s' % message)

        if("phish-master-report//" in message):
            message = message.split("phish-master-report//")[1]
            file = open("reporting_log.txt","a+") 
            file.write(message)
            file.write("\n")
            file.close()
            self.write_message("5")
        else:
            result = str(operations(message))
            print('sending back result: %s' % result)
            self.write_message(result)

    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True


def predict_user_query():
    data = pd.read_csv("user_query_predict.csv")

    #Load the data to predict
    X = data[['Protocol', 'Length', '-', '@', 'Dots', 'In Domain Http',
       'Is IP Address', 'Harmful Host', 'Alexa Availability', 'Alexa Rank',
       'Whois Availability', 'Rank2traffic Availability',
       'Siterankdata Availability', 'Daily Unique Visitors']]

    print()
    #Predict the user query using the trained logistic regression classifier
    user_predictions = classifier1.predict(X)
    print("Prediction using Logistic Regression : " + str(int(user_predictions[0])))
    logisticRegressionPrediction = int(user_predictions[0])
    print()
    #Predict the user query using the trained decision tree classifier
    user_predictions = classifier2.predict(X)
    print("Prediction using Decision Tree : " + str(int(user_predictions[0])))
    decisionTreePrediction = int(user_predictions[0])
    #Predict the user query using the trained Random Forest classifier
    user_predictions = classifier3.predict(X)
    print("Prediction using Random Forest : " + str(int(user_predictions[0])))
    randomForestPrediction = int(user_predictions[0])
    print()

    return logisticRegressionPrediction, decisionTreePrediction, randomForestPrediction 

def parseURL(currentWebsite):
    try:
        parsedUrl = get_tld(currentWebsite, as_object = True, fix_protocol = True)
        if(parsedUrl.subdomain == ""):
            return parsedUrl.tld
        else:
            return parsedUrl.subdomain + "." + parsedUrl.tld
    except:
        if('http://' in currentWebsite or 'https://' in currentWebsite):
            parsedUrl1 = urlparse(currentWebsite)
            if(parsedUrl1.netloc.split("/")[0].replace(".","").isnumeric()):
                return parsedUrl1.netloc.split("/")[0]
        else:
            return currentWebsite.split("/")[0]

def serach_phishlist(current):
    df2 = pd.read_csv('phishing_websites_phishtank.csv')["url"]
    websiteList2 = df2.tolist()     
    for i in websiteList2:
        if(current in i):
            return -1
    return 0

def findInList(current):
    harmfulHosts = ["000webhostapp.com","sites.google.com","panicimis","beget.tech","libero.it",
                    "www.paypal.com.cgi-bin.webscr.ikubiak.webd.pl", "jidrex.cz", "jhanjartv.com",
                    "someakenya.com", "cort.as"]
    for harm in harmfulHosts:
        if((harm in current)):
            if(serach_phishlist(current) == -1):
                return -1


    df1 = pd.read_csv('top-1m.csv')["Website"]
    websiteList1 = df1.tolist()
    try:
        parsedUrl = get_tld(current, as_object = True, fix_protocol = True)
        current = parsedUrl.tld
        for i in websiteList1:
            if(current in i):
                return 1
    except: #For IP
        if(serach_phishlist(current) == -1):
            return -1
        return 1 

    if(serach_phishlist(current) == -1):
        return -1

    return 0

def operations(message):
    result = findInList(parseURL(message))
    if(result == 1):
        return result
    elif(result == -1):
        return result
    else:
        #try:
        data_preprocessing.web_scraper(message)
        data_preprocessing.training_setup("user_query_predict.csv")

        lrPrediction, dtPrediction, rfPrediction = predict_user_query() 

        visualPrediction = visual.visual_action(message)

        if(lrPrediction == 1 and visualPrediction == 1):
            return 1
        elif(lrPrediction == 1 and visualPrediction == -1):
            return -1
        elif(lrPrediction == -1 and visualPrediction == 1):
            return 1
        elif(lrPrediction == -1 and visualPrediction == -1):
            return -1
        #except:
        #    return 0

application = tornado.web.Application([
    (r'/ws', WSHandler),
])

#Program starts __main__
classifier1 = algorithm.train_logistic_regressing()
classifier2 = algorithm.train_decision_tree()
classifier3 = algorithm.train_random_forest()

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8080)
myIP = socket.gethostbyname(socket.gethostname())
#socket.gethostname() return Vaibhav-PC
#socket.gethostbyname(socket.gethostname()) returns Ip address 
print()
print ('******Websocket Server Started at %s******' % myIP)
try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    tornado.ioloop.IOLoop.instance().stop()
    print("Exit Success")