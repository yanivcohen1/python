fetch('http://127.0.0.1:5000/login?username1=maria&password1=selas1983', {
  method: 'POST',
  body: JSON.stringify({
    username: 'yaniv',
    password: 'yaniv_P'
  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)