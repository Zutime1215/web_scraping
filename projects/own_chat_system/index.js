const express = require('express');
const fs = require('fs');
const server = express();

const base_url = "http://localhost:8080"

//bodyParser
server.use(express.json());
server.use(express.static('public'));


server.post('/room',(req, res) =>{
  const room_id = req.body["room_id"];
  var id = Date.now();
  var old_msg = JSON.parse(fs.readFileSync(`./rooms/${room_id}.json`, 'utf-8'));
  old_msg.push(
    {
      "name": req.body["name"],
      "id": (id - id%1000)/1000,
      "msg": req.body["msg"]
    }
  )
  fs.writeFileSync(`./rooms/${room_id}.json`, JSON.stringify(old_msg));
  res.send("ok")
})



server.get('/room/:room_id',(req, res) =>{
  const { room_id } = req.params;
  res.json(JSON.parse(fs.readFileSync(`./rooms/${room_id}.json`, 'utf-8')))
})

server.post('/createRoom', (req, res) => {
  var db_name = Date.now();
  fs.writeFile('./rooms/' + db_name + ".json", '[]', function (err) {
    if (err) throw err;
  });

  if ( req.body["name"].length > 32 || req.body["description"].length > 100 ) {
    res.json({"status": 133})
  }
  else {
    var old_dtls = JSON.parse(fs.readFileSync('./rooms/room_details.json', 'utf-8'));
    old_dtls.push(
      {
        "name": req.body["name"],
        "description": req.body["description"],
        "created": timeNow()
      }
    )
    fs.writeFileSync('./rooms/room_details.json', JSON.stringify(old_dtls));
    res.json({"status": 132, "url": `${base_url}/room/${db_name}`})
  }
})


server.get('/rooms', (req, res) => {
  const rooms = JSON.parse(fs.readFileSync('./rooms/room_details.json', 'utf-8'));
  res.json(rooms);
})


function timeNow() {
  const d = new Date();
  return d.getDate().toString() + '.' + d.getMonth().toString() + '.' + d.getFullYear().toString();
}

server.listen(8080, () => {
  console.log('server started');
});
