fetch('http://127.0.0.1:5000/logout', {
  method: 'POST',
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)