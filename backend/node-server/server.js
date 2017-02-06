const http = require('http');
const hostname = 'localhost';
const port = 3000;
var request = require('request');
var url = require('url')

var data = {coords:[]}
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database("tweets.db", mode = sqlite3.OPEN_READONLY);


//DATABASE INITIALIZATION
db.all("SELECT lat,lng FROM geocoords ORDER BY tm DESC",function(err,rows){
	for(i = 0 ; i < 50; i++){
		data.coords.push({'lat': rows[i].lat, 'lng': rows[i].lng})
	}
		//SERVER RESPONSE INITIALIZATION
		const server = http.createServer((req, res) => {
			//SET RESPONSE CODE AND HEADERS
	  	  	res.statusCode = 200;
	  		res.setHeader('Content-Type','application/json')
	  		res.setHeader("Access-Control-Allow-Origin", "*");
	  		res.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

	  		//RESPONSES
	  		if(req.url === '/geocoords'){
	  			req.pipe(request(url.format(url.parse('http://localhost/geocoords')),function(){res.end(JSON.stringify(data))
	  }))}
	  		if(req.url == '/recent'){
	  		req.pipe(request(url.format(url.parse('http://localhost/recent')),function(){
	  			updateRecent(function(recent){res.end(JSON.stringify(recent))
	  })}))}
	  		if(req.url == '/heatmap'){
	  		req.pipe(request(url.format(url.parse('http://localhost/heatmap')),function(){
	  			updateHeatMap(function(heatmap){res.end(JSON.stringify(heatmap))
	  })}))}
});

//OPEN LISTENING STREAM AFTER DATABASE INITIALIZATION
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

	});


//CALLBACK FUNCTIONS FOR JSON RESPONSE
function updateRecent(callback){
	var recent = {coords:[]}
	var db = new sqlite3.Database("tweets.db", mode = sqlite3.OPEN_READONLY);
	db.all("SELECT lat,lng FROM geocoords ORDER BY tm DESC LIMIT 1",function(err,rows){
		if (typeof rows !== 'undefined'){
		recent.coords.push({'lat': rows[0].lat, 'lng': rows[0].lng})
		callback(recent)}
		else
			callback(data.coords[data.coords.length-1])
})
}

function updateHeatMap(callback){
	var heatmap = {coords:[]}
	var db = new sqlite3.Database("tweets.db", mode = sqlite3.OPEN_READONLY);
	db.all("SELECT lat,lng,size FROM heatmap",function(err,rows){
		for(i = 0; i < rows.length; i++){
			heatmap.coords.push({'lat':rows[i].lat,'lng': rows[i].lng,'size': rows[i].size})
		}
		callback(heatmap)
})
}
