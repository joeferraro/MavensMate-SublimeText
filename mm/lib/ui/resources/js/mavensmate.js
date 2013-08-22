child_metadata = [ 
  {"xmlName" : "CustomField", "tagName" : "fields", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "BusinessProcess", "tagName" : "businessProcesses", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "RecordType", "tagName" : "recordTypes", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "WebLink", "tagName" : "webLinks", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "ValidationRule", "tagName" : "validationRules", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "NamedFilter", "tagName" : "namedFilters", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "SharingReason", "tagName" : "sharingReasons", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "ListView", "tagName" : "listViews", "parentXmlName" : "CustomObject" }, 
  {"xmlName" : "FieldSet", "tagName" : "fieldSets", "parentXmlName" : "CustomObject" },
  {"xmlName" : "CustomLabel", "tagName" : "customLabels", "parentXmlName" : "CustomLabels" },
  {"xmlName" : "WorkflowAlert", "tagName" : "alerts", "parentXmlName" : "Workflow" },
  {"xmlName" : "WorkflowTask", "tagName" : "tasks", "parentXmlName" : "Workflow" },
  {"xmlName" : "WorkflowOutboundMessage", "tagName" : "outboundMessages", "parentXmlName" : "Workflow" },
  {"xmlName" : "WorkflowFieldUpdate", "tagName" : "fieldUpdates", "parentXmlName" : "Workflow" },
  {"xmlName" : "WorkflowRule", "tagName" : "rules", "parentXmlName" : "WorkFlow", "parentXmlName" : "Workflow" }, 
  {"xmlName" : "WorkflowEmailRecipient", "tagName" : "emailRecipients", "parentXmlName" : "Workflow" },
  {"xmlName" : "WorkflowTimeTrigger", "tagName" : "timeTriggers", "parentXmlName" : "Workflow" },
  {"xmlName" : "WorkflowActionReference", "tagName" : "actionReferences", "parentXmlName" : "Workflow" }
]

$(function() {
	
});

function renderTree() {
	tree = $("#tree").dynatree({
	    initAjax: {
	    	type 	 : "POST",
	    	dataType : "json",
	    	url 	 : baseLocalServerURL+"/project/get_index",
		    data 	 : JSON.stringify({
				"project_name" : project_name
			})
		},
		checkbox: true,
		selectMode: 3,
		debugLevel: 0,
		persist: false,
		selectedIds: '',
		onSelect: function(check, node) {
		    var selectedNodes = tree.getSelectedNodes()
		    var ids = $.map(selectedNodes, function(node){
                return node.data.id;
            });
		    this.selectedIds = ids
		},
		onPostInit: function(isReloading, isError) {
			if (this.selectedIds === undefined || this.selectedIds === '' || this.selectedIds == []) {
			    this.selectedIds = []
			    var selected = this.getSelectedNodes();
			    var ids = $.map(selected, function(node){
                    return node.data.id;
                });
			    this.selectedIds = ids
			}

			var filter = $("#txtFilter").val();
			if (filter && filter.length > 2) {
				$("#tree").dynatree("getRoot").visit(function(node){
				    node.expand(true);
				});
			}
			resizeProjectWrapper()
			hideLoading()
		},
		onCreate: function(node, span) {
			if (node.data.level === 1)
				bindContextMenu(span);
		}
	});
	tree = $("#tree").dynatree("getTree")
}

function renderBufferedTree(metadata) {
	try {
		$("#tree").dynatree("destroy");
	} catch(e) {}
	
	tree = $("#tree").dynatree({
		ajaxDefaults: { // Used by initAjax option
	        timeout: 600000, // >0: Make sure we get an ajax error for invalid URLs
	    },
		children: metadata,
		checkbox: true,
		selectMode: 3,
		debugLevel: 0,
		persist: false,
		// onCreate: function(node, span) {
		// 	if (node.data.level === 1)
		// 		bindContextMenu(span);
		// },
		onLazyRead: function(node) {
			$.ajax({
	            url: baseLocalServerURL+"/metadata/list/async",
	            data: {
					"metadata_type"			: node.data.title,
					"sid"					: $("#sid").val(),
					"metadata_server_url" 	: $("#metadata_server_url").val(),
					"server_url" 			: $("#server_url").val()
				},
	            complete: function(data){
	                list_handler(data, node)
	            }
	        });
	 	}
	});
	tree = $("#tree").dynatree("getTree")
}

function getPackage() {
    var json = { }
    var child_def = {}
    for (item in child_metadata) {
        child_def[child_metadata[item]['tagName']] = child_metadata[item]['xmlName']
    }
    try {
        var records = tree.getSelectedNodes()
        $.each(records, function(index, rec) {
            if (rec.data.level == 1) {
                if (json[rec.parent.data.text] === undefined) {
                    try {
                        if (Object.prototype.toString.call(rec.data.type.childXmlNames) === '[object Array]') {
                            if (rec.data.type.childXmlNames.length == 0) {
                                json[rec.data.text] = '*'
                            } else {
                                json[rec.data.text] = []
                            }
                        } else {
                            json[rec.data.text] = '*'
                        }
                    } catch(e) {
                        json[rec.data.text] = '*'
                    }
                    
                }
            } else if (rec.data.level == 2) {
                if (json[rec.parent.data.text] === undefined) {
                    json[rec.parent.data.text] = []
                    json[rec.parent.data.text].push(rec.data.text)
                } else if (json[rec.parent.data.text] !== '*') {
                    json[rec.parent.data.text].push(rec.data.text)
                }
            } else if (rec.data.level == 3) {
                if (rec.parent.parent.data.type.inFolder) {
                    if (json[rec.parent.parent.data.text] === undefined) {
                        json[rec.parent.parent.data.text] = []
                    }
                    //this is a folder name, add it
                    json[rec.parent.parent.data.text].push(rec.parent.data.text + "/" + rec.data.text)
                } else {
                    //this is a sub type like a custom field, list view, etc.
                    
                    if (rec.children != null) {
                    	metadata_type = child_def[rec.data.text]
                    	if (!json[metadata_type]) {
                    	    json[metadata_type] = []
                    	} 

                    	$.each(rec.children, function(index, childNode) {
                    	    if (childNode.data.checked) {
                    	        json[metadata_type].push(childNode.parent.parent.data.text+"."+childNode.data.text)  
                    	    }
                    	})
                    }
                } 
            } else if (rec.data.level == 4) {
                //this is a child metadata object, like a custom field
                metadata_type = child_def[rec.parent.data.text]
                if (json.hasOwnProperty(rec.parent.parent.parent.data.text)) { //json['CustomObject'] exists already
                	if ($.inArray(rec.parent.parent.data.text, json[rec.parent.parent.parent.data.text]) === -1) {
		            	if (!json[metadata_type]) {
		            	    json[metadata_type] = []
		            	} 
		            	json[metadata_type].push(rec.parent.parent.data.text+"."+rec.data.text) 	
		        	}
                } else {
                	if (!json[metadata_type]) {
                	    json[metadata_type] = []
                	} 
                	json[metadata_type].push(rec.parent.parent.data.text+"."+rec.data.text) 	
                } 
            }
        })  
    } catch(e) {
        console.log(e)
        return []
    }
    return json
}

function resizeFilter() {
	$("#txtFilter").width($("#filter").width() - $("#search-btn").width() - $("#select-btn").width()  - 70)
}

function scrollToTop(selector) {
	$(selector).animate({ scrollTop: 0 }, 300);
}

function showElement(id) {
	$("#"+id).show();
}

function hideElement(id) {
	$("#"+id).hide();
}

function toggleRunningIndicator() {
	$(".running_indicator").toggle();
}

function showLoading(message) {
	$(".twipsy").height($(window).height())
	$(".twipsy").width($(window).width())
	$("#loading_message").html(message)
	$(".loading").show();
}

function hideLoading() {
	$(".loading").hide();
}

//window resizer and mover
function resizeAndCenterWindow() {
	resizeWindow();
	centerWindow();
} 

function isArray(what) {
    return Object.prototype.toString.call(what) === '[object Array]';
}

//window resizer and mover
function resizeAndCenterWindowByHeight(height) {
   	window.resizeTo(485, height+160);
	try {
		$("#deploy_output").height(height);
	} catch(e) { }	
	//window.moveTo((screen.width-385)/2,(screen.height-document.getElementById('wrapper').offsetHeight-400)/2);
}

//window resizer and mover
function resizeAndCenterWindowSpecific(width, height) {
   	window.resizeTo(width, height+160);
	try {
		$("#deploy_output").height(height);
	} catch(e) { }	
	window.moveTo((screen.width-width)/2,(screen.height-document.getElementById('wrapper').offsetHeight-(width+15))/2);
}

function resizeWindow() {
   	window.resizeTo(385, document.getElementById('wrapper').offsetHeight+72);
	try {
		$("#deploy_output").height(document.getElementById('wrapper').offsetHeight);
	} catch(e) { } 
}

function centerWindow() {
	window.moveTo((screen.width-$(window).width())/2,(screen.height-$(window).height())/2-190);
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
	$(".content").bind('keyup', function(e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		 if(code == 13) { //enter pressed
			$("#btnSubmit").click();
		 }
	}); 
} 

//gets tree content in json format
function get_tree() {			
	if (tree !== undefined) {
		return getPackage()
		//return tree.getPackage()
	} else {
		return {
			"ApexClass" 		: "*",
			"ApexComponent" 	: "*",
			"ApexPage"			: "*",
			"ApexTrigger" 		: "*",
			"StaticResource" 	: "*"
		}
	}
}

function get_log_levels_json() {
	var options = []
	var logCategories = ['Db', 'Workflow', 'Validation', 'Callout', 'Apex_code', 'Apex_profiling']
	for (category in logCategories) {
		var logCategory = logCategories[category]
		var logLevel = $("#select-"+logCategory).val()
		if (logLevel != '') {
			options.push({
				"category" 	: logCategory,
				"level" 	: logLevel
			})
		}
	}
	return options
}

function get_log_levels_json_tooling() {
	var options = []
	var logCategories = ['Database', 'System', 'Visualforce', 'Workflow', 'Validation', 'Callout', 'ApexCode', 'ApexProfiling']
	for (category in logCategories) {
		var logCategory = logCategories[category]
		var logLevel = $("#select-"+logCategory).val()
		if (logLevel != '') {
			options.push({
				"category" 	: logCategory,
				"level" 	: logLevel
			})
		} else {
			options.push({
				"category" 	: logCategory,
				"level" 	: 'INFO'
			})
		}
	}
	return options
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

function global_init_handler(data) {
	console.log(data)
	try {
		var response = JSON.parse(data.responseText)
		check_status(response["id"])
	} catch(e) {
		show_global_error('The local MavensMate server did not respond properly. This likely means it is not running or it is malfunctioning. Try restarting your text editor and MavensMate.app.');
		hideLoading()
	}
}

function list_handler(data, node) {
	console.log(data)
	console.log('node: ')
	console.log(node)
	try {
		var response = JSON.parse(data.responseText)
		check_list_status(response["id"], node)
	} catch(e) {
		show_global_error('The local MavensMate server did not respond properly. This likely means it is not running or it is malfunctioning. Try restarting your text editor and MavensMate.app.');
		hideLoading()
	}
}

function check_list_status(request_id, node) {
    $.ajax({
        type: "GET",
        url: baseLocalServerURL+"/status", 
        data: {
             id: request_id
        },
        complete: function(data, status, xhr) {
            try {
                console.log('checking status of async request')
                console.log(data)
                console.log('json response: ')
                console.log(data.responseText)
                var response = JSON.parse(data.responseText)
                if (response["status"] == 'pending') {
                    setTimeout(function() { check_list_status(request_id, node); }, CHECK_STATUS_INTERVAL); //poll for completed async request
                } else {
                    handle_list_response(response, node);
                }
            } catch(e) {
                console.log(e)
                console.log('caught an error, polling again...')
                setTimeout(function() { check_list_status(request_id, node); }, 2000);
            }
                        
        } 
    });
}

function handle_list_response(data, node) {
	console.log('processing data')
	console.log(data)
	try {
		for (i in data) {
			data[i]['title'] 		= data[i]['title']    	|| data[i]['fullName']
			data[i]['key'] 			= data[i]['key'] 		|| data[i]['fullName']
			data[i]['isFolder'] 	= data[i]['isFolder'] 	|| false
			data[i]['isLazy'] 		= data[i]['isLazy']   	|| false
		}
		node.setLazyNodeStatus(DTNodeStatus_Ok);
    	node.addChild(data);

	} catch(e) {
		console.log(e)
		return []
	}
}

function show_global_error(message) {
	$("#global_message").html(message)
	$("#global_message_wrapper").show()
}

function hide_global_error() {
	$("#global_message_wrapper").hide()
	$("#global_message").html('')
}

function show_message_with_custom_action(message, mtype, button_label, script) {
	if (mtype === undefined) {
		mtype = 'error'
	}
	message += '<br/><a href="#" class="btn btn-info btn-wide" onclick="'+script+'">'+button_label+'</a>'
	$("#error_message").parent().attr('class', 'alert')
	$("#error_message").parent().addClass('alert-'+mtype)
	$("#error_message").html(message)
	$("#result_output").show()
	resizeElements()
}

function show_message(message, mtype, showCloseButton) {
	if (mtype === undefined) {
		mtype = 'error'
	}
	if (showCloseButton === undefined) {
		showCloseButton = false
	}
	if (showCloseButton) {
		message += '<br/><a href="#" class="btn btn-info btn-wide" onclick="window.close()">Done</a>'
	}
	$("#error_message").parent().attr('class', 'alert')
	$("#error_message").parent().addClass('alert-'+mtype)
	$("#error_message").html(message)
	$("#result_output").show()
	resizeElements()
}

function hide_message(message) {
	$("#error_message").html('')
	$("#result_output").hide()
	resizeElements()
}

function resize_arcade() {
	$(".flash_game").css("width", $(".tab-content").width() - 45)
	$(".flash_game").css("height", $(window).height() - 290)
}

function resizeElements() {
    if ($("#result_output").css('display') != 'none') {
		$("#main-tab-content").height($(window).height() - $(".navbar").height() - $("#result_output").height() - 160)
    } else {
        $("#main-tab-content").height($(window).height() - $(".navbar").height() - 140)
    }
}

function resizeProjectWrapper(offset) {
	if (offset === undefined) {
		offset = 90
	}
	$("#project_wrapper").height($("#main-tab-content").height() - offset)
	if (tree !== undefined) {
		//TODO:tree.setHeight($("#project_wrapper").height())
	}
}

jQuery.fn.selectText = function(){
	var doc = document;
	var element = this[0];
	if (doc.body.createTextRange) {
		var range = document.body.createTextRange();
		range.moveToElementText(element);
		range.select();
	} else if (window.getSelection) {
		var selection = window.getSelection();        
		var range = document.createRange();
		range.selectNodeContents(element);
		selection.removeAllRanges();
		selection.addRange(range);
	}
};

function expandAll() {
	tree.expandAll()
}

function collapseAll() {
	tree.collapseAll()
}

$.expr[':'].Contains = function(a, i, m) {
	return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
};