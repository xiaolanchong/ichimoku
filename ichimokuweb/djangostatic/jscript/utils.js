// Splits the given text into text chunks separated by punctuation delimiters
function splitIntoChunks(text) {
	var minChunkSize = 0;
	var re = /[。、]/g;
	var result = new Array();
	var lastFoundPos = 0;
	var lastChoppedPos = 0;
	var match = null;
	while ((match = re.exec(text)) != null) {
		if(lastChoppedPos + minChunkSize <= match.index) {
			result.push(text.substring(lastChoppedPos, match.index + 1));
			lastChoppedPos = match.index + 1;
		}
		lastFoundPos = match.index + 1;
	}
	if(lastFoundPos < text.length) {
		result.push(text.substring(lastFoundPos));
	}
	return result;
}

// Object to arrange a series of incoming chunks in the correct order.
// E.g. 3, 2, 1 -> 1, 2, 3
var ChunkMerger = (function(callback) {

    function ChunkMerger(callback){
        this._callback = callback;
		this._receivedChunks = new Array();
		this._startIndex = 0;
    };
	
	// Ctor
	// Arguments:
	//     callback - function to call once a series of chunks is complete
	ChunkMerger.prototype.setCallback = function(callback) {
		this._callback = callback;
		}

    // Adds a new chunk
	// Arguments:
	//  index - index of the chunk in the overall array, starting from 0
	//  text - contents of the chunk, may have any type
    ChunkMerger.prototype.addChunk = function(index, text) {
	console.log('populate');
		if(index < this._startIndex) {
			console.error("Input index is out of the expected bound: " 
						+ index.toString() + ", " + this._startIndex.toString());
			return;
		}
		
		index -= this._startIndex;
        for(var i = this._receivedChunks.length; i <= index; ++i) {
			this._receivedChunks.push(null);
		}
		if(this._receivedChunks[index] == null) {
			this._receivedChunks[index] = text;
		}
		else {
			console.error("Chunk #" + (index + this._startIndex).toString() + " already received");
			return;
		}
		while(this._receivedChunks.length) {
			if(this._receivedChunks[0] != null) {
				this._callback(this._receivedChunks[0]);
				this._receivedChunks.shift();
				++this._startIndex;
			}
			else {
				return;
			}
		}
		for(var i = 0; i < index; ++i) {
			if(this._receivedChunks[index] == null) {
				return;
			}
		}		
    };

    return ChunkMerger;
})();

function addCard(word, reading, definition,
				 example, tagsText) {
	//console.log(tags.length.toString());
	$.ajax({
		type: 'post',
		url: '/addcard',
		data: { "word" : word, "reading" : reading,
				"definition" : definition, "example" : example, 
				"tags" : tagsText },
		dataType: "json",
		beforeSend:function(){
			//launchpreloader();
		},
		error: function(jqXHR, textStatus, errorThrown){
			//alert("fail!!");
		},
		success: function(result, textStatus, jqXHR){
			//populateTable(result);
			//merger.addChunk(index, result);
		}
	});
}

function deleteCard(id) {
	$.ajax({
		type: 'post',
		url: '/deletecard',
		data: { "id" : id },
		dataType: "json",
		beforeSend:function(){
			//launchpreloader();
		},
		error: function(jqXHR, textStatus, errorThrown){
			//alert("fail!!");
		},
		success: function(result, textStatus, jqXHR){
			//populateTable(result);
			//merger.addChunk(index, result);
		}
	});
    $(this).closest("tr").remove(); // remove row
    return false;
}

function showWordParameters(allChunks) {
	//console.log(allChunks[0]);
	$("#word").text(allChunks[0]);
	$("#reading").val(allChunks[1]);
	$("#definition").val(allChunks[2]);
	$("#example").val(allChunks[3]);
	$( "#dialog" ).dialog( "open" );
}

function readParametersAndAddCard() {
	var word = $("#word").text();
	var reading = $("#reading").val();
	var definition = $("#definition").val();
	var example = $("#example").val();
	var tags = $("#tags").val();
	addCard(word, reading, definition, example, tags);
}

/// Splits the given string into tags separated by comma and trims them
function tagsToArray(text) {
	var tags = text.split(",");
	//var 
	for(var i = 0; i < tags.length; ++i) {
		tags[i] = $.trim(tags[i]); 
	}
	return tags;
}

function populateTable(data) {
	if($('#wordtable > thead > tr').length == 0)
	{
		headRow = $('<tr></tr>').append("<th></th>")
		                        .append("<th>Word</th>")
								.append("<th>Reading</th>")
								.append("<th>Definition</th>")
								.append("<th>Example</th>");
		$('#wordtable > thead:last').append(headRow);
	}
	var table = $('#wordtable > tbody:last');
	data.forEach( function (element, row) {
		var row = $('<tr></tr>').addClass(row % 2 ? "odd" : "even");
		var link=$("<a href=\"javascript:none\"><img src=\"img/add-icon.png\" title=\"Add the word to the deck\" /></a>");
		link.click(function(e){
							e.preventDefault();
							var addedImg = "img/Ok-icon.png";
							if($("img", this).attr("src") == addedImg) {
								return false;
							}
							var allChunks = new Array();
							$("td", row).each(function(index, tdElem){
									allChunks.push($(tdElem).text());
								});
							allChunks.shift();
							//addCard(allChunks);
							showWordParameters(allChunks);
							
							$("img", this).attr("src", addedImg);
							return false;
						});
		var td = $("<td></td>").append(link)
		row.append(td)
		element.forEach( function (cellText, column) {
			var cell = $("<td></td>").addClass(column < 2 ? "word" : "").text(cellText);
			row.append(cell);
		});
		table.append(row);
	});
}

function submitFileContents(data) {
    $("#element_to_pop_up").append(
	'<form id="exportform" action="/export" method="post" target="_blank">' + 
		'<input type="hidden" id="exportdata" name="exportdata" />' + 
	'</form>');
    $("#exportdata").val(data);
    $("#exportform").submit().remove();
}