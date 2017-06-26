//persistence
var background = {
	
	lastSearch: {},
	init: function(){
			
		chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
			if(request.fn in background){
				background[request.fn](request, sender, sendResponse);
			}
		});
	},
	
	setSearch: function(request, sender, sendResponse){
		console.log(request.lastSearch);
		this.lastSearch = request.lastSearch;
	},

	getSearch: function(request, sender, sendResponse){
		sendResponse(this.lastSearch);
	}

  };

background.init()
