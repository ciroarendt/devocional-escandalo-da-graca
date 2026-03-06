// ============================================
// SPIDER-MAN: WEB SWING — Longe de Casa
// Flappy Bird style game
// ============================================

// ===== DOM ELEMENTS =====
const nicknameScreen = document.getElementById('nickname-screen');
const nicknameInput = document.getElementById('nickname-input');
const nicknameBtn = document.getElementById('nickname-btn');
const canvasEl = document.getElementById('gameCanvas');
const hudEl = document.getElementById('hud');
const hudNickname = document.getElementById('hud-nickname');
const hudScore = document.getElementById('hud-score');

let canvas, ctx;

// ===== GAME STATE =====
const STATE = { MENU: 'menu', PLAYING: 'playing', GAMEOVER: 'gameover' };
let gameState = STATE.MENU;
let playerNickname = '';
let score = 0;
let highScore = 0;
let frameCount = 0;
let gameSpeed = 2.5;
const baseSpeed = 2.5;
let gameRunning = false;

// ===== RANKING SYSTEM =====
const RANKING_KEY = 'spiderman_websling_ranking';

function getRanking() {
  try {
    return JSON.parse(localStorage.getItem(RANKING_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function saveToRanking(name, pts) {
  const ranking = getRanking();
  ranking.push({ name: name, score: pts, date: Date.now() });
  ranking.sort(function(a, b) { return b.score - a.score; });
  const top10 = ranking.slice(0, 10);
  localStorage.setItem(RANKING_KEY, JSON.stringify(top10));
  return top10;
}

function renderRankingPreview() {
  const list = document.getElementById('ranking-list-preview');
  const ranking = getRanking();
  list.innerHTML = '';
  if (ranking.length === 0) {
    var li = document.createElement('li');
    li.style.justifyContent = 'center';
    li.style.color = '#666';
    li.textContent = 'Nenhum record ainda...';
    list.appendChild(li);
    return;
  }
  var medals = ['👑', '🥈', '🥉'];
  ranking.forEach(function(entry, i) {
    var li = document.createElement('li');
    li.innerHTML =
      '<span class="rank-pos">' + (medals[i] || ((i + 1) + 'º')) + '</span>' +
      '<span class="rank-name">' + entry.name + '</span>' +
      '<span class="rank-score">' + entry.score + '</span>';
    list.appendChild(li);
  });
}

// Show ranking on nickname screen
renderRankingPreview();

// ===== NICKNAME ENTRY =====
function enterGame() {
  var name = nicknameInput.value.trim();
  if (name.length < 1) {
    nicknameInput.style.borderColor = '#ff4444';
    nicknameInput.placeholder = 'Digite um nome!';
    nicknameInput.focus();
    return;
  }
  playerNickname = name;

  // Hide nickname screen
  nicknameScreen.style.display = 'none';

  // Show canvas and HUD
  canvasEl.style.display = 'block';
  hudEl.style.display = 'flex';
  hudNickname.textContent = playerNickname;

  // Init canvas
  canvas = canvasEl;
  ctx = canvas.getContext('2d');
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  // Init game
  bgLayers.init();
  spider.reset();
  gameState = STATE.MENU;
  gameRunning = true;
  setupInputListeners();
  gameLoop();
}

nicknameBtn.addEventListener('click', function(e) {
  e.preventDefault();
  e.stopPropagation();
  enterGame();
});

nicknameInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    enterGame();
  }
});

// Focus input on load
setTimeout(function() { nicknameInput.focus(); }, 100);

// ===== SCREEN SIZING =====
function resizeCanvas() {
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  if (gameRunning) {
    bgLayers.init();
  }
}

// ===== SPIDER-MAN (PLAYER) =====
var spider = {
  x: 0,
  y: 0,
  width: 38,
  height: 48,
  velocity: 0,
  gravity: 0.45,
  jumpForce: -8,
  rotation: 0,
  webLines: [],
  swingAngle: 0,

  reset: function() {
    this.x = canvas.width * 0.2;
    this.y = canvas.height * 0.45;
    this.velocity = 0;
    this.rotation = 0;
    this.webLines = [];
    this.swingAngle = 0;
  },

  jump: function() {
    this.velocity = this.jumpForce;
    this.webLines.push({
      x: this.x + this.width / 2,
      y: this.y,
      targetY: this.y - 120,
      alpha: 1,
      life: 25
    });
  },

  update: function() {
    this.velocity += this.gravity;
    this.y += this.velocity;
    this.rotation = Math.max(-0.5, Math.min(this.velocity * 0.04, 1.2));
    this.swingAngle += 0.15;
    for (var i = this.webLines.length - 1; i >= 0; i--) {
      var web = this.webLines[i];
      web.life--;
      web.alpha = web.life / 25;
      if (web.life <= 0) this.webLines.splice(i, 1);
    }
    if (this.y < -this.height) this.y = -this.height;
  },

  draw: function() {
    ctx.save();
    ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
    ctx.rotate(this.rotation);

    var self = this;

    // Web lines
    this.webLines.forEach(function(web) {
      ctx.save();
      ctx.globalAlpha = web.alpha;
      ctx.strokeStyle = '#ddd';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(web.x - (self.x + self.width / 2), web.y - (self.y + self.height / 2));
      ctx.lineTo(web.x - (self.x + self.width / 2), web.targetY - (self.y + self.height / 2));
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(web.x - (self.x + self.width / 2), web.targetY - (self.y + self.height / 2), 4 * web.alpha, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    var w = this.width;
    var h = this.height;

    // Body (red torso)
    ctx.fillStyle = '#be1e2d';
    ctx.beginPath();
    ctx.ellipse(0, 2, w * 0.38, h * 0.35, 0, 0, Math.PI * 2);
    ctx.fill();

    // Blue sides
    ctx.fillStyle = '#1b3a6b';
    ctx.beginPath();
    ctx.ellipse(-w * 0.25, 5, w * 0.15, h * 0.28, -0.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(w * 0.25, 5, w * 0.15, h * 0.28, 0.2, 0, Math.PI * 2);
    ctx.fill();

    // Head
    ctx.fillStyle = '#be1e2d';
    ctx.beginPath();
    ctx.arc(0, -h * 0.28, w * 0.32, 0, Math.PI * 2);
    ctx.fill();

    // Eyes (white, big)
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.ellipse(-w * 0.14, -h * 0.3, w * 0.14, w * 0.11, -0.15, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(w * 0.14, -h * 0.3, w * 0.14, w * 0.11, 0.15, 0, Math.PI * 2);
    ctx.fill();

    // Eye outlines
    ctx.strokeStyle = '#111';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.ellipse(-w * 0.14, -h * 0.3, w * 0.14, w * 0.11, -0.15, 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.ellipse(w * 0.14, -h * 0.3, w * 0.14, w * 0.11, 0.15, 0, Math.PI * 2);
    ctx.stroke();

    // Web pattern on head
    ctx.strokeStyle = 'rgba(0,0,0,0.3)';
    ctx.lineWidth = 0.8;
    ctx.beginPath();
    ctx.moveTo(0, -h * 0.5);
    ctx.lineTo(0, -h * 0.1);
    ctx.stroke();
    for (var i = 1; i <= 3; i++) {
      ctx.beginPath();
      ctx.arc(0, -h * 0.28, w * 0.1 * i, -0.8, 0.8);
      ctx.stroke();
    }

    // Arms (swing pose)
    ctx.strokeStyle = '#be1e2d';
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    var armSwing = Math.sin(this.swingAngle) * 0.3;
    // Right arm (reaching up)
    ctx.beginPath();
    ctx.moveTo(w * 0.2, -2);
    ctx.quadraticCurveTo(w * 0.55, -h * 0.4 + armSwing * 10, w * 0.4, -h * 0.55);
    ctx.stroke();
    ctx.fillStyle = '#be1e2d';
    ctx.beginPath();
    ctx.arc(w * 0.4, -h * 0.55, 3, 0, Math.PI * 2);
    ctx.fill();
    // Left arm
    ctx.beginPath();
    ctx.moveTo(-w * 0.2, -2);
    ctx.quadraticCurveTo(-w * 0.55, h * 0.1 - armSwing * 10, -w * 0.45, h * 0.15);
    ctx.stroke();

    // Legs
    ctx.strokeStyle = '#1b3a6b';
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(w * 0.1, h * 0.2);
    ctx.quadraticCurveTo(w * 0.25, h * 0.4, w * 0.15, h * 0.48);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(-w * 0.1, h * 0.2);
    ctx.quadraticCurveTo(-w * 0.3, h * 0.35, -w * 0.2, h * 0.48);
    ctx.stroke();

    // Spider emblem on chest
    ctx.fillStyle = '#111';
    ctx.beginPath();
    ctx.ellipse(0, 3, 3, 2, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#111';
    ctx.lineWidth = 0.8;
    for (var side = -1; side <= 1; side += 2) {
      for (var j = 0; j < 3; j++) {
        ctx.beginPath();
        ctx.moveTo(0, 3);
        ctx.lineTo(side * (5 + j * 2), 3 + (j - 1) * 3);
        ctx.stroke();
      }
    }

    ctx.restore();
  }
};

// ===== OBSTACLES (European Buildings) =====
var obstacles = [];
var OBSTACLE_WIDTH = 65;
var GAP_SIZE = 170;
var OBSTACLE_SPACING = 220;

function createObstacle(x) {
  var minTop = 80;
  var maxTop = canvas.height - GAP_SIZE - 120;
  var topHeight = minTop + Math.random() * (maxTop - minTop);
  var colors = [
    { wall: '#d4a06a', roof: '#8b4513', accent: '#c4903a' },
    { wall: '#c9b896', roof: '#6b4423', accent: '#b8a07a' },
    { wall: '#e8d5b7', roof: '#7a4e2d', accent: '#d4bf9a' },
    { wall: '#b8c4c8', roof: '#4a5568', accent: '#9aacb4' }
  ];
  var color = colors[Math.floor(Math.random() * colors.length)];
  return {
    x: x,
    topHeight: topHeight,
    bottomY: topHeight + GAP_SIZE,
    width: OBSTACLE_WIDTH,
    color: color,
    scored: false,
    windowPattern: Math.floor(Math.random() * 3)
  };
}

function drawBuilding(obs, isTop) {
  var x = obs.x;
  var w = obs.width;
  var c = obs.color;

  if (isTop) {
    var h = obs.topHeight;
    ctx.fillStyle = c.wall;
    ctx.fillRect(x, 0, w, h);
    ctx.fillStyle = 'rgba(0,0,0,0.15)';
    ctx.fillRect(x + w - 6, 0, 6, h);
    ctx.fillStyle = c.roof;
    ctx.fillRect(x - 5, h - 12, w + 10, 12);
    ctx.fillRect(x - 2, h - 18, w + 4, 8);
    drawWindows(x, 10, w, h - 25, obs.windowPattern);
    ctx.fillStyle = c.accent;
    for (var i = 0; i < w; i += 12) {
      ctx.fillRect(x + i, h - 20, 8, 3);
    }
  } else {
    var y = obs.bottomY;
    var bh = canvas.height - y;
    ctx.fillStyle = c.wall;
    ctx.fillRect(x, y, w, bh);
    ctx.fillStyle = 'rgba(0,0,0,0.15)';
    ctx.fillRect(x + w - 6, y, 6, bh);
    ctx.fillStyle = c.roof;
    ctx.fillRect(x - 5, y, w + 10, 12);
    ctx.fillRect(x - 2, y + 10, w + 4, 8);
    // Pointed roof
    ctx.beginPath();
    ctx.moveTo(x + w / 2, y - 18);
    ctx.lineTo(x - 5, y);
    ctx.lineTo(x + w + 5, y);
    ctx.closePath();
    ctx.fill();
    drawWindows(x, y + 25, w, bh - 25, obs.windowPattern);
    ctx.fillStyle = c.accent;
    for (var i = 0; i < w; i += 12) {
      ctx.fillRect(x + i, y + 18, 8, 3);
    }
  }
}

function drawWindows(bx, by, bw, bh, pattern) {
  var cols = 2;
  var windowW = 14;
  var windowH = 18;
  var gapX = (bw - cols * windowW) / (cols + 1);
  var gapY = 28;
  var rows = Math.floor(bh / gapY);

  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      var wx = bx + gapX + c * (windowW + gapX);
      var wy = by + r * gapY;
      if (wy + windowH > by + bh) continue;

      ctx.fillStyle = 'rgba(0,0,0,0.2)';
      ctx.fillRect(wx - 1, wy - 1, windowW + 2, windowH + 2);

      var isLit = (r + c + pattern) % 3 !== 0;
      ctx.fillStyle = isLit ? 'rgba(255, 220, 100, 0.6)' : 'rgba(40, 60, 100, 0.7)';
      ctx.fillRect(wx, wy, windowW, windowH);

      ctx.strokeStyle = 'rgba(0,0,0,0.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(wx + windowW / 2, wy);
      ctx.lineTo(wx + windowW / 2, wy + windowH);
      ctx.moveTo(wx, wy + windowH / 2);
      ctx.lineTo(wx + windowW, wy + windowH / 2);
      ctx.stroke();
    }
  }
}

// ===== BACKGROUND (Parallax European Skyline) =====
var bgLayers = {
  stars: [],
  farBuildings: [],
  midBuildings: [],
  clouds: [],

  init: function() {
    this.stars = [];
    for (var i = 0; i < 80; i++) {
      this.stars.push({
        x: Math.random() * canvas.width * 2,
        y: Math.random() * canvas.height * 0.5,
        size: Math.random() * 2 + 0.5,
        twinkle: Math.random() * Math.PI * 2
      });
    }
    this.farBuildings = [];
    var fx = 0;
    while (fx < canvas.width * 2) {
      this.farBuildings.push({
        x: fx,
        width: 25 + Math.random() * 40,
        height: 60 + Math.random() * 120,
        hasSpire: Math.random() > 0.7
      });
      fx += 40 + Math.random() * 30;
    }
    this.midBuildings = [];
    var mx = 0;
    while (mx < canvas.width * 2) {
      this.midBuildings.push({
        x: mx,
        width: 30 + Math.random() * 50,
        height: 80 + Math.random() * 150,
        hasDome: Math.random() > 0.6
      });
      mx += 50 + Math.random() * 40;
    }
    this.clouds = [];
    for (var i = 0; i < 6; i++) {
      this.clouds.push({
        x: Math.random() * canvas.width * 2,
        y: 30 + Math.random() * canvas.height * 0.25,
        width: 60 + Math.random() * 100,
        speed: 0.2 + Math.random() * 0.4
      });
    }
  },

  update: function() {
    for (var i = 0; i < this.clouds.length; i++) {
      this.clouds[i].x -= this.clouds[i].speed;
      if (this.clouds[i].x + this.clouds[i].width < 0) {
        this.clouds[i].x = canvas.width + 50;
      }
    }
  },

  draw: function() {
    // Sky gradient
    var skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    skyGrad.addColorStop(0, '#0f0c29');
    skyGrad.addColorStop(0.3, '#1a1a4e');
    skyGrad.addColorStop(0.6, '#302b63');
    skyGrad.addColorStop(0.85, '#c94b4b');
    skyGrad.addColorStop(1, '#f4a261');
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Stars
    for (var i = 0; i < this.stars.length; i++) {
      var star = this.stars[i];
      star.twinkle += 0.03;
      ctx.globalAlpha = 0.4 + Math.sin(star.twinkle) * 0.4;
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(star.x % canvas.width, star.y, star.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    // Far buildings
    for (var i = 0; i < this.farBuildings.length; i++) {
      var b = this.farBuildings[i];
      var bx = ((b.x - frameCount * 0.3) % (canvas.width * 2) + canvas.width * 2) % (canvas.width * 2) - canvas.width * 0.3;
      ctx.fillStyle = 'rgba(15, 12, 41, 0.8)';
      var by = canvas.height - b.height;
      ctx.fillRect(bx, by, b.width, b.height);
      if (b.hasSpire) {
        ctx.beginPath();
        ctx.moveTo(bx + b.width / 2, by - 30);
        ctx.lineTo(bx + b.width * 0.3, by);
        ctx.lineTo(bx + b.width * 0.7, by);
        ctx.closePath();
        ctx.fill();
      }
    }

    // Mid buildings
    for (var i = 0; i < this.midBuildings.length; i++) {
      var b = this.midBuildings[i];
      var bx = ((b.x - frameCount * 0.7) % (canvas.width * 2) + canvas.width * 2) % (canvas.width * 2) - canvas.width * 0.3;
      ctx.fillStyle = 'rgba(26, 26, 78, 0.7)';
      var by = canvas.height - b.height;
      ctx.fillRect(bx, by, b.width, b.height);
      if (b.hasDome) {
        ctx.beginPath();
        ctx.arc(bx + b.width / 2, by, b.width / 2.5, Math.PI, 0);
        ctx.fill();
      }
      ctx.fillStyle = 'rgba(255, 200, 80, 0.3)';
      for (var wy = by + 10; wy < canvas.height - 10; wy += 16) {
        for (var wx = bx + 5; wx < bx + b.width - 5; wx += 12) {
          if (Math.random() > 0.5) {
            ctx.fillRect(wx, wy, 4, 5);
          }
        }
      }
    }

    // Clouds
    for (var i = 0; i < this.clouds.length; i++) {
      var c = this.clouds[i];
      ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.beginPath();
      ctx.ellipse(c.x, c.y, c.width * 0.5, 15, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(c.x - c.width * 0.2, c.y - 5, c.width * 0.3, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(c.x + c.width * 0.25, c.y + 2, c.width * 0.35, 13, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  }
};

// ===== GROUND =====
var groundOffset = 0;

function drawGround() {
  var groundY = canvas.height - 50;
  var groundGrad = ctx.createLinearGradient(0, groundY, 0, canvas.height);
  groundGrad.addColorStop(0, '#5a4e3c');
  groundGrad.addColorStop(0.3, '#4a3f2e');
  groundGrad.addColorStop(1, '#2a2518');
  ctx.fillStyle = groundGrad;
  ctx.fillRect(0, groundY, canvas.width, 50);

  ctx.fillStyle = '#6b5e4a';
  ctx.fillRect(0, groundY, canvas.width, 4);

  groundOffset = (groundOffset + gameSpeed) % 24;
  ctx.fillStyle = 'rgba(0,0,0,0.15)';
  for (var x = -groundOffset; x < canvas.width; x += 24) {
    for (var y = groundY + 8; y < canvas.height; y += 14) {
      var off = (Math.floor((y - groundY) / 14) % 2) * 12;
      ctx.fillRect(x + off, y, 22, 12);
      ctx.strokeStyle = 'rgba(0,0,0,0.1)';
      ctx.lineWidth = 1;
      ctx.strokeRect(x + off, y, 22, 12);
    }
  }
}

// ===== PARTICLES =====
var particles = [];

function spawnParticles(x, y, color, count) {
  for (var i = 0; i < count; i++) {
    particles.push({
      x: x, y: y,
      vx: (Math.random() - 0.5) * 6,
      vy: (Math.random() - 0.5) * 6,
      life: 20 + Math.random() * 20,
      maxLife: 40,
      size: 2 + Math.random() * 4,
      color: color
    });
  }
}

function updateParticles() {
  for (var i = particles.length - 1; i >= 0; i--) {
    var p = particles[i];
    p.x += p.vx;
    p.y += p.vy;
    p.vy += 0.1;
    p.life--;
    if (p.life <= 0) particles.splice(i, 1);
  }
}

function drawParticles() {
  for (var i = 0; i < particles.length; i++) {
    var p = particles[i];
    ctx.globalAlpha = p.life / p.maxLife;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size * (p.life / p.maxLife), 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

// ===== COLLISION =====
function checkCollision() {
  var groundY = canvas.height - 50;
  var sp = {
    x: spider.x + 5,
    y: spider.y + 5,
    w: spider.width - 10,
    h: spider.height - 10
  };
  if (sp.y + sp.h > groundY) return true;
  for (var i = 0; i < obstacles.length; i++) {
    var obs = obstacles[i];
    if (sp.x + sp.w > obs.x && sp.x < obs.x + obs.width) {
      if (sp.y < obs.topHeight) return true;
      if (sp.y + sp.h > obs.bottomY) return true;
    }
  }
  return false;
}

// ===== SCORE CHECK =====
function checkScore() {
  for (var i = 0; i < obstacles.length; i++) {
    var obs = obstacles[i];
    if (!obs.scored && obs.x + obs.width < spider.x) {
      obs.scored = true;
      score++;
      hudScore.textContent = score;
      spawnParticles(spider.x + spider.width, spider.y, '#f4a261', 6);
      gameSpeed = baseSpeed + score * 0.08;
    }
  }
}

// ===== GAME SCREENS (drawn on canvas) =====
function drawMenuScreen() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  var cx = canvas.width / 2;
  var cy = canvas.height / 2;

  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // Title
  ctx.strokeStyle = '#000';
  ctx.lineWidth = 4;
  ctx.fillStyle = '#be1e2d';
  ctx.font = '48px Bangers, cursive';
  ctx.strokeText('SPIDER-MAN', cx, cy - 80);
  ctx.fillText('SPIDER-MAN', cx, cy - 80);

  ctx.fillStyle = '#4a9eff';
  ctx.font = '32px Bangers, cursive';
  ctx.strokeText('WEB SWING', cx, cy - 40);
  ctx.fillText('WEB SWING', cx, cy - 40);

  // Instruction
  var pulse = 0.6 + Math.sin(frameCount * 0.05) * 0.4;
  ctx.globalAlpha = pulse;
  ctx.fillStyle = '#fff';
  ctx.font = '11px "Press Start 2P", monospace';
  ctx.fillText('TOQUE OU PRESSIONE ESPACO', cx, cy + 20);
  ctx.font = '9px "Press Start 2P", monospace';
  ctx.fillText('PARA LANCAR TEIA!', cx, cy + 45);
  ctx.globalAlpha = 1;

  // Web emoji
  ctx.font = '40px sans-serif';
  ctx.fillText('🕸️', cx, cy + 90);

  // Player name
  ctx.fillStyle = '#f4a261';
  ctx.font = '14px "Press Start 2P", monospace';
  ctx.fillText('Heroi: ' + playerNickname, cx, cy + 140);

  drawInGameRanking(cx, cy + 170);
}

function drawGameOverScreen() {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  var cx = canvas.width / 2;
  var cy = canvas.height / 2;

  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.strokeStyle = '#000';
  ctx.lineWidth = 4;

  ctx.fillStyle = '#be1e2d';
  ctx.font = '52px Bangers, cursive';
  ctx.strokeText('GAME OVER', cx, cy - 120);
  ctx.fillText('GAME OVER', cx, cy - 120);

  ctx.fillStyle = '#fff';
  ctx.font = '16px "Press Start 2P", monospace';
  ctx.fillText(playerNickname, cx, cy - 70);

  ctx.fillStyle = '#f4a261';
  ctx.font = '42px Bangers, cursive';
  ctx.fillText('Score: ' + score, cx, cy - 35);

  ctx.fillStyle = '#4a9eff';
  ctx.font = '22px Bangers, cursive';
  ctx.fillText('Melhor: ' + highScore, cx, cy + 5);

  drawInGameRanking(cx, cy + 40);

  var pulse = 0.5 + Math.sin(frameCount * 0.06) * 0.5;
  ctx.globalAlpha = pulse;
  ctx.fillStyle = '#fff';
  ctx.font = '10px "Press Start 2P", monospace';
  ctx.fillText('TOQUE PARA JOGAR DE NOVO', cx, cy + 195);
  ctx.globalAlpha = 1;
}

function drawInGameRanking(cx, startY) {
  var ranking = getRanking();
  if (ranking.length === 0) return;

  var count = Math.min(ranking.length, 5);
  var rh = count * 22 + 35;
  ctx.fillStyle = 'rgba(0,0,0,0.5)';
  ctx.fillRect(cx - 140, startY - 5, 280, rh);
  ctx.strokeStyle = 'rgba(190,30,45,0.5)';
  ctx.lineWidth = 2;
  ctx.strokeRect(cx - 140, startY - 5, 280, rh);

  ctx.fillStyle = '#f4a261';
  ctx.font = '13px Bangers, cursive';
  ctx.textAlign = 'center';
  ctx.fillText('🏆 RANKING MUNDIAL', cx, startY + 14);

  var medals = ['👑', '🥈', '🥉'];
  ctx.font = '9px "Press Start 2P", monospace';

  for (var i = 0; i < count; i++) {
    var entry = ranking[i];
    var y = startY + 32 + i * 22;
    var isMe = entry.name === playerNickname;

    ctx.textAlign = 'left';
    ctx.fillStyle = '#f4a261';
    ctx.fillText(medals[i] || ((i + 1) + 'o'), cx - 125, y);

    ctx.fillStyle = isMe ? '#be1e2d' : '#fff';
    ctx.fillText(entry.name, cx - 85, y);

    ctx.textAlign = 'right';
    ctx.fillStyle = '#4a9eff';
    ctx.fillText('' + entry.score, cx + 125, y);
  }

  ctx.textAlign = 'center';
}

// ===== GAME LOGIC =====
var canRestart = false;

function startGame() {
  score = 0;
  gameSpeed = baseSpeed;
  frameCount = 0;
  obstacles = [];
  particles = [];
  spider.reset();
  hudScore.textContent = '0';
  hudEl.style.display = 'flex';
  gameState = STATE.PLAYING;

  for (var i = 0; i < 4; i++) {
    obstacles.push(createObstacle(canvas.width + 200 + i * OBSTACLE_SPACING));
  }
}

function gameOver() {
  gameState = STATE.GAMEOVER;
  canRestart = false;
  if (score > highScore) highScore = score;
  saveToRanking(playerNickname, score);
  spawnParticles(spider.x + spider.width / 2, spider.y + spider.height / 2, '#be1e2d', 20);
  spawnParticles(spider.x + spider.width / 2, spider.y + spider.height / 2, '#fff', 10);
  setTimeout(function() { canRestart = true; }, 800);
}

// ===== INPUT =====
function handleInput() {
  if (gameState === STATE.MENU) {
    startGame();
  } else if (gameState === STATE.PLAYING) {
    spider.jump();
    spawnParticles(spider.x + spider.width / 2, spider.y + spider.height / 2, '#ddd', 4);
  } else if (gameState === STATE.GAMEOVER && canRestart) {
    gameState = STATE.MENU;
  }
}

function setupInputListeners() {
  canvas.addEventListener('mousedown', function(e) {
    e.preventDefault();
    handleInput();
  });

  canvas.addEventListener('touchstart', function(e) {
    e.preventDefault();
    handleInput();
  }, { passive: false });

  document.addEventListener('keydown', function(e) {
    if (e.code === 'Space' || e.code === 'ArrowUp' || e.key === 'w' || e.key === 'W') {
      e.preventDefault();
      handleInput();
    }
  });
}

// ===== MAIN GAME LOOP =====
function gameLoop() {
  if (!gameRunning) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Background always draws
  bgLayers.update();
  bgLayers.draw();
  drawGround();

  if (gameState === STATE.PLAYING) {
    frameCount++;
    spider.update();

    // Update obstacles
    for (var i = obstacles.length - 1; i >= 0; i--) {
      obstacles[i].x -= gameSpeed;
      if (obstacles[i].x + obstacles[i].width < -10) {
        obstacles.splice(i, 1);
      }
    }

    // Spawn new obstacles
    var lastObs = obstacles[obstacles.length - 1];
    if (!lastObs || lastObs.x < canvas.width - OBSTACLE_SPACING) {
      obstacles.push(createObstacle(canvas.width + 50));
    }

    // Draw obstacles
    for (var i = 0; i < obstacles.length; i++) {
      drawBuilding(obstacles[i], true);
      drawBuilding(obstacles[i], false);
    }

    spider.draw();
    updateParticles();
    drawParticles();

    if (checkCollision()) {
      gameOver();
    }
    checkScore();

  } else if (gameState === STATE.MENU) {
    frameCount++;
    spider.y = canvas.height * 0.45 + Math.sin(frameCount * 0.03) * 15;
    spider.x = canvas.width * 0.2;
    spider.swingAngle += 0.05;
    spider.draw();
    drawMenuScreen();

  } else if (gameState === STATE.GAMEOVER) {
    frameCount++;
    for (var i = 0; i < obstacles.length; i++) {
      drawBuilding(obstacles[i], true);
      drawBuilding(obstacles[i], false);
    }
    spider.velocity += spider.gravity * 0.3;
    spider.y += spider.velocity * 0.3;
    spider.rotation += 0.05;
    if (spider.y < canvas.height) spider.draw();
    updateParticles();
    drawParticles();
    drawGameOverScreen();
  }

  requestAnimationFrame(gameLoop);
}
