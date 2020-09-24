$(document).ready(function () {
	document.getElementById("clear").addEventListener('click',function (){
		document.getElementById("result_div").innerHTML = "";
	});
	
	$('#chat-input').on('keyup keypress', function (e) {
		var keyCode = e.keyCode || e.which;
		var text = $("#chat-input").val();
		if (keyCode === 13) {
			if (text == "" || $.trim(text) == '') {
				e.preventDefault();
				return false;
			} else {
				$("#chat-input").blur();
				setUserResponse(text);
				send(text);
				e.preventDefault();
				return false;
			}
		}
	});
	document.getElementById("send").addEventListener('click',function (){
		var text = $("#chat-input").val();
		setUserResponse(text);
		send(text);
		$('.suggestion').remove();
	});

})

function getID() {
	return Math.random().toString(36).replace(/[^a-z]+/g, '').substr(2, 10);
}

//------------------------------------------- Call the RASA API--------------------------------------
function filesend() {
	const myform=document.getElementById('uploadfiletorasa');
	const selectedFile=document.getElementById('record').files[0];
	const endpoint = "/rasa";
	const data = new FormData();
	data.append('file', selectedFile)
	console.log(selectedFile)
	console.log(data)
//	(async function(){
	myform.addEventListener("submit", e => {
		e.preventDefault();
		
		let response=fetch(endpoint,{
			method: "POST",
			body: data
		}).catch(setBotResponse('error'));
		console.log(response)
		});
//	})
	
}

function send(text) {
	(async function() {
		try{
			let response = await fetch('/rasa', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: text}),
				redirect: 'manual'
			});
			response = await response.json();
			console.log(response);
			setBotResponse(response);
		} catch {
			console.log('Error in Operation');
			setBotResponse('error');
		}
	})();
}

function setAttributes(el, attrs) {
	for(var key in attrs) {
	  el.setAttribute(key, attrs[key]);
	}
  }


function createButton(text, attributes){
	let button = document.createElement("button");
	button.innerHTML = text;
	setAttributes(button, attributes);
	return button
}

function createModalBase(style, id, attributes){
	let modal = createDiv(style, id);
	setAttributes(modal, attributes);
	return modal
}

function createModal(eid){
	
	let main = createModalBase(style=["modal" , "fade"], id= eid, {'tabIndex':-1, 
										"role":"dialog","aria-labelledby":"myModalLabel", "aria-hidden":true});
	let head = createModalBase(style=["modal-dialog","modal-lg","modal-dialog-centered"], id=eid, {"role":"document"});
	let body = createDiv(["modal-content"])
	let section1 = createDiv(["modal-body"])
	let frame = createDiv(["embed-responsive", "embed-responsive-16by9", "z-depth-1-half"])
	let section2 = createDiv(["modal-header"])
	setAttributes(section2,{"style":"background: darkgray;"})
	let innerButton = createButton("", {"type":"button", "class": "close",
													"data-dismiss":"modal","aria-label":"Close"});
	let close =createSpan(style=["close"], text="&times;");
	innerButton.appendChild(close);
	section2.appendChild(innerButton);
	return {main, head, body, section1, frame, section2}
}
function createModalscrollable(title, eid){
	
	let main = createModalBase(style=["modal" , "fade"], id=eid, {'tabIndex':-1, 
										"role":"dialog","aria-labelledby":"myModalLabel", "aria-hidden":true });
	let head = createModalBase(style=["modal-dialog","modal-lg","modal-dialog-centered","modal-dialog-scrollable"], id=eid, {"role":"document"});
	let body = createDiv(["modal-content"])
	let section1 = createDiv(["modal-body"])
	setAttributes(section1,{"style":"font-size: 20px;"})
	let section2 = createDiv(["modal-header"])
	let title1 =createSpan(style=["title-one"], text=title);
	setAttributes(title1,{"style":"font-size: 25px;"})
	let innerButton = createButton("", {"type":"button", "class": "close",
													"data-dismiss":"modal","aria-label":"Close"});
	let close =createSpan(style=["close"], text="&times;");
	innerButton.appendChild(close);
	section2.append(title1,innerButton);
	return {main, head, body, section1, section2}
}

function createDiv(style = [], id = "", text = ""){
	let element = document.createElement('div');
	if(style.length > 0){
		element.classList.add(...style)
	}
	if(id != ""){
		element.id = id;
	}
	if(text != ""){
		element.innerHTML = text;
	}
	return element
}

function createImage(src="", style = "" ){
	let img = document.createElement("img");
	img.src = src;
	img.classList.add(...style);
	return img
}
function createSpan(style, text){
	let element = document.createElement('span');
	element.classList.add(...style)
	element.innerHTML = text;
	return element
}
function createIframe(url){
	let video = document.createElement('iframe');
	let style = ["embed-responsive-item"]
	video.classList.add(...style)
	video.src = url;
	video.height = "480";
	video.width = "720";
	video.frameBorder = "0";
	//video.allow = "autoplay; fullscreen";
	video.id = "iframe";
	return video
}
function createMap(){
	console.log(document.getElementById("gmaps"));
	if (document.getElementById("gmaps") == null){
		console.log("create script tag....");
		let script = document.createElement("script");
		let key = document.getElementById("key").innerHTML;
		script.src = `https://maps.googleapis.com/maps/api/js?key=${key}&libraries=places&callback=initMap`;
		script.defer = true;
		script.async = true;
		script.id = "gmaps";
		document.head.appendChild(script);

	}
}
function createBaseChat(){
	let main = createDiv(["d-flex", "justify-content-start", "reply" ]);
	let first = createDiv(["img_cont_msg"])
	let image = createImage("https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg", ["rounded-circle" ,"user_img_msg"])
	first.appendChild(image);
	main.appendChild(first);
	return main
}



//------------------------------------ Set bot response in result_div -------------------------------------
function setBotResponse(val) {
	let today = new Date();
	let time = today.getHours() + ":" + today.getMinutes() ;
	(async function () {

		if ($.trim(val) == '' || val == 'error') { //if there is no response from bot or there is some error
			let error = 'Sorry I wasn\'t able to understand your Query. Let\' try something else!'
			let base = createBaseChat();
			let response = createDiv(style=["msg_cotainer"], id="", text=error);
			let timespan = createSpan(style=["msg_time"], text=time);
			response.appendChild(timespan)
			base.appendChild(response)
			var BotResponse = base
			$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
		} else {
			for (var i in val) {
				let vid = getID()
				if (val[i].hasOwnProperty("image")) {
					let base = createBaseChat();
					let url = `data:image/png;base64,${val[i].image}`
					let img = createImage(src=url)
					let { main, head, body, section1, frame, section2} = createModal(vid)
					let outerButton = createButton("Please click here to see the quote", {"type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;","data-toggle":"modal","data-target":`#${vid}`});
					let response = createDiv(style=["msg_cotainer1"], id="", text = "");
					let timespan = createSpan(style=["msg_time"], text=time);
					setAttributes(section1,{"style":"padding:0rem;font-size: 20px;"})
					img.height = 480;
					img.width = 798;	
					setAttributes(img,{"class":"responsive"})	
					section1.appendChild(img);
					body.append(section2, section1)
					head.appendChild(body);
					main.appendChild(head);	
					response.append(outerButton,timespan, main);
					base.appendChild(response)
					BotResponse = base;
					$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);

				} else if (val[i].hasOwnProperty("buttons")) {
					console.log("in bot reposne", val[i])
					await addSuggestion(val[i]);
				} 
				else if (val[i].hasOwnProperty("custom")) {
					if (val[i].custom.payload == "video") {
						let url = (val[i].custom.data);
						let base = createBaseChat();
						let { main, head, body, section1, frame, section2} = createModal(vid)
						let outerButton = createButton("Please click here to see the video", {"type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;","data-toggle":"modal","data-target":`#${vid}`});
						let response = createDiv(style=["msg_cotainer1"], id="", text = "");
						let iframe = createIframe(url);
						let timespan = createSpan(style=["msg_time"], text=time);
						setAttributes(section1,{"style":"padding:0rem;"})
						setAttributes(iframe,{"class":"responsive"})
						frame.appendChild(iframe);
						section1.appendChild(frame);
						body.append(section2, section1)
						head.appendChild(body);
						main.appendChild(head);
						response.append(outerButton,timespan, main);
						base.appendChild(response)
						BotResponse = base;						
						$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
					}
					if (val[i].custom.payload == "map") {
						let base = createBaseChat();
						let { main, head, body, section1, frame, section2} = createModal(vid)
						let outerButton = createButton("Please click here to see the map", {"type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;","data-toggle":"modal","data-target":`#${vid}`});
						let map = createDiv(style=[], id="map")
						let response = createDiv(style=["msg_cotainer1"], id="", text = "");
						map.style = "height: 480px; width: 798px;"
						setAttributes(section1,{"style":"padding:0rem;font-size: 20px;"})
						setAttributes(map,{"class":"responsive"})
						section1.appendChild(map);
						body.append(section2, section1)
						head.appendChild(body);
						main.appendChild(head);
						response.append(outerButton, main);
						base.appendChild(response)
						BotResponse = base;
						$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
						createMap()

					}
					//check if the custom payload type is "chart"
						if (val[i].custom.payload == "chart") {
						// sample format of the charts data:
						// var chartData = { "title": "Leaves", "labels": ["Sick Leave", "Casual Leave", "Earned Leave", "Flexi Leave"], "backgroundColor": ["#36a2eb", "#ffcd56", "#ff6384", "#009688", "#c45850"], "chartsData": [5, 10, 22, 3], "chartType": "pie", "displayLegend": "true" }
						//store the below parameters as global variable, 
						// so that it can be used while displaying the charts in modal.
						chartData = (val[i].custom.data)
						title = chartData.title;
						labels = chartData.labels;
						backgroundColor = chartData.backgroundColor;
						chartsData = chartData.chartsData;
						chartType = chartData.chartType;
						displayLegend = chartData.displayLegend;
						// pass the above variable to createChart function
						createChart(title, labels, backgroundColor, chartsData, chartType, displayLegend)
						return;
					}

					if (val[i].custom.payload == "symptom") {
						let base = createBaseChat();
						let response = createDiv(style=["msg_cotainer1"], id="", text = "");
						let timespan = createSpan(style=["msg_time"], text=time);
						console.log(val[i].custom.payload);
						let { main, head, body, section1, section2} = createModalscrollable(val[i].custom.data.name, vid)
						let outerButton = createButton(`Click here to know more about ${val[i].custom.data.name}`, {"type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;","data-toggle":"modal","data-target":`#${vid}`});
						let listElement = document.createElement('div');
						let x = document.createElement("A");
						setAttributes(x,{"class":"btn btn-primary btn-lg btn-block","style":"margin-bottom: 10px;", "data-toggle":"collapse","href":"#desc", "role":"button", "aria-expanded":"false" ,"aria-controls":"desc"})
						x.innerHTML=' Description ';
						let y = document.createElement("A");
						setAttributes(y,{"class":"btn btn-primary btn-lg btn-block","style":"margin-bottom: 10px;", "data-toggle":"collapse","href":"#cause", "role":"button", "aria-expanded":"false" ,"aria-controls":"cause" })
						y.innerHTML=' Causes of this symptom ';
						let z = document.createElement("A");
						setAttributes(z,{"class":"btn btn-primary btn-lg btn-block","style":"margin-bottom: 10px;", "data-toggle":"collapse","href":"#treatment", "role":"button", "aria-expanded":"false" ,"aria-controls":"treatment" })
						z.innerHTML=' Treatment ';
						//desc
						let list = createDiv(style=["collapse"], id="desc", text = "");
						setAttributes(list,{"style":"margin-bottom: 10px;"})
						let para = document.createElement("p");
						let node = document.createTextNode(val[i].custom.data.desc);
						para.appendChild(node);
						list.appendChild(para);						
						// cause
						let list1 = createDiv(style=["collapse"], id="cause", text = "");
						setAttributes(list,{"style":"margin-bottom: 10px;"})
						let para1 = document.createElement("p");
						let node1 = document.createTextNode(val[i].custom.data.causes);
						para1.appendChild(node1);
						list1.appendChild(para1);						
						// treatment
						let list2 = createDiv(style=["collapse"], id="treatment", text = "");
						setAttributes(list,{"style":"margin-bottom: 10px;"})
						let para2 = document.createElement("p");
						let node2 = document.createTextNode(val[i].custom.data.treatment);
						para2.appendChild(node2);
						list2.appendChild(para2);							
						
						listElement.append(x,list,y,list1,z,list2);;
						section1.append(listElement);
						body.append(section2, section1)
						head.appendChild(body);
						main.appendChild(head);
						response.append(outerButton,timespan, main);
						base.appendChild(response)
						BotResponse = base;
						$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
					}

					if (val[i].custom.payload == "fileupload") {
						let base = createBaseChat();
						let response = createDiv(style=["msg_cotainer1"], id="", text = "");
						let timespan = createSpan(style=["msg_time"], text=time);
						let { main, head, body, section1, frame, section2} = createModal(vid)
						let outerButton = createButton("Please click here to upload the file", {"type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;","data-toggle":"modal","data-target":`#${vid}`});
						setAttributes(section1,{"style":"font-size: 20px;"})
						let formElement = document.createElement('div');
						formElement.innerHTML =`<form id=\"uploadfiletorasa\"><div class=\"form-group\"><label for=\"recipient-name\" class=\"col-form-label\"> Report Upload : </label><input type=\"file\" id=\"record\" name=\"file"\ /></div>
												<button type=\"submit\" class=\"btn btn-primary btn-lg btn-block\" id=\"but_upload\" onclick=\"filesend()\"> Upload </button></form>` ;
						section1.appendChild(formElement);
						body.append(section2, section1)
						head.appendChild(body);
						main.appendChild(head);
						response.append(outerButton,timespan, main);
						base.appendChild(response)
						BotResponse = base;
						$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
					}
					if (val[i].custom.payload == "listdocuments") {
						let base = createBaseChat();
						let response = createDiv(style=["msg_cotainer1"], id="", text = "");
						let timespan = createSpan(style=["msg_time"], text=time);
						let { main, head, body, section1, section2} = createModalscrollable("List of Documents", vid)
						let outerButton = createButton("Please click here to see the list of documents", {"type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;","data-toggle":"modal","data-target":`#${vid}`});
						setAttributes(section1,{"style":"font-size: 20px;"})
						//this has to be put in loop {loop start}
						val[i].custom.data.forEach((record, index)=>
						{
							let listElement = document.createElement('div');
							listElement.innerHTML =`<a class=\"btn btn-primary btn-lg btn-block\" style=\"margin-bottom: 10px;\" data-toggle=\"collapse\" href=\"#${index}\" role=\"button\" aria-expanded=\"false\" aria-controls=\"collapseExample\"> Document Name </a> ` ;
							let list = createDiv(style=["collapse"], id=`${index}`, text = "");
							setAttributes(list,{"style":"margin-bottom: 10px;"})
							let x = document.createElement("A");
							// href we put file link
							setAttributes(x,{"class":"btn btn-primary btn-lg", "href":`${record.url}`,"target":"_blank"})
							x.innerHTML=' View ';
							let history = createButton(" History ", {"type":"button", "class":"btn btn-primary btn-lg" ,"style":"margin-left:10;","data-toggle":"modal",  "data-target":"#transactions","onclick":"showhistory()"});//"data-dismiss":"modal">
							list.append(x,history)
							listElement.appendChild(list);
							section1.appendChild(listElement);
						});
						//till here { loop end}
						body.append(section2, section1)
						head.appendChild(body);
						main.appendChild(head);
						response.append(outerButton,timespan, main);
						base.appendChild(response)
						BotResponse = base;
						$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
					}
				}
				else {
					let base = createBaseChat();
					let response = createDiv(style=["msg_cotainer"], id="", text = val[i].text);
					let timespan = createSpan(style=["msg_time"], text=time);
					response.appendChild(timespan)
					base.appendChild(response)
					BotResponse = base
					console.log(BotResponse)
					$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
				}
			}
			

		}
		scrollToBottomOfResults();
		hideSpinner();
	})();
}


//------------------------------------- Set user response in result_div ------------------------------------
function setUserResponse(val) {
	let today = new Date();
	let time = today.getHours() + ":" + today.getMinutes() ;
	let UserResponse = '<div class="d-flex justify-content-end reply mb-4" ><div class="msg_cotainer_send">' + val +'<span class="msg_time_send">'+ time+ '</span></div><img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg"></div></div>';//<div class="clearfix"></div>
	$(UserResponse).appendTo('#result_div');
	$("#chat-input").val('');
	scrollToBottomOfResults();
	showSpinner();
	$('.suggestion').remove();
}


//---------------------------------- Scroll to the bottom of the results div -------------------------------
function scrollToBottomOfResults() {
	let terminalResultsDiv = document.getElementById('result_div');
	terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
}


//---------------------------------------- Spinner ---------------------------------------------------
function showSpinner() {
	$('.spinner').show();
}

function hideSpinner() {
	$('.spinner').hide();
}

//------------------------------------------- Buttons(suggestions)--------------------------------------------------
async function addSuggestion(textToAdd) {
	(async function () {
		let today = new Date();
		let time = today.getHours() + ":" + today.getMinutes() ;
		let suggestions = textToAdd['buttons'];
		console.log(suggestions)
		let base = createBaseChat();
		let response = createDiv(style=["msg_cotainer"], id="", text = textToAdd['text']);
		let timespan = createSpan(style=["msg_time"], text=time);
		response.appendChild(timespan)
		base.appendChild(response)
		BotResponse = base
		$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
		console.log(BotResponse)

		let base1 = createBaseChat();
		let response1 = createDiv(style=["msg_cotainer1"], id="", text = "");
		let timespan1 = createSpan(style=["msg_time"], text=time);
				// Loop through suggestions
		suggestions.forEach(data =>{
			//let div = createDiv(style=[], id=`${data.title}-container`)
			let outerButton = createButton(`${data.title}`, {"id":data.title, "type":"button", "class":"btn btn-primary" ,"style":"border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;padding:12px 48px 12px 48p;margin-left:10px;", "onClick":"buttonResponse(this)", "value":data.payload});
			//$('<button class="btn btn-primary" style="border-radius: 25px;background-color: #00d0ff;color:black;font-size: 20px;box-shadow: 5px 5px #888888;">' + suggestions[i].title + '</button>').appendTo('.suggestion');
			//div.appendChild(outerButton)
			response1.appendChild(outerButton)
		}); 
		response1.appendChild(timespan1)
		base1.appendChild(response1)
		BotResponse1 = base1
		console.log(BotResponse1)
		$(BotResponse1).appendTo('#result_div').hide().fadeIn(1000);
		scrollToBottomOfResults();
	})();
}
function buttonResponse(button){
	send(button.value);
}
//====================================== creating Charts ======================================

//function to create the charts & render it to the canvas
function createChart(title, labels, backgroundColor, chartsData, chartType, displayLegend) {

//create the ".chart-container" div that will render the charts in canvas as required by charts.js,
// for more info. refer: https://www.chartjs.org/docs/latest/getting-started/usage.html
var html = '<div class=\"chart-container\"> <span class=\"modal-trigger\" id=\"expand\" title=\"expand\" href=\"#modal1\"><i class=\"fa fa-external-link\" aria-hidden=\"true\"></i></span> <canvas id=\"chat-chart\" ></canvas> </div> <div style=\"margin-top: 2px;margin-bottom: 2px;\"></div>'
$(html).appendTo('.chats');

//create the context that will draw the charts over the canvas in the ".chart-container" div
var ctx = $('#chat-chart');

// Once you have the element or context, instantiate the chart-type by passing the configuration,
//for more info. refer: https://www.chartjs.org/docs/latest/configuration/
var data = {
	labels: labels,
	datasets: [{
		label: title,
		backgroundColor: backgroundColor,
		data: chartsData,
		fill: false
	}]
};
var options = {
	title: {
		display: true,
		text: title
	},
	layout: {
		padding: {
			left: 5,
			right: 0,
			top: 0,
			bottom: 0
		}
	},
	legend: {
		display: displayLegend,
		position: "right",
		labels: {
			boxWidth: 5,
			fontSize: 10
		}
	}
}

//draw the chart by passing the configuration
chatChart = new Chart(ctx, {
	type: chartType,
	data: data,
	options: options
});

scrollToBottomOfResults();
}

// on click of expand button, get the chart data from gloabl variable & render it to modal
$(document).on("click", "#expand", function() {

//the parameters are declared gloabally while we get the charts data from rasa.
createChartinModal(title, labels, backgroundColor, chartsData, chartType, displayLegend)
});

//function to render the charts in the modal
function createChartinModal(title, labels, backgroundColor, chartsData, chartType, displayLegend) {
//if you want to display the charts in modal, make sure you have configured the modal in index.html
//create the context that will draw the charts over the canvas in the "#modal-chart" div of the modal
var ctx = $('#modal-chart');

// Once you have the element or context, instantiate the chart-type by passing the configuration,
//for more info. refer: https://www.chartjs.org/docs/latest/configuration/
var data = {
	labels: labels,
	datasets: [{
		label: title,
		backgroundColor: backgroundColor,
		data: chartsData,
		fill: false
	}]
};
var options = {
	title: {
		display: true,
		text: title
	},
	layout: {
		padding: {
			left: 5,
			right: 0,
			top: 0,
			bottom: 0
		}
	},
	legend: {
		display: displayLegend,
		position: "right"
	},

}

modalChart = new Chart(ctx, {
	type: chartType,
	data: data,
	options: options
});

}

function sleep(milliseconds) {
	const date = Date.now();
	let currentDate = null;
	do {
		currentDate = Date.now();
	} while (currentDate - date < milliseconds);
}
