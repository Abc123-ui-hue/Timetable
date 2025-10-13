require('dotenv').config();
const http = require('http');
const app = require('./app');

const port = normalizePort(process.env.PORT || '3000');
app.set('port', port);

const server = http.createServer(app);
server.listen(port, () => {
  console.log(`Hospital web server listening at http://localhost:${port}`);
});
server.on('error', onError);

function normalizePort(val) {
  const portNumber = parseInt(val, 10);
  if (Number.isNaN(portNumber)) return val; // named pipe
  if (portNumber >= 0) return portNumber; // port number
  return 3000;
}

function onError(error) {
  if (error.syscall !== 'listen') throw error;
  const bind = typeof port === 'string' ? 'Pipe ' + port : 'Port ' + port;
  switch (error.code) {
    case 'EACCES':
      console.error(bind + ' requires elevated privileges');
      process.exit(1);
    case 'EADDRINUSE':
      console.error(bind + ' is already in use');
      process.exit(1);
    default:
      throw error;
  }
}
