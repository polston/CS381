let express = require('express')
let app = express()
let graph = require('./graphstuff')
// let server = require('http').createServer(app)


// Create the app
// var app = express()

// Set up the server
server = app.listen(process.env.PORT || 3000, listen)

let io = require('socket.io')(server)

//server info in callback
function listen() {
  var host = server.address().address
  var port = server.address().port
  console.log('Example app listening at http://' + host + ':' + port)
}

//public folder is exposed
app.use(express.static('public'))
app.use('/sockets', express.static('./node_modules/socket.io-client/dist/socket.io.js'))
app.use('/cytoscape', express.static('./node_modules/cytoscape/dist/cytoscape.min.js'))
// app.use('/graphstuff', express.static('./graph/graphstuff.js'))
// app.use('/', require('./lolroutes'))

//websockets
// let io = require('socket.io')(server);

// app.get('/graphstuff', function (req, res) {
//   res.sendFile(__dirname + '/graphstuff.js');
// });
app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});


//every user connected
io.on('connection', function (socket) {
    //socket id of the client connected
    console.log("We have a new client: " + socket.id);
    // io.sockets.emit('connection', 'beep boop');
    let g = graph.json()
    // console.log(graph.elements().nodes())
    io.to(socket.id).emit('initGraph', graph.json())
    
  
    // When this user emits, client side: socket.emit('otherevent',some data);
    socket.on('clickaroo', function(data) {
      // Data comes in as whatever was sent, including objects
      // console.log("Received: 'clickaroo' " + JSON.stringify(data, null, 2));
      console.log("Received: 'clickaroo' " + JSON.stringify(data));
      // Send it to all other clients
      // io.sockets.emit('clickaroo', {data: 'beep boop'});
      socket.broadcast.emit('clickaroo', data);
      
      // This is a way to send to everyone including sender
      // io.sockets.emit('clickaroo', "this goes to everyone");
    })
    
    socket.on('disconnect', function() {
      console.log("Client has disconnected");
    })
  }
)