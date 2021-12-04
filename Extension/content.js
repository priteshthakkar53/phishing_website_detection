var flag="ON";


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse){
    flag = message.status;
    //alert(flag);
    console.log(flag);
    });

if(flag=="ON"){
	var url
	window.onload = function() {
        url = window.location.href
        console.log("content - " + url);
        
        chrome.runtime.sendMessage({from: 'content', urls: url}, function(response) {
                console.log("Final Result")
                console.log(response.output);

                if(response.output == -1){
                    console.log("Blocked");
                }

        });
	}
/*
	function redirect(){
		window.location = "https://www.google.com";
	}*/
	console.log("ON");
}
else{
	console.log("OFFF");
}



 
/*
function download_csv(){
    var csv = "URL\n";
    url.forEach(function(row){
        csv += row.join(",");
        csv += "\n";
    });
    //console.log(csv);
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'url.csv';
    hiddenElement.click();
}
*/
//download_csv();
//create()




    /*var queryInfo = {
        active: true,
        currentWindow: true
    };     
*/
//chrome.tabs.onCreated.addListener(function(tab) {
/*
chrome.tabs.query(queryInfo, function(tabs){
        // chrome.tabs.query invokes the callback with a list of tabs that match the query. A window can only have one active tab at a time, so the array consists of exactly one tab.
        var flag = 0; // 0 - nothing, 1 - onUpdated(), 2 - onCreate()  
        var tab = tabs[0];
        //var url = tab.url;              //url

        //EXPORTING URL AS CSV FILE
        var url = [[tab.url]];
          
        function download_csv(){
            var csv = "URL\n";
            url.forEach(function(row){
                csv += row.join(",");
                csv += "\n";
            });
            //console.log(csv);
            var hiddenElement = document.createElement('a');
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
            hiddenElement.target = '_blank';
            hiddenElement.download = 'url.csv';
            hiddenElement.click();
        }

        download_csv();
*/
/*
        chrome.tabs.onActivated.addListener(function(info) {
            flag = 1;
            try{
                chrome.tabs.executeScript(null, { code: 'console.log("First!! ");' });
            }catch(e){
                console.log(e)
            }

        });
        console.log(flag);

        chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
            flag = 2;
            try{
                chrome.tabs.executeScript(null, { code: 'console.log("Second!! ");' });
            }catch(e){
                console.log(e)
            }

        });
        console.log(flag);
        
        chrome.tabs.onCreated.addListener(function(tab) {
            flag = 3;
            try{
                chrome.tabs.executeScript(null, { code: 'console.log("Third!! ");' });
            }catch(e){
                console.log(e)
            }

        });
        console.log(flag);
*/
        //var urlObject = parseUrl(url);
        //console.log(urlObject.protocol);
        //var title = tab.title;          //title
        //var iconurl = tab.favIconUrl;   //icon
        //document.getElementById("ff").textContent = url;
        

        //document.write(url+"<br>"+title+"<br>"+iconurl);
/*
        // Splitting url                    eg. url = https://www.google.com
        var url1 = url.split(":");          //we get [https, //www.google.com]

        var url2 = url1[1].split("/");      //we get [,,www.google.com]

        var url3 = url2[2].split(".");      //we get [www,google,com]

        var  splitUrl = [];
        splitUrl[0] = url1[0];              //https
          
        for(var i=0;i<url3.length;i++){
            if(url3[i] == "www"){
                splitUrl[1] = url3[i];
                url3.splice(i,1);
            }else if(url3[i] == "in"){
                splitUrl[2] = url3[i];
                url3.splice(i,1);
            }
        }

        console.log(url3);
        console.log(splitUrl);
        console.assert(typeof url == 'string', 'tab.url should be a string');
*/
//});

  /* Most methods of the Chrome extension APIs are asynchronous. This means that you CANNOT do something like this:
    var url;
    chrome.tabs.query(queryInfo, (tabs) => {
    url = tabs[0].url;
    });
    alert(url);
  Shows "undefined", because chrome.tabs.query is async.
*/
