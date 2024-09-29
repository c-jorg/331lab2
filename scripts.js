function getEncrypt(callback){
	var key = document.getElementById("enkey").value;
	var plaintext = document.getElementById("plain").value
	var xmlHttp = new XMLHttpRequest();
	
	xmlHttp.open("GET", "http://127.0.0.1:8080/encrypt?key=" + key + "&plaintext=" + plaintext, true);
	xmlHttp.send('null');
	
	xmlHttp.onreadystatechange = function(){
	if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
		callback(xmlHttp.responseText);
	}
}

}

function callEncrypt(){
	console.log("getEncrypt function called");
	getEncrypt(function(response){
		var insertionPoint = document.getElementById("inputText");
		insertionPoint.innerHTML = response;
		console.log(insertionPoint.inne)
		console.log(response);
	});
}

function getDecrypt(callback){
	var key = document.getElementById('dekey').value;
	var ciphertext = document.getElementById('cipher').value;
	var xmlHttp = new XMLHttpRequest();
	
	xmlHttp.open("GET", "http://127.0.0.1:8080/decrypt?key=" + key + "&ciphertext=" + ciphertext, true);
	xmlHttp.send('null')
	
	xmlHttp.onreadystatechange = function(){
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200){
			callback(xmlHttp.responseText);
		}
	}
}

function callDecrypt(){
	getDecrypt(function(response){
		var insertionPoint = document.getElementById("inputText");
		insertionPoint.innerHTML = response;
	});
}