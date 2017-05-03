let app = require('express')()
let server = require('http').createServer(app)
let io = require('socket.io')(server)

// Create the app
// var app = express()

// Set up the server
// var server = app.listen(process.env.PORT || 3000, listen)

//server info in callback
function listen() {
  var host = server.address().address
  var port = server.address().port
  console.log('Example app listening at http://' + host + ':' + port)
}

//public folder is exposed
// app.use(express.static('public'))
// app.use('/sockets', express.static('./node_modules/socket.io/lib'))
server.use('/cytoscape', app.static('./node_modules/cytoscape/dist/cytoscape.min.js'))
// app.use('/', require('./lolroutes'))

//websockets
// let io = require('socket.io')(server);

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

//every user connected
io.on('connection', function (socket) {
    //socket id of the client connected
    console.log("We have a new client: " + socket.id);
    // io.sockets.emit('connection', 'beep boop');
    
  
    // When this user emits, client side: socket.emit('otherevent',some data);
    socket.on('clickaroo', function(data) {
      // Data comes in as whatever was sent, including objects
      console.log("Received: 'clickaroo' " + data);
    
      // Send it to all other clients
      // io.sockets.emit('clickaroo', {data: 'beep boop'});
      socket.broadcast.emit('clickaroo', {stuff: 'beep boop 2'});
      
      // This is a way to send to everyone including sender
      io.sockets.emit('clickaroo', "this goes to everyone");
    })
    
    socket.on('disconnect', function() {
      console.log("Client has disconnected");
    })
  }
)