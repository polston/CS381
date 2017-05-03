let express = require('express')
let router = express.Router()

router.route('/')
.get(function(res, req, next){
  console.log(res)
  res.sendfile('/index.html')
})

module.exports = router