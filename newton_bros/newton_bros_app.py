"""
╔══════════════════════════════════════════════╗
║       NEWTON BROS - Calculadora Física       ║
║     Leyes de Newton con estilo Mario Bros    ║
║                                              ║
║  Requisitos:  pip install flask              ║
║  Ejecutar:    python newton_bros_app.py      ║
║  Abrir:       http://localhost:5000          ║
╚══════════════════════════════════════════════╝
"""

from flask import Flask, request, jsonify, render_template_string
import math

app = Flask(__name__)

# ══════════════════════════════════════════════
#   LÓGICA DE CÁLCULO — LEYES DE NEWTON
# ══════════════════════════════════════════════

def calcular_ley1(masa, velocidad, friccion, tiempo):
    """
    Primera Ley de Newton — Ley de Inercia
    Si fricción = 0: objeto sigue a velocidad constante
    Si fricción > 0: la fricción desacelera al objeto
    """
    g = 9.8  # m/s²
    if friccion == 0:
        distancia = velocidad * tiempo
        return {
            "resultado": round(velocidad, 4),
            "unidad": "m/s (velocidad constante, sin fricción)",
            "extra": f"Distancia recorrida en {tiempo}s: {round(distancia, 4)} m",
            "datos": {
                "masa": masa,
                "velocidad_inicial": velocidad,
                "friccion": friccion,
                "tiempo": tiempo,
                "aceleracion": 0,
                "velocidad_final": velocidad,
                "distancia": distancia,
            }
        }
    else:
        a = -friccion * g
        v_final = velocidad + a * tiempo
        v_final = max(0.0, round(v_final, 4))
        distancia = velocidad * tiempo + 0.5 * a * tiempo**2
        distancia = max(0.0, round(distancia, 4))
        tiempo_stop = velocidad / (friccion * g) if friccion > 0 else float("inf")
        return {
            "resultado": v_final,
            "unidad": f"m/s (velocidad final con μ={friccion})",
            "extra": (
                f"Desaceleración: {round(abs(a), 4)} m/s²  |  "
                f"Distancia recorrida: {distancia} m  |  "
                f"Se detiene en: {round(tiempo_stop, 2)} s"
            ),
            "datos": {
                "masa": masa,
                "velocidad_inicial": velocidad,
                "friccion": friccion,
                "tiempo": tiempo,
                "aceleracion": round(a, 4),
                "velocidad_final": v_final,
                "distancia": distancia,
            }
        }


def calcular_ley2(masa, fuerza, tiempo, v0):
    """
    Segunda Ley de Newton — F = m · a
    Calcula: aceleración, velocidad final, distancia recorrida
    """
    aceleracion = fuerza / masa
    v_final     = v0 + aceleracion * tiempo
    distancia   = v0 * tiempo + 0.5 * aceleracion * tiempo**2
    return {
        "resultado": round(aceleracion, 4),
        "unidad": "m/s² (aceleración)",
        "extra": (
            f"Velocidad final: {round(v_final, 4)} m/s  |  "
            f"Distancia recorrida: {round(distancia, 4)} m"
        ),
        "datos": {
            "masa": masa,
            "fuerza": fuerza,
            "tiempo": tiempo,
            "v0": v0,
            "aceleracion": round(aceleracion, 4),
            "velocidad_final": round(v_final, 4),
            "distancia": round(distancia, 4),
        }
    }


def calcular_ley3(fuerza, masa1, masa2, tiempo):
    """
    Tercera Ley de Newton — Acción y Reacción
    F_accion = -F_reaccion
    Calcula aceleración de cada cuerpo ante la misma fuerza
    """
    a1 = fuerza / masa1
    a2 = fuerza / masa2
    d1 = 0.5 * a1 * tiempo**2
    d2 = 0.5 * a2 * tiempo**2
    return {
        "resultado": round(fuerza, 4),
        "unidad": "N (fuerza de reacción, igual y opuesta)",
        "extra": (
            f"Aceleración A: {round(a1, 4)} m/s², dist: {round(d1, 4)} m  |  "
            f"Aceleración B: {round(a2, 4)} m/s², dist: {round(d2, 4)} m"
        ),
        "datos": {
            "fuerza": fuerza,
            "masa1": masa1,
            "masa2": masa2,
            "tiempo": tiempo,
            "a1": round(a1, 4),
            "a2": round(a2, 4),
            "d1": round(d1, 4),
            "d2": round(d2, 4),
        }
    }


# ══════════════════════════════════════════════
#   RUTAS FLASK
# ══════════════════════════════════════════════

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        data = request.get_json()
        ley  = int(data.get("ley", 1))

        if ley == 1:
            masa      = float(data["masa"])
            velocidad = float(data["velocidad"])
            friccion  = float(data["friccion"])
            tiempo    = float(data["tiempo"])
            if masa <= 0:
                return jsonify({"error": "La masa debe ser mayor que 0"}), 400
            if tiempo < 0:
                return jsonify({"error": "El tiempo no puede ser negativo"}), 400
            resultado = calcular_ley1(masa, velocidad, friccion, tiempo)

        elif ley == 2:
            masa   = float(data["masa"])
            fuerza = float(data["fuerza"])
            tiempo = float(data["tiempo"])
            v0     = float(data["v0"])
            if masa <= 0:
                return jsonify({"error": "La masa debe ser mayor que 0"}), 400
            resultado = calcular_ley2(masa, fuerza, tiempo, v0)

        elif ley == 3:
            fuerza = float(data["fuerza"])
            masa1  = float(data["masa1"])
            masa2  = float(data["masa2"])
            tiempo = float(data["tiempo"])
            if masa1 <= 0 or masa2 <= 0:
                return jsonify({"error": "Las masas deben ser mayores que 0"}), 400
            resultado = calcular_ley3(fuerza, masa1, masa2, tiempo)

        else:
            return jsonify({"error": "Ley no válida"}), 400

        return jsonify(resultado)

    except (KeyError, ValueError) as e:
        return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400
    except ZeroDivisionError:
        return jsonify({"error": "División por cero — revisa los valores"}), 400


# ══════════════════════════════════════════════
#   PÁGINA HTML (inline — todo en un archivo)
# ══════════════════════════════════════════════

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Calculadora Leyes de Newton</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

:root {
  --sky:        #5c94fc;
  --brick:      #c84010;
  --brick-dark: #8b2d08;
  --coin:       #fcc800;
  --coin-dark:  #a87800;
  --pipe:       #00a800;
  --pipe-dark:  #005000;
  --panel:      #001880;
  --ground:     #8B4513;
  --green-top:  #228B22;
  --white:      #fcfcfc;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Press Start 2P', monospace;
  background: linear-gradient(180deg, #3878fc 0%, #5c94fc 100%);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}

/* ── CLOUDS ── */
.clouds { position: fixed; inset: 0; pointer-events: none; z-index: 1; overflow: hidden; }
.cloud  {
  position: absolute;
  animation: cloudDrift linear infinite;
}
@keyframes cloudDrift {
  from { transform: translateX(-220px); }
  to   { transform: translateX(110vw);  }
}

/* ── GROUND ── */
.ground {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 2;
}
.ground-green { height: 16px; background: var(--green-top); border-top: 4px solid #5ec45e; }
.ground-brown { height: 40px; background: var(--ground); }
.brick-strip  {
  position: fixed; bottom: 40px; left: 0; right: 0; height: 20px;
  display: flex; z-index: 3; pointer-events: none;
}
.brick-tile { flex: 1; background: var(--brick); border: 2px solid var(--brick-dark); }
.brick-tile:nth-child(even) { background: #b83008; }

/* ── PIPES ── */
.pipe { position: fixed; bottom: 60px; z-index: 4; }
.pipe.left  { left:  24px; }
.pipe.right { right: 24px; }
.pipe-top  { width:60px; height:20px; background:var(--pipe); border:3px solid var(--pipe-dark); margin:0 auto; }
.pipe-body { width:48px; height:70px; background:var(--pipe); border:3px solid var(--pipe-dark); margin:0 auto; }

/* ── MARIO ── */
.mario {
  position: fixed; bottom: 82px; z-index: 20; width:32px; height:32px;
  animation: marioRun 9s linear infinite;
}
@keyframes marioRun {
  0%   { left:-60px;  transform:scaleX(1);  }
  49%  { left:110vw;  transform:scaleX(1);  }
  50%  { left:110vw;  transform:scaleX(-1); }
  99%  { left:-60px;  transform:scaleX(-1); }
  100% { left:-60px;  transform:scaleX(1);  }
}

/* ── STARS ── */
.star { position:fixed; background:#fff; animation:blink 1.6s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.15} }

/* ── WRAPPER ── */
.wrapper {
  position: relative; z-index: 10;
  max-width: 900px; margin: 0 auto;
  padding: 20px 14px 100px;
}

/* ── HEADER ── */
.header { text-align: center; margin-bottom: 20px; }
.title-box {
  display: inline-block;
  background: var(--coin); border: 4px solid var(--coin-dark);
  padding: 12px 22px; font-size: 10px; line-height: 1.9;
  box-shadow: 4px 4px 0 var(--coin-dark), inset -2px -2px 0 rgba(0,0,0,.25);
  text-shadow: 1px 1px 0 #fff; color: #000;
  animation: bounce 2.2s ease-in-out infinite;
}
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-7px)} }
.subtitle {
  font-family: 'VT323', monospace; font-size: 20px; color: #fff;
  text-shadow: 2px 2px 0 #001880; margin-top: 8px; letter-spacing: 2px;
}

/* ── STATUS BAR ── */
.status-bar {
  display: flex; justify-content: space-between; align-items: center;
  background: #001050; border: 3px solid #000;
  padding: 8px 14px; margin-bottom: 14px;
  box-shadow: 3px 3px 0 #000; font-size: 7px; color: #fff;
  text-shadow: 1px 1px 0 #000;
}
.coins-count { color: var(--coin); text-shadow: 0 0 6px var(--coin); }

/* ── LAW BUTTONS ── */
.law-selector { display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-bottom:18px; }
.law-btn {
  font-family: 'Press Start 2P', monospace; font-size: 7px;
  padding: 10px 16px; border: none; cursor: pointer;
  color: #fff; text-shadow: 1px 1px 0 #000;
  transition: transform .1s; line-height: 1.6; text-align: center;
  letter-spacing: .5px;
}
.law-btn:active { transform: translateY(3px); box-shadow: none !important; }
.btn1 { background:#e84010; border:3px solid #6b1e06; box-shadow:3px 3px 0 #6b1e06; }
.btn2 { background:#00a800; border:3px solid #005000; box-shadow:3px 3px 0 #005000; }
.btn3 { background:#7038f8; border:3px solid #340094; box-shadow:3px 3px 0 #340094; }
.law-btn.active { transform:translateY(3px); box-shadow:none !important; filter:brightness(1.2); }

/* ── CALC PANEL ── */
.calc-panel {
  background: var(--panel); border: 4px solid #000;
  box-shadow: 6px 6px 0 #000; padding: 20px; margin-bottom: 14px;
}
.law-title { font-size:8px; color:var(--coin); text-shadow:1px 1px 0 #000; margin-bottom:6px; letter-spacing:1px; }
.law-desc  { font-family:'VT323',monospace; font-size:16px; color:#a0b8ff; margin-bottom:12px; line-height:1.4; }
.formula   {
  background:#000; border:2px solid var(--coin); padding:8px 14px;
  display:inline-block; margin-bottom:16px; color:var(--coin);
  font-size:9px; letter-spacing:2px; box-shadow:2px 2px 0 var(--coin-dark);
}

/* ── INPUTS ── */
.inputs-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px; }
.inp-group   { display:flex; flex-direction:column; gap:5px; }
.inp-label   { font-size:6px; color:#a0c8ff; text-shadow:1px 1px 0 #000; line-height:1.6; }
.pixel-input {
  font-family:'Press Start 2P',monospace; font-size:10px;
  background:#fff; border:3px solid #000; padding:8px 10px;
  color:#001880; width:100%; outline:none;
  box-shadow:inset 2px 2px 0 #aaa, 2px 2px 0 #000;
}
.pixel-input:focus { background:#ffffd0; border-color:var(--coin); }

/* ── CALC BUTTON ── */
.calc-btn {
  font-family:'Press Start 2P',monospace; font-size:9px; width:100%;
  padding:14px; background:var(--coin); border:3px solid var(--coin-dark);
  box-shadow:4px 4px 0 var(--coin-dark), inset 1px 1px 0 rgba(255,255,255,.5);
  color:#000; cursor:pointer; letter-spacing:1px; transition:transform .1s;
}
.calc-btn:active { transform:translateY(4px); box-shadow:none; }
.calc-btn:hover  { background:#fce000; }

/* ── RESULT ── */
.result-panel {
  background:#000; border:4px solid var(--coin); padding:16px;
  margin-bottom:16px; display:none; box-shadow:4px 4px 0 var(--coin-dark);
}
.result-panel.visible { display:block; }
.result-label { font-size:7px; color:#aaa; margin-bottom:6px; }
.result-value {
  font-size:15px; color:var(--coin); text-shadow:0 0 8px var(--coin);
  animation:popIn .5s ease-out; letter-spacing:1px; margin-bottom:6px;
}
@keyframes popIn { 0%{transform:scale(.4);opacity:0} 70%{transform:scale(1.1)} 100%{transform:scale(1);opacity:1} }
.result-unit  { font-family:'VT323',monospace; font-size:18px; color:#a0c8ff; }
.result-extra { font-family:'VT323',monospace; font-size:16px; color:#80ff80; margin-top:4px; white-space:pre-line; }

/* ── ERROR ── */
.error-msg { font-family:'VT323',monospace; font-size:20px; color:#ff6060; margin-top:8px; display:none; }
.error-msg.visible { display:block; }

/* ── CANVAS ── */
.canvas-section { background:#001050; border:4px solid #000; box-shadow:6px 6px 0 #000; display:none; overflow:hidden; }
.canvas-section.visible { display:block; }
.canvas-header {
  background:var(--brick); border-bottom:4px solid var(--brick-dark);
  padding:8px 16px; font-size:7px; color:#fff; text-shadow:1px 1px 0 #000;
}
canvas { display:block; background:#1a1a4e; width:100%; }

/* ── COIN POP ── */
.coin-pop {
  position:fixed; pointer-events:none; font-size:22px;
  animation:coinUp 1s ease-out forwards; z-index:200;
}
@keyframes coinUp { 0%{transform:translateY(0) scale(1);opacity:1} 100%{transform:translateY(-90px) scale(.4);opacity:0} }

/* ── RESPONSIVE ── */
@media(max-width:600px){
  .inputs-grid{ grid-template-columns:1fr; }
  .title-box  { font-size:7px; padding:10px 12px; }
  .pipe       { display:none; }
}
</style>
</head>
<body>

<!-- STARS -->
<div id="stars"></div>

<!-- CLOUDS -->
<div class="clouds" id="clouds"></div>

<!-- GROUND -->
<div class="ground">
  <div class="ground-green"></div>
  <div class="ground-brown"></div>
</div>
<div class="brick-strip" id="bricks"></div>

<!-- PIPES -->
<div class="pipe left"><div class="pipe-top"></div><div class="pipe-body"></div></div>
<div class="pipe right"><div class="pipe-top"></div><div class="pipe-body"></div></div>

<!-- MARIO SVG -->
<div class="mario">
<svg viewBox="0 0 16 16" width="32" height="32" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="0" width="8" height="2" fill="#e84010"/>
  <rect x="3" y="2" width="10" height="2" fill="#e84010"/>
  <rect x="2" y="4" width="10" height="4" fill="#fcb878"/>
  <rect x="4" y="5" width="2" height="1" fill="#000"/>
  <rect x="8" y="5" width="2" height="1" fill="#000"/>
  <rect x="3" y="7" width="7" height="1" fill="#8b4513"/>
  <rect x="2" y="8" width="12" height="4" fill="#0050e8"/>
  <rect x="4" y="8" width="8" height="2" fill="#e84010"/>
  <rect x="5" y="9" width="1" height="1" fill="#fcc800"/>
  <rect x="9" y="9" width="1" height="1" fill="#fcc800"/>
  <rect x="2" y="12" width="4" height="2" fill="#0050e8"/>
  <rect x="9" y="12" width="4" height="2" fill="#0050e8"/>
  <rect x="1" y="14" width="5" height="2" fill="#8b4513"/>
  <rect x="9" y="14" width="5" height="2" fill="#8b4513"/>
  <rect x="0" y="8" width="2" height="3" fill="#fcb878"/>
  <rect x="14" y="8" width="2" height="3" fill="#fcb878"/>
  <rect x="0" y="11" width="2" height="2" fill="#e84010"/>
  <rect x="14" y="11" width="2" height="2" fill="#e84010"/>
</svg>
</div>

<!-- APP -->
<div class="wrapper">

  <div class="header">
    <div class="title-box">🍄 LEYES DE NEWTON 🍄<br>CALCULADORA DE FÍSICA</div>
    <div class="subtitle">▶ LEYES DE NEWTON ◀</div>
  </div>

  <div class="status-bar">
    <span>MARIO &nbsp;<span style="color:#e84010">♥♥♥</span></span>
    <span>🪙 x <span class="coins-count" id="coinCount">00</span></span>
    <span>WORLD <span style="color:var(--coin)">PHYSICS</span></span>
  </div>

  <div class="law-selector">
    <button class="law-btn btn1 active" onclick="selectLaw(1)">⭐ 1RA LEY<br>INERCIA</button>
    <button class="law-btn btn2"        onclick="selectLaw(2)">🔥 2DA LEY<br>F = m·a</button>
    <button class="law-btn btn3"        onclick="selectLaw(3)">💥 3RA LEY<br>ACCIÓN</button>
  </div>

  <div class="calc-panel">
    <div class="law-title" id="lawTitle"></div>
    <div class="law-desc"  id="lawDesc"></div>
    <div class="formula"   id="formula"></div>
    <div class="inputs-grid" id="inputsGrid"></div>
    <div class="error-msg"   id="errorMsg">⚠ ERROR: VERIFICA LOS VALORES</div>
    <button class="calc-btn" onclick="calcular()">▶ CALCULAR &nbsp; 🍄</button>
  </div>

  <div class="result-panel" id="resultPanel">
    <div class="result-label">RESULTADO:</div>
    <div class="result-value" id="resultVal">—</div>
    <div class="result-unit"  id="resultUnit"></div>
    <div class="result-extra" id="resultExtra"></div>
  </div>

  <div class="canvas-section" id="canvasSection">
    <div class="canvas-header" id="canvasHeader">🎮 DEMOSTRACIÓN</div>
    <canvas id="animCanvas" height="280"></canvas>
  </div>

</div>

<script>
/* ══════════════ DECORACIÓN ══════════════ */
// Estrellas
const starsEl = document.getElementById('stars');
for(let i=0;i<28;i++){
  const s = document.createElement('div'); s.className='star';
  const sz = Math.random()<.5?2:4;
  s.style.cssText=`width:${sz}px;height:${sz}px;top:${Math.random()*65}%;left:${Math.random()*100}%;animation-delay:${Math.random()*2}s;position:fixed`;
  starsEl.appendChild(s);
}

// Nubes pixel-art
const cloudsEl = document.getElementById('clouds');
function mkCloud(x,y,sc,dur){
  const d=document.createElement('div'); d.className='cloud';
  d.style.cssText=`left:${x}px;top:${y}px;transform:scale(${sc});animation-duration:${dur}s;animation-delay:-${Math.random()*dur}s`;
  d.innerHTML=`<svg width="80" height="48" viewBox="0 0 80 48" xmlns="http://www.w3.org/2000/svg">
    <rect x="16" y="16" width="48" height="8" fill="#fff"/>
    <rect x="8"  y="8"  width="64" height="8" fill="#fff"/>
    <rect x="0"  y="16" width="80" height="16" fill="#fff"/>
    <rect x="8"  y="32" width="64" height="8"  fill="#fff"/>
    <rect x="8"  y="32" width="8"  height="4"  fill="#c0c0e0"/>
    <rect x="56" y="32" width="8"  height="4"  fill="#c0c0e0"/>
  </svg>`;
  cloudsEl.appendChild(d);
}
mkCloud(-80,10,1.2,22); mkCloud(250,6,0.9,28);
mkCloud(550,20,1.4,18); mkCloud(820,5,1.0,32);

// Ladrillos
const brickRow=document.getElementById('bricks');
for(let i=0;i<42;i++){const b=document.createElement('div');b.className='brick-tile';brickRow.appendChild(b);}

/* ══════════════ MONEDAS ══════════════ */
let coins=0;
function addCoin(x,y){
  coins++; document.getElementById('coinCount').textContent=String(coins).padStart(2,'0');
  const el=document.createElement('div'); el.className='coin-pop'; el.textContent='🪙';
  el.style.cssText=`left:${x}px;top:${y}px`; document.body.appendChild(el);
  setTimeout(()=>el.remove(),1000);
}

/* ══════════════ DEFINICIÓN DE LEYES ══════════════ */
const LAWS = {
  1: {
    title:   '⭐ PRIMERA LEY — LEY DE INERCIA',
    desc:    'Un objeto en reposo permanece en reposo y uno en movimiento continúa a velocidad constante, a menos que una fuerza neta actúe sobre él.',
    formula: 'Σ F = 0   ⟹   v = constante',
    inputs: [
      {id:'masa',      label:'MASA (kg)',               ph:'ej: 10'},
      {id:'velocidad', label:'VELOCIDAD INICIAL (m/s)', ph:'ej: 5'},
      {id:'friccion',  label:'COEF. FRICCIÓN μ',        ph:'0 = sin rozamiento'},
      {id:'tiempo',    label:'TIEMPO (s)',               ph:'ej: 5'},
    ],
    draw: drawLaw1
  },
  2: {
    title:   '🔥 SEGUNDA LEY — F = m · a',
    desc:    'La aceleración de un objeto es directamente proporcional a la fuerza neta e inversamente proporcional a su masa.',
    formula: 'F = m · a   →   a = F / m',
    inputs: [
      {id:'masa',   label:'MASA (kg)',               ph:'ej: 5'},
      {id:'fuerza', label:'FUERZA NETA (N)',          ph:'ej: 20'},
      {id:'tiempo', label:'TIEMPO (s)',               ph:'ej: 4'},
      {id:'v0',     label:'VELOCIDAD INICIAL (m/s)',  ph:'ej: 0'},
    ],
    draw: drawLaw2
  },
  3: {
    title:   '💥 TERCERA LEY — ACCIÓN Y REACCIÓN',
    desc:    'Para toda acción hay una reacción igual y opuesta. Las fuerzas siempre ocurren en pares.',
    formula: 'F_acción = − F_reacción',
    inputs: [
      {id:'fuerza', label:'FUERZA DE ACCIÓN (N)',  ph:'ej: 30'},
      {id:'masa1',  label:'MASA OBJETO A (kg)',     ph:'ej: 5'},
      {id:'masa2',  label:'MASA OBJETO B (kg)',     ph:'ej: 8'},
      {id:'tiempo', label:'TIEMPO (s)',             ph:'ej: 3'},
    ],
    draw: drawLaw3
  }
};

let currentLaw = 1;
let animID     = null;

function selectLaw(n){
  currentLaw = n;
  document.querySelectorAll('.law-btn').forEach((b,i)=>b.classList.toggle('active',i===n-1));
  const L=LAWS[n];
  document.getElementById('lawTitle').textContent = L.title;
  document.getElementById('lawDesc').textContent  = L.desc;
  document.getElementById('formula').textContent  = L.formula;
  buildInputs(L.inputs);
  document.getElementById('resultPanel').classList.remove('visible');
  document.getElementById('canvasSection').classList.remove('visible');
  document.getElementById('errorMsg').classList.remove('visible');
  if(animID) cancelAnimationFrame(animID);
}

function buildInputs(inputs){
  const g=document.getElementById('inputsGrid'); g.innerHTML='';
  inputs.forEach(inp=>{
    const d=document.createElement('div'); d.className='inp-group';
    d.innerHTML=`<label class="inp-label">${inp.label}</label>
      <input class="pixel-input" id="inp_${inp.id}" type="number" placeholder="${inp.ph}" step="any">`;
    g.appendChild(d);
  });
}

/* ══════════════ CALCULAR (llama al backend Python) ══════════════ */
async function calcular(){
  const L    = LAWS[currentLaw];
  const body = { ley: currentLaw };
  let valid  = true;

  L.inputs.forEach(inp=>{
    const el = document.getElementById('inp_'+inp.id);
    const v  = parseFloat(el.value);
    if(isNaN(v)){ valid=false; el.style.borderColor='#f00'; }
    else { el.style.borderColor=''; body[inp.id]=v; }
  });

  const errEl = document.getElementById('errorMsg');
  if(!valid){ errEl.textContent='⚠ ERROR: INGRESA TODOS LOS VALORES'; errEl.classList.add('visible'); return; }
  errEl.classList.remove('visible');

  try {
    const resp = await fetch('/calcular', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(body)
    });
    const data = await resp.json();

    if(data.error){
      errEl.textContent='⚠ '+data.error; errEl.classList.add('visible'); return;
    }

    // Mostrar resultado
    document.getElementById('resultVal').textContent   = data.resultado;
    document.getElementById('resultUnit').textContent  = data.unidad;
    document.getElementById('resultExtra').textContent = data.extra || '';
    document.getElementById('resultPanel').classList.add('visible');
    document.getElementById('canvasSection').classList.add('visible');
    document.getElementById('canvasHeader').textContent = '🎮 DEMO — '+L.title;

    // Moneda animada
    const btn=document.querySelector('.calc-btn');
    const r=btn.getBoundingClientRect();
    addCoin(r.left+r.width/2, r.top-10);

    // Animación canvas
    if(animID) cancelAnimationFrame(animID);
    const canvas=document.getElementById('animCanvas');
    canvas.width=canvas.offsetWidth||860;
    L.draw(canvas, body, data.datos);

  } catch(e){
    errEl.textContent='⚠ ERROR DE CONEXIÓN CON EL SERVIDOR'; errEl.classList.add('visible');
  }
}

/* ══════════════ ANIMACIONES CANVAS ══════════════ */

/* ─── HELPERS ─── */
function drawCrate(ctx,x,y,w,h){
  ctx.fillStyle='#c84010'; ctx.fillRect(x,y,w,h);
  ctx.fillStyle='#e85830'; ctx.fillRect(x+2,y+2,w-4,h/2-2);
  ctx.fillStyle='#a83008'; ctx.fillRect(x+2,y+h/2,w-4,h/2-2);
  ctx.fillStyle='#8b2d08';
  ctx.fillRect(x+w/2-2,y+4,4,h-8);
  ctx.fillRect(x+4,y+h/2-2,w-8,4);
  ctx.fillStyle='#fcc800';
  [[x+4,y+4],[x+w-8,y+4],[x+4,y+h-8],[x+w-8,y+h-8]].forEach(([sx,sy])=>ctx.fillRect(sx,sy,4,4));
  ctx.strokeStyle='#000'; ctx.lineWidth=2; ctx.strokeRect(x,y,w,h);
}

function drawArrow(ctx,x1,y1,x2,y2,color,label){
  ctx.strokeStyle=color; ctx.lineWidth=3;
  ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
  const dx=x2-x1, dy=y2-y1, len=Math.sqrt(dx*dx+dy*dy);
  if(len<1) return;
  const ux=dx/len, uy=dy/len;
  ctx.fillStyle=color;
  ctx.beginPath();
  ctx.moveTo(x2+ux*8, y2+uy*8);
  ctx.lineTo(x2-uy*5, y2+ux*5);
  ctx.lineTo(x2+uy*5, y2-ux*5);
  ctx.closePath(); ctx.fill();
  if(label){ ctx.fillStyle=color; ctx.font='bold 10px monospace'; ctx.fillText(label,x2+ux*12,y2+uy*12+4); }
}

function drawRocket(ctx,x,y,w,h,t){
  ctx.fillStyle='#e0e0f8'; ctx.fillRect(x,y+h*.35,w,h*.65);
  ctx.fillStyle='#e84010';
  ctx.beginPath(); ctx.moveTo(x+w/2,y); ctx.lineTo(x,y+h*.38); ctx.lineTo(x+w,y+h*.38); ctx.closePath(); ctx.fill();
  ctx.fillStyle='#a0d0ff'; ctx.beginPath(); ctx.arc(x+w/2,y+h*.55,w*.22,0,Math.PI*2); ctx.fill();
  ctx.strokeStyle='#6688aa'; ctx.lineWidth=2; ctx.stroke();
  ctx.fillStyle='#e84010';
  ctx.beginPath(); ctx.moveTo(x,y+h*.88); ctx.lineTo(x-13,y+h); ctx.lineTo(x,y+h); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(x+w,y+h*.88); ctx.lineTo(x+w+13,y+h); ctx.lineTo(x+w,y+h); ctx.closePath(); ctx.fill();
  ctx.fillStyle='#888'; ctx.fillRect(x+w*.3,y+h,w*.4,8);
  ['#fcc800','#f08000','#e84010'].forEach((c,i)=>{
    const fh=20+Math.sin(t*14+i)*9;
    ctx.fillStyle=c;
    ctx.beginPath();
    ctx.moveTo(x+w*.3+i*w*.1,y+h+8);
    ctx.lineTo(x+w/2,y+h+8+fh);
    ctx.lineTo(x+w*.7-i*w*.1,y+h+8);
    ctx.closePath(); ctx.fill();
  });
  ctx.strokeStyle='#000'; ctx.lineWidth=2; ctx.strokeRect(x,y+h*.35,w,h*.65);
}

function skyGrad(ctx,W,H){
  const g=ctx.createLinearGradient(0,0,0,H);
  g.addColorStop(0,'#3878fc'); g.addColorStop(1,'#5c94fc');
  ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
}

function drawGround(ctx,W,H,groundY){
  ctx.fillStyle='#228B22'; ctx.fillRect(0,groundY,W,14);
  ctx.fillStyle='#8B4513'; ctx.fillRect(0,groundY+14,W,H);
  for(let i=0;i<W;i+=32){
    ctx.fillStyle=i%64===0?'#c84010':'#b83008';
    ctx.fillRect(i,groundY+14,32,12);
    ctx.strokeStyle='#8b2d08'; ctx.lineWidth=1; ctx.strokeRect(i,groundY+14,32,12);
  }
}

function header(ctx,W,txt1,txt2){
  ctx.fillStyle='#001050'; ctx.fillRect(0,0,W,44);
  ctx.fillStyle='#fcc800'; ctx.font='bold 11px "Press Start 2P",monospace'; ctx.fillText(txt1,14,26);
  ctx.fillStyle='#a0c8ff'; ctx.font='bold 11px monospace'; ctx.fillText(txt2,txt1.length*9+20,26);
}

/* ─── LEY 1 — Caja con/sin fricción ─── */
function drawLaw1(canvas, vals, datos){
  const ctx=canvas.getContext('2d'), W=canvas.width, H=canvas.height;
  const v0=datos.velocidad_inicial, a=datos.aceleracion;
  const hasFric=vals.friccion>0;
  const maxT=vals.tiempo||5;
  const maxDist=hasFric ? Math.max(1,-(v0*v0)/(2*a)) : Math.max(1,v0*maxT);
  const px=Math.min((W-120)/maxDist,28);
  const groundY=H-60, bw=48, bh=48;
  let t=0, bx=60, stopped=false;

  function frame(){
    ctx.clearRect(0,0,W,H);
    skyGrad(ctx,W,H); drawGround(ctx,W,H,groundY);

    let vCur, xNow;
    if(!stopped){
      vCur = v0+a*t;
      if(hasFric&&vCur<=0){vCur=0;stopped=true;}
      const d=v0*t+.5*a*t*t;
      xNow=60+Math.max(0,d)*px;
    } else { xNow=bx; vCur=0; }
    bx=Math.min(xNow,W-bw-20);

    const by=groundY-bh-2;
    // Flecha velocidad
    if(vCur>0.05){
      const al=Math.min(vCur*9,130);
      drawArrow(ctx,bx+bw,by+bh/2,bx+bw+al,by+bh/2,'#fcc800',`v=${vCur.toFixed(1)}`);
    }
    // Flecha fricción
    if(hasFric&&vCur>0.05){
      drawArrow(ctx,bx,by+bh/2,bx-55,by+bh/2,'#ff4040','f');
    }
    drawCrate(ctx,bx,by,bw,bh);
    // Normal y Peso
    drawArrow(ctx,bx+bw/2,by,bx+bw/2,by-42,'#80ff80','N');
    drawArrow(ctx,bx+bw/2,by+bh,bx+bw/2,by+bh+42,'#ff80ff','W');

    header(ctx,W,`t=${t.toFixed(1)}s`,`v=${vCur.toFixed(2)}m/s  m=${vals.masa}kg  μ=${vals.friccion}`);
    if(stopped){
      ctx.fillStyle='rgba(0,0,0,.55)'; ctx.fillRect(W/2-100,H/2-30,200,42);
      ctx.fillStyle='#fcc800'; ctx.font='bold 13px "Press Start 2P",monospace';
      ctx.textAlign='center'; ctx.fillText('¡DETENIDO!',W/2,H/2-3); ctx.textAlign='left';
    }
    if(!stopped) t+=.033;
    if(t>maxT+2){t=0;bx=60;stopped=false;}
    animID=requestAnimationFrame(frame);
  }
  frame();
}

/* ─── LEY 2 — Cohete acelerado ─── */
function drawLaw2(canvas, vals, datos){
  const ctx=canvas.getContext('2d'), W=canvas.width, H=canvas.height;
  const acc=datos.aceleracion, v0=datos.v0||0;
  const maxT=vals.tiempo||5;
  const maxDist=Math.max(1,v0*maxT+.5*acc*maxT*maxT);
  const pxm=Math.min((W-160)/maxDist,25);
  const groundY=H-60, rW=34, rH=60;
  let t=0;

  function frame(){
    ctx.clearRect(0,0,W,H);
    const grad=ctx.createLinearGradient(0,0,0,H);
    grad.addColorStop(0,'#000020'); grad.addColorStop(.5,'#001880'); grad.addColorStop(1,'#3878fc');
    ctx.fillStyle=grad; ctx.fillRect(0,0,W,H);
    // mini estrellas
    ctx.fillStyle='#fff';
    [[50,30],[180,18],[350,48],[500,12],[680,38]].forEach(([sx,sy])=>ctx.fillRect(sx,sy,2,2));
    drawGround(ctx,W,H,groundY);

    const dist=v0*t+.5*acc*t*t;
    const rx=55+dist*pxm;
    const ry=groundY-rH-2;

    // Fuerza
    const fl=Math.min(vals.fuerza*1.4,110);
    drawArrow(ctx,rx-5,ry+rH/2,rx-5-fl,ry+rH/2,'#fcc800',`F=${vals.fuerza}N`);

    drawRocket(ctx,rx,ry,rW,rH,t);

    const vCur=v0+acc*t;
    header(ctx,W,`t=${t.toFixed(1)}s`,`v=${vCur.toFixed(2)}m/s  a=${acc.toFixed(2)}m/s²  F=${vals.fuerza}N  m=${vals.masa}kg`);

    t+=.033; if(t>maxT+1) t=0;
    animID=requestAnimationFrame(frame);
  }
  frame();
}

/* ─── LEY 3 — Colisión ─── */
function drawLaw3(canvas, vals, datos){
  const ctx=canvas.getContext('2d'), W=canvas.width, H=canvas.height;
  const {a1,a2,fuerza}=datos;
  const maxT=vals.tiempo||3;
  const groundY=H-60, bh=50, cx=W/2;
  let t=0;

  function drawBlock(x,y,w,h,color,lbl,mass){
    ctx.fillStyle=color; ctx.fillRect(x,y,w,h);
    ctx.fillStyle='rgba(255,255,255,.2)'; ctx.fillRect(x+2,y+2,w-4,h/3);
    ctx.fillStyle='#fcc800'; ctx.font=`bold ${Math.min(w*.45,18)}px monospace`;
    ctx.textAlign='center'; ctx.fillText(lbl,x+w/2,y+h/2+6);
    ctx.fillStyle='#ddd'; ctx.font='8px monospace'; ctx.fillText(`${mass}kg`,x+w/2,y+h-7);
    ctx.textAlign='left';
    ctx.strokeStyle='#000'; ctx.lineWidth=2; ctx.strokeRect(x,y,w,h);
  }

  function frame(){
    ctx.clearRect(0,0,W,H);
    skyGrad(ctx,W,H); drawGround(ctx,W,H,groundY);

    const bw1=Math.min(vals.masa1*4+22,80), bw2=Math.min(vals.masa2*4+22,80);
    const by=groundY-bh;
    const phase1=maxT/3, col=phase1+.3;
    let x1,x2;

    if(t<phase1){
      const p=t/phase1;
      x1=60+p*(cx-bw1-62); x2=W-60-bw2-p*(W-60-bw2-cx);
    } else if(t<col){
      x1=cx-bw1; x2=cx;
      const f=1-(t-phase1)/.3;
      ctx.fillStyle=`rgba(255,220,0,${f*.7})`; ctx.fillRect(0,0,W,H);
    } else {
      const p=(t-col)/(maxT*2/3);
      x1=cx-bw1-p*.5*a1*(maxT*2/3)**2*2;
      x2=cx+p*.5*a2*(maxT*2/3)**2*2;
    }
    x1=Math.max(4,Math.min(x1,cx-bw1));
    x2=Math.max(cx,Math.min(x2,W-bw2-4));

    drawBlock(x1,by,bw1,bh,'#e84010','A',vals.masa1);
    drawBlock(x2,by,bw2,bh,'#00a800','B',vals.masa2);

    if(t>=col){
      const al=Math.min(fuerza*1.5,80);
      drawArrow(ctx,x1,by+bh/2,x1-al,by+bh/2,'#ff8040',`-${fuerza}N`);
      drawArrow(ctx,x2+bw2,by+bh/2,x2+bw2+al,by+bh/2,'#40ff80',`+${fuerza}N`);
    }
    if(t>=phase1&&t<col+.4){
      ctx.font='bold 30px monospace'; ctx.textAlign='center';
      ctx.fillText('💥',cx,by+bh/2+12); ctx.textAlign='left';
    }

    header(ctx,W,'ACCIÓN=REACCIÓN',`F=${fuerza}N | A:${vals.masa1}kg ${a1.toFixed(2)}m/s² | B:${vals.masa2}kg ${a2.toFixed(2)}m/s²`);
    t+=.033; if(t>maxT*1.6) t=0;
    animID=requestAnimationFrame(frame);
  }
  frame();
}

/* ══════════════ INICIO ══════════════ */
selectLaw(1);
window.addEventListener('resize',()=>{
  const c=document.getElementById('animCanvas');
  if(c&&document.getElementById('canvasSection').classList.contains('visible')) c.width=c.offsetWidth;
});
</script>
</body>
</html>
"""

# ══════════════════════════════════════════════
#   PUNTO DE ENTRADA
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║       NEWTON BROS — Calculadora Física       ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  Servidor iniciado en: http://localhost:5000  ║")
    print("║  Presiona Ctrl+C para detener               ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(debug=True, port=5000)
