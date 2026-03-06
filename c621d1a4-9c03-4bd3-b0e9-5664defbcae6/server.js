'use strict';

const express     = require('express');
const bcrypt      = require('bcrypt');
const jwt         = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const fs          = require('fs');
const path        = require('path');
const crypto      = require('crypto');

// ── Config ──────────────────────────────────────────────────
const PORT       = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || crypto.randomBytes(48).toString('hex');
const JWT_EXPIRY = '1h';
const DB_PATH    = path.join(__dirname, 'data', 'users.json');
const RATE_LIMIT = 5;          // max login attempts
const RATE_WINDOW = 60 * 1000; // per minute (ms)

// ── Logging ─────────────────────────────────────────────────
function log(level, msg, meta = {}) {
  const ts = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const extra = Object.keys(meta).length ? ' ' + JSON.stringify(meta) : '';
  console.log(`[${ts}] [${level.toUpperCase().padEnd(5)}] ${msg}${extra}`);
}

// ── DB helpers (JSON file) ───────────────────────────────────
function readDB() {
  try {
    return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
  } catch {
    return { users: [] };
  }
}

function writeDB(db) {
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));
}

// ── Rate limiter (in-memory, per IP) ────────────────────────
const attempts = new Map(); // ip -> [timestamp, ...]

function isRateLimited(ip) {
  const now = Date.now();
  const hits = (attempts.get(ip) || []).filter(t => now - t < RATE_WINDOW);
  hits.push(now);
  attempts.set(ip, hits);
  return hits.length > RATE_LIMIT;
}

// Clean up old rate limit entries every 5 minutes
setInterval(() => {
  const cutoff = Date.now() - RATE_WINDOW;
  for (const [ip, times] of attempts.entries()) {
    const fresh = times.filter(t => t > cutoff);
    if (fresh.length === 0) attempts.delete(ip);
    else attempts.set(ip, fresh);
  }
}, 5 * 60 * 1000);

// ── Auth middleware ──────────────────────────────────────────
function requireAuth(req, res, next) {
  const token = req.cookies && req.cookies.auth;
  if (!token) {
    log('info', 'Unauthenticated access', { path: req.path, ip: clientIP(req) });
    return res.redirect('/login');
  }
  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch (err) {
    const reason = err.name === 'TokenExpiredError' ? 'expired' : 'invalid';
    log('warn', 'Token rejected', { reason, ip: clientIP(req) });
    res.clearCookie('auth');
    return res.redirect('/login?reason=' + reason);
  }
}

function clientIP(req) {
  return req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown';
}

// ── App setup ───────────────────────────────────────────────
const app = express();
app.use(cookieParser());
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: false, limit: '10kb' }));

// Request logger
app.use((req, res, next) => {
  log('info', `${req.method} ${req.path}`, { ip: clientIP(req) });
  next();
});

// ── Public routes ────────────────────────────────────────────

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

// ── Auth API ─────────────────────────────────────────────────

app.post('/api/login', (req, res) => {
  const ip = clientIP(req);

  // Rate limit check
  if (isRateLimited(ip)) {
    log('warn', 'Rate limit hit on /api/login', { ip });
    return res.status(429).json({ error: 'Muitas tentativas. Aguarde 1 minuto.' });
  }

  const { email, password } = req.body;

  // Basic input validation
  if (!email || typeof email !== 'string' || !password || typeof password !== 'string') {
    return res.status(400).json({ error: 'Email e senha são obrigatórios.' });
  }

  const db = readDB();
  const user = db.users.find(u => u.email.toLowerCase() === email.trim().toLowerCase());

  // Constant-time comparison even on miss (prevents timing attacks)
  const hashToCheck = user ? user.password : '$2b$10$invalidhashpaddinginvalidhash..';
  const valid = bcrypt.compareSync(password, hashToCheck);

  if (!user || !valid) {
    log('warn', 'Failed login attempt', { email: email.trim(), ip });
    return res.status(401).json({ error: 'Email ou senha inválidos.' });
  }

  // Update lastLogin
  user.lastLogin = new Date().toISOString();
  writeDB(db);

  const token = jwt.sign(
    { id: user.id, email: user.email, name: user.name, role: user.role },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRY }
  );

  res.cookie('auth', token, {
    httpOnly: true,
    sameSite: 'Strict',
    maxAge: 60 * 60 * 1000 // 1 hour in ms
  });

  log('info', 'Successful login', { email: user.email, ip });
  return res.json({ ok: true, name: user.name });
});

app.post('/api/logout', (req, res) => {
  const ip = clientIP(req);
  log('info', 'Logout', { ip });
  res.clearCookie('auth');
  return res.json({ ok: true });
});

app.get('/api/verify', (req, res) => {
  const token = req.cookies && req.cookies.auth;
  if (!token) return res.status(401).json({ authenticated: false });
  try {
    const user = jwt.verify(token, JWT_SECRET);
    return res.json({ authenticated: true, name: user.name, role: user.role });
  } catch {
    return res.status(401).json({ authenticated: false });
  }
});

// Admin-only: create a new user
app.post('/api/register', requireAuth, async (req, res) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Acesso negado.' });
  }
  const { email, password, name, role = 'viewer' } = req.body;
  if (!email || !password || !name) {
    return res.status(400).json({ error: 'email, password e name são obrigatórios.' });
  }
  const db = readDB();
  if (db.users.find(u => u.email.toLowerCase() === email.toLowerCase())) {
    return res.status(409).json({ error: 'Email já cadastrado.' });
  }
  const hash = await bcrypt.hash(password, 10);
  const newUser = {
    id: crypto.randomUUID(),
    email: email.trim().toLowerCase(),
    password: hash,
    name: name.trim(),
    role: ['admin', 'viewer'].includes(role) ? role : 'viewer',
    createdAt: new Date().toISOString(),
    lastLogin: null
  };
  db.users.push(newUser);
  writeDB(db);
  log('info', 'New user registered', { email: newUser.email, role: newUser.role, by: req.user.email });
  return res.status(201).json({ ok: true, id: newUser.id });
});

// ── Protected routes ─────────────────────────────────────────

app.get('/', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// ── 404 fallback ─────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// ── Global error handler ─────────────────────────────────────
app.use((err, req, res, _next) => {
  log('error', 'Unhandled error', { message: err.message, path: req.path });
  res.status(500).json({ error: 'Erro interno. Tente novamente.' });
});

// ── Start ────────────────────────────────────────────────────
app.listen(PORT, () => {
  log('info', `Server started on port ${PORT}`);
  log('info', `JWT secret: ${JWT_EXPIRY} expiry, ${JWT_SECRET.substring(0, 8)}...`);
});
