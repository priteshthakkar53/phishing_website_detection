window.onload = function(){
	document.getElementById("myonoffswitch").onclick = function(){
		if(this.checked){
			console.log("ON");
			chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
    		var activeTab = tabs[0];
    		chrome.tabs.sendMessage(activeTab.id, {status: "ON"});
	   		});
		}
		else{
			console.log("OFF");
			chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
    		var activeTab = tabs[0];
    		chrome.tabs.sendMessage(activeTab.id, {status: "OFF"});
	   		});
		}
	}
	
	document.getElementById("b1").onclick = function(){
		var input = document.getElementById("t1").value;
		console.log(input);
		console.log("Clicked");
		
		if(input == ""){
			console.log("Null");
		}
		else{
			console.log("Not Null");
			input = "phish-master-report//" + input;
			console.log(input);
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
		            ws.send(input);    
		        }
		    };

		    // Handle incoming websocket message callback
		    ws.onmessage = function(evt) {
		        console.log("Message Received: " + evt.data);
		        //received = evt.data  
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
	}

}

