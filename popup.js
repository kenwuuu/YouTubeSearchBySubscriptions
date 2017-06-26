// channel and subscription are essentially synonymous. 

var channelIDs = [];
var globalToken = '';

chrome.identity.getAuthToken({'interactive': true}, function(token) {
	if (chrome.runtime.lastError) {
		alert(chrome.runtime.lastError.string);
        callback(chrome.runtime.lastError);
        return;
    } else {
		// store token
		console.log(token); 
		globalToken = token;
		
		// send REST request for user's subscriptions
		var xhr = new XMLHttpRequest();
		xhr.open('GET',
		  'https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true');
		xhr.setRequestHeader('Authorization', 'Bearer ' + globalToken);
		xhr.send();
		
		// when response received, parse into JSON and do work
		xhr.onreadystatechange = function() {
			if (xhr.readyState == XMLHttpRequest.DONE) {
				var subsInfo = xhr.responseText;
				var subsParsed = JSON.parse(subsInfo);
				
				// count number of subscriptions
				var channelCount = subsParsed.pageInfo.totalResults;
				// store all channel id's
				for(var count = 0; count < channelCount; count++){
					channelIDs.push(subsParsed.items[count].snippet.resourceId.channelId);
				}
			}
		}
	}
});

function getQuery() {
	var query = document.getElementById('query-field').value;
	chrome.runtime.sendMessage({fn: "setSearch", lastSearch: query});
	
	document.getElementById('display').innerHTML = '';
	
	// searches all channelIDs for query
	for (var i = 0; i < channelIDs.length; i++) {
		var channel = channelIDs[i];
		searchAllSubs(query, channel);
	}
}

function searchAllSubs(query, channel) {
	// send REST request for channel's videos that match query
	var xhr = new XMLHttpRequest();
	xhr.open('GET',
	  'https://www.googleapis.com/youtube/v3/search?q=' + query + 
	  '&part=id,snippet&maxResults=2&channelId=' + channel);
	xhr.setRequestHeader('Authorization', 'Bearer ' + globalToken);
	xhr.send();

	// when response received, parse into JSON and do work
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			var videosInfo = xhr.responseText;
			var videosParsed = JSON.parse(videosInfo);
			
			// count # of videos, store channel names
			var videoCount = videosParsed.pageInfo.totalResults;
			var channelTitle = document.createTextNode(videosParsed.items[0].snippet.channelTitle);
			
			// channelContainer contains title and related videos
			var channelContainer = document.createElement('div');
			var channelTitlePlace = document.createElement('h2');
			channelTitlePlace.appendChild(channelTitle);
			channelContainer.appendChild(channelTitlePlace);
			
			for( var count = 0; count < videoCount; count++){
				// to insert breaks
				var linebreak = document.createElement("br");
				var videoContainer = document.createElement('div');
				videoContainer.className = "video";
				// create video player
				var videoPlayerIframe = document.createElement('iframe');
				
				// create link and add to image and title
				var videoItem = videosParsed.items[count];
				// broken undefined link
				if (!videoItem)
					continue;
				var videoId = videoItem.id.videoId;
				
				// double check undefined link
				if(!videoId)
					continue;
				videoPlayerIframe.src = "https://www.youtube.com/embed/" + videoId; 
				
				calculateLikeRatio(videoId);
				//alert(calculateLikeRatio(videoId));
				
				videoContainer.appendChild(videoPlayerIframe);
				videoContainer.appendChild(linebreak);
				channelContainer.appendChild(videoContainer);
				// breaks up the videos so they don't mesh
				channelContainer.appendChild(linebreak);
				document.getElementById('display').appendChild(channelContainer);
			}
		}
	}
}

function calculateLikeRatio(videoId) {
	// send REST request for video stats
	var xhr = new XMLHttpRequest();
	xhr.open('GET',
	  'https://www.googleapis.com/youtube/v3/videos?id=' + videoId + '&part=statistics');
	xhr.setRequestHeader('Authorization', 'Bearer ' + globalToken);
	xhr.send();
	
	// when response received, parse into JSON and do work
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			statsInfo = xhr.responseText;
			statsParsed = JSON.parse(statsInfo);
			
			// basic math
			var likeCount = parseInt(statsParsed.items[0].statistics.likeCount);
			var dislikeCount = parseInt(statsParsed.items[0].statistics.dislikeCount);
			var totalCount = likeCount + dislikeCount;
			var ratio = 100 * (likeCount / totalCount);
			ratio = parseInt(ratio);
			alert(ratio);
			return ratio;
		}
	}
}

// TODO: 6/26/2017 add ability to search by hitting enter button
// event listener for search button
document.addEventListener('DOMContentLoaded', function () {
	var query = document.getElementById('query-field');
	chrome.runtime.sendMessage({fn: "getSearch"}, function(response){
		console.log(typeof response);
		if(response instanceof String || typeof response === "string"){
			query.value = response;
		}
	});
    document.getElementById('button').addEventListener('click', getQuery);
});