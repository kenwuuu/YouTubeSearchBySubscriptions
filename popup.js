var channelIDs = [];
var toke = '';

chrome.identity.getAuthToken(function(token) {
	if (chrome.runtime.lastError) {
		alert('ass');
        callback(chrome.runtime.lastError);
        return;
    } else {
		// Use the token.
		console.log(token); 
		toke = token;
		
		var xhr = new XMLHttpRequest();
		xhr.open('GET',
		  'https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true');
		xhr.setRequestHeader('Authorization',
		  'Bearer ' + token);
		xhr.send();
		
		xhr.onreadystatechange = function() {
			if (xhr.readyState == XMLHttpRequest.DONE) {
				var subInfo = xhr.responseText;
				var subParsed = JSON.parse(subInfo);
				var channelCount = subParsed.pageInfo.totalResults;
				
				//alert(channelCount);
				var count = 0;
				while (count < channelCount) {
					channelIDs.push(subParsed.items[count].snippet.resourceId.channelId);
					count = count + 1;
				}
			}
		}
	}
});

function getQuery(){
	var query = document.getElementById('query-field').value;
	var channelIDsLength = channelIDs.length;
	
	document.getElementById('display').innerHTML = '';
	
	for (var i = 0; i < channelIDsLength; i++) {
		var channel = channelIDs[i];
		searchAllSubs(query, channel);
	}
}

function searchAllSubs(query, channel) {
	var videos = [];
	var videosInfo;
	var videosParsed;
	var videoCount;
	
	var xhr = new XMLHttpRequest();
	xhr.open('GET',
	  'https://www.googleapis.com/youtube/v3/search?q=' + 
	  query + '&part=id,snippet&maxResults=2&channelId=' + 
	  channel);
	xhr.setRequestHeader('Authorization', 'Bearer ' + toke);
	xhr.send();

	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			videosInfo = xhr.responseText;
			videosParsed = JSON.parse(videosInfo);
			videoCount = videosParsed.pageInfo.totalResults;
			
			//alert(videoCount);
			var count = 0;
			
			var channelTitlePlace = document.createElement('h2');
			var channelTitle = document.createTextNode(videosParsed.items[0].snippet.channelTitle);
			channelTitlePlace.appendChild(channelTitle);
			document.getElementById('display').appendChild(channelTitlePlace);
			
			//document.getElementById('display').innerHTML = document.getElementById('display').innerHTML + 
			//'<br />===' + videosParsed.items[0].snippet.channelTitle + '===<br />';
			
			while (count < videoCount) {
				
				//create image
				var thumb = document.createElement('img');
				thumb.src = videosParsed.items[count].snippet.thumbnails.default.url;
				thumb.align = 'top';
				thumb.style.marginBottom = "10px";
				thumb.style.marginRight = "10px";
				document.getElementById('display').appendChild(thumb);
				
				//create title text
				var videoTitlePlace = document.createElement('a');
				videoTitlePlace.appendChild(document.createTextNode(videosParsed.items[count].snippet.title));
				document.getElementById('display').appendChild(videoTitlePlace);
				
				//create link and add to image and title
				var att = document.createAttribute('href');
				att.value = "https://youtu.be/" + videosParsed.items[count].id.videoId;
				videoTitlePlace.setAttributeNode(att);
				thumb.href = att;
				
				//document.getElementById('display').appendChild(document.createElement("BR"));
				
				//document.getElementById('display').innerHTML = document.getElementById('display').innerHTML +
				//	'<a href = \"https://youtu.be/' + videosParsed.items[count].id.videoId + 
				//	'\">  ' + videosParsed.items[count].snippet.title + '</a>';
					
				count = count + 1;
			}
		}
	}
}

function displayResults(shit){
    document.getElementById('display').innerHTML = shit;
}

function authDone() {
    document.getElementById('display').innerHTML = 'done';
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('button').addEventListener('click', getQuery);
});