let express = require('express')
 
let app = express()
 
 
app.get('/*', function(req, res) {
    let originalUrl = req.originalUrl
    res.send(`This is bad actor that will save your cookie and access your bank account: ${originalUrl}`)
})
  
app.listen(5000, function() {
    console.log("server running.....")
})