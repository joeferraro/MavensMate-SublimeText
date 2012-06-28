$(function() {

	$("input:first").focus(); //focus first input element
	resizeWindowOnDomElementRemoved();
	//submitFormOnEnter();
		
});

//window resizer and mover
function resizeAndCenterWindow() {
	resizeWindow();
	centerWindow();
} 

//window resizer and mover
function resizeAndCenterWindowByHeight(height) {
   	window.resizeTo(325, height+160);
	try {
		$("#deploy_output").height(height);
	} catch(e) { }	
	window.moveTo((screen.width-325)/2,(screen.height-document.getElementById('wrapper').offsetHeight-400)/2);
}

function resizeWindow() {
   	window.resizeTo(325, document.getElementById('wrapper').offsetHeight+72);
	try {
		$("#deploy_output").height(document.getElementById('wrapper').offsetHeight);
	} catch(e) { } 
}

function centerWindow() {
	window.moveTo((screen.width-325)/2,(screen.height-document.getElementById('wrapper').offsetHeight-400)/2);
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

//update project
function updateProject() {
	$('#result_output').html(
		dispatch({
			controller: 'project', 
			action: 'update',   
			tree: get_tree()
		})
	);
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