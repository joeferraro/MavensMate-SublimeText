$(function() {
	try {
		setUpAjaxErrorHandling()
	} catch(e) {
		console.log(e)
	}
	$("input[type='text']:first").focus(); //focus first input element
	//resizeWindowOnDomElementRemoved();
	//submitFormOnEnter();
	$(".alert-message p a.close").live("click", function(){
		$(this).parent().parent().hide();
	})	
});

function showElement(id) {
	$("#"+id).show();
}

function hideElement(id) {
	$("#"+id).hide();
}

function showLoading(message) {
	$("#loading_message").html(message)
	$(".loading").fadeIn();
}

function hideLoading() {
	$(".loading").hide();
}

//window resizer and mover
function resizeAndCenterWindow() {
	resizeWindow();
	centerWindow();
} 

//window resizer and mover
function resizeAndCenterWindowByHeight(height) {
   	window.resizeTo(385, height+160);
	try {
		$("#deploy_output").height(height);
	} catch(e) { }	
	window.moveTo((screen.width-385)/2,(screen.height-document.getElementById('wrapper').offsetHeight-400)/2);
}

function resizeWindow() {
   	window.resizeTo(385, document.getElementById('wrapper').offsetHeight+72);
	try {
		$("#deploy_output").height(document.getElementById('wrapper').offsetHeight);
	} catch(e) { } 
}

function centerWindow() {
	window.moveTo((screen.width-385)/2,(screen.height-document.getElementById('wrapper').offsetHeight-400)/2);
}   

//if dom elements is removed, we need to resize the window
function resizeWindowOnDomElementRemoved() {
	$( "body" ).bind(
		"DOMNodeRemoved",
		function( event ) {
			if (event.target.id == "result_wrapper") {
				resizeWindow();
				$("#project_details_tab").click();
			}
		}
	);
}  

//submit form on enter
function submitFormOnEnter() {
	//submit form on enter
	$(".content").bind('keyup', function(e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		 if(code == 13) { //enter pressed
		 	//if ($('#un').val() && $('#pw').val() && $('#pn').val())
				$("#btnSubmit").click();
		 }
	}); 
} 

//gets tree content in ruby hash form
function get_tree() {			
	var json = { }
	var tree = $("#tree").dynatree("getTree")
	
	//process top level (these are top level metadata types)
	var selected_items = tree.getSelectedAndPartselNodesByLevel(1)
	for (var i in selected_items) {
		json[selected_items[i].data.title] = selected_items[i].bSelected && !selected_items[i].data.inFolder && !selected_items[i].data.in_folder ? "*" : []
	} 
	
	//console.log(json) 
	
	//process children (can either be files or folders)
	selected_items = tree.getSelectedAndPartselNodesByLevel(2)
	for (var i in selected_items) {
		if (json[selected_items[i].parent.data.title] == "*") continue;   
		if (selected_items[i].parent.data.hasChildTypes == true && !selected_items[i].bSelected) continue;
		json[selected_items[i].parent.data.title].push({name:selected_items[i].data.title})
	}
	
	//console.log(json)
	
	//process grandchildren (this is either metadata in folders or child metadata types like fields, weblinks, listviews, etc.)
	selected_items = tree.getSelectedAndPartselNodesByLevel(3)
	for (var i in selected_items) {
		if (selected_items[i].parent.parent.data.inFolder || selected_items[i].parent.parent.data.in_folder) {
			//this is folder-based metadata, we need to add this item explicitly
		    items = json[selected_items[i].parent.parent.data.title] //=> items is an array
		  	var item;
			folder_name = ""
			for (var j = 0; j < items.length; j++) {
				if (items[j].name == selected_items[i].parent.data.title) {
					folder_name = items[j].name
					item = items[j]
					break;
				}
			} 
			console.log(item)
			items.push({name:item.name + "/" + selected_items[i].data.title})
		} else if (selected_items[i].parent.parent.data.hasChildTypes) {
			if (selected_items[i].parent.parent.data.select || selected_items[i].parent.parent.bSelected) {
				continue;
			} else {
				if (selected_items[i].parent.data.select || selected_items[i].parent.bSelected) {
					continue;
				}
				metadata_type = child_def[selected_items[i].data.title]
				if (!json[metadata_type]) {
					json[metadata_type] = []
				}    
				//console.log(metadata_type)
				for (var j = 0; j < selected_items[i].childList.length; j++) {
					//console.log(selected_items[i].childList[j])
					if (selected_items[i].childList[j].bSelected || selected_items[i].childList[j].data.select) {
						json[metadata_type].push({name:selected_items[i].parent.data.title+"."+selected_items[i].childList[j].data.title})  
					}
				}
			}
		}
	}       
	//console.log(selected)  
	var myJSONText = JSON.stringify(json, "\/") 
	myJSONText = myJSONText.replace(/\"/g,"\'")    
	myJSONText = myJSONText.replace(/\:/g,"\=>")    
	myJSONText = myJSONText.replace(/\$/g,"\\$")
	//console.log(myJSONText) 
	return myJSONText
}

function setUpAjaxErrorHandling() {
	$.ajaxSetup({
        error: function(jqXHR, exception) {
            try {
            	errorMessage = ''
	            if (jqXHR.status === 0) {
	               	errorMessage = 'Not connected.\n Verify Network.'
	            } else if (jqXHR.status == 404) {
	                errorMessage = 'Requested page not found. [404]'
	            } else if (jqXHR.status == 500) {
	                errorMessage = 'Internal Server Error [500].'
	            } else if (exception === 'parsererror') {
	                errorMessage = 'Requested JSON parse failed.'
	            } else if (exception === 'timeout') {
	                errorMessage = 'Timeout error.'
	            } else if (exception === 'abort') {
	                errorMessage = 'Ajax request aborted.'
	            } else {
	                errorMessage = 'Uncaught Error.\n' + jqXHR.responseText
	            }
	            $("#error_message").html(errorMessage)
    			hideLoading()
            } catch(e) {
            	console.log(e)
            }
        },
        timeout: 3600000
    });
}

function resize_games() {
	$(".flash_game").css("width", $(window).width() - 20)
	$(".flash_game").css("height", $(window).height() - 225)
}

var CHECK_STATUS_INTERVAL = 3000

function check_status(request_id) {
	$.ajax({
		type: "GET",
		url: "http://127.0.0.1:7777/status", 
		data: {
			 id: request_id
		},
		complete: function(data, status, xhr){
			try {
				console.log('checking status of async request')
			    console.log(data)
			    var response = JSON.parse(data.responseText)
				if (response["status"] == 'pending') {
			    	setTimeout(function() { check_status(request_id); }, CHECK_STATUS_INTERVAL); //poll for completed async request
			    } else {
			    	handle_response(response);
			    }
			} catch(e) {
				console.log('caught an error, polling again...')
				setTimeout(function() { check_status(request_id); }, 1000);
			}
						
		} 
	});
}