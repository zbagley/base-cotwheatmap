//var and map object initialization
var marker = new Array();
var heatmap = new Array();
var recent;
var mymap = L.map('mapid').fitBounds([[36.99,-109.06],[41.0,-102.04]]);
L.tileLayer.provider('OpenStreetMap.Mapnik').addTo(mymap);


//local API called for tweet data
var url = "http://localhost:3000/geocoords";
var url2 = "http://localhost:3000/recent";
var url3 = "http://localhost:3000/heatmap";

//primary call
$.getJSON(url,function(data) {
    for( var i = 0; i < data['coords'].length; i++){
      var LamMarker = new L.marker([data['coords'][i]['lat'], data['coords'][i]['lng']]);
      marker.push(LamMarker);
      mymap.addLayer(marker[i]);
};
recent = data['coords'][0]['lat']	
setInterval(recentTweet,1000)
addHeatMap()
});

//call to pull most recent tweet and compare to see if new
function recentTweet(){
$.getJSON(url2).done(function(data){
	if(data['coords'][0]['lat']!=recent){
		recent = data['coords'][0]['lat'];
		mymap.removeLayer(marker[0]);
		marker.shift();
		var LamMarker = new L.marker([data['coords'][0]['lat'],data['coords'][0]['lng']]);
		marker.push(LamMarker);
		mymap.addLayer(marker[marker.length-1]);
		}
})}

//call to fill heatmap data
function addHeatMap(){
	$.getJSON(url3).done(function(data){
    for( var i = 0; i < data['coords'].length; i++){
      heatmap.push([data['coords'][i]['lat'], data['coords'][i]['lng'], data['coords'][i]['size']]);
  	}
  	var heat = L.heatLayer(heatmap,{max: Math.max(heatmap['size']),radius:15,gradient:{0.5: 'blue',0.75:'lime',1:'red'}}).addTo(mymap);
  })
}