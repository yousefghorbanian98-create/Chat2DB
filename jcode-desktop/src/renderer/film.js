/* ============================================================
 * CELESTIAL FILM — a continuous, looping cinematic sequence.
 *
 * Scenes play back-to-back with smooth cross-fades:
 *   1. warp       — flying through a streaming star field
 *   2. pulsar     — a spinning neutron star (Vela-style) with twin
 *                   lighthouse beams sweeping from the poles
 *   3. black hole — vercel-labs/vgpu raymarched black hole
 *                   (geodesic lensing + accretion disk + HDR bloom)  [MIT]
 *   4. galaxy     — Eluvade/cosmos grand-design spiral  [MIT]
 *   5. nebula     — drifting volumetric fbm clouds + stars
 *
 * No controls, no switching — it just plays, forever.
 * ============================================================ */
(function () {
  'use strict';

  var canvas = document.getElementById('cosmos-canvas');
  var fallback = document.getElementById('cosmos-fallback');
  if (!canvas) return;

  var gl = canvas.getContext('webgl2', {
    antialias: false, depth: false, stencil: false, alpha: false,
    powerPreference: 'high-performance',
  }) || canvas.getContext('webgl', {
    antialias: false, depth: false, stencil: false, alpha: false,
    powerPreference: 'high-performance',
  });

  if (!gl) {
    if (fallback) fallback.hidden = false;
    if (canvas.parentElement) canvas.remove();
    return;
  }

  var IS_GL2 = typeof WebGL2RenderingContext !== 'undefined' && gl instanceof WebGL2RenderingContext;
  // The black-hole passes use GLSL ES 3.00, so the film needs WebGL2.
  if (!IS_GL2) {
    if (fallback) fallback.hidden = false;
    if (canvas.parentElement) canvas.remove();
    return;
  }
  if (fallback) fallback.remove();
  var halfFloat = IS_GL2 && !!(
    gl.getExtension('EXT_color_buffer_float') || gl.getExtension('EXT_color_buffer_half_float')
  );
  var INTERNAL = halfFloat ? gl.RGBA16F : gl.RGBA;
  var FLOAT_TYPE = halfFloat ? gl.HALF_FLOAT : gl.UNSIGNED_BYTE;

  /* ============================================================
   * Shader sources
   * ============================================================ */

  // Fullscreen-triangle vertex (WebGL2 gl_VertexID) — used by black hole passes.
  var FULL_VS_3 = [
    '#version 300 es',
    'out vec2 vUv;',
    'void main(){',
    '  vec2 pos = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));',
    '  vUv = pos;',
    '  gl_Position = vec4(pos * 2.0 - 1.0, 0.0, 1.0);',
    '}',
  ].join('\n');

  // Attribute quad vertex (ES 1.00) — used by the ES1 shaders below.
  var QUAD_VS = [
    'attribute vec2 aPosition;',
    'varying vec2 vUV;',
    'void main(){ vUV = aPosition * 0.5 + 0.5; gl_Position = vec4(aPosition, 0.0, 1.0); }',
  ].join('\n');

  // Centered varying ([-0.5,0.5]) — matches Eluvade's v_pos convention.
  var CENTER_VS = [
    'attribute vec2 aPosition;',
    'varying vec2 v_pos;',
    'void main(){ v_pos = aPosition * 0.5; gl_Position = vec4(aPosition, 0.0, 1.0); }',
  ].join('\n');

  // --- Eluvade/cosmos GLSL_COMMON (MIT) — verbatim ---
  var COMMON = [
    'vec2 rotate2d(vec2 coord, float angle) {',
    '    coord -= 0.5;',
    '    coord *= mat2(vec2(cos(angle), -sin(angle)), vec2(sin(angle), cos(angle)));',
    '    return coord + 0.5;',
    '}',
    'vec2 spherify(vec2 uv) {',
    '    vec2 centered = uv * 2.0 - 1.0;',
    '    float z2 = 1.0 - dot(centered, centered);',
    '    if (z2 < 0.0) return uv;',
    '    float z = sqrt(z2);',
    '    vec2 sphere = centered / (z + 1.0);',
    '    return sphere * 0.5 + 0.5;',
    '}',
    'float rand_s(vec2 coord, float s, float sz) {',
    '    coord = mod(coord, vec2(floor(sz + 0.5)));',
    '    return fract(sin(dot(coord, vec2(12.9898, 78.233))) * 15.5453 * s);',
    '}',
    'float noise_s(vec2 coord, float s, float sz) {',
    '    vec2 i = floor(coord);',
    '    vec2 f = fract(coord);',
    '    float a = rand_s(i, s, sz);',
    '    float b = rand_s(i + vec2(1.0, 0.0), s, sz);',
    '    float c = rand_s(i + vec2(0.0, 1.0), s, sz);',
    '    float d = rand_s(i + vec2(1.0, 1.0), s, sz);',
    '    vec2 cubic = f * f * (3.0 - 2.0 * f);',
    '    return mix(a, b, cubic.x) + (c - a) * cubic.y * (1.0 - cubic.x) + (d - b) * cubic.x * cubic.y;',
    '}',
    'float fbm_s(vec2 coord, int oct, float s, float sz) {',
    '    float value = 0.0;',
    '    float scale = 0.5;',
    '    for (int i = 0; i < 10; i++) {',
    '        if (i >= oct) break;',
    '        value += noise_s(coord, s, sz) * scale;',
    '        coord *= 2.0;',
    '        scale *= 0.5;',
    '    }',
    '    return value;',
    '}',
    'float circleNoise_s(vec2 uv, float s, float sz) {',
    '    float uv_y = floor(uv.y);',
    '    uv.x += uv_y * 0.31;',
    '    vec2 f = fract(uv);',
    '    float h = rand_s(vec2(floor(uv.x), floor(uv_y)), s, sz);',
    '    float m = length(f - 0.25 - h * 0.5);',
    '    float r = h * 0.25;',
    '    return smoothstep(0.0, r, m * 0.75);',
    '}',
    'vec2 Hash2(vec2 p) {',
    '    float r = 523.0 * sin(dot(p, vec2(53.3158, 43.6143)));',
    '    return vec2(fract(15.32354 * r), fract(17.25865 * r));',
    '}',
    'float cells(vec2 p, float numCells, float tiles) {',
    '    p *= numCells;',
    '    float d = 1.0e10;',
    '    for (int xo = -1; xo <= 1; xo++) {',
    '        for (int yo = -1; yo <= 1; yo++) {',
    '            vec2 tp = floor(p) + vec2(float(xo), float(yo));',
    '            tp = p - tp - Hash2(mod(tp, numCells / tiles));',
    '            d = min(d, dot(tp, tp));',
    '        }',
    '    }',
    '    return sqrt(d);',
    '}',
    'float circlePattern(vec2 uv, float circle_amt, float circle_sz, float s, float sz) {',
    '    float invert = 1.0 / circle_amt;',
    '    float offset = step(invert, mod(uv.y, invert * 2.0));',
    '    uv.x += offset * invert * 0.5;',
    '    vec2 rand_co = floor(uv * circle_amt) / circle_amt;',
    '    uv = mod(uv, invert) * circle_amt;',
    '    float r = rand_s(rand_co, s, sz);',
    '    r = clamp(r, invert, 1.0 - invert);',
    '    float circ = distance(uv, vec2(r));',
    '    return smoothstep(circ, circ + 0.5, invert * circle_sz * rand_s(rand_co * 1.5, s, sz));',
    '}',
    'vec4 alphaBlend(vec4 bg, vec4 fg) {',
    '    float a = fg.a + bg.a * (1.0 - fg.a);',
    '    if (a < 0.001) return vec4(0.0);',
    '    vec3 rgb = (fg.rgb * fg.a + bg.rgb * bg.a * (1.0 - fg.a)) / a;',
    '    return vec4(rgb, a);',
    '}',
    'vec4 sampleRamp4(float t, vec4 c0, vec4 c1, vec4 c2, vec4 c3) {',
    '    t = clamp(t, 0.0, 1.0);',
    '    vec4 r = mix(c0, c1, step(0.25, t));',
    '    r = mix(r, c2, step(0.5, t));',
    '    r = mix(r, c3, step(0.75, t));',
    '    return r;',
    '}',
  ].join('\n');

  // --- Pulsar scene: neutron star + twin lighthouse beams (built from the
  //     NASA lighthouse model; no third-party shader code) ---
  var STAR_FRAG = [
    'precision highp float;',
    'varying vec2 v_pos;',
    'uniform float u_time;',
    'uniform vec2 u_resolution;',
    '',
    'float hash21(vec2 p){ vec2 q = fract(p * vec2(123.34, 456.21)); q += vec2(dot(q, q + vec2(45.32))); return fract(q.x * q.y); }',
    'float vnoise(vec2 p){ vec2 i = floor(p); vec2 f = fract(p); f = f * f * (3.0 - 2.0 * f); return mix(mix(hash21(i), hash21(i + vec2(1.0, 0.0)), f.x), mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), f.x), f.y); }',
    'float fbm(vec2 p){ float v = 0.0; float a = 0.5; for (int i = 0; i < 5; i++){ v += a * vnoise(p); p *= 2.03; a *= 0.5; } return v; }',
    '',
    'void main(){',
    '    vec2 uv = v_pos;',
    '    float aspect = u_resolution.x / u_resolution.y;',
    '    vec2 p = vec2(uv.x * aspect, uv.y);',
    '    float t = u_time;',
    '',
    '    // background starfield',
    '    vec3 bg = vec3(0.0);',
    '    vec2 gcell = floor(p * 220.0);',
    '    float gs = hash21(gcell);',
    '    float gpos = step(0.9965, gs);',
    '    vec2 gf = fract(p * 220.0) - 0.5;',
    '    vec2 goff = (vec2(hash21(gcell + vec2(7.3, 2.1)), hash21(gcell + vec2(1.7, 9.9))) - 0.5) * 0.6;',
    '    float gd = length(gf - goff);',
    '    float gtw = 0.6 + 0.4 * sin(t * (1.0 + gs * 2.0) + gs * 90.0);',
    '    bg += vec3(0.75, 0.85, 1.0) * gpos * smoothstep(0.12, 0.0, gd) * gtw;',
    '',
    '    // magnetic axis: precesses around a tilted rotation axis (lighthouse model)',
    '    vec3 rotAxis = normalize(vec3(0.15, 1.0, 0.45));',
    '    float tilt = 0.9;',
    '    float th = t * 1.8;',
    '    vec3 uu = normalize(cross(rotAxis, vec3(0.0, 0.0, 1.0)));',
    '    vec3 vv = cross(rotAxis, uu);',
    '    vec3 m = normalize(rotAxis * cos(tilt) + (uu * cos(th) + vv * sin(th)) * sin(tilt));',
    '',
    '    // neutron star (small, hot, blue-white)',
    '    float R = 0.15;',
    '    float d = length(p);',
    '    float starDisc = smoothstep(R, R - 0.004, d);',
    '    float ang = atan(p.y, p.x);',
    '    float an01 = ang / 6.28318 + 0.5;',
    '    float gran = fbm(vec2(an01 * 30.0, t * 0.18)) * 0.55 + fbm(vec2(an01 * 90.0, t * 0.3)) * 0.45;',
    '    vec3 hotC = vec3(0.95, 0.97, 1.0);',
    '    vec3 coolC = vec3(0.55, 0.70, 0.98);',
    '    vec3 surf = mix(coolC, hotC, clamp(gran * 1.25, 0.0, 1.0));',
    '    float limb = 1.0 - 0.75 * pow(clamp(d / R, 0.0, 1.0), 2.4);',
    '    surf = mix(coolC, surf, limb);',
    '',
    '    // glow',
    '    float glow = exp(-d * d * 260.0);',
    '    float halo = exp(-d * d * 26.0) * 0.30;',
    '',
    '    // beams: two cones along +m / -m, foreshortening + lighthouse pulse',
    '    vec2 m2d = normalize(m.xy + vec2(1e-4));',
    '    vec2 perp2d = vec2(-m2d.y, m2d.x);',
    '    float al = dot(p, m2d);',
    '    float aLen = abs(al);',
    '    float pe = abs(dot(p, perp2d));',
    '    float mzAbs = abs(m.z);',
    '    float mlen = length(m.xy);',
    '    float width = 0.015 + aLen * 0.16;',
    '    float cone = smoothstep(width, width * 0.30, pe);',
    '    float fil = smoothstep(0.010, 0.0, pe);',
    '    float reach = smoothstep(mlen * 2.0, mlen * 0.55, aLen);',
    '    float beamOn = smoothstep(R * 0.9, R * 1.15, aLen);',
    '    float pulseN = 0.35 + 0.65 * smoothstep(-0.15, 0.95, m.z);',
    '    float pulseS = 0.35 + 0.65 * smoothstep(-0.15, 0.95, -m.z);',
    '    float pulse = mix(pulseS, pulseN, step(0.0, al));',
    '    vec3 beamCol = vec3(0.62, 0.80, 1.0);',
    '    float beamA = (cone * 0.55 + fil * 0.95) * reach * pulse * beamOn;',
    '',
    '    // head-on pulse flash (beam sweeping across the line of sight)',
    '    float headOn = smoothstep(0.70, 0.97, mzAbs) * exp(-d * d * 30.0);',
    '',
    '    // magnetosphere glow (violet)',
    '    float magPulse = 0.5 + 0.5 * sin(t * 3.6 + 0.5);',
    '    float mag = exp(-d * d * 55.0) * (0.22 + 0.30 * magPulse);',
    '    vec3 magCol = vec3(0.52, 0.42, 0.85);',
    '',
    '    vec3 col = bg;',
    '    col += surf * starDisc;',
    '    col += hotC * glow * 0.9;',
    '    col += coolC * halo;',
    '    col += magCol * mag;',
    '    col += beamCol * beamA;',
    '    col += vec3(1.0) * fil * reach * pulse * beamOn * 0.8;',
    '    col += vec3(1.0, 0.95, 1.0) * headOn * (0.55 + 0.45 * pulse);',
    '',
    '    gl_FragColor = vec4(col, 1.0);',
    '}',
  ].join('\n');

  // --- Galaxy scene: Eluvade FRAG_GALAXY (MIT) ---
  var GALAXY_FRAG = [
    'precision highp float;',
    'varying vec2 v_pos;',
    'uniform float u_pixels;',
    'uniform float u_time;',
    'uniform float u_time_speed;',
    'uniform float u_rotation;',
    'uniform float u_zoom;',
    'uniform float u_incl;',
    'uniform float u_seed1, u_seed2, u_seed3, u_seed4, u_seed5;',
    'uniform vec4 u_col0, u_col1, u_col2, u_col3, u_col4, u_col5, u_col6;',
    COMMON,
    'const float GX_ARMS  = 2.0;',
    'const float GX_PITCH = 3.4;',
    'const float GX_CLUMP = 0.78;',
    'mat2 gx_rot(float a) { return mat2(cos(a), -sin(a), sin(a), cos(a)); }',
    'float gx_pattern(float r, float t) {',
    '    return t * 0.55 + 0.20 * sin(t * 0.45 - r * 3.2);',
    '}',
    'float gx_stars(vec2 uv, float density, float s) {',
    '    vec2 g = floor(uv * density);',
    '    vec2 f = fract(uv * density) - 0.5;',
    '    float h  = rand_s(g, s, density);',
    '    float h2 = rand_s(g + vec2(19.0, 7.0), s, density);',
    '    float d  = length(f - (vec2(h2, fract(h * 7.3)) - 0.5) * 0.7);',
    '    return step(0.88, h) * smoothstep(0.18, 0.0, d) * (0.35 + h2 * 0.65);',
    '}',
    'void main() {',
    '    vec2 uv = (floor(v_pos * u_pixels) / u_pixels) + 0.5;',
    '    float t = u_time * u_time_speed;',
    '    float ci = clamp(u_incl, 0.16, 1.0);',
    '    float edge = 1.0 - smoothstep(0.28, 0.95, ci);',
    '    vec2 p = gx_rot(u_seed1 * 0.0628 + u_rotation) * ((uv - 0.5) * u_zoom);',
    '    vec2 nq = vec2(p.x, p.y / ci) * 2.0;',
    '    float r = length(nq);',
    '    if (r > 1.5 && length(p) > 0.42) { gl_FragColor = vec4(0.0); return; }',
    '    float a = atan(nq.y, nq.x);',
    '    float spin = gx_pattern(min(r, 1.5), t);',
    '    float logr = log(max(r, 0.03));',
    '    float phase = GX_ARMS * (a + spin) + logr * GX_PITCH * GX_ARMS;',
    '    float wave = pow(cos(phase) * 0.5 + 0.5, 2.2);',
    '    vec2 wq = gx_rot(-logr * GX_PITCH + spin) * nq;',
    '    float clump = fbm_s(wq * 11.0 + 3.0, 4, u_seed2, 20.0);',
    '    float knots = fbm_s(wq * 30.0 + 9.0, 3, u_seed3, 20.0);',
    '    float haze  = fbm_s(wq * 5.0, 3, u_seed4, 20.0);',
    '    float env = smoothstep(0.07, 0.36, r) * (1.0 - smoothstep(0.55, 1.10, r));',
    '    float arm = wave * env * mix(0.55, clump * 2.0, GX_CLUMP);',
    '    float disc = (1.0 - smoothstep(0.12, 1.10, r)) * (0.26 + haze * 0.92);',
    '    float by = 0.150 * mix(1.0, 0.62, edge);',
    '    float rb = length(vec2(p.x / 0.150, p.y / by));',
    '    float bulge = exp(-rb * rb * 1.55);',
    '    float core = exp(-rb * rb * 9.0);',
    '    float halo = exp(-(p.x * p.x / 0.055 + p.y * p.y / mix(0.055, 0.017, edge)));',
    '    float dust = pow(cos(phase - 0.7) * 0.5 + 0.5, 3.5) * env * (0.4 + clump)',
    '               * smoothstep(0.22, 0.48, r);',
    '    float wob = fbm_s(vec2(p.x * 7.0 + 4.0, 1.0), 3, u_seed4, 20.0);',
    '    float lw = (0.012 + 0.011 * wob) * mix(2.4, 1.0, edge);',
    '    float ly = p.y / lw;',
    '    float lane = exp(-ly * ly)',
    '               * (1.0 - smoothstep(0.24, 0.46, abs(p.x)))',
    '               * smoothstep(0.03, 0.14, abs(p.x)) * edge;',
    '    float pts = gx_stars(uv, 115.0, u_seed5) * (0.24 + (arm + disc) * 1.7);',
    '    vec3 light = vec3(0.0);',
    '    light += u_col6.rgb * halo * 0.18;',
    '    light += u_col3.rgb * disc * mix(0.30, 0.52, edge);',
    '    light += mix(u_col3.rgb, u_col2.rgb, smoothstep(0.22, 1.05, arm)) * arm * 1.05;',
    '    light += u_col4.rgb * arm * smoothstep(0.46, 0.74, knots) * 2.10;',
    '    light += u_col1.rgb * bulge * 1.05;',
    '    light += u_col0.rgb * core * 1.50;',
    '    light += vec3(1.0) * pts * 0.50;',
    '    float shield = 1.0 - core;',
    '    light *= 1.0 - dust * 0.55 * shield - lane * 0.85;',
    '    light = mix(light, u_col5.rgb, clamp(dust * 0.20 + lane * 0.32, 0.0, 1.0) * shield);',
    '    float lum = max(light.r, max(light.g, light.b));',
    '    gl_FragColor = vec4(light / max(lum, 0.0001), clamp(lum, 0.0, 1.0));',
    '}',
  ].join('\n');

  // --- Warp scene: streaming star field ---
  var WARP_FRAG = [
    'precision highp float;',
    'varying vec2 vUV;',
    'uniform float uTime;',
    'uniform vec2 uResolution;',
    'float hash21(vec2 p){ vec2 q = fract(p * vec2(123.34, 456.21)); q += vec2(dot(q, q + vec2(45.32))); return fract(q.x * q.y); }',
    'void main(){',
    '    vec2 uv = vUV - 0.5;',
    '    uv.x *= uResolution.x / uResolution.y;',
    '    float r = length(uv);',
    '    float a = atan(uv.y, uv.x);',
    '    vec3 col = vec3(0.0);',
    '    for (int i = 0; i < 4; i++){',
    '        float layer = float(i);',
    '        float speed = 0.5 + layer * 0.7;',
    '        float nn = 48.0 + layer * 16.0;',
    '        float cell = floor(a / (6.28318 / nn));',
    '        float h = hash21(vec2(cell, layer * 7.31));',
    '        float rr = fract(r * (2.5 + layer * 1.2) - uTime * speed * (0.2 + h * 0.8));',
    '        float star = smoothstep(0.10, 0.0, abs(rr - 0.6) - 0.02);',
    '        float streak = (1.0 - smoothstep(0.0, 0.5, rr)) * 0.20;',
    '        float b = star * 0.85 + streak * h;',
    '        vec3 tint = mix(vec3(0.5, 0.7, 1.0), vec3(1.0, 0.85, 0.7), h);',
    '        col += tint * b * (0.25 + 0.75 * h) / max(1.0 + r * 3.5, 1.0);',
    '    }',
    '    col *= 1.0 - smoothstep(0.35, 1.25, r);',
    '    gl_FragColor = vec4(col, 1.0);',
    '}',
  ].join('\n');

  // --- Nebula scene: drifting fbm clouds + stars ---
  var NEBULA_FRAG = [
    'precision highp float;',
    'varying vec2 vUV;',
    'uniform float uTime;',
    'uniform vec2 uResolution;',
    'float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }',
    'float noise(vec2 p){',
    '    vec2 i = floor(p);',
    '    vec2 f = fract(p);',
    '    f = f * f * (3.0 - 2.0 * f);',
    '    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),',
    '               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);',
    '}',
    'float fbm(vec2 p){',
    '    float v = 0.0;',
    '    float a = 0.5;',
    '    for (int i = 0; i < 6; i++){ v += a * noise(p); p *= 2.03; a *= 0.5; }',
    '    return v;',
    '}',
    'void main(){',
    '    vec2 uv = vUV - 0.5;',
    '    uv.x *= uResolution.x / uResolution.y;',
    '    float t = uTime * 0.05;',
    '    vec2 p = uv * 2.1;',
    '    vec2 q = vec2(fbm(p + vec2(0.0, t)), fbm(p + vec2(5.2, 1.3) - t * 0.7));',
    '    vec2 qq = vec2(fbm(p + 4.0 * q + vec2(1.7, 9.2) + t * 0.3),',
    '                   fbm(p + 4.0 * q + vec2(8.3, 2.8) - t * 0.2));',
    '    float f = fbm(p + 4.0 * qq);',
    '    vec3 c1 = vec3(0.05, 0.03, 0.16);',
    '    vec3 c2 = vec3(0.09, 0.15, 0.33);',
    '    vec3 c3 = vec3(0.11, 0.28, 0.40);',
    '    vec3 c4 = vec3(0.46, 0.20, 0.52);',
    '    vec3 col = mix(c1, c2, clamp(f * 1.35, 0.0, 1.0));',
    '    col = mix(col, c3, clamp(f * 2.2 - 0.4, 0.0, 1.0) * 0.75);',
    '    col = mix(col, c4, clamp(pow(q.x * 0.6 + 0.5, 2.0), 0.0, 1.0) * 0.38);',
    '    vec2 g = floor(uv * 220.0);',
    '    float s = hash(g);',
    '    float tw = 0.6 + 0.4 * sin(uTime * (1.0 + s * 2.0) + s * 90.0);',
    '    float st = step(0.996, s);',
    '    col += vec3(0.8, 0.9, 1.0) * st * tw * 0.8;',
    '    col *= smoothstep(1.35, 0.45, length(uv));',
    '    gl_FragColor = vec4(col, 1.0);',
    '}',
  ].join('\n');

  // --- Black hole scene (vercel-labs/vgpu, MIT) — ES3 ---
  var BH_FRAG = [
    '#version 300 es',
    'precision highp float;',
    'in vec2 vUv;',
    'out vec4 outColor;',
    'uniform vec2 uResolution;',
    'uniform vec2 uPointer;',
    'uniform float uTime;',
    'uniform float uOrbitRadius;',
    'const float PI = 3.14159265359;',
    'const float HORIZON = 1.0;',
    'const float ISCO = 3.0;',
    'const float DISK_OUTER = 9.5;',
    'float hash21(vec2 p){ vec2 q = fract(p * vec2(123.34, 456.21)); q += vec2(dot(q, q + vec2(45.32))); return fract(q.x * q.y); }',
    'float noise(vec2 p){ vec2 i = floor(p); vec2 f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f); return mix(mix(hash21(i), hash21(i + vec2(1.0, 0.0)), u.x), mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), u.x), u.y); }',
    'float fbm(vec2 p0){ vec2 p = p0; float value = 0.0; float amplitude = 0.5; for (int i = 0; i < 4; i++){ value += amplitude * noise(p); p = mat2(1.6, 1.2, -1.2, 1.6) * p; amplitude *= 0.5; } return value; }',
    'vec3 geodesicAcceleration(vec3 position, vec3 velocity){ float r2 = dot(position, position); vec3 angularMomentum = cross(position, velocity); float h2 = dot(angularMomentum, angularMomentum); return -1.5 * h2 * position / (r2 * r2 * sqrt(r2)); }',
    'vec3 starField(vec3 direction){ vec3 d = normalize(direction); vec2 spherical = vec2(atan(d.z, d.x) / (2.0 * PI), asin(clamp(d.y, -1.0, 1.0)) / PI); vec2 grid = spherical * vec2(720.0, 360.0); vec2 cell = floor(grid); vec2 local = fract(grid) - 0.5; float seed = hash21(cell); float radius = mix(0.02, 0.07, seed * seed); float point = smoothstep(radius, 0.0, length(local)) * step(0.986, seed); float glow = smoothstep(radius * 4.0, 0.0, length(local)) * step(0.997, seed) * 0.35; float temperature = hash21(cell + vec2(17.0, 29.0)); vec3 tint = mix(vec3(0.48, 0.65, 1.0), vec3(1.0, 0.72, 0.42), temperature); return tint * (point * (1.5 + seed * 3.0) + glow); }',
    'vec4 volumeSample(vec3 point, vec3 rayVelocity){ float radius = length(point.xz); float height = abs(point.y); if (radius <= ISCO || radius >= DISK_OUTER || height > 0.42){ return vec4(0.0); } float omega = 0.42 / pow(radius, 1.5); float swirl = 2.2 * log(radius); float ang = uTime * omega + swirl; float c = cos(ang); float s = sin(ang); vec2 rc = vec2(c * point.x - s * point.z, s * point.x + c * point.z); float broad = fbm(rc * 0.9 + vec2(0.0, uTime * 0.02)); float detail = fbm(rc * 2.6 + broad * 1.5); float rings = 0.5 + 0.5 * sin(radius * 8.5 + broad * 6.0); float clumps = smoothstep(0.26, 0.84, broad * 0.72 + detail * 0.46 + rings * 0.22); float thickness = mix(0.05, 0.24, smoothstep(ISCO, DISK_OUTER, radius)); float vertical = exp(-pow(height / thickness, 2.0) * 3.4); float innerFade = smoothstep(ISCO, ISCO + 0.45, radius); float outerFade = 1.0 - smoothstep(DISK_OUTER - 2.4, DISK_OUTER, radius); float radial = (DISK_OUTER - radius) / (DISK_OUTER - ISCO); float radialFalloff = pow(radial, 0.36); float density = vertical * innerFade * outerFade * radialFalloff * clumps; float heat = pow(radial, 1.35); vec3 thermal = mix(vec3(0.55, 0.14, 0.03), vec3(1.0, 0.55, 0.16), smoothstep(0.05, 0.55, heat)); thermal = mix(thermal, vec3(1.0, 0.94, 0.82), pow(heat, 2.4)); vec3 tangent = normalize(vec3(-point.z, 0.0, point.x)); float orbitalSpeed = min(0.64, 0.94 / sqrt(max(radius - HORIZON, 0.25))); float towardObserver = dot(tangent, -normalize(rayVelocity)); float doppler = pow(clamp(1.0 / (1.0 - orbitalSpeed * towardObserver), 0.72, 1.55), 1.5); float gravitationalRedshift = sqrt(1.0 - HORIZON / radius); vec3 emission = thermal * density * doppler * gravitationalRedshift * 9.5; return vec4(emission, density * 2.1); }',
    'void main(){ float aspect = uResolution.x / uResolution.y; vec2 screen = (vUv * 2.0 - 1.0) * vec2(aspect, 1.0); float yaw = uPointer.x; float pitch = clamp(uPointer.y, -1.319, 1.319); float orbitRadius = uOrbitRadius; vec3 cameraPosition = vec3(sin(yaw) * cos(pitch) * orbitRadius, sin(pitch) * orbitRadius, cos(yaw) * cos(pitch) * orbitRadius); vec3 forward = normalize(-cameraPosition); vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0))); vec3 up = cross(right, forward); vec3 position = cameraPosition; vec3 velocity = normalize(forward * 1.72 + right * screen.x + up * screen.y); vec3 accumulated = vec3(0.0); float transmittance = 1.0; bool escaped = false; for (int stepIndex = 0; stepIndex < 256; stepIndex++){ float radius = length(position); if (radius < HORIZON * 1.015){ break; } if (radius > 24.0 && stepIndex > 24 && dot(position, velocity) > 0.0){ escaped = true; break; } float stepSize = clamp((radius - HORIZON) * 0.07, 0.016, 0.24); float rxz = length(position.xz); if (rxz > ISCO - 0.6 && rxz < DISK_OUTER + 0.6){ float slab = mix(0.05, 0.24, smoothstep(ISCO, DISK_OUTER, rxz)); float vy = max(abs(velocity.y), 0.001); float band = slab * 3.0; float ay = abs(position.y); if (ay < band){ stepSize = min(stepSize, (slab * 0.4) / vy); } else if (position.y * velocity.y < 0.0){ stepSize = min(stepSize, (ay - band) / vy); } stepSize = max(stepSize, 0.004); } vec3 previousPosition = position; vec3 acceleration0 = geodesicAcceleration(position, velocity); velocity += acceleration0 * (0.5 * stepSize); position += velocity * stepSize; vec3 acceleration1 = geodesicAcceleration(position, velocity); velocity += acceleration1 * (0.5 * stepSize); velocity = normalize(velocity); vec3 samplePoint = mix(previousPosition, position, 0.5); vec4 volume = volumeSample(samplePoint, velocity); if (volume.a > 0.0001 && transmittance > 0.008){ float opticalDepth = volume.a * stepSize; float absorbed = 1.0 - exp(-opticalDepth); accumulated += volume.rgb * transmittance * absorbed / max(volume.a, 0.001); transmittance *= exp(-opticalDepth); } } if (escaped){ accumulated += starField(velocity) * transmittance; } outColor = vec4(accumulated, 1.0); }',
  ].join('\n');

  var BRIGHT_FRAG = [
    '#version 300 es', 'precision highp float;', 'in vec2 vUv;', 'out vec4 outColor;',
    'uniform sampler2D uSrc;',
    'void main(){ vec3 color = texture(uSrc, vUv).rgb; float luminance = dot(color, vec3(0.2126, 0.7152, 0.0722)); float knee = 0.6; float soft = clamp((luminance - 1.0 + knee) / (2.0 * knee), 0.0, 1.0); float contribution = max(soft * soft * knee, luminance - 1.0); float weight = contribution / max(luminance, 0.0001); outColor = vec4(color * weight, 1.0); }',
  ].join('\n');

  var BLUR_FRAG = [
    '#version 300 es', 'precision highp float;', 'in vec2 vUv;', 'out vec4 outColor;',
    'uniform sampler2D uSrc;',
    'uniform vec2 uTexelSize;',
    'uniform vec2 uDirection;',
    'uniform float uRadius;',
    'void main(){ float w0 = 0.227027; float w1 = 0.1945946; float w2 = 0.1216216; float w3 = 0.054054; float w4 = 0.016216; vec2 step = uTexelSize * uDirection * uRadius; vec3 result = texture(uSrc, vUv).rgb * w0; result += texture(uSrc, vUv + step).rgb * w1; result += texture(uSrc, vUv - step).rgb * w1; result += texture(uSrc, vUv + step * 2.0).rgb * w2; result += texture(uSrc, vUv - step * 2.0).rgb * w2; result += texture(uSrc, vUv + step * 3.0).rgb * w3; result += texture(uSrc, vUv - step * 3.0).rgb * w3; result += texture(uSrc, vUv + step * 4.0).rgb * w4; result += texture(uSrc, vUv - step * 4.0).rgb * w4; outColor = vec4(result, 1.0); }',
  ].join('\n');

  var COMPOSITE_FRAG = [
    '#version 300 es', 'precision highp float;', 'in vec2 vUv;', 'out vec4 outColor;',
    'uniform sampler2D uScene;',
    'uniform sampler2D uBloom;',
    'vec3 aces(vec3 x){ float a = 2.51; float b = 0.03; float c = 2.43; float d = 0.59; float e = 0.14; return clamp((x * (a * x + vec3(b))) / (x * (c * x + vec3(d)) + vec3(e)), vec3(0.0), vec3(1.0)); }',
    'void main(){ vec3 hdrScene = texture(uScene, vUv).rgb; vec3 hdrBloom = texture(uBloom, vUv).rgb; vec3 color = hdrScene + hdrBloom * 0.9; color *= 1.15; color = aces(color); vec2 centered = vUv - vec2(0.5); float vignette = 1.0 - smoothstep(0.55, 1.15, length(centered) * 1.6); color *= mix(0.72, 1.0, vignette); color = pow(color, vec3(1.0 / 2.2)); outColor = vec4(color, 1.0); }',
  ].join('\n');

  // --- Crossfade (ES1) ---
  var FADE_FRAG = [
    'precision highp float;',
    'varying vec2 vUV;',
    'uniform sampler2D uPrev;',
    'uniform sampler2D uCurr;',
    'uniform float uMix;',
    'void main(){ vec3 a = texture2D(uPrev, vUV).rgb; vec3 b = texture2D(uCurr, vUV).rgb; vec3 col = mix(a, b, uMix); float vig = 1.0 - smoothstep(0.62, 1.28, length(vUV - 0.5) * 1.6); col *= mix(0.82, 1.0, vig); gl_FragColor = vec4(col, 1.0); }',
  ].join('\n');

  /* ============================================================
   * GL plumbing
   * ============================================================ */

  function compile(type, source) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, source);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      throw new Error('shader: ' + gl.getShaderInfoLog(sh));
    }
    return sh;
  }

  function link(fragSrc, vsSrc, attribs) {
    var p = gl.createProgram();
    if (attribs) {
      for (var i = 0; i < attribs.length; i++) gl.bindAttribLocation(p, i, attribs[i]);
    }
    gl.attachShader(p, compile(gl.FRAGMENT_SHADER, fragSrc));
    gl.attachShader(p, compile(gl.VERTEX_SHADER, vsSrc));
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      throw new Error('link: ' + gl.getProgramInfoLog(p));
    }
    return p;
  }

  function makeTarget(w, h) {
    var tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texImage2D(gl.TEXTURE_2D, 0, INTERNAL, w, h, 0, gl.RGBA, FLOAT_TYPE, null);
    var fbo = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return { tex: tex, fbo: fbo, w: w, h: h };
  }

  function destroyTarget(t) {
    gl.deleteTexture(t.tex);
    gl.deleteFramebuffer(t.fbo);
  }

  // Quad buffer (ES1 draws)
  var quadBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1, 1, -1, -1, 1, 1, 1,
  ]), gl.STATIC_DRAW);
  var quadIdx = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, quadIdx);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array([0, 1, 2, 1, 3, 2]), gl.STATIC_DRAW);

  var vaoQuad = gl.createVertexArray();
  gl.bindVertexArray(vaoQuad);
  gl.bindBuffer(gl.ARRAY_BUFFER, quadBuf);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, quadIdx);
  gl.bindVertexArray(null);

  var vaoFull = gl.createVertexArray(); // empty, for gl_VertexID triangle

  function drawQuad() {
    gl.bindVertexArray(vaoQuad);
    gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0);
  }
  function drawFull() {
    gl.bindVertexArray(vaoFull);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }

  /* ---------------- programs ---------------- */

  var prog = {
    warp: link(WARP_FRAG, QUAD_VS, ['aPosition']),
    star: link(STAR_FRAG, CENTER_VS, ['aPosition']),
    galaxy: link(GALAXY_FRAG, CENTER_VS, ['aPosition']),
    nebula: link(NEBULA_FRAG, QUAD_VS, ['aPosition']),
    fade: link(FADE_FRAG, QUAD_VS, ['aPosition']),
    bhScene: link(BH_FRAG, FULL_VS_3),
    bhBright: link(BRIGHT_FRAG, FULL_VS_3),
    bhBlur: link(BLUR_FRAG, FULL_VS_3),
    bhComposite: link(COMPOSITE_FRAG, FULL_VS_3),
  };

  var locCache = {};
  function L(p, name) {
    var k = p.__key + ':' + name;
    if (locCache[k] === undefined) locCache[k] = gl.getUniformLocation(p, name);
    return locCache[k];
  }
  (function tag() {
    var i = 0;
    for (var k in prog) prog[k].__key = i++;
  })();

  /* ---------------- sizes + targets ---------------- */

  var W = 0, H = 0, dpr = Math.min(1.6, Math.max(1, window.devicePixelRatio || 1));
  var currTex = null, prevTex = null;
  var bhScene = null, bhBloomA = null, bhBloomB = null;

  function createTargets(w, h) {
    if (currTex) { destroyTarget(currTex); destroyTarget(prevTex); }
    if (bhScene) { destroyTarget(bhScene); destroyTarget(bhBloomA); destroyTarget(bhBloomB); }
    currTex = makeTarget(w, h);
    prevTex = makeTarget(w, h);
    bhScene = makeTarget(w, h);
    var bh = Math.min(360, h);
    var bw = Math.max(1, Math.round(bh * w / h));
    bhBloomA = makeTarget(bw, bh);
    bhBloomB = makeTarget(bw, bh);
  }

  function resize() {
    var w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (w === W && h === H) return;
    W = w; H = h;
    canvas.width = w; canvas.height = h;
    createTargets(w, h);
  }

  /* ============================================================
   * Timeline
   * ============================================================ */

  var SCENES = [
    { id: 'warp', dur: 9 },
    { id: 'star', dur: 11 },
    { id: 'blackhole', dur: 15 },
    { id: 'galaxy', dur: 11 },
    { id: 'nebula', dur: 13 },
  ];
  var FADE = 2.6;
  var TOTAL = 0;
  SCENES.forEach(function (s) { s.start = TOTAL; TOTAL += s.dur; });

  function sceneAt(t) {
    for (var i = 0; i < SCENES.length; i++) {
      if (t < SCENES[i].start + SCENES[i].dur) return { idx: i, local: t - SCENES[i].start };
    }
    return { idx: 0, local: 0 };
  }

  function lerp(a, b, t) { return a + (b - a) * t; }
  function clamp01(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

  /* ============================================================
   * Scene renderers (each draws into an FBO at local time t)
   * ============================================================ */

  var CLEAR = [0, 0, 0, 1];
  function bindAndClear(fbo) {
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo.fbo);
    gl.viewport(0, 0, fbo.w, fbo.h);
    gl.clearColor.apply(gl, CLEAR);
    gl.clear(gl.COLOR_BUFFER_BIT);
  }

  function renderWarp(t, fbo) {
    bindAndClear(fbo);
    gl.useProgram(prog.warp);
    gl.uniform1f(L(prog.warp, 'uTime'), t);
    gl.uniform2f(L(prog.warp, 'uResolution'), fbo.w, fbo.h);
    drawQuad();
  }

  function renderStar(t, fbo) {
    bindAndClear(fbo);
    var p = prog.star;
    gl.useProgram(p);
    gl.uniform1f(L(p, 'u_time'), t);
    gl.uniform2f(L(p, 'u_resolution'), fbo.w, fbo.h);
    drawQuad();
  }

  function renderGalaxy(t, fbo) {
    bindAndClear(fbo);
    var p = prog.galaxy;
    gl.useProgram(p);
    gl.uniform1f(L(p, 'u_pixels'), fbo.h);
    gl.uniform1f(L(p, 'u_time'), t);
    gl.uniform1f(L(p, 'u_time_speed'), 1.0);
    gl.uniform1f(L(p, 'u_rotation'), t * 0.02);
    gl.uniform1f(L(p, 'u_zoom'), 1.0 + t * 0.012);
    gl.uniform1f(L(p, 'u_incl'), 0.70 + 0.22 * Math.sin(t * 0.18));
    gl.uniform1f(L(p, 'u_seed1'), 3.3);
    gl.uniform1f(L(p, 'u_seed2'), 11.1);
    gl.uniform1f(L(p, 'u_seed3'), 6.6);
    gl.uniform1f(L(p, 'u_seed4'), 8.8);
    gl.uniform1f(L(p, 'u_seed5'), 2.2);
    gl.uniform4f(L(p, 'u_col0'), 1.000, 0.972, 0.898, 1); // core
    gl.uniform4f(L(p, 'u_col1'), 1.000, 0.839, 0.573, 1); // bulge
    gl.uniform4f(L(p, 'u_col2'), 0.784, 0.867, 1.000, 1); // arm1
    gl.uniform4f(L(p, 'u_col3'), 0.396, 0.545, 0.878, 1); // arm2
    gl.uniform4f(L(p, 'u_col4'), 1.000, 0.541, 0.616, 1); // knot
    gl.uniform4f(L(p, 'u_col5'), 0.180, 0.106, 0.129, 1); // dust
    gl.uniform4f(L(p, 'u_col6'), 0.318, 0.294, 0.514, 1); // halo
    drawQuad();
  }

  function renderNebula(t, fbo) {
    bindAndClear(fbo);
    var p = prog.nebula;
    gl.useProgram(p);
    gl.uniform1f(L(p, 'uTime'), t);
    gl.uniform2f(L(p, 'uResolution'), fbo.w, fbo.h);
    drawQuad();
  }

  function renderBlackhole(t, fbo) {
    // camera timeline: approach → orbit → plunge
    var d = SCENES[2].dur;
    var phase = t / d;
    var yaw, pitch, orbitR;
    if (phase < 0.25) {
      var p0 = phase / 0.25;
      orbitR = lerp(30, 21, p0);
      pitch = lerp(0.02, 0.12, p0);
      yaw = t * 0.05;
    } else if (phase < 0.7) {
      var p1 = (phase - 0.25) / 0.45;
      orbitR = 21;
      pitch = lerp(0.12, 0.5, p1);
      yaw = (t - 0.25 * d) * 0.28;
    } else {
      var p2 = (phase - 0.7) / 0.3;
      orbitR = lerp(21, 6.5, p2);
      pitch = lerp(0.5, 0.25, p2);
      yaw = (t - 0.25 * d) * 0.28;
    }

    // pass 1: scene → bhScene
    bindAndClear(bhScene);
    gl.useProgram(prog.bhScene);
    gl.uniform2f(L(prog.bhScene, 'uResolution'), bhScene.w, bhScene.h);
    gl.uniform2f(L(prog.bhScene, 'uPointer'), yaw, pitch);
    gl.uniform1f(L(prog.bhScene, 'uTime'), t);
    gl.uniform1f(L(prog.bhScene, 'uOrbitRadius'), orbitR);
    drawFull();

    // pass 2: bright → bhBloomA
    bindAndClear(bhBloomA);
    gl.useProgram(prog.bhBright);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, bhScene.tex);
    gl.uniform1i(L(prog.bhBright, 'uSrc'), 0);
    drawFull();

    // passes 3–6: 4 blurs ping-pong
    var blurs = [
      { dir: [1, 0], radius: 1 },
      { dir: [0, 1], radius: 1 },
      { dir: [1, 0], radius: 2.4 },
      { dir: [0, 1], radius: 2.4 },
    ];
    gl.useProgram(prog.bhBlur);
    for (var i = 0; i < blurs.length; i++) {
      var src = i % 2 === 0 ? bhBloomA : bhBloomB;
      var dst = i % 2 === 0 ? bhBloomB : bhBloomA;
      bindAndClear(dst);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, src.tex);
      gl.uniform1i(L(prog.bhBlur, 'uSrc'), 0);
      gl.uniform2f(L(prog.bhBlur, 'uTexelSize'), 1 / src.w, 1 / src.h);
      gl.uniform2f(L(prog.bhBlur, 'uDirection'), blurs[i].dir[0], blurs[i].dir[1]);
      gl.uniform1f(L(prog.bhBlur, 'uRadius'), blurs[i].radius);
      drawFull();
    }

    // pass 7: composite → fbo
    bindAndClear(fbo);
    gl.useProgram(prog.bhComposite);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, bhScene.tex);
    gl.uniform1i(L(prog.bhComposite, 'uScene'), 0);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, bhBloomA.tex);
    gl.uniform1i(L(prog.bhComposite, 'uBloom'), 1);
    drawFull();
  }

  function renderScene(id, t, fbo) {
    if (id === 'warp') renderWarp(t, fbo);
    else if (id === 'star') renderStar(t, fbo);
    else if (id === 'blackhole') renderBlackhole(t, fbo);
    else if (id === 'galaxy') renderGalaxy(t, fbo);
    else if (id === 'nebula') renderNebula(t, fbo);
  }

  function drawFade(aTex, bTex, mix) {
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.viewport(0, 0, W, H);
    gl.clearColor.apply(gl, CLEAR);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(prog.fade);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, aTex);
    gl.uniform1i(L(prog.fade, 'uPrev'), 0);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, bTex);
    gl.uniform1i(L(prog.fade, 'uCurr'), 1);
    gl.uniform1f(L(prog.fade, 'uMix'), mix);
    drawQuad();
  }

  /* ============================================================
   * Director
   * ============================================================ */

  var startTime = performance.now();

  function frame(now) {
    resize();
    var t = ((now - startTime) / 1000) % TOTAL;
    var s = sceneAt(t);
    var cur = SCENES[s.idx];
    var remaining = cur.dur - s.local;
    var next = SCENES[(s.idx + 1) % SCENES.length];

    if (remaining < FADE) {
      var mix = clamp01(1 - remaining / FADE);
      renderScene(cur.id, s.local, prevTex);
      renderScene(next.id, 0.0, currTex);
      drawFade(prevTex.tex, currTex.tex, mix);
    } else {
      renderScene(cur.id, s.local, currTex);
      drawFade(currTex.tex, currTex.tex, 0.0);
    }
    requestAnimationFrame(frame);
  }

  /* ============================================================
   * Boot + fallback
   * ============================================================ */

  var raf = 0;
  try {
    resize();
    raf = requestAnimationFrame(frame);
  } catch (err) {
    console.error('celestial film failed:', err);
    if (canvas.parentElement) canvas.parentElement.removeChild(canvas);
    var fb = document.getElementById('cosmos-fallback');
    if (fb) fb.hidden = false;
    return;
  }

  window.addEventListener('resize', function () {
    var nd = Math.min(1.6, Math.max(1, window.devicePixelRatio || 1));
    if (nd !== dpr) { dpr = nd; W = 0; H = 0; }
  });

  window.__filmDispose = function () {
    cancelAnimationFrame(raf);
  };
})();
