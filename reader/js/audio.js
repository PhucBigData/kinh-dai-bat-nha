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
 * Cache of synthesized organic wooden fish (Mõ gia trì) buffers
 */
let mokugyoBuffers = [];
let bufferIndex = 0;

/**
 * Synthesize an authentic acoustic model of a Buddhist temple wooden fish (Mõ gỗ mít)
 * Models: Padded felt mallet strike + Hollow cavity resonance + Wood shell harmonics
 */
function createMokugyoBuffer(ctx, fBase = 275) {
  const sampleRate = ctx.sampleRate || 44100;
  const duration = 0.28;
  const numSamples = Math.floor(sampleRate * duration);
  const audioBuffer = ctx.createBuffer(1, numSamples, sampleRate);
  const channelData = audioBuffer.getChannelData(0);

  let seed = Math.floor(fBase * 107);
  function rand() {
    seed = (seed * 9301 + 49297) % 233280;
    return (seed / 233280.0) * 2 - 1;
  }

  for (let i = 0; i < numSamples; i++) {
    const t = i / sampleRate;

    // 1. Mallet impact: Dùi bọc nỉ gõ vào vỏ gỗ - tiếng 'cốc' ấm đầu tiên
    let mallet = 0;
    if (t < 0.022) {
      const malletEnv = Math.exp(-t * 260) * Math.sin(Math.PI * Math.min(1.0, t / 0.0028));
      const thud = Math.sin(2 * Math.PI * (fBase * 1.48) * t) * malletEnv * 0.42;
      const noise = rand() * Math.exp(-t * 420) * 0.12;
      mallet = thud + noise;
    }

    // 2. Hollow wood cavity resonance: Lòng mõ rỗng - âm trầm ấm, tròn tiếng (~275Hz)
    const f0 = fBase + 6.0 * Math.exp(-t * 140);
    const env0 = Math.exp(-t * 15.5); // Ngân dịu tự nhiên trong ~220ms
    const sin0 = Math.sin(2 * Math.PI * f0 * t);
    // Độ bão hoà cộng hưởng lòng gỗ mít
    const w0 = (sin0 + 0.10 * sin0 * sin0) * env0 * 0.72;

    // 3. Wood shell resonance: Độ rung thành gỗ mít - hài âm bậc 2 (~560Hz)
    const f1 = fBase * 2.03 + 6.0 * Math.exp(-t * 180);
    const env1 = Math.exp(-t * 32.0); // Tắt trong ~90ms
    const w1 = Math.sin(2 * Math.PI * f1 * t) * env1 * 0.22;

    // 4. Slit lip harmonic: Mép rãnh miệng mõ - tiếng đanh thanh thoát (~850Hz)
    const f2 = fBase * 3.12;
    const env2 = Math.exp(-t * 68.0); // Tắt trong ~40ms
    const w2 = Math.sin(2 * Math.PI * f2 * t) * env2 * 0.08;

    // Tổng hợp âm sắc & bão hòa mộc ấm (tanh saturation)
    let sig = mallet + w0 + w1 + w2;
    sig = Math.tanh(sig * 1.15) * 0.82;

    // Fadeout cực ngắn ở đuôi tránh hoàn toàn tiếng click
    if (i > numSamples - 128) {
      sig *= (numSamples - i) / 128;
    }

    channelData[i] = sig;
  }

  return audioBuffer;
}

function initMokugyoBuffers(ctx) {
  if (mokugyoBuffers.length === 0) {
    // 3 biến thể cao độ vi mô (274Hz, 277Hz, 275Hz) tạo cảm giác tay người gõ tự nhiên, không lặp cơ học
    mokugyoBuffers = [
      createMokugyoBuffer(ctx, 274),
      createMokugyoBuffer(ctx, 277),
      createMokugyoBuffer(ctx, 275)
    ];
  }
}

/**
 * Play an authentic Buddhist temple wooden fish (Mõ gia trì tụng kinh)
 */
export function playMokugyo() {
  const ctx = getAudioContext();
  if (!ctx) return;

  initMokugyoBuffers(ctx);

  const buffer = mokugyoBuffers[bufferIndex % mokugyoBuffers.length];
  bufferIndex++;

  const source = ctx.createBufferSource();
  source.buffer = buffer;

  const gain = ctx.createGain();
  const now = ctx.currentTime;
  // Biến thiên lực gõ vi mô tự nhiên (±3%)
  const vol = 0.62 + (Math.random() * 0.06 - 0.03);
  gain.gain.setValueAtTime(vol, now);

  source.connect(gain);
  gain.connect(ctx.destination);

  source.start(now);
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
