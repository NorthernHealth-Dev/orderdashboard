var chatdata = {};
var maindata = "";

function GetDataID() {
	
	const { host, hostname, href, origin, pathname, port, protocol, search } = window.location;
	const myData = search.split('?mode=');

	return myData[1];
	
}

function GetDataParm() {

	maindata = GetDataID();
	
	var turl = maindata + ".js";
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			try {
				var tdata = JSON.parse(xmlhttp.responseText);
			} catch(err) {
				console.log(err.message + " in " + xmlhttp.responseText);
				return;
			}
			ShowOrders(tdata);
		}
	};
 
    xmlhttp.open("GET", turl, true);
    xmlhttp.send();

	//var tdata = GetData(maindata);
	//ShowOrders(tdata);
		
}

function ShowDoctorPopup() {

	document.getElementById("doctor_message").style.display = "block";
	console.log("Showing doctor popup!");
		
}

function closeDoctorMsgWindow() {
	
	document.getElementById("doctor_message").style.display = "none";	
	
}

function ShowOrders(tjson) {

	var order_data = [];
	var tdata = "";
	
	//order_data[0] = "title:STEMI PowerPlan";
	//order_data[1] = "category:Laboratory";
	//order_data[2] = "order:CBC and Electrolytes";
	//order_data[3] = "note:Make sure to order the appropriate labwork";
	//order_data[4] = "order:INR";
	//order_data[5] = "order:PTT";
	
	var tHTML = "";
	var currCat = "";
	var tsentences = [];
	for (var x=0; x<tjson.length; x++) {
		let obj = tjson[x];
		if (obj.type == "title") {
			tHTML += MakeTitle(obj.data);
		}
		
		if (obj.type == "note") {
			tHTML += MakeNote(obj.data);
		}
		
		if (obj.type == "category") {
			tHTML += MakeCategory(obj.data);
			currCat = obj.data;
		}
		
		if (obj.type == "order") {
			tvalue = obj.value;
			// check if next in list is a sentence:
			var numsentence = 0;
			tsentences = [];
			var y = x + 1;
			console.log("JSON length: " + tjson.length + " and y value: " + y);

			while (y < tjson.length) {
				console.log(y);
				var obj2 = tjson[y];
				if (obj2.type == "sentence") {
					tsentences.push(obj2.data);
					numsentence += 1;
				}
				if (obj2.type != "sentence") {
					y = tjson.length + 1;
				}
				y++;
			}
			
			if (numsentence == 0) {
				tsentences = [""];
			}
			console.log("ShowOrders Order: " + obj.data);
			console.log("ShowOrders: " + tsentences);
			tHTML += MakeOrder(obj.data, tsentences, currCat, tvalue);			
		}
		
	}

	document.getElementById("order_data").innerHTML = tHTML;
	//console.log(tHTML);

	// now display the order set
	

}

function GetFontSize(tstr) {
	
	var tfont = "";
	var tlen = tstr.length;
	if (tlen > 70) {
		tfont = "font-size: 8px;"
	}
	if (tlen > 90) {
		tfont = "font-size: 7px;"
	}
	
	return tfont;
	
}

function MakeOrder(torder, tsentences, ttype, tvalue) {
	
	var tHTML = "\n";
	var orderfontsize = GetFontSize(torder);
	var ticon = "order_icon.png";
	if ((ttype == "Medication") || (ttype == "Medications")) {
		ticon = "cerner_pill.png";
	}
	
	tHTML += '		<div class="powerplan_order">' + "\n";
	if (tvalue == "checked") {
		tHTML += '			<div class="order_checkbox"><input type="checkbox" id="tcheck" name="tcheck" checked></div>' + "\n";
	}
	if (tvalue == "") {
		tHTML += '			<div class="order_checkbox"><input type="checkbox" id="tcheck" name="tcheck"></div>' + "\n";
	}
	tHTML += '			<div class="order_icon_div">' + "\n";
	tHTML += '				<img src="' + ticon + '" style="width: 16px;">' + "\n";
	tHTML += '			</div>' + "\n";
	tHTML += '			<div class="order_text" style="font-size:' + orderfontsize + 'px;">' + torder + '</div>' + "\n";
	
	// display a single order sentence or list
	if (tsentences.length == 0) {
		tHTML += '			<div class="sentence_text">' + '</div>' + "\n";		
	}

	if (tsentences.length == 1) {
		var tfont = GetFontSize(tsentences[0]);
		tHTML += '			<div class="sentence_text" style="top: -2px; ' + tfont + '">' + tsentences[0] + '</div>' + "\n";
	}
	
	if (tsentences.length > 1) {
		
		// get font size
		var tmaxlen = "";
		for (var x=0; x<tsentences.length; x++) {
			tdrop = tdrop + '<option>' + tsentences[x] + '</option>';
			if (tsentences[x].length > tmaxlen.length) {
				tmaxlen = tsentences[x];
			}
		}
		
		var tfont = GetFontSize(tmaxlen);
		var tdrop = '<select class="selectmenu" style="' + tfont + '">';
		for (var x=0; x<tsentences.length; x++) {
			tdrop = tdrop + '<option>' + tsentences[x] + '</option>';
		}
		tdrop = tdrop + '</select>';
		tHTML += '			<div class="sentence_text" style="left: 3%;"><img src="menu_arrow.png" class="sentence_arrow">' + tdrop + '</div>' + "\n";
	}

	tHTML += '		</div>' + "\n";

	return tHTML;

}

function MakeNote(tnote) {

	var tHTML = "\n";
	
	if (tnote.indexOf('&amp;#13;&amp;#10;') > -1) {tnote = tnote.replace(/\&amp;\#13;\&amp;\#10;/g, '<br>');}
	if (tnote.indexOf('&#13;&#10;&#13;') > -1) {tnote = tnote.replace(/\&\#13;\&\#10;\&\#13;/g, '<br>');}
	if (tnote.indexOf('&#13;&#10;') > -1) {tnote = tnote.replace(/\&\#13;\&\#10;/g, '<br>');}
	if (tnote.indexOf('&amp;#13;') > -1) {tnote = tnote.replace(/\&amp;\#13;/g, '');}
	if (tnote.indexOf('&#13;') > -1) {tnote = tnote.replace(/\&\#13;/g, '');}

	tHTML += '		<div class="powerplan_note">' + "\n"
	tHTML += '			<div class="order_checkbox">&nbsp;</div>' + "\n";
	tHTML += '			<div class="note_icon_div">' + "\n";
	tHTML += '				<img src="note_icon.png" style="width: 16px;">' + "\n";
	tHTML += '			</div>' + "\n";
	tHTML += '			<div class="note_text">' + tnote + '</div>' + "\n";	
	tHTML += '		</div>' + "\n";
	
	return tHTML;


}

function MakeCategory(tcat) {

	var tHTML = "\n";

	tHTML += '		<div class="powerplan_category">' + "\n";
	tHTML += '			<div><img src="triangle.png" style="width: 15px; float: left;"></div>' + "\n";
	tHTML += '			<div style="float: left; margin-top: 2px;">' + tcat + '</div>' + "\n";
	tHTML += '		</div>' + "\n";
	
	return tHTML;

}

function MakeTitle(ttitle) {

	var tHTML = "\n";

	tHTML += '		<div class="powerplan_category">' + "\n";
	tHTML += '			<div style="float: left; margin-top: 2px;"><b>' + ttitle + '</b></div>' + "\n";
	tHTML += '		</div>' + "\n";
	
	return tHTML;

}

function ShowComments() {
	
	console.clear();
	console.log("hiding comment_box");
	maindata = GetDataID();
	document.getElementById('comment_box').style.display = 'block';
	ajaxGetChat(maindata);
	
}

function CloseComments() {
	
	document.getElementById('comment_box').style.display = 'none';
	
}

function closeAddMessageWindow() {

	document.getElementById("add_message_window").style.display = "none";	

}

function showAddMessageWindow() {

	document.getElementById("add_message_window").style.display = "block";	
	const today = new Date();
	const yyyy = today.getFullYear();
	let mm = today.getMonth();
	let dd = today.getDate();
	if (dd < 10) dd = '0' + dd;
	if (mm < 10) mm = '0' + mm;
	const formattedToday = dd + '-' + mm + '-' + yyyy;
	
	document.getElementById("order_title_field").innerHTML = '';
	document.getElementById("msg_by_field").innerHTML = '';
	//document.getElementById("msg_to_field").innerHTML = '';
	document.getElementById("msg_date_field").innerHTML = '';
	//document.getElementById("message_field").innerHTML = '';
	
	document.getElementById("msg_date_field").innerHTML = formattedToday;

}

function ajaxGetChat(maindata) {
	//alert("ajaxGetChat");
	var hr2 = new XMLHttpRequest();
	var tconsole = "chat.py?mode=show&id=" + maindata;
	hr2.open("GET", tconsole, true);
	//console.clear();
	console.log(tconsole);
	hr2.setRequestHeader("Content-type", "application/json", true);
	hr2.onreadystatechange = function() {
		if (hr2.readyState == 4 && hr2.status == 200) {
			chatdata = JSON.parse(hr2.responseText);
			//console.log(hr2.responseText);
			//alert(hr2.responseText);
			ShowMessages(chatdata);
		}
	}
	hr2.send(null);
	
}

function showMsg(ttype, ttitle, tby, tto, tdate, tmessage) {

	// create message DIV
	var tclass = "message_tag";
	var class_text = "Message";
	if (ttype == "task") {
		tclass = "task_tag";
		class_text = "Task";
	}
	if (ttype == "decision") {
		tclass = "decision_tag";
		class_text = "Decision";
	}
	if (ttype == "physician") {
		tclass = "physician_tag";
		class_text = "Physician";
	}

	var tHTML = "";
	tHTML += '<div id="tmsg" class="message_text">' + "\n";
	tHTML += '	<div class="message_title">' + "\n";
	tHTML += '		<span class="' + tclass + '">' + class_text + '</span> <span style="font-size: 14px;"><b>' + ttitle + "</b></span>\n";
	tHTML += '	</div>' + "\n";
	tHTML += '	<div class="msg_line"></div>' + "\n";
	tHTML += '	<div class="message_body">' + "\n";
	tHTML += "<i><div style='position: absolute; left: 0%; color: black;'>Date: " + tdate + "</div><div style='position: absolute; left: 33%; color: black;'>From: " + tby + "</div> " + " <div style='position: absolute; left: 66%; color: black;'>To: " + tto + "</div></i>";		
	tHTML += '<br><br><span style="font-size: 14px;">' + tmessage + "</span>\n";
	tHTML += '	</div>' + "\n";
	tHTML += '</div>' + "\n";
	
	return tHTML;
		
}

// load messages
function ShowMessages(chatdata) {

	var tHTML = "";
	chatdata["chat"].forEach(function(object) {
		//console.log("Object: " + JSON.stringify(object));
		var ttitle = object.title;
		var tby = object.by;
		var tto = object.to;
		var tdate = object.date;
		var tmessage = object.message;
		var ttype = object.type;

		var titem = showMsg(ttype, ttitle, tby, tto, tdate, tmessage);
		//console.log(titem);
		tHTML += titem;
	
	});
	
	// append to main display panel
	document.getElementById("main_body_msgs").innerHTML = tHTML;

}
	
function updateMessages(tmpjson) {

	var tHTML = showMsg(tmpjson["type"], tmpjson["title"], tmpjson["by"], tmpjson["to"], tmpjson["date"], tmpjson["message"]);
	
	// append to main display panel
	document.getElementById("main_body_msgs").innerHTML += tHTML;

}

function saveChatData(tmpjson, maindata) {
	var xhr = new XMLHttpRequest();
	var url = "chat.py?mode=save&id=" + maindata + "&data=" + encodeURIComponent(JSON.stringify(tmpjson));
	xhr.open("GET", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 200) {
			//console.log("Saving conversation");
			mainjson = tmpjson;
		}
	}
	xhr.send();
	//document.location.reload(true);
	console.log(url);

}

function saveChatMessage() {
	var tmpjson = {};
	tmpjson["title"] = document.getElementById("order_title_field").innerText;
	tmpjson["by"] = document.getElementById("msg_by_field").innerText;
	tmpjson["to"] = "Everyone";		
	tmpjson["date"] = document.getElementById("msg_date_field").innerText;
	tmpjson["message"] = document.getElementById("message_field").innerText;
	tmpjson["location"] = document.getElementById("msg_location_field").innerText;	
	
	// get type from dropdown
	var e = document.getElementById("position_field");
	var value = e.value;
	tmpjson["type"] = e.options[e.selectedIndex].text;
	
	//tmpjson["type"] = "physician";
	
	//console.log(JSON.stringify(tmpjson));
	saveChatData(tmpjson, maindata);
	document.getElementById("add_message_window").style.display = "none";
	
	// update on the screen
	updateMessages(tmpjson);
	
}

// load data
GetDataParm();

