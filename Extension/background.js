/*
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.greeting == "hello")
      sendResponse({farewell: "goodbye"});
});
*/

var received = 99

chrome.runtime.onMessage.addListener(
    function(message, sender, sendResponse){
        var url = message.urls

        connect(url)

        setTimeout(() => {
            sendResponse({output: received});
        }, 30000);  


        return true;
        
    }
);
//var url = "Hey"

function connect(url){
	var ws 
    var openFlag = 0
    var host = "localhost";
    var port = 8080
    var path = "/ws"
    // create websocket instance
    ws = new WebSocket("ws://" + host + ":" + port + path);
    
    // Open Websocket callback
    ws.onopen = function(evt) { 
        openFlag = 1
        if(openFlag === 1){
            ws.send(url);    
        }
    };

    // Handle incoming websocket message callback
    ws.onmessage = function(evt) {
        console.log("Message Received: " + evt.data)
        
        if(evt.data == -1){
            alert("Potentially malicious website. Redirecting to safe area !");
            chrome.tabs.query({ active: true }, function(tabs) {
                chrome.tabs.remove(tabs[0].id);
                chrome.tabs.create({url: chrome.extension.getURL('Redirect.html')});
            });
        }    
        received = evt.data  
    };

    // Close Websocket callback
    ws.onclose = function(evt) {
        openFlag = 0
    };

    // Errors
    ws.onerror = function(evt) {
        console.log(evt)
    };
}

//create()