//var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
//var http = new XMLHttpRequest();

var express = require('express');
var bodyParser = require('body-parser');
var validator = require('validator');
const PORT = process.env.PORT;	//Proper syntax?
const path = require('path')	//WHAT IS THIS

var app = express();
// See https://stackoverflow.com/questions/5710358/how-to-get-post-query-in-express-node-js
app.use(bodyParser.json());
// See https://stackoverflow.com/questions/25471856/express-throws-error-as-body-parser-deprecated-undefined-extended
app.use(bodyParser.urlencoded({ extended: true })); // Required if we need to use HTTP post parameters

//var cors = require('cors');
//app.use(cors());

// Serve static content in folder named "public"
app.use(express.static(path.join(__dirname, 'public')));

// viewed at http://localhost:5000
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
});


app.listen(PORT || 5000);