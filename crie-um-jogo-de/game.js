// ============================================================
// ENDURO — Atari 2600 Clone
// Mobile-first HTML5 Canvas game
// ============================================================

(function () {
  "use strict";

  // --- Canvas Setup ---
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");

  const GAME_W = 320;
  const GAME_H = 480;
  let scale = 1;
  let offsetX = 0;
  let offsetY = 0;

  function resize() {
    canvas.width = GAME_W;
    canvas.height = GAME_H;
    const wRatio = window.innerWidth / GAME_W;
    const hRatio = window.innerHeight / GAME_H;
    scale = Math.min(wRatio, hRatio);
    offsetX = (window.innerWidth - GAME_W * scale) / 2;
    offsetY = (window.innerHeight - GAME_H * scale) / 2;
    canvas.style.width = GAME_W * scale + "px";
    canvas.style.height = GAME_H * scale + "px";
    canvas.style.marginLeft = offsetX + "px";
    canvas.style.marginTop = offsetY + "px";
  }
  window.addEventListener("resize", resize);
  resize();

  // --- Audio Engine (Web Audio API) ---
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  let audioCtx = null;

  function ensureAudio() {
    if (!audioCtx) {
      audioCtx = new AudioCtx();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
  }

  function playTone(freq, duration, type, vol) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type || "square";
    osc.frequency.value = freq;
    gain.gain.value = vol || 0.08;
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
  }

  function playEngine(speed) {
    const freq = 40 + speed * 0.6;
    playTone(freq, 0.08, "sawtooth", 0.04);
  }

  function playCollision() {
    playTone(80, 0.3, "sawtooth", 0.15);
    setTimeout(() => playTone(50, 0.2, "square", 0.1), 100);
  }

  function playPass() {
    playTone(600, 0.08, "square", 0.06);
    setTimeout(() => playTone(800, 0.08, "square", 0.06), 80);
  }

  function playDayComplete() {
    const notes = [523, 659, 784, 1047];
    notes.forEach((n, i) => setTimeout(() => playTone(n, 0.2, "square", 0.1), i * 150));
  }

  function playGameOver() {
    const notes = [400, 350, 300, 250];
    notes.forEach((n, i) => setTimeout(() => playTone(n, 0.3, "square", 0.1), i * 200));
  }

  function vibrate(ms) {
    if (navigator.vibrate) navigator.vibrate(ms);
  }

  // --- Color Palettes (Day Cycle) ---
  const PALETTES = {
    day: {
      sky: ["#4a90d9", "#6ba3e0", "#8cb8e8"],
      road: "#555555",
      roadLight: "#666666",
      stripe: "#cccccc",
      ground: ["#4a8c3f", "#3d7a34"],
      mountain: "#5a7a4a",
      mountainSnow: "#ddeedd",
      cars: ["#e74c3c", "#f39c12", "#2ecc71", "#3498db", "#9b59b6", "#e67e22"],
      horizon: "#88bbdd",
      sun: "#ffdd44",
      text: "#ffffff",
    },
    sunset: {
      sky: ["#e8734a", "#d4553a", "#b8382e"],
      road: "#444444",
      roadLight: "#555555",
      stripe: "#aa9988",
      ground: ["#6b5a30", "#5a4a28"],
      mountain: "#4a3a2a",
      mountainSnow: "#cc9977",
      cars: ["#ff6644", "#ffaa33", "#44bb66", "#4488cc", "#aa55cc", "#ff8844"],
      horizon: "#cc6644",
      sun: "#ff6622",
      text: "#ffddcc",
    },
    night: {
      sky: ["#0a0a2e", "#0d0d3a", "#111146"],
      road: "#222222",
      roadLight: "#2a2a2a",
      stripe: "#555555",
      ground: ["#0a1a0a", "#081408"],
      mountain: "#111122",
      mountainSnow: "#222244",
      cars: ["#ff4444", "#ffcc22", "#44ff66", "#4499ff", "#cc66ff", "#ff8844"],
      horizon: "#111133",
      sun: null,
      text: "#8888cc",
    },
    dawn: {
      sky: ["#2a2a6e", "#4a3a7e", "#7a5a8e"],
      road: "#3a3a3a",
      roadLight: "#444444",
      stripe: "#888877",
      ground: ["#2a3a20", "#223018"],
      mountain: "#2a2a3a",
      mountainSnow: "#6a6a8a",
      cars: ["#ee5544", "#eebb33", "#33cc55", "#3388bb", "#9955bb", "#ee7733"],
      horizon: "#5544666",
      sun: "#ffaa66",
      text: "#ccbbdd",
    },
    snow: {
      sky: ["#c8d8e8", "#b8c8d8", "#a8b8c8"],
      road: "#888899",
      roadLight: "#9999aa",
      stripe: "#ffffff",
      ground: ["#ddeeff", "#ccddee"],
      mountain: "#99aabb",
      mountainSnow: "#ffffff",
      cars: ["#cc3333", "#dd9922", "#22aa44", "#2277aa", "#8844aa", "#dd6622"],
      horizon: "#aabbcc",
      sun: "#eeeedd",
      text: "#334455",
    },
    fog: {
      sky: ["#aaaaaa", "#999999", "#888888"],
      road: "#777777",
      roadLight: "#808080",
      stripe: "#bbbbbb",
      ground: ["#99aa88", "#889977"],
      mountain: "#999999",
      mountainSnow: "#aaaaaa",
      cars: ["#cc4444", "#ccaa33", "#44aa55", "#4488aa", "#8855aa", "#cc7733"],
      horizon: "#999999",
      sun: null,
      text: "#dddddd",
    },
  };

  // --- Game State ---
  const STATE = {
    TITLE: 0,
    PLAYING: 1,
    DAY_COMPLETE: 2,
    GAME_OVER: 3,
  };

  let gameState = STATE.TITLE;
  let day = 1;
  let carsToPass = 200;
  let carsPassed = 0;
  let speed = 0;
  let maxSpeed = 180;
  let playerX = 0; // -1 to 1
  let roadScroll = 0;
  let score = 0;
  let dayTimer = 0;
  let dayDuration = 60; // seconds per day cycle
  let palettePhase = 0; // 0=day, 1=sunset, 2=night, 3=dawn
  let paletteLerp = 0;
  let enemies = [];
  let collisionTimer = 0;
  let engineSoundTimer = 0;
  let titleBlink = 0;
  let dayCompleteTimer = 0;
  let gameOverTimer = 0;
  let snowParticles = [];
  let fogAlpha = 0;
  let isSnowDay = false;
  let isFogDay = false;
  let frameCount = 0;

  // --- Input ---
  let touchLeft = false;
  let touchRight = false;
  let touchBrake = false;
  let keyLeft = false;
  let keyRight = false;
  let keyBrake = false;
  let keyAccel = false;

  // --- Road Parameters ---
  const ROAD_SEGMENTS = 120;
  const SEGMENT_LENGTH = 5;
  const ROAD_WIDTH = 1200;
  const LANES = 4;
  const VISIBLE_SEGMENTS = 80;
  const CAMERA_HEIGHT = 800;
  const CAMERA_DEPTH = 1 / Math.tan((80 / 2) * Math.PI / 180);
  const DRAW_DISTANCE = VISIBLE_SEGMENTS;

  // --- Mountain shape (procedural) ---
  const mountainProfile = [];
  for (let i = 0; i <= 64; i++) {
    const x = i / 64;
    const h = Math.sin(x * Math.PI) * 0.6 +
      Math.sin(x * Math.PI * 3) * 0.15 +
      Math.sin(x * Math.PI * 7 + 1) * 0.08;
    mountainProfile.push(h);
  }

  // --- Helper Functions ---
  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function lerpColor(c1, c2, t) {
    const r1 = parseInt(c1.slice(1, 3), 16);
    const g1 = parseInt(c1.slice(3, 5), 16);
    const b1 = parseInt(c1.slice(5, 7), 16);
    const r2 = parseInt(c2.slice(1, 3), 16);
    const g2 = parseInt(c2.slice(3, 5), 16);
    const b2 = parseInt(c2.slice(5, 7), 16);
    const r = Math.round(lerp(r1, r2, t));
    const g = Math.round(lerp(g1, g2, t));
    const b = Math.round(lerp(b1, b2, t));
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }

  function getPalette() {
    const phases = ["day", "sunset", "night", "dawn"];
    const weatherPhases = isSnowDay ? ["snow", "snow", "snow", "snow"] :
      isFogDay ? ["fog", "fog", "fog", "fog"] : null;

    const currentKey = weatherPhases ? weatherPhases[palettePhase] : phases[palettePhase];
    const nextPhase = (palettePhase + 1) % 4;
    const nextKey = weatherPhases ? weatherPhases[nextPhase] : phases[nextPhase];
    const p1 = PALETTES[currentKey];
    const p2 = PALETTES[nextKey];
    const t = paletteLerp;

    return {
      sky: p1.sky.map((c, i) => lerpColor(c, p2.sky[i], t)),
      road: lerpColor(p1.road, p2.road, t),
      roadLight: lerpColor(p1.roadLight, p2.roadLight, t),
      stripe: lerpColor(p1.stripe, p2.stripe, t),
      ground: p1.ground.map((c, i) => lerpColor(c, p2.ground[i], t)),
      mountain: lerpColor(p1.mountain, p2.mountain, t),
      mountainSnow: lerpColor(p1.mountainSnow, p2.mountainSnow, t),
      cars: p1.cars.map((c, i) => lerpColor(c, p2.cars[i], t)),
      horizon: lerpColor(p1.horizon, p2.horizon, t),
      text: lerpColor(p1.text, p2.text, t),
    };
  }

  function project(z) {
    const scale = CAMERA_DEPTH / z;
    return {
      x: GAME_W / 2,
      y: GAME_H * 0.45 - scale * CAMERA_HEIGHT * GAME_H * 0.4,
      w: scale * ROAD_WIDTH * GAME_W * 0.3,
      scale: scale,
    };
  }

  // --- Enemy Car Management ---
  function spawnEnemy() {
    const lane = Math.floor(Math.random() * LANES) - LANES / 2 + 0.5;
    const laneX = (lane / (LANES / 2)) * 0.7;
    enemies.push({
      z: DRAW_DISTANCE * SEGMENT_LENGTH,
      x: laneX,
      colorIndex: Math.floor(Math.random() * 6),
      speed: 40 + Math.random() * 60,
      passed: false,
      w: 0.12,
    });
  }

  // --- Draw Car Sprite (Pixel Art Style) ---
  function drawPlayerCar(px, py, w) {
    const carW = w * 0.18;
    const carH = carW * 1.5;
    const cx = px;
    const cy = py;

    // Shadow
    ctx.fillStyle = "rgba(0,0,0,0.3)";
    ctx.fillRect(cx - carW * 0.6, cy + carH * 0.1, carW * 1.2, carH * 0.15);

    // Body
    ctx.fillStyle = "#e8e8e8";
    ctx.fillRect(cx - carW * 0.4, cy - carH * 0.7, carW * 0.8, carH * 0.95);

    // Windshield
    ctx.fillStyle = "#224488";
    ctx.fillRect(cx - carW * 0.3, cy - carH * 0.6, carW * 0.6, carH * 0.25);

    // Hood
    ctx.fillStyle = "#cccccc";
    ctx.fillRect(cx - carW * 0.35, cy - carH * 0.3, carW * 0.7, carH * 0.35);

    // Side stripes
    ctx.fillStyle = "#cc3333";
    ctx.fillRect(cx - carW * 0.45, cy - carH * 0.5, carW * 0.08, carH * 0.7);
    ctx.fillRect(cx + carW * 0.37, cy - carH * 0.5, carW * 0.08, carH * 0.7);

    // Rear / tail lights
    ctx.fillStyle = "#ff2222";
    ctx.fillRect(cx - carW * 0.35, cy + carH * 0.05, carW * 0.15, carH * 0.08);
    ctx.fillRect(cx + carW * 0.2, cy + carH * 0.05, carW * 0.15, carH * 0.08);

    // Wheels
    ctx.fillStyle = "#111111";
    ctx.fillRect(cx - carW * 0.5, cy - carH * 0.45, carW * 0.12, carH * 0.25);
    ctx.fillRect(cx + carW * 0.38, cy - carH * 0.45, carW * 0.12, carH * 0.25);
    ctx.fillRect(cx - carW * 0.5, cy + carH * -0.05, carW * 0.12, carH * 0.2);
    ctx.fillRect(cx + carW * 0.38, cy + carH * -0.05, carW * 0.12, carH * 0.2);
  }

  function drawEnemyCar(ex, ey, ew, colorIndex, pal) {
    const carW = ew;
    const carH = carW * 1.4;
    const color = pal.cars[colorIndex % pal.cars.length];

    // Shadow
    ctx.fillStyle = "rgba(0,0,0,0.3)";
    ctx.fillRect(ex - carW * 0.6, ey + carH * 0.05, carW * 1.2, carH * 0.12);

    // Body
    ctx.fillStyle = color;
    ctx.fillRect(ex - carW * 0.4, ey - carH * 0.7, carW * 0.8, carH * 0.95);

    // Windshield (rear window from player perspective)
    ctx.fillStyle = "#112233";
    ctx.fillRect(ex - carW * 0.25, ey - carH * 0.55, carW * 0.5, carH * 0.2);

    // Roof highlight
    ctx.fillStyle = lerpColor(color, "#ffffff", 0.3);
    ctx.fillRect(ex - carW * 0.3, ey - carH * 0.65, carW * 0.6, carH * 0.12);

    // Tail lights
    const isNight = palettePhase === 2 || (palettePhase === 1 && paletteLerp > 0.5);
    if (isNight) {
      ctx.fillStyle = "#ff4444";
      ctx.shadowColor = "#ff0000";
      ctx.shadowBlur = carW * 0.5;
    } else {
      ctx.fillStyle = "#cc2222";
      ctx.shadowBlur = 0;
    }
    ctx.fillRect(ex - carW * 0.38, ey + carH * 0.05, carW * 0.15, carH * 0.08);
    ctx.fillRect(ex + carW * 0.23, ey + carH * 0.05, carW * 0.15, carH * 0.08);
    ctx.shadowBlur = 0;

    // Wheels
    ctx.fillStyle = "#111111";
    ctx.fillRect(ex - carW * 0.5, ey - carH * 0.4, carW * 0.12, carH * 0.2);
    ctx.fillRect(ex + carW * 0.38, ey - carH * 0.4, carW * 0.12, carH * 0.2);
  }

  // --- Snow Particles ---
  function initSnow() {
    snowParticles = [];
    for (let i = 0; i < 80; i++) {
      snowParticles.push({
        x: Math.random() * GAME_W,
        y: Math.random() * GAME_H,
        vx: (Math.random() - 0.5) * 0.5,
        vy: 1 + Math.random() * 2,
        size: 1 + Math.random() * 2,
      });
    }
  }

  function updateSnow(dt) {
    for (const p of snowParticles) {
      p.x += p.vx + Math.sin(frameCount * 0.02 + p.y * 0.01) * 0.3;
      p.y += p.vy;
      if (p.y > GAME_H) { p.y = -5; p.x = Math.random() * GAME_W; }
      if (p.x < 0) p.x = GAME_W;
      if (p.x > GAME_W) p.x = 0;
    }
  }

  function drawSnow() {
    ctx.fillStyle = "rgba(255,255,255,0.8)";
    for (const p of snowParticles) {
      ctx.fillRect(Math.floor(p.x), Math.floor(p.y), p.size, p.size);
    }
  }

  // --- Touch Input ---
  function getTouchGamePos(touch) {
    const rect = canvas.getBoundingClientRect();
    const x = (touch.clientX - rect.left) / rect.width * GAME_W;
    const y = (touch.clientY - rect.top) / rect.height * GAME_H;
    return { x, y };
  }

  canvas.addEventListener("touchstart", function (e) {
    e.preventDefault();
    ensureAudio();
    if (gameState === STATE.TITLE) {
      startGame();
      return;
    }
    if (gameState === STATE.GAME_OVER) {
      if (gameOverTimer > 2) { resetToTitle(); }
      return;
    }
    if (gameState === STATE.DAY_COMPLETE) return;

    for (const touch of e.changedTouches) {
      const pos = getTouchGamePos(touch);
      if (pos.y > GAME_H * 0.82) {
        touchBrake = true;
      } else if (pos.x < GAME_W * 0.5) {
        touchLeft = true;
      } else {
        touchRight = true;
      }
    }
  }, { passive: false });

  canvas.addEventListener("touchend", function (e) {
    e.preventDefault();
    touchLeft = false;
    touchRight = false;
    touchBrake = false;
    // Re-check remaining touches
    for (const touch of e.touches) {
      const pos = getTouchGamePos(touch);
      if (pos.y > GAME_H * 0.82) {
        touchBrake = true;
      } else if (pos.x < GAME_W * 0.5) {
        touchLeft = true;
      } else {
        touchRight = true;
      }
    }
  }, { passive: false });

  canvas.addEventListener("touchmove", function (e) {
    e.preventDefault();
  }, { passive: false });

  // Click for desktop title
  canvas.addEventListener("click", function () {
    ensureAudio();
    if (gameState === STATE.TITLE) {
      startGame();
    } else if (gameState === STATE.GAME_OVER && gameOverTimer > 2) {
      resetToTitle();
    }
  });

  // --- Keyboard Input ---
  document.addEventListener("keydown", function (e) {
    ensureAudio();
    if (e.key === "ArrowLeft" || e.key === "a") keyLeft = true;
    if (e.key === "ArrowRight" || e.key === "d") keyRight = true;
    if (e.key === "ArrowDown" || e.key === "s") keyBrake = true;
    if (e.key === "ArrowUp" || e.key === "w") keyAccel = true;
    if (e.key === " " || e.key === "Enter") {
      if (gameState === STATE.TITLE) startGame();
      if (gameState === STATE.GAME_OVER && gameOverTimer > 2) resetToTitle();
    }
  });

  document.addEventListener("keyup", function (e) {
    if (e.key === "ArrowLeft" || e.key === "a") keyLeft = false;
    if (e.key === "ArrowRight" || e.key === "d") keyRight = false;
    if (e.key === "ArrowDown" || e.key === "s") keyBrake = false;
    if (e.key === "ArrowUp" || e.key === "w") keyAccel = false;
  });

  // --- Game Flow ---
  function startGame() {
    gameState = STATE.PLAYING;
    day = 1;
    carsToPass = 200;
    carsPassed = 0;
    speed = 0;
    playerX = 0;
    roadScroll = 0;
    score = 0;
    dayTimer = 0;
    palettePhase = 0;
    paletteLerp = 0;
    enemies = [];
    collisionTimer = 0;
    isSnowDay = false;
    isFogDay = false;
    fogAlpha = 0;
    initSnow();
  }

  function nextDay() {
    day++;
    carsPassed = 0;
    carsToPass = Math.min(200 + (day - 1) * 10, 300);
    dayTimer = 0;
    palettePhase = 0;
    paletteLerp = 0;
    enemies = [];
    dayCompleteTimer = 0;
    // Weather conditions for advanced days
    isSnowDay = day % 4 === 3;
    isFogDay = day % 4 === 0;
    if (isSnowDay) initSnow();
    fogAlpha = 0;
    gameState = STATE.PLAYING;
  }

  function resetToTitle() {
    gameState = STATE.TITLE;
    titleBlink = 0;
  }

  // --- Update ---
  let lastTime = 0;

  function update(dt) {
    frameCount++;

    if (gameState === STATE.TITLE) {
      titleBlink += dt;
      return;
    }

    if (gameState === STATE.DAY_COMPLETE) {
      dayCompleteTimer += dt;
      speed = Math.max(0, speed - 200 * dt);
      if (dayCompleteTimer > 3) {
        nextDay();
      }
      return;
    }

    if (gameState === STATE.GAME_OVER) {
      gameOverTimer += dt;
      speed = Math.max(0, speed - 200 * dt);
      return;
    }

    // --- Day cycle ---
    dayTimer += dt;
    const phaseDuration = dayDuration / 4;
    palettePhase = Math.floor(dayTimer / phaseDuration) % 4;
    paletteLerp = (dayTimer % phaseDuration) / phaseDuration;

    // Check day end
    if (dayTimer >= dayDuration) {
      if (carsPassed >= carsToPass) {
        gameState = STATE.DAY_COMPLETE;
        playDayComplete();
        return;
      } else {
        gameState = STATE.GAME_OVER;
        gameOverTimer = 0;
        playGameOver();
        return;
      }
    }

    // --- Speed / acceleration ---
    const accel = (touchBrake || keyBrake) ? -220 :
      (collisionTimer > 0) ? -350 : 120;

    speed += accel * dt;
    // Reduce max speed on snow/fog
    let effectiveMax = maxSpeed;
    if (isSnowDay) effectiveMax = 140;
    if (isFogDay) effectiveMax = 150;
    speed = Math.max(0, Math.min(effectiveMax, speed));

    // Collision cooldown
    if (collisionTimer > 0) {
      collisionTimer -= dt;
    }

    // --- Player movement ---
    const steerSpeed = 1.8;
    let steering = 0;
    if (touchLeft || keyLeft) steering = -steerSpeed;
    if (touchRight || keyRight) steering = steerSpeed;
    playerX += steering * dt;
    playerX = Math.max(-1.1, Math.min(1.1, playerX));

    // Off-road friction
    if (Math.abs(playerX) > 0.85) {
      speed = Math.max(0, speed - 80 * dt);
    }

    // --- Road scroll ---
    roadScroll += speed * dt;

    // --- Spawn enemies ---
    const spawnRate = 0.6 + Math.min(day * 0.1, 0.8);
    if (Math.random() < spawnRate * dt && enemies.length < 12) {
      spawnEnemy();
    }

    // --- Update enemies ---
    const playerZ = 5;
    for (let i = enemies.length - 1; i >= 0; i--) {
      const e = enemies[i];
      e.z -= (speed - e.speed) * dt * 0.15;

      // Check if passed
      if (!e.passed && e.z < playerZ) {
        e.passed = true;
        carsPassed++;
        score += 10;
        playPass();
      }

      // Remove if too far behind or ahead
      if (e.z < -10 || e.z > DRAW_DISTANCE * SEGMENT_LENGTH + 50) {
        enemies.splice(i, 1);
        continue;
      }

      // Collision check
      if (collisionTimer <= 0 && e.z > 0 && e.z < 8) {
        const projP = project(playerZ);
        const projE = project(Math.max(e.z, 0.5));
        const pScreenX = projP.x + playerX * projP.w * 0.5;
        const eScreenX = projE.x + e.x * projE.w * 0.5;
        const pCarW = projP.w * 0.09;
        const eCarW = projE.w * 0.09;

        if (Math.abs(pScreenX - eScreenX) < (pCarW + eCarW) * 0.7 &&
          Math.abs(projP.y - projE.y) < 30) {
          collisionTimer = 0.8;
          speed = Math.max(0, speed * 0.2);
          playCollision();
          vibrate(100);
          // Push enemy away
          e.z = playerZ + 10;
        }
      }
    }

    // --- Engine sound ---
    engineSoundTimer += dt;
    if (engineSoundTimer > 0.1 && speed > 5) {
      playEngine(speed);
      engineSoundTimer = 0;
    }

    // --- Snow ---
    if (isSnowDay) updateSnow(dt);

    // --- Fog ---
    if (isFogDay) {
      fogAlpha = 0.3 + Math.sin(dayTimer * 0.5) * 0.1;
    }
  }

  // --- Render ---
  function render() {
    const pal = getPalette();

    // --- Sky gradient ---
    const skyGrad = ctx.createLinearGradient(0, 0, 0, GAME_H * 0.45);
    skyGrad.addColorStop(0, pal.sky[0]);
    skyGrad.addColorStop(0.5, pal.sky[1]);
    skyGrad.addColorStop(1, pal.sky[2]);
    ctx.fillStyle = skyGrad;
    ctx.fillRect(0, 0, GAME_W, GAME_H * 0.45);

    // --- Mountains ---
    const horizonY = GAME_H * 0.45;
    ctx.fillStyle = pal.mountain;
    ctx.beginPath();
    ctx.moveTo(0, horizonY);
    for (let i = 0; i <= 64; i++) {
      const x = (i / 64) * GAME_W;
      const h = mountainProfile[i] * 60;
      ctx.lineTo(x, horizonY - h);
    }
    ctx.lineTo(GAME_W, horizonY);
    ctx.closePath();
    ctx.fill();

    // Mountain snow caps
    ctx.fillStyle = pal.mountainSnow;
    ctx.beginPath();
    ctx.moveTo(0, horizonY);
    for (let i = 0; i <= 64; i++) {
      const x = (i / 64) * GAME_W;
      const h = mountainProfile[i] * 60;
      if (mountainProfile[i] > 0.5) {
        ctx.lineTo(x, horizonY - h);
      } else {
        ctx.lineTo(x, horizonY);
      }
    }
    ctx.lineTo(GAME_W, horizonY);
    ctx.closePath();
    ctx.fill();

    // --- Road rendering (pseudo-3D) ---
    const scrollOffset = (roadScroll / SEGMENT_LENGTH) % 1;

    for (let n = DRAW_DISTANCE; n > 0; n--) {
      const z1 = (n + scrollOffset) * SEGMENT_LENGTH;
      const z2 = (n - 1 + scrollOffset) * SEGMENT_LENGTH;
      const p1 = project(z1);
      const p2 = project(z2);

      if (p2.y < horizonY - 2) continue;

      const segIndex = Math.floor(roadScroll / SEGMENT_LENGTH) + n;

      // Ground
      const groundColor = segIndex % 4 < 2 ? pal.ground[0] : pal.ground[1];
      ctx.fillStyle = groundColor;
      ctx.fillRect(0, p2.y, GAME_W, p1.y - p2.y + 1);

      // Road
      const roadColor = segIndex % 4 < 2 ? pal.road : pal.roadLight;
      ctx.fillStyle = roadColor;
      const r1x1 = p1.x - p1.w * 0.5;
      const r1x2 = p1.x + p1.w * 0.5;
      const r2x1 = p2.x - p2.w * 0.5;
      const r2x2 = p2.x + p2.w * 0.5;

      ctx.beginPath();
      ctx.moveTo(r1x1, p1.y);
      ctx.lineTo(r1x2, p1.y);
      ctx.lineTo(r2x2, p2.y);
      ctx.lineTo(r2x1, p2.y);
      ctx.closePath();
      ctx.fill();

      // Center stripe
      if (segIndex % 6 < 3) {
        ctx.fillStyle = pal.stripe;
        const sw1 = p1.w * 0.008;
        const sw2 = p2.w * 0.008;
        ctx.beginPath();
        ctx.moveTo(p1.x - sw1, p1.y);
        ctx.lineTo(p1.x + sw1, p1.y);
        ctx.lineTo(p2.x + sw2, p2.y);
        ctx.lineTo(p2.x - sw2, p2.y);
        ctx.closePath();
        ctx.fill();
      }

      // Road edge lines
      ctx.fillStyle = pal.stripe;
      const ew1 = p1.w * 0.006;
      const ew2 = p2.w * 0.006;
      // Left edge
      ctx.beginPath();
      ctx.moveTo(r1x1 - ew1, p1.y);
      ctx.lineTo(r1x1 + ew1, p1.y);
      ctx.lineTo(r2x1 + ew2, p2.y);
      ctx.lineTo(r2x1 - ew2, p2.y);
      ctx.closePath();
      ctx.fill();
      // Right edge
      ctx.beginPath();
      ctx.moveTo(r1x2 - ew1, p1.y);
      ctx.lineTo(r1x2 + ew1, p1.y);
      ctx.lineTo(r2x2 + ew2, p2.y);
      ctx.lineTo(r2x2 - ew2, p2.y);
      ctx.closePath();
      ctx.fill();
    }

    // --- Draw enemies (back to front for proper overlap) ---
    const sortedEnemies = enemies.filter(e => e.z > 0.5).sort((a, b) => b.z - a.z);
    for (const e of sortedEnemies) {
      const proj = project(e.z);
      const ex = proj.x + e.x * proj.w * 0.5;
      const ey = proj.y;
      const ew = proj.w * 0.09;
      if (ew < 1) continue;
      if (ey < horizonY - 10 || ey > GAME_H) continue;
      drawEnemyCar(ex, ey, ew, e.colorIndex, pal);
    }

    // --- Draw player car ---
    if (gameState === STATE.PLAYING || gameState === STATE.DAY_COMPLETE || gameState === STATE.GAME_OVER) {
      const pProj = project(5);
      const px = pProj.x + playerX * pProj.w * 0.5;
      const py = GAME_H * 0.88;

      // Collision flash
      if (collisionTimer > 0 && Math.floor(collisionTimer * 10) % 2 === 0) {
        ctx.globalAlpha = 0.5;
      }
      drawPlayerCar(px, py, pProj.w);
      ctx.globalAlpha = 1;
    }

    // --- Snow ---
    if (isSnowDay) drawSnow();

    // --- Fog overlay ---
    if (isFogDay && fogAlpha > 0) {
      ctx.fillStyle = "rgba(180,180,180," + fogAlpha.toFixed(2) + ")";
      ctx.fillRect(0, GAME_H * 0.3, GAME_W, GAME_H * 0.7);
    }

    // --- HUD ---
    if (gameState === STATE.PLAYING || gameState === STATE.DAY_COMPLETE) {
      ctx.fillStyle = pal.text;
      ctx.font = "bold 11px monospace";
      ctx.textAlign = "left";

      // Speed bar
      const barX = 10;
      const barY = 14;
      const barW = 70;
      const barH = 8;
      ctx.fillStyle = "rgba(0,0,0,0.5)";
      ctx.fillRect(barX, barY, barW, barH);
      const speedPct = speed / maxSpeed;
      const speedColor = speedPct > 0.7 ? "#ff4444" : speedPct > 0.4 ? "#ffaa22" : "#44cc44";
      ctx.fillStyle = speedColor;
      ctx.fillRect(barX, barY, barW * speedPct, barH);
      ctx.fillStyle = pal.text;
      ctx.fillText(Math.floor(speed) + " km/h", barX, barY + barH + 12);

      // Day & Cars passed
      ctx.textAlign = "right";
      ctx.fillText("DIA " + day, GAME_W - 10, 14);
      ctx.fillText(carsPassed + " / " + carsToPass, GAME_W - 10, 28);

      // Time remaining in day
      const timeLeft = Math.max(0, dayDuration - dayTimer);
      const mins = Math.floor(timeLeft / 60);
      const secs = Math.floor(timeLeft % 60);
      ctx.textAlign = "center";
      ctx.fillText(mins + ":" + (secs < 10 ? "0" : "") + secs, GAME_W / 2, 14);

      // Score
      ctx.fillText("SCORE: " + score, GAME_W / 2, 28);

      // Weather indicator
      if (isSnowDay) {
        ctx.fillText("* NEVE *", GAME_W / 2, 42);
      }
      if (isFogDay) {
        ctx.fillText("~ NEBLINA ~", GAME_W / 2, 42);
      }

      // Touch control hints (semi-transparent)
      ctx.fillStyle = "rgba(255,255,255,0.12)";
      ctx.fillRect(0, GAME_H * 0.82, GAME_W, GAME_H * 0.18);
      ctx.fillStyle = "rgba(255,255,255,0.2)";
      ctx.font = "9px monospace";
      ctx.textAlign = "center";
      ctx.fillText("FREIO", GAME_W / 2, GAME_H * 0.95);

      // Left/right indicators
      ctx.fillStyle = "rgba(255,255,255,0.08)";
      ctx.fillRect(0, GAME_H * 0.45, GAME_W * 0.15, GAME_H * 0.37);
      ctx.fillRect(GAME_W * 0.85, GAME_H * 0.45, GAME_W * 0.15, GAME_H * 0.37);
      ctx.fillStyle = "rgba(255,255,255,0.15)";
      ctx.font = "16px monospace";
      ctx.textAlign = "center";
      ctx.fillText("<", GAME_W * 0.075, GAME_H * 0.65);
      ctx.fillText(">", GAME_W * 0.925, GAME_H * 0.65);
    }

    // --- Title Screen ---
    if (gameState === STATE.TITLE) {
      // Dark overlay
      ctx.fillStyle = "rgba(0,0,0,0.7)";
      ctx.fillRect(0, 0, GAME_W, GAME_H);

      // Title
      ctx.fillStyle = "#ffcc00";
      ctx.font = "bold 38px monospace";
      ctx.textAlign = "center";
      ctx.fillText("ENDURO", GAME_W / 2, GAME_H * 0.28);

      // Subtitle
      ctx.fillStyle = "#ff8844";
      ctx.font = "12px monospace";
      ctx.fillText("ATARI CLASSIC TRIBUTE", GAME_W / 2, GAME_H * 0.34);

      // Car sprite on title
      drawPlayerCar(GAME_W / 2, GAME_H * 0.50, 350);

      // Instructions
      ctx.fillStyle = "#cccccc";
      ctx.font = "11px monospace";
      ctx.fillText("ULTRAPASSE OS CARROS", GAME_W / 2, GAME_H * 0.64);
      ctx.fillText("ANTES DO TEMPO ACABAR!", GAME_W / 2, GAME_H * 0.68);

      ctx.font = "10px monospace";
      ctx.fillStyle = "#888888";
      ctx.fillText("TOQUE ESQUERDA/DIREITA = MOVER", GAME_W / 2, GAME_H * 0.75);
      ctx.fillText("TOQUE EMBAIXO = FREIO", GAME_W / 2, GAME_H * 0.79);

      // Blink prompt
      if (Math.floor(titleBlink * 2) % 2 === 0) {
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 14px monospace";
        ctx.fillText("TOQUE PARA JOGAR", GAME_W / 2, GAME_H * 0.89);
      }
    }

    // --- Day Complete Screen ---
    if (gameState === STATE.DAY_COMPLETE) {
      ctx.fillStyle = "rgba(0,0,0,0.6)";
      ctx.fillRect(0, GAME_H * 0.3, GAME_W, GAME_H * 0.3);

      ctx.fillStyle = "#ffcc00";
      ctx.font = "bold 22px monospace";
      ctx.textAlign = "center";
      ctx.fillText("DIA " + day + " COMPLETO!", GAME_W / 2, GAME_H * 0.42);

      ctx.fillStyle = "#ffffff";
      ctx.font = "14px monospace";
      ctx.fillText(carsPassed + " CARROS ULTRAPASSADOS", GAME_W / 2, GAME_H * 0.50);
      ctx.fillText("SCORE: " + score, GAME_W / 2, GAME_H * 0.55);
    }

    // --- Game Over Screen ---
    if (gameState === STATE.GAME_OVER) {
      ctx.fillStyle = "rgba(0,0,0,0.7)";
      ctx.fillRect(0, GAME_H * 0.25, GAME_W, GAME_H * 0.4);

      ctx.fillStyle = "#ff4444";
      ctx.font = "bold 26px monospace";
      ctx.textAlign = "center";
      ctx.fillText("GAME OVER", GAME_W / 2, GAME_H * 0.38);

      ctx.fillStyle = "#ffffff";
      ctx.font = "13px monospace";
      ctx.fillText("DIA " + day, GAME_W / 2, GAME_H * 0.45);
      ctx.fillText("ULTRAPASSOU: " + carsPassed + " / " + carsToPass, GAME_W / 2, GAME_H * 0.50);
      ctx.fillText("SCORE FINAL: " + score, GAME_W / 2, GAME_H * 0.55);

      if (gameOverTimer > 2 && Math.floor(gameOverTimer * 2) % 2 === 0) {
        ctx.fillStyle = "#cccccc";
        ctx.font = "12px monospace";
        ctx.fillText("TOQUE PARA RECOMECAR", GAME_W / 2, GAME_H * 0.62);
      }
    }
  }

  // --- Game Loop ---
  function gameLoop(timestamp) {
    const dt = Math.min((timestamp - lastTime) / 1000, 0.05);
    lastTime = timestamp;

    update(dt);
    render();

    requestAnimationFrame(gameLoop);
  }

  lastTime = performance.now();
  requestAnimationFrame(gameLoop);
})();
