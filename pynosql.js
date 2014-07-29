function pynosql(){
	this.host = "localhost";
	this.port = "9998";
	this.query = function query( query, callback ){
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
					if ( typeof callback !== "undefined" ) callback( xmlhttp.responseText );
					}
				else if(xmlhttp.status == 400) {
					console.log('There was an error 400');
					}
				else {
					console.log('something else other than 200 was returned');
					}
				}
			}
		var url = 'http://'+this.host+':'+this.port+'/?'+query._action+" ";
		delete query._action;
		url += JSON.stringify(query);
		xmlhttp.open("GET", url, true);
		xmlhttp.send();
		};
	this.makeTable = function makeTable( _table ){
		var table = document.createElement("table");
		for ( var _row in _table ) {
			var header  = table.createTHead();
			var row = header.insertRow(0);
			for ( var column in _table[_row] ) {
				var cell = row.insertCell( row.cells.length );
				cell.innerHTML = column;
				}
			break;
			}
		var body = table.createTBody();
		for ( var _row in _table ) {
			var row = body.insertRow( body.rows.length );
			for ( var column in _table[_row] ) {
				var cell = row.insertCell( row.cells.length );
				var text = _table[_row][column];
				var html = text;
				cell.innerHTML = html;
				}
			}
		return table
		};
	return this;
	}
