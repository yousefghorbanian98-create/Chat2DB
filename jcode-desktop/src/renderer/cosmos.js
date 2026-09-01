'use strict';
/**
 * COSMIC ODYSSEY — cinematic film engine.
 *
 * The cosmos is no longer a static backdrop: a director runs an automatic
 * film made of scenes that play one after another (non-interactive):
 *
 *   warp      — camera flying through a streaming star field
 *   approach  — a black hole grows in the distance, disk + lensing appear
 *   orbit     — the camera orbits the black hole at close range
 *   plunge    — the camera falls THROUGH the event horizon (true lensing)
 *   pulsar    — a realistic neutron star with vertical (top↔bottom) beams
 *   nebula    — drifting through volumetric nebula clouds
 *
 * Rendering quality upgrades:
 *   - The universe (stars + nebula) is rendered into an offscreen FBO, then
 *     the black-hole shader samples it through a gravitational-lens warp, so
 *     background stars genuinely bend around the hole (Einstein ring).
 *   - Chromatic aberration, doppler-shifted accretion disk, photon ring,
 *     limb-darkened star, 6-octave fbm — tuned for a "real footage" feel.
 */
(function () {
  const Cosmos = {
    opts: {
      blackhole: true, pulsar: true, nebula: true,
      starDensity: 3000, intensity: 0.85,
      mouseX: 0.5, mouseY: 0.5
    },
    _gl: null, _canvas: null,
    _programs: {}, _buffers: {},
    _stars: null,
    _fbo: null, _fboTex: null, _fboW: 0, _fboH: 0, _noFbo: false,
    _blackTex: null,
    _ul: new Map(),
    _raf: 0, _t0: performance.now(), _running: false,
    film: [], starts: [], total: 8,
    _fallback: false
  };

  /* ==================== SHADERS ==================== */

  const STAR_VS = `
    attribute vec3 aPosition;
    attribute float aSize;
    attribute float aBrightness;
    attribute vec3 aColor;
    uniform mat4 uProjection;
    uniform mat4 uView;
    uniform float uTime;
    uniform float uWarpPhase;
    uniform float uBank;
    varying float vBrightness;
    varying vec3 vColor;
    void main() {
      vec3 pos = aPosition;
      pos.z = mod(pos.z + uWarpPhase * (0.3 + aBrightness * 1.2), 4.0) - 2.0;
      float c = cos(uBank);
      float s = sin(uBank);
      pos = vec3(pos.x * c - pos.y * s, pos.x * s + pos.y * c, pos.z);
      vec4 mvPos = uView * vec4(pos, 1.0);
      gl_Position = uProjection * mvPos;
      float twinkle = sin(uTime * (1.0 + aBrightness * 3.0) + aBrightness * 100.0) * 0.3 + 0.7;
      gl_PointSize = aSize * twinkle * (300.0 / max(0.5, -mvPos.z));
      vBrightness = aBrightness * twinkle;
      vColor = aColor;
    }`;

  const STAR_FS = `
    precision mediump float;
    varying float vBrightness;
    varying vec3 vColor;
    void main() {
      vec2 center = gl_PointCoord - 0.5;
      float dist = length(center);
      if (dist > 0.5) discard;
      float alpha = smoothstep(0.5, 0.0, dist);
      alpha *= alpha;
      gl_FragColor = vec4(vColor * vBrightness, alpha * vBrightness);
    }`;

  const QUAD_VS = `
    attribute vec2 aPosition;
    varying vec2 vUV;
    void main() { vUV = aPosition * 0.5 + 0.5; gl_Position = vec4(aPosition, 0.0, 1.0); }`;

  const FBM = `
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }
    float noise(vec2 p){
      vec2 i = floor(p);
      vec2 f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      return mix(
        mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
        mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x),
        f.y);
    }
    float fbm(vec2 p){
      float v = 0.0;
      float a = 0.5;
      for (int i = 0; i < 6; i++){ v += a * noise(p); p *= 2.0; a *= 0.5; }
      return v;
    }`;

  // Subtle nebula painted into the universe FBO (behind the stars).
  const UNIVERSE_NEBULA_FS = `
    precision mediump float;
    varying vec2 vUV;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform float uDrift;
    uniform float uNebAmt;
    ${FBM}
    void main() {
      vec2 uv = vUV - 0.5;
      uv.x *= uResolution.x / uResolution.y;
      vec2 p = uv * 2.0 + vec2(uTime * uDrift, uTime * uDrift * 0.6);
      float n1 = fbm(p);
      float n2 = fbm(p * 1.7 + 13.0);
      vec3 a = vec3(0.06, 0.0, 0.14);
      vec3 b = vec3(0.0, 0.05, 0.12);
      vec3 c = vec3(0.10, 0.03, 0.16);
      vec3 col = mix(a, b, clamp(n1, 0.0, 1.0));
      col = mix(col, c, clamp(n2, 0.0, 1.0) * 0.5);
      gl_FragColor = vec4(col * uNebAmt, 1.0);
    }`;

  // Direct view of the universe (used by the warp scene).
  const PASSTHROUGH_FS = `
    precision mediump float;
    varying vec2 vUV;
    uniform sampler2D uUniverse;
    uniform vec2 uResolution;
    uniform float uFade;
    void main() {
      vec2 uv = vUV - 0.5;
      uv.x *= uResolution.x / uResolution.y;
      vec3 col = texture2D(uUniverse, vUV).rgb;
      float vig = 1.0 - dot(uv * 0.5, uv * 0.5);
      col *= max(0.0, vig);
      col = col / (col + 1.0);
      col = pow(col, vec3(0.9));
      gl_FragColor = vec4(col * uFade, 1.0);
    }`;

  const BLACKHOLE_FS = `
    precision highp float;
    varying vec2 vUV;
    uniform sampler2D uUniverse;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform vec2 uMouse;
    uniform float uScale;
    uniform vec2 uOffset;
    uniform float uFall;
    uniform float uTilt;
    uniform float uFade;
    #define PI 3.14159265359
    ${FBM}
    void main() {
      vec2 uv = (gl_FragCoord.xy - 0.5 * uResolution) / uResolution.y;
      uv += (uMouse - 0.5) * 0.05;

      vec2 bh = uOffset;
      vec2 d = uv - bh;
      float r = length(d);
      float rs = 0.14 * uScale;

      // Gravitational lensing — sample the universe through the warp.
      float lens = (rs * rs) / (r * r + 0.0006) * (1.0 + uFall * 7.0);
      vec2 dir = d / max(r, 1e-4);
      vec2 lensed = bh + dir * (r + lens * 0.7);
      vec2 tc = lensed * 0.5 + vec2(0.5);
      vec3 bg = texture2D(uUniverse, clamp(tc, 0.0, 1.0)).rgb;

      // Chromatic aberration (fake, radial).
      float ca = clamp(lens * 0.015, 0.0, 0.05);
      vec3 bgR = texture2D(uUniverse, clamp(tc + vec2(ca, 0.0), 0.0, 1.0)).rgb;
      vec3 bgB = texture2D(uUniverse, clamp(tc - vec2(ca, 0.0), 0.0, 1.0)).rgb;
      bg = vec3(bgR.r, bg.g, bgB.b);

      // Tilted accretion disk (elliptical) with fbm detail.
      vec2 q = d;
      q.y /= mix(0.5, 0.12, clamp(uTilt, 0.0, 1.0));
      float rr = length(q);
      float diskCenter = 0.36 * uScale;
      float diskWidth = 0.15 * uScale + 0.02;
      float diskR = smoothstep(diskWidth, 0.0, abs(rr - diskCenter));
      float ang = atan(q.y, q.x);
      float spin = ang + uTime * 0.9;
      float diskNoise = fbm(vec2(spin * 2.0, rr * 14.0 - uTime * 0.4));
      diskR *= (0.45 + diskNoise * 1.5);

      // Doppler beaming: one side blue-white, the other red-orange.
      float dop = sin(ang) * 0.5 + 0.5;
      vec3 diskCol = mix(vec3(0.45, 0.15, 0.85), vec3(1.0, 0.55, 0.1), dop);
      diskCol += vec3(0.85, 0.9, 1.0) * pow(max(0.0, 1.0 - dop), 3.0) * 0.7;

      float horizon = smoothstep(rs * 0.95, rs * 0.5, r);
      float ring = exp(-pow((r - rs * 1.35) / (rs * 0.16), 2.0));
      float inner = exp(-r * 6.0 / max(rs, 0.05)) * 0.6;

      vec3 col = bg;
      col = mix(col, col * 0.08, clamp(uFall, 0.0, 1.0) * 0.8);
      col += diskCol * diskR * (1.0 - horizon) * (1.25 + uFall * 1.5);
      col += vec3(0.75, 0.55, 1.0) * ring * (0.9 + uFall * 2.5);
      col += vec3(0.5, 0.25, 1.0) * inner * (1.0 - horizon) * (1.0 + uFall * 3.0);
      col += vec3(1.0, 0.85, 0.5) * pow(uFall, 2.0) * exp(-abs(r - rs * 1.1) * 4.0 / max(rs, 0.05)) * 0.9;
      col *= (1.0 - horizon);

      vec2 vv = uv;
      float vig = 1.0 - dot(vv * 0.5, vv * 0.5);
      col *= max(0.0, vig);
      col = col / (col + 1.0);
      col = pow(col, vec3(0.9));
      gl_FragColor = vec4(col * uFade, 1.0);
    }`;

  const PULSAR_FS = `
    precision highp float;
    varying vec2 vUV;
    uniform sampler2D uUniverse;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform float uFade;
    uniform float uFlash;
    #define PI 3.14159265359
    ${FBM}
    void main() {
      vec2 uv = (gl_FragCoord.xy - 0.5 * uResolution) / uResolution.y;
      vec3 bg = texture2D(uUniverse, vUV).rgb * 0.4;

      vec2 d = uv;
      float r = length(d);
      float ang = atan(d.y, d.x);

      // Neutron star core with granulation + limb darkening.
      float core = exp(-r * 24.0);
      float gran = fbm(d * 30.0 - uTime * 0.05);
      vec3 coreCol = mix(vec3(0.55, 0.65, 1.0), vec3(1.0, 0.95, 0.88), clamp(gran, 0.0, 1.0));
      coreCol *= (1.0 - r * r * 5.0);

      float pulse = 0.5 + 0.5 * sin(uTime * 6.0);
      float cosUp = d.y / max(r, 1e-4);

      // Vertical polar beams — light shooting straight UP and DOWN.
      float vert = pow(max(0.0, abs(cosUp)), 26.0) * exp(-r * 2.4) * (0.55 + 0.45 * pulse);

      // Rotating lighthouse beams sweeping the sky.
      float sw = uTime * 1.6;
      float c1 = cos(ang - sw);
      float c2 = cos(ang - sw - PI);
      float sweep = (pow(max(0.0, c1), 120.0) + pow(max(0.0, c2), 120.0)) * exp(-r * 1.7);

      // Magnetosphere glow + equatorial ring.
      float cone = exp(-r * 3.0) * (0.35 + 0.4 * pulse);
      float eq = exp(-pow((r - 0.13) / 0.025, 2.0)) * (1.0 - pow(cosUp, 2.0));

      vec3 beamCol = vec3(0.35, 0.75, 1.0) + vec3(0.55, 0.4, 1.0) * pulse;

      vec3 col = bg;
      col += coreCol * core;
      col += beamCol * vert * 1.8;
      col += vec3(0.85, 0.9, 1.0) * sweep * 1.5;
      col += beamCol * cone * 0.5;
      col += vec3(0.3, 0.6, 1.0) * eq * 0.9;

      vec2 vv = uv;
      float vig = 1.0 - dot(vv * 0.6, vv * 0.6);
      col *= max(0.0, vig);
      col = col / (col + 1.0);
      col = pow(col, vec3(0.9));
      col = col * uFade + vec3(1.0) * uFlash;
      gl_FragColor = vec4(col, 1.0);
    }`;

  const NEBULA_SCENE_FS = `
    precision highp float;
    varying vec2 vUV;
    uniform sampler2D uUniverse;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform float uFade;
    uniform float uDrift;
    ${FBM}
    void main() {
      vec2 uv = vUV - 0.5;
      uv.x *= uResolution.x / uResolution.y;
      vec3 bg = texture2D(uUniverse, vUV).rgb;

      vec2 p = uv * 2.2 + vec2(uTime * uDrift, uTime * uDrift * 0.5);
      float n1 = fbm(p);
      float n2 = fbm(p * 1.6 + 7.0);
      float n3 = fbm(p * 3.2 - 3.0);

      vec3 a = vec3(0.10, 0.0, 0.22);
      vec3 b = vec3(0.0, 0.09, 0.20);
      vec3 c = vec3(0.36, 0.08, 0.26);
      vec3 neb = mix(a, b, clamp(n1, 0.0, 1.0));
      neb = mix(neb, c, clamp(n2 * 0.5 + n3 * 0.5, 0.0, 1.0) * 0.55);
      float ridge = 1.0 - abs(n2 - n3);
      neb += c * pow(ridge, 3.0) * 0.35;

      vec3 col = bg * 0.9 + neb * 1.0;
      vec2 vv = uv;
      float vig = 1.0 - dot(vv * 0.5, vv * 0.5);
      col *= max(0.0, vig);
      col = col / (col + 1.0);
      col = pow(col, vec3(0.9));
      gl_FragColor = vec4(col * uFade, 1.0);
    }`;

  /* ==================== GL HELPERS ==================== */

  function createShader(gl, type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.error('[cosmos] shader error:', gl.getShaderInfoLog(s));
      gl.deleteShader(s);
      return null;
    }
    return s;
  }

  function createProgram(gl, vsSrc, fsSrc) {
    const vs = createShader(gl, gl.VERTEX_SHADER, vsSrc);
    const fs = createShader(gl, gl.FRAGMENT_SHADER, fsSrc);
    if (!vs || !fs) return null;
    const p = gl.createProgram();
    gl.attachShader(p, vs);
    gl.attachShader(p, fs);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      console.error('[cosmos] link error:', gl.getProgramInfoLog(p));
      return null;
    }
    return p;
  }

  function makeBuffer(gl, data) {
    const b = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
    return b;
  }

  function perspective(fov, aspect, near, far) {
    const f = 1 / Math.tan(fov / 2);
    const nf = 1 / (near - far);
    return [f / aspect, 0, 0, 0, 0, f, 0, 0, 0, 0, (far + near) * nf, -1, 0, 0, 2 * far * near * nf, 0];
  }

  function lookAt(eye, target, up) {
    let zx = eye[0] - target[0], zy = eye[1] - target[1], zz = eye[2] - target[2];
    const zl = Math.hypot(zx, zy, zz); zx /= zl; zy /= zl; zz /= zl;
    let xx = up[1] * zz - up[2] * zy, xy = up[2] * zx - up[0] * zz, xz = up[0] * zy - up[1] * zx;
    const xl = Math.hypot(xx, xy, xz); xx /= xl; xy /= xl; xz /= xl;
    const yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
    return [xx, yx, zx, 0, xy, yy, zy, 0, xz, yz, zz, 0,
      -(xx * eye[0] + xy * eye[1] + xz * eye[2]),
      -(yx * eye[0] + yy * eye[1] + yz * eye[2]),
      -(zx * eye[0] + zy * eye[1] + zz * eye[2]), 1];
  }

  const clamp01 = (x) => Math.min(1, Math.max(0, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);
  const easeIn = (t) => t * t * t;
  const smooth = (t) => t * t * (3 - 2 * t);

  /* ==================== STARS ==================== */

  function buildStars(count) {
    const pos = new Float32Array(count * 3);
    const size = new Float32Array(count);
    const bright = new Float32Array(count);
    const color = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 6;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 6;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 4;
      size[i] = Math.random() * 3 + 0.5;
      bright[i] = Math.random();
      const t = Math.random();
      if (t < 0.3) { color[i * 3] = 0.7 + Math.random() * 0.3; color[i * 3 + 1] = 0.8 + Math.random() * 0.2; color[i * 3 + 2] = 1.0; }
      else if (t < 0.7) { color[i * 3] = 1.0; color[i * 3 + 1] = 0.9 + Math.random() * 0.1; color[i * 3 + 2] = 0.7 + Math.random() * 0.3; }
      else { color[i * 3] = 1.0; color[i * 3 + 1] = 0.5 + Math.random() * 0.3; color[i * 3 + 2] = 0.3 + Math.random() * 0.2; }
    }
    return { pos, size, bright, color };
  }

  function bindAttrib(gl, prog, name, buffer, size) {
    const loc = gl.getAttribLocation(prog, name);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 0, 0);
  }

  /* ==================== PUBLIC API ==================== */

  Cosmos.init = function (canvas) {
    this._canvas = canvas;
    const gl = canvas.getContext('webgl', { alpha: false, antialias: false }) || canvas.getContext('experimental-webgl');
    if (!gl) return false;
    this._gl = gl;

    this._programs.stars = createProgram(gl, STAR_VS, STAR_FS);
    this._programs.universeNebula = createProgram(gl, QUAD_VS, UNIVERSE_NEBULA_FS);
    this._programs.passthrough = createProgram(gl, QUAD_VS, PASSTHROUGH_FS);
    this._programs.blackhole = createProgram(gl, QUAD_VS, BLACKHOLE_FS);
    this._programs.pulsar = createProgram(gl, QUAD_VS, PULSAR_FS);
    this._programs.nebulaScene = createProgram(gl, QUAD_VS, NEBULA_SCENE_FS);

    this._buffers.quad = makeBuffer(gl, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]));
    this._rebuildStars();

    // 1x1 black texture used as a safe fallback sampler.
    this._blackTex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, this._blackTex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([0, 0, 0, 255]));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

    if (!this._programs.stars) this._fallback = true;
    this.rebuildFilm();
    this.resize();
    this._running = true;

    const loop = () => {
      this._raf = requestAnimationFrame(loop);
      this._render();
    };
    loop();
    return true;
  };

  Cosmos.rebuildFilm = function () {
    const f = [{ id: 'warp', dur: 8 }];
    if (this.opts.blackhole) f.push({ id: 'approach', dur: 9 }, { id: 'orbit', dur: 10 }, { id: 'plunge', dur: 10 });
    if (this.opts.pulsar) f.push({ id: 'pulsar', dur: 12 });
    if (this.opts.nebula) f.push({ id: 'nebula', dur: 13 });
    this.film = f;
    this.starts = [];
    let acc = 0;
    for (const s of f) { this.starts.push(acc); acc += s.dur; }
    this.total = acc || 1;
  };

  Cosmos.setOption = function (key, value) {
    this.opts[key] = value;
    if (key === 'starDensity') this._rebuildStars();
    if (key === 'intensity' && this._canvas) this._canvas.style.opacity = String(value);
    if (key === 'blackhole' || key === 'pulsar' || key === 'nebula') this.rebuildFilm();
  };

  Cosmos.resize = function () {
    const canvas = this._canvas, gl = this._gl;
    if (!gl) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    const w = canvas.clientWidth || window.innerWidth;
    const h = canvas.clientHeight || window.innerHeight;
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
  };

  Cosmos._rebuildStars = function () {
    const gl = this._gl;
    if (!gl) return;
    this._stars = buildStars(Math.max(200, this.opts.starDensity));
    this._buffers.starPos = makeBuffer(gl, this._stars.pos);
    this._buffers.starSize = makeBuffer(gl, this._stars.size);
    this._buffers.starBright = makeBuffer(gl, this._stars.bright);
    this._buffers.starColor = makeBuffer(gl, this._stars.color);
  };

  /* ==================== FBO ==================== */

  Cosmos._ensureFBO = function () {
    const gl = this._gl;
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    if (this._fbo && this._fboW === w && this._fboH === h) return;
    if (this._fbo) { gl.deleteFramebuffer(this._fbo); gl.deleteTexture(this._fboTex); }
    const tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    const fbo = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
    const status = gl.checkFramebufferStatus(gl.FRAMEBUFFER);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this._noFbo = status !== gl.FRAMEBUFFER_COMPLETE;
    this._fbo = fbo; this._fboTex = tex; this._fboW = w; this._fboH = h;
  };

  function setQuad(cosmos, prog) {
    const gl = cosmos._gl;
    bindAttrib(gl, prog, 'aPosition', cosmos._buffers.quad, 2);
  }

  function drawStarsInto(c, t, warp, bank) {
    const gl = c._gl;
    const sp = c._programs.stars;
    if (!sp) return;
    gl.useProgram(sp);
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    const proj = perspective(60 * Math.PI / 180, w / h, 0.1, 100);
    const view = lookAt([0, 0, 3], [0, 0, 0], [0, 1, 0]);
    gl.uniformMatrix4fv(gl.getUniformLocation(sp, 'uProjection'), false, proj);
    gl.uniformMatrix4fv(gl.getUniformLocation(sp, 'uView'), false, view);
    gl.uniform1f(gl.getUniformLocation(sp, 'uTime'), t);
    gl.uniform1f(gl.getUniformLocation(sp, 'uWarpPhase'), (warp * t) % 4);
    gl.uniform1f(gl.getUniformLocation(sp, 'uBank'), bank);
    bindAttrib(gl, sp, 'aPosition', c._buffers.starPos, 3);
    bindAttrib(gl, sp, 'aSize', c._buffers.starSize, 1);
    bindAttrib(gl, sp, 'aBrightness', c._buffers.starBright, 1);
    bindAttrib(gl, sp, 'aColor', c._buffers.starColor, 3);
    gl.drawArrays(gl.POINTS, 0, c.opts.starDensity);
  }

  /* ==================== RENDER ==================== */

  Cosmos._render = function () {
    const gl = this._gl;
    if (!gl || !this._running) return;
    if (this._fallback) { gl.clearColor(0, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT); return; }

    const t = (performance.now() - this._t0) / 1000;
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;

    // --- select scene from the film timeline ---
    const loopT = t % this.total;
    let idx = 0;
    while (idx < this.starts.length - 1 && loopT >= this.starts[idx + 1]) idx++;
    const scene = this.film[idx] || { id: 'warp', dur: 8 };
    const dur = scene.dur || 8;
    const localT = loopT - this.starts[idx];
    const p = clamp01(localT / dur);
    const fade = clamp01(localT / 0.7) * clamp01((dur - localT) / 0.8);

    let warp = 0.6, bank = 0;
    switch (scene.id) {
      case 'warp': warp = 2.6; bank = Math.sin(t * 0.12) * 0.5; break;
      case 'approach': warp = 0.7; bank = Math.sin(t * 0.08) * 0.2; break;
      case 'orbit': warp = 0.55; bank = Math.sin(t * 0.1) * 0.3; break;
      case 'plunge': warp = lerp(0.7, 3.4, easeIn(p)); bank = Math.sin(t * 0.2) * 0.6; break;
      case 'pulsar': warp = 0.45; break;
      case 'nebula': warp = 0.35; break;
    }

    this._ensureFBO();

    // 1) Render the universe (nebula + stars) into the offscreen FBO.
    gl.bindFramebuffer(gl.FRAMEBUFFER, this._fbo);
    gl.viewport(0, 0, w, h);
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    const nebP = this._programs.universeNebula;
    if (nebP) {
      gl.useProgram(nebP);
      gl.uniform1f(gl.getUniformLocation(nebP, 'uTime'), t);
      gl.uniform2f(gl.getUniformLocation(nebP, 'uResolution'), w, h);
      gl.uniform1f(gl.getUniformLocation(nebP, 'uDrift'), 0.02);
      gl.uniform1f(gl.getUniformLocation(nebP, 'uNebAmt'), this.opts.nebula ? 0.42 : 0.05);
      setQuad(this, nebP);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    drawStarsInto(this, t, warp, bank);

    // 2) Composite the scene to the screen, sampling the lensed universe.
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.viewport(0, 0, w, h);
    gl.disable(gl.BLEND);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this._noFbo ? this._blackTex : this._fboTex);

    const bindUniverse = (prog) => {
      gl.useProgram(prog);
      gl.uniform1i(gl.getUniformLocation(prog, 'uUniverse'), 0);
    };

    switch (scene.id) {
      case 'warp': {
        const pt = this._programs.passthrough;
        if (pt) { bindUniverse(pt); gl.uniform2f(gl.getUniformLocation(pt, 'uResolution'), w, h); gl.uniform1f(gl.getUniformLocation(pt, 'uFade'), fade); setQuad(this, pt); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); }
        break;
      }
      case 'approach':
      case 'orbit':
      case 'plunge': {
        const bh = this._programs.blackhole;
        if (!bh) break;
        bindUniverse(bh);
        gl.uniform1f(gl.getUniformLocation(bh, 'uTime'), t);
        gl.uniform2f(gl.getUniformLocation(bh, 'uResolution'), w, h);
        gl.uniform2f(gl.getUniformLocation(bh, 'uMouse'), this.opts.mouseX, this.opts.mouseY);
        gl.uniform1f(gl.getUniformLocation(bh, 'uFade'), fade);
        if (scene.id === 'approach') {
          const e = easeOut(p);
          gl.uniform1f(gl.getUniformLocation(bh, 'uScale'), lerp(0.45, 1.05, e));
          gl.uniform2f(gl.getUniformLocation(bh, 'uOffset'), lerp(0.3, 0.02, e), lerp(0.12, 0.0, e));
          gl.uniform1f(gl.getUniformLocation(bh, 'uFall'), 0);
          gl.uniform1f(gl.getUniformLocation(bh, 'uTilt'), lerp(0.8, 0.4, e));
        } else if (scene.id === 'orbit') {
          gl.uniform1f(gl.getUniformLocation(bh, 'uScale'), 1.08 + 0.06 * Math.sin(t * 0.5));
          gl.uniform2f(gl.getUniformLocation(bh, 'uOffset'), 0.05 * Math.cos(t * 0.3), 0.04 * Math.sin(t * 0.22));
          gl.uniform1f(gl.getUniformLocation(bh, 'uFall'), 0);
          gl.uniform1f(gl.getUniformLocation(bh, 'uTilt'), 0.38 + 0.12 * Math.sin(t * 0.6));
        } else {
          const e = easeIn(p);
          gl.uniform1f(gl.getUniformLocation(bh, 'uScale'), lerp(1.08, 2.6, e));
          gl.uniform2f(gl.getUniformLocation(bh, 'uOffset'), lerp(0.05, 0, e), lerp(0.03, 0, e));
          gl.uniform1f(gl.getUniformLocation(bh, 'uFall'), e);
          gl.uniform1f(gl.getUniformLocation(bh, 'uTilt'), lerp(0.4, 0.5, e));
        }
        setQuad(this, bh);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        break;
      }
      case 'pulsar': {
        const ps = this._programs.pulsar;
        if (!ps) break;
        bindUniverse(ps);
        gl.uniform1f(gl.getUniformLocation(ps, 'uTime'), t);
        gl.uniform2f(gl.getUniformLocation(ps, 'uResolution'), w, h);
        gl.uniform1f(gl.getUniformLocation(ps, 'uFade'), fade);
        const flash = localT < 1.2 ? Math.pow(1 - localT / 1.2, 2) * 0.95 : 0;
        gl.uniform1f(gl.getUniformLocation(ps, 'uFlash'), flash);
        setQuad(this, ps);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        break;
      }
      case 'nebula': {
        const nb = this._programs.nebulaScene;
        if (!nb) break;
        bindUniverse(nb);
        gl.uniform1f(gl.getUniformLocation(nb, 'uTime'), t);
        gl.uniform2f(gl.getUniformLocation(nb, 'uResolution'), w, h);
        gl.uniform1f(gl.getUniformLocation(nb, 'uFade'), fade);
        gl.uniform1f(gl.getUniformLocation(nb, 'uDrift'), 0.05);
        setQuad(this, nb);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        break;
      }
    }
  };

  window.Cosmos = Cosmos;
})();
