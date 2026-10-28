/**
 * Prajñā Web Audio Bell & Meditation Chime
 * Synthesizes peaceful temple bell sounds using native Web Audio API (zero external audio files)
 */

let audioCtx = null;

function getAudioContext() {
  if (!audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
      audioCtx = new AudioContext();
    }
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

/**
 * Play a peaceful Buddhist temple bell (Đại hồng chung / Chuông u minh)
 */
export function playBell() {
  const ctx = getAudioContext();
  if (!ctx) return;

  const now = ctx.currentTime;

  // Master Gain
  const masterGain = ctx.createGain();
  masterGain.connect(ctx.destination);
  masterGain.gain.setValueAtTime(0.4, now);
  masterGain.gain.exponentialRampToValueAtTime(0.0001, now + 4.5);

  // Frequencies for a rich, warm singing bowl / bronze bell
  // Fundamental + overtone harmonics (inharmonic metallic spectrum)
  const partials = [
    { freq: 432, gain: 0.6, decay: 4.5 },
    { freq: 432 * 1.5, gain: 0.35, decay: 3.5 },
    { freq: 432 * 2.01, gain: 0.25, decay: 2.8 },
    { freq: 432 * 2.76, gain: 0.15, decay: 2.0 },
    { freq: 432 * 4.12, gain: 0.08, decay: 1.2 }
  ];

  partials.forEach(p => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(p.freq, now);

    gain.gain.setValueAtTime(p.gain, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);

    osc.connect(gain);
    gain.connect(masterGain);

    osc.start(now);
    osc.stop(now + p.decay + 0.1);
  });
}

/**
 * Play a subtle wooden fish / mokugyo (Mõ) chime
 */
export function playMokugyo() {
  const ctx = getAudioContext();
  if (!ctx) return;

  const now = ctx.currentTime;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const filter = ctx.createBiquadFilter();

  osc.type = 'sine';
  osc.frequency.setValueAtTime(580, now);
  osc.frequency.exponentialRampToValueAtTime(260, now + 0.08);

  filter.type = 'lowpass';
  filter.frequency.setValueAtTime(800, now);

  gain.gain.setValueAtTime(0.5, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);

  osc.connect(filter);
  filter.connect(gain);
  gain.connect(ctx.destination);

  osc.start(now);
  osc.stop(now + 0.16);
}

/**
 * Rhythmic Mokugyo Metronome for Buddhist Chanting
 */
let metronomeTimer = null;

export function startMokugyoMetronome(bpm = 45) {
  stopMokugyoMetronome();
  const safeBpm = Math.min(90, Math.max(30, bpm || 45));
  const intervalMs = (60 / safeBpm) * 1000;
  
  playMokugyo();
  metronomeTimer = setInterval(() => {
    playMokugyo();
  }, intervalMs);
}

export function stopMokugyoMetronome() {
  if (metronomeTimer) {
    clearInterval(metronomeTimer);
    metronomeTimer = null;
  }
}

export function isMetronomeRunning() {
  return metronomeTimer !== null;
}
