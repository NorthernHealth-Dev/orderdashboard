var chatdata = {};
function ajaxGetChat(tid) {
	var hr2 = new XMLHttpRequest();
	hr2.open("GET", "chat.py?mode=show&id=" + tid, true);
	console.log("chat.py?mode=show&id=" + tid);
	hr2.setRequestHeader("Content-type", "application/json", true);
	hr2.onreadystatechange = function() {
		if (hr2.readyState == 4 && hr2.status == 200) {
			chatdata = JSON.parse(hr2.responseText);
			console.log(hr2.responseText);
			alert(hr2.responseText);
			//ShowMessages(tid, chatdata);
		}
	}
}

// call function
ajaxGetChat('XHB7HS');

