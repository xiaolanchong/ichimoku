
test( "splitIntoChunks test", 
function() {
	var text = 
	"　ある日の暮方の事である。一人の下人（げにん）が、羅生門（らしょうもん）の下で雨やみを待っていた。\r\n" +　"　広い門の下には、この男のほかに誰もいない。ただ、所々丹塗（にぬり）の剥（は）げた、大きな円柱（まるばしら）に、蟋蟀（きりぎりす）が一匹とまっている。羅生門が、朱雀大路（すざくおおじ）にある以上は、この男のほかにも、雨やみをする市女笠（いちめがさ）や揉烏帽子（もみえぼし）が、もう二三人はありそうなものである。それが、この男のほかには誰もいない。"
	var result = splitIntoChunks(text);
		equal( result.length, 16 );
		equal( result[0], "　ある日の暮方の事である。" );
		equal( result[1], "一人の下人（げにん）が、" );
		equal( result[2], "羅生門（らしょうもん）の下で雨やみを待っていた。" );
		equal( result[3], "\r\n　広い門の下には、" );
		equal( result[4], "この男のほかに誰もいない。" );
		equal( result[5], "ただ、" );
		equal( result[6], "所々丹塗（にぬり）の剥（は）げた、" );
		equal( result[7], "大きな円柱（まるばしら）に、" );
		equal( result[8], "蟋蟀（きりぎりす）が一匹とまっている。" );
}
);

test( "ChunkMerger test", 
function() {
	var expectedText = ["0", "1", "2", "3", "4", "5"];
	var merger = new ChunkMerger(function(text) {
			equal(text, expectedText.shift());
		});
	merger.addChunk(-11, "0");
	equal(6, expectedText.length);
	merger.addChunk(0, "0");
	equal(5, expectedText.length);	
	merger.addChunk(2, "2");
	equal(5, expectedText.length);	
	merger.addChunk(1, "1");
	equal(3, expectedText.length);	
	merger.addChunk(5, "5");
	equal(3, expectedText.length);
	merger.addChunk(5, "1");
	equal(3, expectedText.length);
	merger.addChunk(4, "4");
	equal(3, expectedText.length);
	merger.addChunk(3, "3");
	equal(0, expectedText.length);
}
);

test( "Splitting tags test", 
function() {
	var result = tagsToArray("	verb, url:none  ,text-ok ");
	equal(result.length, 3);
	equal(result[0], "verb");
	equal(result[1], "url:none");
	equal(result[2], "text-ok");
	var result = tagsToArray("	verb ");
	equal(result.length, 1);
	equal(result[0], "verb");
	var result = tagsToArray("	verb,, ");
	equal(result.length, 1);
	equal(result[0], "verb");	
}
);