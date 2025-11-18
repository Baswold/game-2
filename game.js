// Game Constants
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = 800;
canvas.height = 600;

// Game State
let gameState = {
    running: false,
    paused: false,
    score: 0,
    highScore: localStorage.getItem('highScore') || 0,
    level: 1,
    lives: 3,
    combo: 0,
    comboTimer: 0
};

// Player
const player = {
    x: canvas.width / 2,
    y: canvas.height - 80,
    width: 40,
    height: 40,
    speed: 6,
    dx: 0
};

// Game Arrays
let bullets = [];
let enemies = [];
let particles = [];
let powerUps = [];

// Input
const keys = {};

// Enemy spawn settings
let enemySpawnTimer = 0;
let enemySpawnRate = 60; // frames between spawns

// Animation frame
let animationId;

// Event Listeners
document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('resumeButton').addEventListener('click', togglePause);
document.getElementById('restartButton').addEventListener('click', restartGame);

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;

    if (e.key === ' ' && gameState.running && !gameState.paused) {
        e.preventDefault();
        shoot();
    }

    if (e.key === 'p' || e.key === 'P') {
        if (gameState.running) {
            togglePause();
        }
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Initialize high score display
document.getElementById('highScore').textContent = gameState.highScore;

// Game Functions
function startGame() {
    document.getElementById('startScreen').classList.add('hidden');
    gameState.running = true;
    gameState.paused = false;
    gameState.score = 0;
    gameState.level = 1;
    gameState.lives = 3;
    gameState.combo = 0;

    // Reset game state
    bullets = [];
    enemies = [];
    particles = [];
    powerUps = [];

    player.x = canvas.width / 2;
    player.y = canvas.height - 80;

    enemySpawnRate = 60;

    updateUI();
    gameLoop();
}

function togglePause() {
    if (!gameState.running) return;

    gameState.paused = !gameState.paused;

    if (gameState.paused) {
        document.getElementById('pauseScreen').classList.remove('hidden');
        cancelAnimationFrame(animationId);
    } else {
        document.getElementById('pauseScreen').classList.add('hidden');
        gameLoop();
    }
}

function gameOver() {
    gameState.running = false;
    cancelAnimationFrame(animationId);

    document.getElementById('finalScore').textContent = `Final Score: ${gameState.score}`;

    if (gameState.score > gameState.highScore) {
        gameState.highScore = gameState.score;
        localStorage.setItem('highScore', gameState.highScore);
        document.getElementById('highScore').textContent = gameState.highScore;
        document.getElementById('newHighScore').classList.remove('hidden');
    } else {
        document.getElementById('newHighScore').classList.add('hidden');
    }

    document.getElementById('gameOverScreen').classList.remove('hidden');
}

function restartGame() {
    document.getElementById('gameOverScreen').classList.add('hidden');
    startGame();
}

function updateUI() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('level').textContent = gameState.level;

    let heartsDisplay = '';
    for (let i = 0; i < gameState.lives; i++) {
        heartsDisplay += '❤️';
    }
    document.getElementById('lives').textContent = heartsDisplay || '💀';
}

// Player Movement
function movePlayer() {
    player.dx = 0;

    if (keys['ArrowLeft'] || keys['a'] || keys['A']) {
        player.dx = -player.speed;
    }
    if (keys['ArrowRight'] || keys['d'] || keys['D']) {
        player.dx = player.speed;
    }

    player.x += player.dx;

    // Boundaries
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
}

function drawPlayer() {
    // Draw spaceship
    ctx.save();
    ctx.translate(player.x + player.width / 2, player.y + player.height / 2);

    // Ship body
    ctx.fillStyle = '#00ffff';
    ctx.beginPath();
    ctx.moveTo(0, -20);
    ctx.lineTo(-15, 20);
    ctx.lineTo(15, 20);
    ctx.closePath();
    ctx.fill();

    // Ship cockpit
    ctx.fillStyle = '#0099ff';
    ctx.beginPath();
    ctx.arc(0, 0, 8, 0, Math.PI * 2);
    ctx.fill();

    // Engine glow
    ctx.fillStyle = '#ff6600';
    ctx.beginPath();
    ctx.moveTo(-10, 20);
    ctx.lineTo(-8, 28);
    ctx.lineTo(-12, 28);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(10, 20);
    ctx.lineTo(8, 28);
    ctx.lineTo(12, 28);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
}

// Shooting
let shootCooldown = 0;
const shootCooldownMax = 15;

function shoot() {
    if (shootCooldown > 0) return;

    bullets.push({
        x: player.x + player.width / 2 - 2,
        y: player.y,
        width: 4,
        height: 15,
        speed: 8,
        damage: 1
    });

    shootCooldown = shootCooldownMax;
}

function updateBullets() {
    if (shootCooldown > 0) shootCooldown--;

    bullets.forEach((bullet, index) => {
        bullet.y -= bullet.speed;

        // Remove off-screen bullets
        if (bullet.y < -bullet.height) {
            bullets.splice(index, 1);
        }
    });
}

function drawBullets() {
    ctx.fillStyle = '#ffff00';
    ctx.shadowBlur = 10;
    ctx.shadowColor = '#ffff00';

    bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });

    ctx.shadowBlur = 0;
}

// Enemies
function spawnEnemy() {
    const types = ['basic', 'fast', 'tank'];
    const weights = [70, 20, 10];

    let random = Math.random() * 100;
    let type = 'basic';

    if (random > 70 && random <= 90) type = 'fast';
    else if (random > 90) type = 'tank';

    let enemy = {
        x: Math.random() * (canvas.width - 40),
        y: -50,
        width: 35,
        height: 35,
        speed: 2,
        health: 1,
        points: 10,
        type: type
    };

    // Adjust stats based on type
    switch(type) {
        case 'fast':
            enemy.speed = 4;
            enemy.health = 1;
            enemy.points = 20;
            enemy.width = 25;
            enemy.height = 25;
            break;
        case 'tank':
            enemy.speed = 1;
            enemy.health = 3;
            enemy.points = 50;
            enemy.width = 45;
            enemy.height = 45;
            break;
    }

    // Increase difficulty with level
    enemy.speed += gameState.level * 0.3;

    enemies.push(enemy);
}

function updateEnemies() {
    enemySpawnTimer++;

    // Spawn enemies
    if (enemySpawnTimer >= enemySpawnRate) {
        spawnEnemy();
        enemySpawnTimer = 0;

        // Increase spawn rate with level
        enemySpawnRate = Math.max(20, 60 - gameState.level * 3);
    }

    enemies.forEach((enemy, index) => {
        enemy.y += enemy.speed;

        // Remove off-screen enemies and lose life
        if (enemy.y > canvas.height) {
            enemies.splice(index, 1);
            loseLife();
        }
    });
}

function drawEnemies() {
    enemies.forEach(enemy => {
        ctx.save();
        ctx.translate(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2);

        // Different colors for different types
        switch(enemy.type) {
            case 'basic':
                ctx.fillStyle = '#ff0000';
                break;
            case 'fast':
                ctx.fillStyle = '#ff00ff';
                break;
            case 'tank':
                ctx.fillStyle = '#ff6600';
                break;
        }

        ctx.shadowBlur = 10;
        ctx.shadowColor = ctx.fillStyle;

        // Draw enemy ship
        ctx.beginPath();
        ctx.moveTo(0, enemy.height / 2);
        ctx.lineTo(-enemy.width / 2, -enemy.height / 2);
        ctx.lineTo(enemy.width / 2, -enemy.height / 2);
        ctx.closePath();
        ctx.fill();

        // Draw health indicator for tanks
        if (enemy.type === 'tank') {
            ctx.fillStyle = '#ffffff';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(enemy.health, 0, 5);
        }

        ctx.restore();
    });

    ctx.shadowBlur = 0;
}

// Collision Detection
function checkCollisions() {
    // Bullet-Enemy collisions
    bullets.forEach((bullet, bulletIndex) => {
        enemies.forEach((enemy, enemyIndex) => {
            if (
                bullet.x < enemy.x + enemy.width &&
                bullet.x + bullet.width > enemy.x &&
                bullet.y < enemy.y + enemy.height &&
                bullet.y + bullet.height > enemy.y
            ) {
                // Hit!
                bullets.splice(bulletIndex, 1);
                enemy.health -= bullet.damage;

                createParticles(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2, '#ffff00');

                if (enemy.health <= 0) {
                    // Enemy destroyed
                    enemies.splice(enemyIndex, 1);

                    // Update score with combo
                    gameState.combo++;
                    gameState.comboTimer = 60; // Reset combo timer
                    let multiplier = 1 + Math.floor(gameState.combo / 5) * 0.5;
                    let points = Math.floor(enemy.points * multiplier);
                    gameState.score += points;

                    createParticles(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2, '#ff0000', 20);

                    // Level up every 500 points
                    if (Math.floor(gameState.score / 500) + 1 > gameState.level) {
                        gameState.level++;
                        createLevelUpEffect();
                    }

                    updateUI();
                }
            }
        });
    });

    // Player-Enemy collisions
    enemies.forEach((enemy, index) => {
        if (
            player.x < enemy.x + enemy.width &&
            player.x + player.width > enemy.x &&
            player.y < enemy.y + enemy.height &&
            player.y + player.height > enemy.y
        ) {
            enemies.splice(index, 1);
            loseLife();
            createParticles(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2, '#ff0000', 30);
        }
    });
}

function loseLife() {
    gameState.lives--;
    gameState.combo = 0; // Reset combo on hit
    updateUI();

    if (gameState.lives <= 0) {
        gameOver();
    } else {
        // Brief invincibility flash effect
        createParticles(player.x + player.width / 2, player.y + player.height / 2, '#ffffff', 15);
    }
}

// Particles
function createParticles(x, y, color, count = 10) {
    for (let i = 0; i < count; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 6,
            vy: (Math.random() - 0.5) * 6,
            life: 30,
            color: color,
            size: Math.random() * 3 + 1
        });
    }
}

function updateParticles() {
    // Update combo timer
    if (gameState.comboTimer > 0) {
        gameState.comboTimer--;
    } else {
        gameState.combo = 0;
    }

    particles.forEach((particle, index) => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.life--;
        particle.size *= 0.95;

        if (particle.life <= 0) {
            particles.splice(index, 1);
        }
    });
}

function drawParticles() {
    particles.forEach(particle => {
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.life / 30;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1;
}

// Level up effect
function createLevelUpEffect() {
    for (let i = 0; i < 50; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 2,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            life: 60,
            color: '#00ffff',
            size: Math.random() * 5 + 2
        });
    }
}

// Draw starfield background
let stars = [];
for (let i = 0; i < 100; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2,
        speed: Math.random() * 2 + 0.5
    });
}

function updateStars() {
    stars.forEach(star => {
        star.y += star.speed;
        if (star.y > canvas.height) {
            star.y = 0;
            star.x = Math.random() * canvas.width;
        }
    });
}

function drawStars() {
    ctx.fillStyle = '#ffffff';
    stars.forEach(star => {
        ctx.globalAlpha = 0.8;
        ctx.fillRect(star.x, star.y, star.size, star.size);
    });
    ctx.globalAlpha = 1;
}

// Draw combo indicator
function drawCombo() {
    if (gameState.combo > 4) {
        ctx.save();
        ctx.font = 'bold 24px Arial';
        ctx.fillStyle = '#ffff00';
        ctx.strokeStyle = '#ff6600';
        ctx.lineWidth = 2;
        ctx.textAlign = 'center';

        let multiplier = 1 + Math.floor(gameState.combo / 5) * 0.5;
        let text = `COMBO x${gameState.combo} (${multiplier.toFixed(1)}x POINTS!)`;

        ctx.strokeText(text, canvas.width / 2, 40);
        ctx.fillText(text, canvas.width / 2, 40);

        ctx.restore();
    }
}

// Main Game Loop
function gameLoop() {
    if (!gameState.running || gameState.paused) return;

    // Clear canvas
    ctx.fillStyle = 'rgba(0, 0, 20, 0.3)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Update
    updateStars();
    movePlayer();
    updateBullets();
    updateEnemies();
    updateParticles();
    checkCollisions();

    // Draw
    drawStars();
    drawPlayer();
    drawBullets();
    drawEnemies();
    drawParticles();
    drawCombo();

    animationId = requestAnimationFrame(gameLoop);
}

// Initial draw
ctx.fillStyle = '#000010';
ctx.fillRect(0, 0, canvas.width, canvas.height);
drawStars();
