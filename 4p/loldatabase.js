let cytoscape = require('cytoscape')
let graph = require('./graphstuff')

module.exports = {
  graph: graph.graph,
  nodes: graph.nodes,
  edges: graph.edges
}