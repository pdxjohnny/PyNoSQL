function pynosql(){
	this.host = "localhost";
	this.port = "9998";
	this.database = null;
	this.select = function( table, callback ){
		var xmlhttp;
		if (window.XMLHttpRequest) {
			xmlhttp = new XMLHttpRequest();
			}
		else {
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 ) {
				if(xmlhttp.status == 200){
					if ( typeof callback !== "undefined" ) callback(JSON.parse('[' + xmlhttp.responseText.slice(0, -2) + ']') );
					}
				else if(xmlhttp.status == 400) {
					console.log('There was an error 400');
					}
				else {
					console.log('something else other than 200 was returned');
					}
				}
			}
		var url = 'http://'+this.host+':'+this.port+'/'+this.database+'/'+table+".html";
		xmlhttp.open("GET", url, true);
		xmlhttp.send();
		}
	this.show = function( database, callback ){
		var xmlhttp;
		if (window.XMLHttpRequest) {
			xmlhttp = new XMLHttpRequest();
			}
		else {
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 ) {
				if(xmlhttp.status == 200){
					if ( typeof callback !== "undefined" ) callback(JSON.parse( xmlhttp.responseText ) );
					}
				else if(xmlhttp.status == 400) {
					console.log('There was an error 400');
					}
				else {
					console.log('something else other than 200 was returned');
					}
				}
			}
		if ( typeof database !== "undefined" ) var url = 'http://'+this.host+':'+this.port+'/'+database+'/';
		else if ( this.database != null ) var url = 'http://'+this.host+':'+this.port+'/'+this.database+'/';
		else var url = 'http://'+this.host+':'+this.port+'/';
		xmlhttp.open("GET", url, true);
		xmlhttp.send();
		}
	return this;
	}