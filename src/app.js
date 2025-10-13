const express = require('express');
const morgan = require('morgan');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const cookieParser = require('cookie-parser');
const hpp = require('hpp');
const path = require('path');

const app = express();

app.set('trust proxy', 1);

app.use(helmet());
app.use(hpp());
app.use(cors());
app.use(compression());

app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

const env = process.env.NODE_ENV || 'development';
if (env !== 'test') {
  app.use(morgan('combined'));
}

const publicDir = path.join(__dirname, '../public');
app.use(
  express.static(publicDir, {
    maxAge: '1d',
    etag: true,
    immutable: true,
  })
);

app.get(['/healthz', '/api/health'], (req, res) => {
  res.status(200).json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: Date.now(),
  });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(publicDir, 'index.html'));
});

app.use('/api', (req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.use((err, req, res, next) => {
  console.error(err);
  if (req.path.startsWith('/api')) {
    res.status(err.status || 500).json({ error: err.message || 'Server error' });
  } else {
    res.status(err.status || 500).send('Server error');
  }
});

module.exports = app;
