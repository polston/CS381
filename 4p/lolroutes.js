let express = require('express')
let router = express.Router()

router.route('/')
.get(function(res, req, next){
  console.log(res)
  res.sendFile('/index.html')
})

module.exports = router