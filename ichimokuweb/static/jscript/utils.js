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

function showWordParameters(allChunks, imgElement) {
	$("#word").text(allChunks[0]);
	$("#reading").val(allChunks[1]);
	$("#definition").val(allChunks[2]);
	$("#example").val(allChunks[3]);
	$("#dialog").data('imgToChange', imgElement).dialog("open");
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

function fillRow(rowData, rowIndex, table, tdSentenceElem) {
	var isKnown = rowData[rowData.length - 1];
	var sentenceIndex = rowData.length - 2;
	var rowClass = rowIndex % 2 ? "odd" : "even"
	if (isKnown) {
		rowClass = "knownWord";
	}
	var row = $('<tr></tr>').addClass(rowClass);
	var link=$("<a href=\"javascript:none\"><img src=\"static/img/add-icon.png\" title=\"Add the word to the deck\" /></a>");
	link.click(function(e){
				e.preventDefault();
				var addedImg = "static/img/Ok-icon.png";
				if($("img", this).attr("src") == addedImg) {
					return false;
				}
				var allChunks = rowData.slice(0, rowData.length - 1);
				showWordParameters(allChunks, this);				
			});
	var td = $("<td></td>");
	if(!isKnown) {
		td.append(link);
	}
	row.append(td);
	rowData.forEach( function (cellText, column) {
		// skip the sentence and the word status
		if(column >= sentenceIndex) {
			return;
		}
		var cell = $("<td></td>").addClass(column < 2 ? "word" : "").text(cellText);
		row.append(cell);
	});
	if( tdSentenceElem != null &&
		$(tdSentenceElem).text() == rowData[sentenceIndex]) {
			var val = $(tdSentenceElem).attr("rowspan");
			if(val == undefined && val == null) {
				$(tdSentenceElem).attr("rowspan", "2");
			}
			else {
				val = parseInt(val) + 1;
				$(tdSentenceElem).attr("rowspan", val.toString());			
			}
		}
		else {
			var cell = $("<td></td>").text(rowData[sentenceIndex]).addClass("example");
			row.append(cell);
			tdSentenceElem = cell;
		}
	table.append(row);
	return tdSentenceElem;
}

var annotatedWords = [];
var currentPage = 0;
var items_per_page = 30;

function handlePaginationClick(page_index, jq) {
	currentPage = page_index;
	$("#wordtable > tbody > tr").remove();
	var table = $('#wordtable > tbody:last');
    var max_elem = Math.min((page_index+1) * items_per_page, annotatedWords.length);
	var tdSentenceElem = null;
	for(var i=page_index*items_per_page;i<max_elem;i++) {
		tdSentenceElem = fillRow(annotatedWords[i], i, table, tdSentenceElem);
	}
	return false;
}

function populatePaginatedTable(data) {
	annotatedWords = annotatedWords.concat(data);
	$("#Pagination").pagination(annotatedWords.length, {
		items_per_page: items_per_page, 
		num_edge_entries: 2,
		current_page: currentPage,
		callback:handlePaginationClick
	});
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
	data.forEach(function(rowData, rowIndex) {
			fillRow(rowData, rowIndex, table);
		});
}

////////////////////////////////////
// Deck page
///////////////////////////////////

function fillDeckRow(rowData, rowIndex, table) {
	var rowClass = rowIndex % 2 ? "odd" : "even"
	var row = $('<tr></tr>').addClass(rowClass);
	var columnClasses = { 
			0: "wordz", 
			1: "word", 
			4: "tags"
			};
	rowData.forEach( function (cellText, column) {
		var cell = $("<td></td>").addClass(columnClasses[column]).text(cellText);
		row.append(cell);
	});
	var td = $("<td></td>").attr("style", "text-align:center;");
	var img = $("<img></img>").attr("src", "static/img/edit_card.png")
							  .attr("id", "card_1")
							  .addClass("editCardImg")
							  .attr("title", "Edit the card");
	var a = $("<a></a>").attr("href", "#");
	a.append(img);
	td.append(a);
	img = $("<img></img>").attr("src", "static/img/Close-2-icon.png")
						  .attr("id", "card_1")
						  .addClass("delCardImg")
						  .attr("title", "Delete the word from the deck");
	a = $("<a></a>").attr("href", "#");	
	a.append(img);
	td.append(a);
	row.append(td);
	td = $("<td></td>").attr("style", "text-align:center;");
	checkBox = $("<input>").attr("type", "checkbox");//.attr("checked","");
	td.append(checkBox);
	row.append(td);
	table.append(row);
}

function handlePaginationDeckClick(page_index, jq) {
	$("#wordtable > tbody > tr").remove();
	var table = $('#wordtable > tbody:last');
	var max_elem = Math.min((page_index+1) * items_per_page, deckWords.length);
	for(var i=page_index*items_per_page;i<max_elem;i++) {
		fillDeckRow(deckWords[i], i, table);
	}
	return false;
}

function submitFileContents(data) {
    $("#element_to_pop_up").append(
	'<form id="exportform" action="/export" method="post" target="_blank">' + 
		'<input type="hidden" id="exportdata" name="exportdata" />' + 
	'</form>');
    $("#exportdata").val(data);
    $("#exportform").submit().remove();
}