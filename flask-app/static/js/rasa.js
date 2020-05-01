$(document).ready(function () {
	$('#OpenImgUpload').click(function(){ 
		$('#imgupload').trigger('click');
	});
	$('#imgupload').change(function(){ 
		var file_data = $('#imgupload').prop('files')[0]; 
		console.log(file_data); 
	});
	const user_id = document.getElementById("username").innerHTML;
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
				send(text, user_id);
				e.preventDefault();
				return false;
			}
		}
	});

})
//------------------------------------------- Call the RASA API--------------------------------------
function send(text, user_id) {
	$.ajax({
		url: `/rasa`, //  RASA API
		type: 'POST',
		contentType: "application/json",
		data: JSON.stringify({ message: text, sender: user_id }),
		success: function (data, textStatus, xhr) {
			console.log(data);

			if (Object.keys(data).length !== 0) {
				for (i = 0; i < Object.keys(data[0]).length; i++) {
					if (Object.keys(data[0])[i] == "buttons") { //check if buttons(suggestions) are present.
						addSuggestion(data[0]["buttons"])
					}
				}
			}

			setBotResponse(data);

		},
		error: function (xhr, textStatus, errorThrown) {
			console.log('Error in Operation');
			setBotResponse('error');
		}
	});
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
	video.src = url;
	video.height = "480";
	video.width = "720";
	video.frameBorder = "0";
	video.allow = "autoplay; fullscreen";
	video.id = "youtube";
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
	let main = createDiv(["d-flex", "justify-content-start", "mb-4"]);
	let first = createDiv(["img_cont_msg"])
	let image = createImage("https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg", ["rounded-circle" ,"user_img_msg"])
	first.appendChild(image);
	main.appendChild(first);
	return main
}



//------------------------------------ Set bot response in result_div -------------------------------------
function setBotResponse(val) {
	var today = new Date();
	var time = today.getHours() + ":" + today.getMinutes() ;
	setTimeout(async function () {

		if ($.trim(val) == '' || val == 'error') { //if there is no response from bot or there is some error
			let error = 'Sorry I wasn\'t able to understand your Query. Let\' try something else!'
			let base = createBaseChat();
			let response = createDiv(style=["msg_cotainer"], id="", text=error);
			let timespan = createSpan(style=["msg_time"], text=time);
			var BotResponse = base.appendChild(response.appendChild(timespan));
			$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);
		} else {
			for (var i in val) {
				if (val[i].hasOwnProperty("image")) {
					let base = createBaseChat();
					let response = createDiv(style=[], id="quote", text="");
					let url = `data:image/png;base64,${val[i].image}`
					let img = createImage(src=url)
					img.height = 720;
					img.width = 720;
					let timespan = createSpan(style=["msg_time"], text=time);
					response.appendChild(img);
					response.appendChild(timespan)
					base.appendChild(response)
					BotResponse = base;
					$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);

				} else if (val[i].hasOwnProperty("buttons")) {
					addSuggestion(val[i].buttons);
				} 
				else if (val[i].hasOwnProperty("custom")) {
					if (val[i].custom.payload == "video") {
						let url = (val[i].custom.data);
						let base = createBaseChat();
						let container = createDiv(style=[], id="video")
						let iframe = createIframe(url);
						let timespan = createSpan(style=["msg_time"], text=time);
						container.appendChild(iframe);
						container.appendChild(timespan);
						base.appendChild(container);
						BotResponse = base;
						$(BotResponse).appendTo('#result_div').hide().fadeIn(1000);

					}
					if (val[i].custom.payload == "map") {
						let base = createBaseChat();
						let map = createDiv(style=[], id="map")
						let timespan = createSpan(style=["msg_time"], text=time);
						map.appendChild(timespan);
						map.style = "height: 500px; margin: 30px auto 50px; width: 800px;"
						base.appendChild(map);
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
				}
				else {
					let base = createBaseChat();
					let response = createDiv(style=["msg_cotainer"], id="", text = val[0].text);
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
	}, 500);
}


//------------------------------------- Set user response in result_div ------------------------------------
function setUserResponse(val) {
	if(document.getElementById("video") != null){
		console.log("video");
		document.getElementById("video").remove();
	}
	if(document.getElementById("map") != null){
		document.getElementById("map").remove();
		document.getElementById("gmaps").remove();
	}
	var today = new Date();
	var time = today.getHours() + ":" + today.getMinutes() ;
	var UserResponse = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + val +'<span class="msg_time_send">'+ time+ '</span></div><img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg"></div></div>';//<div class="clearfix"></div>
	$(UserResponse).appendTo('#result_div');
	$("#chat-input").val('');
	scrollToBottomOfResults();
	showSpinner();
	$('.suggestion').remove();
}


//---------------------------------- Scroll to the bottom of the results div -------------------------------
function scrollToBottomOfResults() {
	var terminalResultsDiv = document.getElementById('result_div');
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
function addSuggestion(textToAdd) {
	setTimeout(function () {
		var suggestions = textToAdd;
		var suggLength = textToAdd.length;
		$('<p class="suggestion"></p>').appendTo('#result_div');
		// Loop through suggestions
		for (i = 0; i < suggLength; i++) {
			$('<span class="sugg-options">' + suggestions[i].title + '</span>').appendTo('.suggestion');
		}
		scrollToBottomOfResults();
	}, 1000);
}


// on click of suggestions get value and send to API.AI
$(document).on("click", ".suggestion span", function () {
	var text = this.innerText;
	setUserResponse(text);
	send(text);
	$('.suggestion').remove();
});
// Suggestions end -----------------------------------------------------------------------------------------

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
