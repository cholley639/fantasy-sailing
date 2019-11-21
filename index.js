//var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
//var http = new XMLHttpRequest();

var express = require('express');
var bodyParser = require('body-parser');
var validator = require('validator');

/* You shouldn't need to create a variable, just app.listen(process.env.PORT)
 * Also, you would usually create a .local.env file which contains the PORT
 * variable
 */
const PORT = process.env.PORT;	//Proper syntax?

/* path is the package that does all kinds of file navigation commands.
 * See https://nodejs.org/api/path.html
 */
const path = require('path')	//WHAT IS THIS

var app = express();
// See https://stackoverflow.com/questions/5710358/how-to-get-post-query-in-express-node-js
app.use(bodyParser.json());
// See https://stackoverflow.com/questions/25471856/express-throws-error-as-body-parser-deprecated-undefined-extended
app.use(bodyParser.urlencoded({ extended: true })); // Required if we need to use HTTP post parameters

//var cors = require('cors');
//app.use(cors());

// We can see path being used here to navigate from the working directory into
// folder "public"
// Serve static content in folder named "public"
app.use(express.static(path.join(__dirname, 'public')));


// Mongo initialization and connect to database
// process.env.MONGODB_URI is the default environment variable on Heroku for the MongoLab add-on
// If environment variables not found, there is option to fall back to local database: mongodb://localhost/example
// example is the name of the local database

/*
var mongoUri = process.env.MONGODB_URI; //|| 'mongodb://localhost/example';
var MongoClient = require('mongodb').MongoClient, format = require('util').format;
var db = MongoClient.connect(mongoUri, function(error, databaseConnection) {
	db = databaseConnection;
});
*/

/* In the future, we will probably only expose methods from this api and
 * develop the frontend separately. Take a look at this page to get an idea
 * of what that looks like: https://expressjs.com/en/guide/using-middleware.html
 */
// viewed at http://localhost:5000
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
});


app.listen(PORT || 5000);
