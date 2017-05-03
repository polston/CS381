// let socket = re
// socket = io.connect('http://localhost:3000')

// socket.on('mouse',
//   // When we receive data
//   function(data) {
//     console.log("Got: " + data.x + " " + data.y);
//   }
// )

//setup stuff
let cy = cytoscape({
  container: document.getElementById('cy'),
  style: [
    {
      selector: 'node',
      style: {
        shape: 'hexagon',
        'background-color': 'red',
        label: 'data(id)'
      }
    },
    {
      selector: 'edge',
      style: {
        label: 'data(weight)'
      }
    }]
});

//max number of nodes, probably take user input for this in 
//createNodes(), currently only used to determine max number of
//nodes in randMax
let max= 10 

//how many nodes are on the canvas(is it a canvas?)
let nodes = 0

//how many edges are on the canvas(is it a canvas?)
let edges = 0

//minimum number of nodes, kind of worthless to be less than 2
let min = 2

//randomly generated number inclusive of max and min
//e.g. min: 3, max: 7
//would generate an integer in the set of [3, 4, 5, 6, 7]
let randMax = Math.floor(Math.random() * (max - min + 1)) + min

//whether or not the graph is connected
//(not necessarily complete)
//changed in connectedGraph()
let connected = false

//FIXME: it's an array of all of the paths, see the
//comment below for a better implementation
let paths = []
/*
  paths should be:
  paths = {
    sourceNode#: {
      destNode#:{
        array from paths for this source -> dest
      },
      destNode#+1:{
        array from paths for this source -> dest
      },
      ...
    },
    sourceNode#+1:{
      destNode#:{
        array from paths for this source -> dest
      },
      destNode#+1:{
        array from paths for this source -> dest
      },
      ...
    },
    ...
  }

  I'm too stupid to figure this out at the moment
*/

//TODO: not implemented
// createNodes(numNodes)

//creates n nodes between min (2, by default) and randMax
console.log('create nodes')
createRandomNodes(min, randMax)
// cy.ready() //I forgot what this does, but seems to do nothing

console.log('create edges')
//creates random edges from the nodes available
createRandomEdges(cy.elements(), cy.nodes())

//renders the layout of the nodes in a circle, or whatever
//you end up putting here from the documentation
let layout = cy.layout({
    name: 'circle'
})

//renders the layout once everything is set
layout.run()


//WORTHLESS TESTING STUFF
let test = dijkstra(cy.elements(), cy.nodes()[0], cy.nodes()[randMax - 1])
console.log('nodes:')
console.log(cy.nodes())
// console.log(dijkstra)
let pathToA = test.path
console.log('path:')
console.log(pathToA)

let distToA = test.dist
console.log('distance: ' + distToA)
console.log('path(): ')
console.log(path(pathToA))
//WORTHLESS TESTING STUFF


//returns an array of the path of nodes
//from the dijkstra object
function path(obj){
  let a = []
  for(let i = 0; i < obj.size(); i++){
    if(obj[i].isNode()){
      a.push(obj[i].data('id'))
    }
    // console.log(JSON.stringify(obj[i].data()))
  }
  return a
}

//does fuck-all
//FIXME: eventually make n nodes defined by the user
function createNodes(num){
  for (var i = 1; i < num; i++) {
    
  }
}

//creates n nodes, where n is the integer value
//of the global randMax
function createRandomNodes(){
  // nodes = Math.floor(Math.random() * (max - min + 1)) + min
  for (var i = 0; i < randMax; i++) {
    //ip is static
    //TODO: probably also needs be dynamic 
    //and add a port or something
    createNode('1.0.0.1:whatever', i)
  }
}

//creates a node from:
//addr = ip address, basically
//identifer = node#
//FIXME: make ip dynamic and add dynamic port
function createNode(addr, identifier){
  cy.add({
        data: { 
          id: 'node' + identifier,
          ip: addr,
          table: {}
        }
    })
}

//randomly creates edges between all nodes on the graph
function createRandomEdges(graph, nodes){
  console.log('random edge')
  //while there are less nodes with edges than there are nodes
  while(nodes.connectedEdges()['length'] <= nodes['length']){
    //50% chance to keep adding nodes after the fact, currently does nothing
    //because the while breaks out, maybe fix it later
    if(nodes.connectedEdges()['length'] >= nodes['length']){
      //random 50/50 true or false
      let choice = Math.random() < 0.5 ? true : false
        if(choice){ break }
      }
    
    //between 0 and the max random number,
    //so in createEdges() 'node#', basically
    let source = Math.floor(Math.random() * randMax)
    let target = Math.floor(Math.random() * randMax)
    console.log('create edges')
    createEdge(nodes, source, target, edges)
  }
  //recursion, son
  if(!connectedGraph(graph, nodes)){
    console.log('connected graph')
    createRandomEdges(graph, nodes)
  }
}

//returns the distance and path objects for a path from node -> destination
function dijkstra(graph, node, dest){
  //give a graph and node .dijkstra produces a function
  let dijkstra = graph.dijkstra(node)
  //dist object between a source and target, can be type Infinity
  let dist = dijkstra.distanceTo(dest)
  //path object between source and target
  //both nodes and edges are maintained
  let path = dijkstra.pathTo(dest)
  
  return {dist: dist, path: path}
}

//returns true if the graph is fully connected (no stray nodes)
function connectedGraph(graph, nodes){
  let dists = []
  // let paths = []
  //for each source node
  for(let source = 0; source < nodes['length']; source++){
    //for each destination node
    for(let dest = 0; dest < nodes['length']; dest++){
      //if the source and desination node aren't the same node
      if(source != dest){
        // paths[source] = {}
        
        //push the dijkstra {dist, path} object 
        //for this source -> dest onto the dist array
        dists.push(dijkstra(cy.elements(), cy.nodes()[source], cy.nodes()[dest]))
      }
    }
  }
  
  //for each dijkstra path found
  for(let d = 0; d < dists.length; d++){
    let a = {}
    // paths[d].push(path(dists[d].path))
    // paths.push([d].push(path(dists[d].path)))
    //TODO: this is poopy, and needs to be changed to
    //how it is in the comment near the top
    paths.push(path(dists[d].path))
    
    //if the distance between the source and destination is infinity, 
    //the graph is not fully connected, and is invalid
    if(dists[d].dist == Infinity){
      return false
    }
  }
  
  //the graph is fully connected (but not necessarily complete)
  connected = true
  console.log('temp: ' + paths)
  return true
}

//creates an edge from:
//s = source node
//t = target/destination node
//identifer = the # after the node name, basically
//FIXME: I think the inifinite loop that crashes the browser
//is occuring here, but I'm not entirely sure where...?
function createEdge(nodes, s, t, identifier){
  let tempSource = cy.$('#node' + s)
  let tempTarget = cy.$('#node' + t)

  //prevents multiple edges between two nodes
  console.log('create edges: s: ' + s + ' t: ' + t)
  if(tempSource.edgesWith(tempTarget)['length'] > 0){
    console.log('return')
    return
  }
  
  //creates edge
  let edge = cy.add({
    data: {
      id: 'edge' + identifier,
      source: 'node' + s,
      target: 'node' + t,
      weight: Math.floor(Math.random() * 10) + 1
    }
  })
  
  //makes sure the edge isn't a loop
  if(edge.isSimple()){
    console.log('loop')
    edges++
    return
  }
  console.log('not loop')
  //edge is a loop, so remove it
  edge.remove()
}

// document.getElementById('connected').innerHTML = 'connected: ' + connected
// document.getElementById('paths').innerHTML = 'paths: ' + JSON.stringify(paths, null, 2)

let realGraph = cy.elements()
let realNodes = cy.nodes()
let realEdges = cy.edges()

module.exports = {
  cytostuff: cy,
  graph: realGraph,
  nodes: realNodes,
  edges: realEdges
}