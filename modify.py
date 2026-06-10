import re

file_path = "index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace fonts
content = content.replace("font-family: 'Playfair Display', serif;", "font-family: 'Space Mono', monospace;")
content = content.replace("font-family: 'JetBrains Mono', monospace;", "font-family: 'Space Mono', monospace;")
content = content.replace("font-family: 'Plus Jakarta Sans', sans-serif;", "font-family: 'Outfit', sans-serif;")

# 2. Update CSS for Glassmorphism & High-tech look
# Nav background
content = content.replace("background: rgba(7,9,14,0.85);", "background: rgba(2,4,10,0.65);\n  backdrop-filter: blur(24px);\n  -webkit-backdrop-filter: blur(24px);")
# problem-card
content = content.replace(".problem-card {\n  background: var(--surface);\n  border: 1px solid var(--border);\n  border-radius: var(--radius);\n  padding: 24px;\n  transition: all 0.3s ease;\n  position: relative;\n  overflow: hidden;\n}", ".problem-card {\n  background: var(--surface);\n  backdrop-filter: blur(16px);\n  -webkit-backdrop-filter: blur(16px);\n  border: 1px solid var(--border);\n  border-radius: var(--radius);\n  padding: 24px;\n  transition: all 0.3s ease;\n  position: relative;\n  overflow: hidden;\n}")
# demo-terminal
content = content.replace(".demo-terminal {\n  background: #0a0e18;\n  border: 1px solid rgba(240,160,32,0.18);\n  border-radius: var(--radius-lg);\n  overflow: hidden;\n  box-shadow: 0 24px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04);\n}", ".demo-terminal {\n  background: rgba(10, 15, 25, 0.45);\n  backdrop-filter: blur(20px);\n  -webkit-backdrop-filter: blur(20px);\n  border: 1px solid var(--border2);\n  border-radius: var(--radius-lg);\n  overflow: hidden;\n  box-shadow: 0 24px 80px rgba(0,0,0,0.7), 0 0 0 1px rgba(0,240,255,0.1);\n}")
# callout
content = content.replace(".callout {\n  background: linear-gradient(135deg, rgba(248,113,113,0.05), rgba(251,146,60,0.03));\n  border: 1px solid rgba(248,113,113,0.13);\n  border-radius: var(--radius);\n  padding: 22px 26px;\n}", ".callout {\n  background: linear-gradient(135deg, rgba(0,240,255,0.05), rgba(161,66,244,0.03));\n  backdrop-filter: blur(12px);\n  border: 1px solid rgba(0,240,255,0.13);\n  border-radius: var(--radius);\n  padding: 22px 26px;\n}")
# ftbl th
content = content.replace("background: var(--surface);", "background: rgba(10, 15, 25, 0.6);\n  backdrop-filter: blur(10px);")

# Update section labels to look like HUD brackets
content = re.sub(r'<span class="section-label([^>]*)">(.*?)</span>', r'<span class="section-label\1">// \2 -></span>', content)

# 3. Add canvas right after body
content = content.replace("<body>", "<body>\n\n<canvas id=\"bg-canvas\"></canvas>\n")

# 4. Add particle logic at the end before </body>
particle_script = """
<script>
// --- ACTIVE THEORY PARTICLE BACKGROUND ---
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d', { alpha: false });
let w, h;
let particles = [];
const PARTICLE_COUNT = 3000;

function init() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    particles = [];
    
    for(let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
            x: Math.random() * w,
            y: Math.random() * h,
            z: Math.random() * 1000 + 100, // depth
            ox: Math.random() * w,
            oy: Math.random() * h,
            vx: 0, vy: 0,
            baseColor: Math.random() > 0.8 ? '#00f0ff' : (Math.random() > 0.5 ? '#a142f4' : '#f06292'),
            size: Math.random() * 2 + 0.5
        });
    }
}

let mouseX = window.innerWidth/2;
let mouseY = window.innerHeight/2;
let targetMouseX = mouseX;
let targetMouseY = mouseY;

window.addEventListener('mousemove', (e) => {
    targetMouseX = e.clientX;
    targetMouseY = e.clientY;
});

window.addEventListener('resize', init);
init();

function draw() {
    // Very dark blue/black background with trail effect
    ctx.fillStyle = 'rgba(2, 4, 10, 0.2)';
    ctx.fillRect(0, 0, w, h);
    
    // Smooth mouse
    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;
    
    // Move origin to center for 3D calculations
    const cx = w/2;
    const cy = h/2;
    
    particles.forEach(p => {
        // Parallax effect based on depth (z)
        const prlxX = (mouseX - cx) * (p.z * 0.0005);
        const prlxY = (mouseY - cy) * (p.z * 0.0005);
        
        // Gentle swirling motion
        p.ox += Math.sin(p.z) * 0.2;
        p.oy += Math.cos(p.z) * 0.2;
        
        // Wrap around
        if (p.ox > w + 200) p.ox = -200;
        if (p.ox < -200) p.ox = w + 200;
        if (p.oy > h + 200) p.oy = -200;
        if (p.oy < -200) p.oy = h + 200;
        
        const finalX = p.ox - prlxX;
        const finalY = p.oy - prlxY;
        
        // Perspective scaling
        const scale = 1000 / p.z;
        
        ctx.fillStyle = p.baseColor;
        ctx.globalAlpha = Math.min(1, scale * 0.5);
        ctx.beginPath();
        ctx.arc(finalX, finalY, p.size * scale, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
}
draw();
</script>
"""

content = content.replace("</body>", particle_script + "\n</body>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Modifications applied successfully.")
