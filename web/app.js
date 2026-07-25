// --- MOTEUR MATHÉMATIQUE (Canvas 2D) ---

function getPointAngle(index, modulo) {
    return -Math.PI / 2.0 + (2.0 * Math.PI * index) / modulo;
}

function getPointCoords(index, modulo, cx, cy, radius) {
    const angle = getPointAngle(index, modulo);
    return {
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle)
    };
}

function computeDestination(index, table, modulo) {
    return (table * index) % modulo;
}

function hexToRgba(hex, opacityPercent) {
    if (!hex) return 'rgba(255, 255, 255, 1)';
    hex = hex.replace('#', '');
    if (hex.length === 3) {
        hex = hex.split('').map(c => c + c).join('');
    }
    const r = parseInt(hex.substring(0, 2), 16) || 0;
    const g = parseInt(hex.substring(2, 4), 16) || 0;
    const b = parseInt(hex.substring(4, 6), 16) || 0;
    const opacity = (opacityPercent !== undefined ? opacityPercent : 100) / 100;
    return `rgba(${r}, ${g}, ${b}, ${opacity.toFixed(2)})`;
}

// --- ÉLÉMENTS DU DOM ---

const canvas = document.getElementById('main-canvas');
const ctx = canvas.getContext('2d');

const rangeTable = document.getElementById('range-table');
const inputTable = document.getElementById('input-table');
const rangeModulo = document.getElementById('range-modulo');
const inputModulo = document.getElementById('input-modulo');

const checkCircle = document.getElementById('check-circle');
const checkPoints = document.getElementById('check-points');
const checkLabels = document.getElementById('check-labels');
const checkTitle = document.getElementById('check-title');
const inputLabelStep = document.getElementById('input-label-step');
const selectTitlePos = document.getElementById('select-title-pos');

const colorBg = document.getElementById('color-bg');
const colorCircle = document.getElementById('color-circle');
const colorLine = document.getElementById('color-line');
const colorPoint = document.getElementById('color-point');
const colorText = document.getElementById('color-text');

const rangeCircleOpacity = document.getElementById('range-circle-opacity');
const valCircleOpacity = document.getElementById('val-circle-opacity');
const rangeOpacity = document.getElementById('range-opacity');
const valOpacity = document.getElementById('val-opacity');
const rangeLineWidth = document.getElementById('range-linewidth');
const valLineWidth = document.getElementById('val-linewidth');

const btnPlay = document.getElementById('btn-play');
const btnReset = document.getElementById('btn-reset');
const rangeSpeed = document.getElementById('range-speed');
const valSpeed = document.getElementById('val-speed');

const statusDot = document.getElementById('status-dot');
const txtStatus = document.getElementById('txt-status');
const txtFps = document.getElementById('txt-fps');

const btnExportPng = document.getElementById('btn-export-png');
const btnExportSvg = document.getElementById('btn-export-svg');
const btnRecordVideo = document.getElementById('btn-record-video');

// --- ÉTAT GLOBAL DE L'APPLICATION ---
const state = {
    table: 2.0,
    modulo: 100,
    isPlaying: false,
    isRecording: false,
    speed: 0.02,
    mediaRecorder: null,
    recordedChunks: []
};

// --- RENDU CANVAS ---

function render() {
    const width = canvas.width;
    const height = canvas.height;
    const margin = 60;
    const cx = width / 2.0;
    const cy = height / 2.0;
    const radius = (Math.min(width, height) - 2 * margin) / 2.0;

    const table = state.table;
    const modulo = Math.max(1, parseInt(inputModulo.value) || 100);
    const labelStep = Math.max(1, parseInt(inputLabelStep.value) || 5);
    const opacity = parseInt(rangeOpacity.value) || 65;
    const circleOpacity = parseInt(rangeCircleOpacity.value) || 25;
    const lineWidth = parseFloat(rangeLineWidth.value) || 1.5;

    // 1. Fond
    ctx.fillStyle = colorBg.value || '#0f172a';
    ctx.fillRect(0, 0, width, height);

    // 2. Cercle principal
    if (checkCircle.checked) {
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
        ctx.strokeStyle = hexToRgba(colorCircle.value || '#ffffff', circleOpacity);
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    // 3. Cordes
    ctx.strokeStyle = hexToRgba(colorLine.value || '#ec4899', opacity);
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';

    for (let i = 0; i < modulo; i++) {
        const p1 = getPointCoords(i, modulo, cx, cy, radius);
        const destIdx = computeDestination(i, table, modulo);
        const p2 = getPointCoords(destIdx, modulo, cx, cy, radius);

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
    }

    // 4. Points
    if (checkPoints.checked) {
        ctx.fillStyle = colorPoint.value || '#38bdf8';
        const ptRadius = 3;
        for (let i = 0; i < modulo; i++) {
            const p = getPointCoords(i, modulo, cx, cy, radius);
            ctx.beginPath();
            ctx.arc(p.x, p.y, ptRadius, 0, 2 * Math.PI);
            ctx.fill();
        }
    }

    // 5. Labels (Numéros des points)
    if (checkLabels.checked) {
        ctx.fillStyle = colorText.value || '#f8fafc';
        ctx.font = '12px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const labelOffset = 15;

        for (let i = 0; i < modulo; i++) {
            if (i % labelStep !== 0) continue;
            const p = getPointCoords(i, modulo, cx, cy, radius);
            const dx = p.x - cx;
            const dy = p.y - cy;
            const dist = Math.hypot(dx, dy);

            let tx = p.x, ty = p.y;
            if (dist > 0) {
                tx = p.x + (dx / dist) * labelOffset;
                ty = p.y + (dy / dist) * labelOffset;
            }
            ctx.fillText(i.toString(), tx, ty);
        }
    }

    // 6. Titre d'identification
    if (checkTitle.checked) {
        ctx.fillStyle = colorText.value || '#f8fafc';
        ctx.font = 'bold 14px Inter, sans-serif';
        const tStr = Number.isInteger(table) ? table.toString() : table.toFixed(2);
        const titleStr = `Table ${tStr}  |  Modulo ${modulo}`;
        const titleMargin = 20;

        if (selectTitlePos.value === 'left') {
            ctx.textAlign = 'left';
            ctx.fillText(titleStr, titleMargin, height - titleMargin);
        } else {
            ctx.textAlign = 'right';
            ctx.fillText(titleStr, width - titleMargin, height - titleMargin);
        }
    }
}

// --- BOUCLE D'ANIMATION (60 FPS) ---

let frameCount = 0;
let lastFrameTime = performance.now();

function animationLoop(now) {
    // Calcul FPS
    frameCount++;
    if (now - lastFrameTime >= 1000) {
        txtFps.textContent = `${frameCount} FPS`;
        frameCount = 0;
        lastFrameTime = now;
    }

    if (state.isPlaying) {
        state.table += state.speed;
        if (state.table > 100) state.table = 1.0;

        // Mise à jour synchrone des champs UI
        inputTable.value = state.table.toFixed(2);
        rangeTable.value = state.table;
    }

    render();
    requestAnimationFrame(animationLoop);
}

// --- COMMANDE PLAY / PAUSE ---

function setPlayingState(playing) {
    state.isPlaying = playing;
    if (state.isPlaying) {
        btnPlay.textContent = '⏸ Pause';
        btnPlay.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
        if (!state.isRecording) {
            statusDot.className = 'status-dot playing';
            txtStatus.textContent = 'Animation en cours...';
        }
    } else {
        btnPlay.textContent = '▶ Lecture';
        btnPlay.style.background = 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)';
        if (!state.isRecording) {
            statusDot.className = 'status-dot';
            txtStatus.textContent = 'Animation en pause';
        }
    }
}

btnPlay.addEventListener('click', () => {
    setPlayingState(!state.isPlaying);
});

// --- ÉCOUTEURS D'ÉVÉNEMENTS RÉACTIFS ---

// Modification de la table : met l'animation en pause pour capturer le choix exact
rangeTable.addEventListener('input', () => {
    setPlayingState(false);
    state.table = parseFloat(rangeTable.value) || 2.0;
    inputTable.value = state.table.toFixed(2);
    render();
});

inputTable.addEventListener('input', () => {
    setPlayingState(false);
    state.table = parseFloat(inputTable.value) || 2.0;
    rangeTable.value = state.table;
    render();
});

rangeModulo.addEventListener('input', () => {
    inputModulo.value = rangeModulo.value;
    render();
});

inputModulo.addEventListener('input', () => {
    rangeModulo.value = inputModulo.value;
    render();
});

rangeSpeed.addEventListener('input', () => {
    state.speed = parseFloat(rangeSpeed.value) || 0.02;
    valSpeed.textContent = state.speed.toFixed(3);
});

rangeCircleOpacity.addEventListener('input', () => {
    valCircleOpacity.textContent = rangeCircleOpacity.value;
    render();
});

rangeOpacity.addEventListener('input', () => {
    valOpacity.textContent = rangeOpacity.value;
    render();
});

rangeLineWidth.addEventListener('input', () => {
    valLineWidth.textContent = rangeLineWidth.value;
    render();
});

// Écoute des couleurs et options
const reactElements = [
    colorBg, colorCircle, colorLine, colorPoint, colorText,
    checkCircle, checkPoints, checkLabels, checkTitle,
    inputLabelStep, selectTitlePos
];

reactElements.forEach(elem => {
    elem.addEventListener('input', render);
    elem.addEventListener('change', render);
});

// Bouton Réinitialiser
btnReset.addEventListener('click', () => {
    setPlayingState(false);
    state.table = 2.0;
    inputTable.value = '2.00';
    rangeTable.value = 2;
    inputModulo.value = '100';
    rangeModulo.value = 100;
    render();
});

// --- ENREGISTREMENT VIDÉO (WebM/MP4) ---

btnRecordVideo.addEventListener('click', () => {
    if (!state.isRecording) {
        startVideoRecording();
    } else {
        stopVideoRecording();
    }
});

function startVideoRecording() {
    if (!state.isPlaying) setPlayingState(true);

    const stream = canvas.captureStream(30);
    state.recordedChunks = [];

    let options = { mimeType: 'video/webm;codecs=vp9' };
    if (!MediaRecorder.isTypeSupported(options.mimeType)) options = { mimeType: 'video/webm' };
    if (!MediaRecorder.isTypeSupported(options.mimeType)) options = { mimeType: 'video/mp4' };

    try {
        state.mediaRecorder = new MediaRecorder(stream, options);
    } catch (e) {
        alert("Enregistrement non supporté : " + e.message);
        return;
    }

    state.mediaRecorder.ondataavailable = function(e) {
        if (e.data && e.data.size > 0) {
            state.recordedChunks.push(e.data);
        }
    };

    state.mediaRecorder.onstop = function() {
        const mimeType = state.mediaRecorder.mimeType || 'video/webm';
        const ext = mimeType.includes('mp4') ? 'mp4' : 'webm';
        const blob = new Blob(state.recordedChunks, { type: mimeType });
        const url = URL.createObjectURL(blob);

        const tStr = Number.isInteger(state.table) ? state.table.toString() : state.table.toFixed(2);
        const moduloVal = parseInt(inputModulo.value) || 100;
        
        let filename = `video_table_${tStr}_modulo_${moduloVal}`;
        if (checkLabels.checked) filename += `_labelstep_${inputLabelStep.value}`;
        filename += `.${ext}`;

        const a = document.createElement('a');
        a.download = filename;
        a.href = url;
        a.click();
        URL.revokeObjectURL(url);
    };

    state.mediaRecorder.start();
    state.isRecording = true;
    btnRecordVideo.textContent = "🔴 Arrêter & Télécharger la Vidéo";
    btnRecordVideo.classList.add('recording');
    statusDot.className = 'status-dot recording';
    txtStatus.textContent = 'Enregistrement vidéo en cours...';
}

function stopVideoRecording() {
    if (state.mediaRecorder && state.mediaRecorder.state !== 'inactive') {
        state.mediaRecorder.stop();
    }
    state.isRecording = false;
    btnRecordVideo.textContent = "🎥 Enregistrer Vidéo (WebM/MP4)";
    btnRecordVideo.classList.remove('recording');
    statusDot.className = state.isPlaying ? 'status-dot playing' : 'status-dot';
    txtStatus.textContent = state.isPlaying ? 'Animation en cours...' : 'Animation en pause';
}

// --- EXPORT PNG & SVG ---

btnExportPng.addEventListener('click', () => {
    const tStr = Number.isInteger(state.table) ? state.table.toString() : state.table.toFixed(2);
    const moduloVal = parseInt(inputModulo.value) || 100;
    
    let filename = `image_table_${tStr}_modulo_${moduloVal}`;
    if (checkLabels.checked) filename += `_labelstep_${inputLabelStep.value}`;
    filename += `.png`;

    const a = document.createElement('a');
    a.download = filename;
    a.href = canvas.toDataURL('image/png');
    a.click();
});

btnExportSvg.addEventListener('click', () => {
    const width = canvas.width;
    const height = canvas.height;
    const margin = 60;
    const cx = width / 2.0;
    const cy = height / 2.0;
    const radius = (Math.min(width, height) - 2 * margin) / 2.0;

    const table = state.table;
    const modulo = parseInt(inputModulo.value) || 100;
    const labelStep = Math.max(1, parseInt(inputLabelStep.value) || 5);
    const opacity = (parseInt(rangeOpacity.value) / 100).toFixed(2);
    const circleOpacity = (parseInt(rangeCircleOpacity.value) / 100).toFixed(2);
    const lineWidth = parseFloat(rangeLineWidth.value) || 1.5;

    let svgLines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">`,
        `  <rect width="100%" height="100%" fill="${colorBg.value}" />`
    ];

    if (checkCircle.checked) {
        svgLines.push(`  <circle cx="${cx}" cy="${cy}" r="${radius}" stroke="${colorCircle.value}" stroke-opacity="${circleOpacity}" fill="none" stroke-width="1" />`);
    }

    svgLines.push(`  <g stroke="${colorLine.value}" stroke-opacity="${opacity}" stroke-width="${lineWidth}" stroke-linecap="round">`);
    for (let i = 0; i < modulo; i++) {
        const p1 = getPointCoords(i, modulo, cx, cy, radius);
        const destIdx = computeDestination(i, table, modulo);
        const p2 = getPointCoords(destIdx, modulo, cx, cy, radius);
        svgLines.push(`    <line x1="${p1.x.toFixed(2)}" y1="${p1.y.toFixed(2)}" x2="${p2.x.toFixed(2)}" y2="${p2.y.toFixed(2)}" />`);
    }
    svgLines.push(`  </g>`);

    if (checkPoints.checked) {
        svgLines.push(`  <g fill="${colorPoint.value}">`);
        for (let i = 0; i < modulo; i++) {
            const p = getPointCoords(i, modulo, cx, cy, radius);
            svgLines.push(`    <circle cx="${p.x.toFixed(2)}" cy="${p.y.toFixed(2)}" r="3" />`);
        }
        svgLines.push(`  </g>`);
    }

    if (checkLabels.checked) {
        svgLines.push(`  <g fill="${colorText.value}" font-family="sans-serif" font-size="12" text-anchor="middle" dominant-baseline="central">`);
        for (let i = 0; i < modulo; i++) {
            if (i % labelStep !== 0) continue;
            const p = getPointCoords(i, modulo, cx, cy, radius);
            const dx = p.x - cx;
            const dy = p.y - cy;
            const dist = Math.hypot(dx, dy);
            let tx = p.x, ty = p.y;
            if (dist > 0) {
                tx = p.x + (dx / dist) * 15;
                ty = p.y + (dy / dist) * 15;
            }
            svgLines.push(`    <text x="${tx.toFixed(2)}" y="${ty.toFixed(2)}">${i}</text>`);
        }
        svgLines.push(`  </g>`);
    }

    if (checkTitle.checked) {
        const tStr = Number.isInteger(table) ? table.toString() : table.toFixed(2);
        const titleStr = `Table ${tStr} | Modulo ${modulo}`;
        const anchor = selectTitlePos.value === 'left' ? 'start' : 'end';
        const xPos = selectTitlePos.value === 'left' ? 20 : width - 20;

        svgLines.push(`  <text x="${xPos}" y="${height - 20}" fill="${colorText.value}" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="${anchor}">${titleStr}</text>`);
    }

    svgLines.push('</svg>');

    const blob = new Blob([svgLines.join('\n')], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    
    let filename = `image_table_${Number.isInteger(table) ? table : table.toFixed(2)}_modulo_${modulo}`;
    if (checkLabels.checked) filename += `_labelstep_${inputLabelStep.value}`;
    filename += `.svg`;

    a.download = filename;
    a.href = url;
    a.click();
    URL.revokeObjectURL(url);
});

// INITIALISATION & LANCEMENT
state.table = parseFloat(inputTable.value) || 2.0;
render();
requestAnimationFrame(animationLoop);
