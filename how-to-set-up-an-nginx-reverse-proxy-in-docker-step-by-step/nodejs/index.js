// Assign the HTTP server object, built-in to NodeJS
var http = require('http');

// Create the server, on port 3000, and output the text content "Hello World!"
http.createServer(function (req, res) {
    res.write('Hello World!');
    res.end();
}).listen(3000, function(){
    console.log("server start at port 3000");
});