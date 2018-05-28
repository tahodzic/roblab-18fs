var http = require("http");
var fs = require('fs');
var express = require('express');
var bodyParser = require("body-parser");
var app = express();
var port = 8080;
var serverUrl = "127.0.0.1";
var counter = 0;
var MongoClient = require('mongodb').MongoClient;
var mongourl = "mongodb://localhost:27017/";
var myobj = { name: "Company Inc", address: "Highway 37" };
//Richtige Root hier anpassen falls nötig
var __dirroot = 'C:\Users\Damir\Documents\Semester 6\RobLab\mainpage';
var path = require('path');
var ObjectID = require('mongodb').ObjectID;
var net = require('net');

app.use(express.static('public'));
app.set('view engine', 'ejs');

var index = require('./routes/index');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Start listening 
app.listen(8080,function(){
    console.log("Working on port 8080");
});

//Show list of Gericht
app.get('/position/:tagId', function(req, res, next) {
	currentPosition = parseInt(req.params.tagId);
	MongoClient.connect(mongourl, function(err, db) {
		if (err) throw err("Error happened.")
		var dbo = db.db("RoboDB");
		// fetch and sort Gericht collection by id in descending order
		dbo.collection('Gericht').find().toArray(function(err, result) {
			if (err) {
				console.log("not working");
				res.render('index', {
					title: 'error', 
					data: ''
				})
			} else {
				// render to
				res.render('index', {
					title: 'Gerichte', 
					data: result
				})
			}
		})
		db.close();
	})
	
});

//GET JSON Position from Mongodb
app.get('/position/:tagId/json', function(req,res){
	currentPosition = parseInt(req.params.tagId);
	JSONresult = {};
	MongoClient.connect(mongourl, function(err, db) {
		if (err) throw err("Error happened.")
		var dbo = db.db("RoboDB");
		dbo.collection('Position').find({'_id':currentPosition}).toArray(function(err, result) {
			if (err) {
				console.log("not working");
				res.render('index', {
					title: 'error', 
					data: ''
				})
			} else {
				console.log(result);
				// return JSON with position
				JSONresult = result;
				res.send(JSONresult);
			}
		})
		db.close();
	})
});

//Save order to Mongodb and send info to pepper that order has been made
app.post('/order.html',[
	function(req, res){
		
		MongoClient.connect(mongourl, function(err, db){
			if(err) throw err("mongo connection failed");
			var dbo = db.db("RoboDB");
			var orders = [];
			var _id;
			//req contains order received from Pepper 
			if (typeof(req.body['order[]']) == 'string') {
				_id = new ObjectID.createFromHexString(req.body['order[]']);
				orders.push(ObjectID(_id));
				
			} else {
				req.body['order[]'].forEach(function(item){
					_id = new ObjectID.createFromHexString(item);
					orders.push(ObjectID(_id));
				});
			}
			finishedOrder = {};
			finishedOrder["PositionID"] = currentPosition;
			finishedOrder["GerichtID"] = orders;
			//Write order to MongoDB
			dbo.collection("Bestellung").insert(finishedOrder, function(err, result) {
				res.writeHead(200, {"Content-Type": "text/plain"});
				console.log("post worked");
				res.write("worked");
				res.end();	
			});
			  
		db.close();
		});
		
		//Connect to pepper to send success info
		const client = net.createConnection(5000, '192.168.1.102', () => {
		  console.log('connected to server!');
			//Send success to pepper
			client.write('1');
		});
	

}]);