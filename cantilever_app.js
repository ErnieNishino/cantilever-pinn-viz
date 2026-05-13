const beamCanvas = document.getElementById('beamCanvas');
const bctx = beamCanvas.getContext('2d');

function analyticalDefl(F, Lr, EIr, xPos) {
  return (F * xPos * xPos * (3 * Lr - xPos)) / (6 * EIr);
}

function lerp(arr, t) {
  const maxIdx = arr.length - 1;
  const fi = t * maxIdx;
  const lo = Math.min(Math.floor(fi), maxIdx - 1);
  const hi = lo + 1;
  const frac = fi - lo;
  return arr[lo] * (1 - frac) + arr[hi] * frac;
}

function drawBeam() {
  const F = parseFloat(document.getElementById('sl-F').value);
  const Lr = parseFloat(document.getElementById('sl-L').value);
  const EIr = parseFloat(document.getElementById('sl-EI').value);

  document.getElementById('lbl-F').textContent = F.toFixed(0);
  document.getElementById('lbl-L').textContent = Lr.toFixed(1);
  document.getElementById('lbl-EI').textContent = EIr.toString();

  const dpr = window.devicePixelRatio || 1;
  const cssW = beamCanvas.parentElement.clientWidth - 24;
  const cssH = 240;

  beamCanvas.width = cssW * dpr;
  beamCanvas.height = cssH * dpr;
  beamCanvas.style.width = cssW + 'px';
  beamCanvas.style.height = cssH + 'px';
  bctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  const W = cssW;
  const H = cssH;

  const wallX = 60;
  const wallW = 18;
  const bx0 = wallX + wallW + 2;

  const maxL = parseFloat(document.getElementById('sl-L').max) || 5.0;
  const maxBx1 = W - 100;
  const maxBLen = maxBx1 - bx0;
  const bLen = maxBLen * (Lr / maxL);
  const bx1 = bx0 + bLen;
  const baseY = H * 0.45;

  const maxDefl = Math.abs(analyticalDefl(F, Lr, EIr, Lr));
  const maxPxDown = H * 0.45;
  const visualMaxDefl = Math.max(0.35, maxDefl * 1.1);
  const scl = maxPxDown / visualMaxDefl;

  bctx.fillStyle = '#f9f9f7';
  bctx.fillRect(0, 0, W, H);

  bctx.fillStyle = '#e8e8e8';
  bctx.fillRect(wallX, baseY - 45, wallW, 90);
  bctx.strokeStyle = '#666';
  bctx.lineWidth = 1;
  for (let hi = -6; hi <= 8; hi++) {
    bctx.beginPath();
    bctx.moveTo(wallX, baseY - 45 + hi * 9);
    bctx.lineTo(wallX - 12, baseY - 33 + hi * 9);
    bctx.stroke();
  }
  bctx.strokeStyle = '#555';
  bctx.lineWidth = 1.5;
  bctx.beginPath();
  bctx.moveTo(wallX + wallW, baseY - 45);
  bctx.lineTo(wallX + wallW, baseY + 45);
  bctx.stroke();

  bctx.strokeStyle = '#aaa';
  bctx.lineWidth = 1.2;
  bctx.setLineDash([6, 6]);
  bctx.beginPath();
  bctx.moveTo(bx0, baseY);
  bctx.lineTo(bx1, baseY);
  bctx.stroke();
  bctx.setLineDash([]);

  const N = 150;

  bctx.strokeStyle = '#185FA5';
  bctx.lineWidth = 3;
  bctx.setLineDash([8, 8]);
  bctx.beginPath();
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const xm = t * Lr;
    const d = analyticalDefl(F, Lr, EIr, xm);
    const px = bx0 + t * bLen;
    const py = baseY + d * scl;
    i === 0 ? bctx.moveTo(px, py) : bctx.lineTo(px, py);
  }
  bctx.stroke();

  bctx.strokeStyle = '#E24B4A';
  bctx.lineWidth = 3;
  bctx.setLineDash([8, 8]);
  bctx.lineDashOffset = 8;
  bctx.beginPath();
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const xm = t * Lr;
    const dExact = analyticalDefl(F, Lr, EIr, xm);
    const ratio = lerp(pinnRatio, t);
    const dPinn = dExact * ratio;
    const px = bx0 + t * bLen;
    const py = baseY + dPinn * scl;
    i === 0 ? bctx.moveTo(px, py) : bctx.lineTo(px, py);
  }
  bctx.stroke();
  bctx.setLineDash([]);
  bctx.lineDashOffset = 0;

  const afx = bx1;
  const afy = baseY + maxDefl * scl;

  bctx.strokeStyle = '#185FA5';
  bctx.fillStyle = '#185FA5';
  bctx.lineWidth = 1.5;
  bctx.beginPath();

  const arrowTop = Math.min(baseY - 24, afy - 45);
  bctx.moveTo(afx, arrowTop);
  bctx.lineTo(afx, afy - 3);
  bctx.stroke();

  bctx.beginPath();
  bctx.moveTo(afx - 4, afy - 12);
  bctx.lineTo(afx, afy);
  bctx.lineTo(afx + 4, afy - 12);
  bctx.fill();

  bctx.font = '13px -apple-system, sans-serif';
  bctx.textAlign = 'center';
  bctx.fillStyle = '#333';
  bctx.fillText('F = ' + F.toFixed(0) + 'N', afx, arrowTop - 8);

  document.getElementById('hdr-phys').innerHTML = (maxDefl).toFixed(4) + ' <span style="font-size:12px">m</span>';
  const pinnMaxDefl = maxDefl * Math.abs(lerp(pinnRatio, 1.0));
  document.getElementById('hdr-surr').innerHTML = (pinnMaxDefl).toFixed(4) + ' <span style="font-size:12px">m</span>';
}

['sl-F', 'sl-L', 'sl-EI'].forEach((id) =>
  document.getElementById(id).addEventListener('input', drawBeam)
);
document.getElementById('btn-reset').addEventListener('click', () => {
  document.getElementById('sl-F').value = 752;
  document.getElementById('sl-L').value = 1.7;
  document.getElementById('sl-EI').value = 38952;
  drawBeam();
});
window.addEventListener('resize', drawBeam);
drawBeam();

const absErr = yPred.map((v, i) => Math.abs(v - yExact[i]));
new Chart(document.getElementById('compChart'), {
  type: 'line',
  data: {
    labels: xData.map((v) => v.toFixed(3)),
    datasets: [
      { label: '解析解（左轴）', data: yExact, borderColor: '#185FA5', borderWidth: 2.5, pointRadius: 0, tension: 0.3, yAxisID: 'yLeft' },
      { label: 'PINN 误差 |Δy|（右轴）', data: absErr, borderColor: '#E24B4A', borderWidth: 2, pointRadius: 0, tension: 0.3, yAxisID: 'yRight', borderDash: [6, 4] }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
    scales: {
      x: { title: { display: true, text: 'x（无量纲，0→1）' } },
      yLeft: { type: 'linear', position: 'left', title: { display: true, text: '挠度 y' } },
      yRight: { type: 'linear', position: 'right', title: { display: true, text: '|PINN 误差|' }, grid: { drawOnChartArea: false } }
    }
  }
});

new Chart(document.getElementById('errChart'), {
  type: 'line',
  data: {
    labels: xData.map((v) => v.toFixed(3)),
    datasets: [{ label: '|y_PINN − y_exact|', data: absErr, borderColor: '#854F0B', backgroundColor: 'rgba(133,79,11,0.07)', borderWidth: 1.5, pointRadius: 0, fill: true, tension: 0.25 }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { title: { display: true, text: 'x（无量纲）' } },
      y: { title: { display: true, text: '绝对误差' } }
    }
  }
});

new Chart(document.getElementById('lossChart'), {
  type: 'line',
  data: {
    labels: lossSteps,
    datasets: [{ label: '总训练损失', data: lossVals, borderColor: '#185FA5', borderWidth: 1.5, pointRadius: 0, tension: 0.2 }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { title: { display: true, text: '训练步数' } },
      y: { type: 'logarithmic', title: { display: true, text: '损失（对数轴）' } }
    }
  }
});
