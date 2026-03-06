// Ranking API Server — Spider-Man: Web Swing
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3777;
const DATA_FILE = path.join(__dirname, 'ranking-data.json');
const MAX_ENTRIES = 50;

// Load or init ranking
function loadRanking() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    }
  } catch (e) {}
  return [];
}

function saveRankingFile(ranking) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(ranking, null, 2), 'utf8');
}

// Init
let ranking = loadRanking();

function handleCORS(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

const server = http.createServer(function (req, res) {
  handleCORS(res);

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // GET /ranking — return top 50
  if (req.method === 'GET' && req.url === '/ranking') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(ranking));
    return;
  }

  // POST /ranking — submit score { name, score }
  if (req.method === 'POST' && req.url === '/ranking') {
    let body = '';
    req.on('data', function (chunk) { body += chunk; });
    req.on('end', function () {
      try {
        var data = JSON.parse(body);
        var name = (data.name || '').trim().substring(0, 12);
        var pts = parseInt(data.score, 10);
        if (!name || isNaN(pts) || pts < 0) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Invalid data' }));
          return;
        }

        // Update existing or add
        var nameLow = name.toLowerCase();
        var found = false;
        for (var i = 0; i < ranking.length; i++) {
          if (ranking[i].name.toLowerCase() === nameLow) {
            found = true;
            if (pts > ranking[i].score) {
              ranking[i].score = pts;
              ranking[i].date = Date.now();
            }
            ranking[i].name = name;
            break;
          }
        }
        if (!found) {
          ranking.push({ name: name, score: pts, date: Date.now() });
        }

        ranking.sort(function (a, b) { return b.score - a.score; });
        ranking = ranking.slice(0, MAX_ENTRIES);
        saveRankingFile(ranking);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(ranking));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON' }));
      }
    });
    return;
  }

  // GET /nickname-check?name=xxx — check if nickname is taken
  if (req.method === 'GET' && req.url.startsWith('/nickname-check')) {
    var url = new URL(req.url, 'http://localhost');
    var checkName = (url.searchParams.get('name') || '').trim().toLowerCase();
    var exists = false;
    for (var i = 0; i < ranking.length; i++) {
      if (ranking[i].name.toLowerCase() === checkName) { exists = true; break; }
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ taken: exists }));
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, '0.0.0.0', function () {
  console.log('Ranking API running on port ' + PORT);
});
