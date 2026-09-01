/* ============================================================
 * Black Hole — faithful WebGL2 port of vercel-labs/vgpu's
 * "black-hole" example (MIT). Same maths, same pipeline:
 *   scene (raymarched geodesic lensing + accretion disk + stars)
 *   → bright-pass → 4 gaussian blurs (ping-pong) → composite
 *     (ACES tonemap + vignette + gamma).
 *
 * Pointer orbit + continuous disk animation, exactly like the
 * original renderer.ts / installOrbitInput.
 * ============================================================ */
(function () {
  'use strict';

  var canvas = document.getElementById('blackhole-canvas');
  var fallback = document.getElementById('cosmos-fallback');
  if (!canvas) return;

  var gl = canvas.getContext('webgl2', {
    antialias: false,
    depth: false,
    stencil: false,
    alpha: false,
    powerPreference: 'high-performance',
  });

  // Graceful fallback: no WebGL2 → show the Cosmos B timelapse instead.
  if (!gl) {
    if (fallback) { fallback.hidden = false; }
    if (canvas.parentElement) canvas.remove();
    return;
  }
  if (fallback) fallback.remove();

  var halfFloat = !!(gl.getExtension('EXT_color_buffer_float') || gl.getExtension('EXT_color_buffer_half_float'));
  var INTERNAL = halfFloat ? gl.RGBA16F : gl.RGBA8;

  /* ---------------- shaders ---------------- */

  var VERT = [
    '#version 300 es',
    'precision highp float;',
    'out vec2 vUv;',
    'void main(){',
    '  vec2 pos = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));',
    '  vUv = pos;',
    '  gl_Position = vec4(pos * 2.0 - 1.0, 0.0, 1.0);',
    '}',
  ].join('\n');

  // --- scene: raymarched black hole (port of black-hole.wgsl) ---
  var SCENE_FRAG = [
    '#version 300 es',
    'precision highp float;',
    'in vec2 vUv;',
    'out vec4 outColor;',
    'uniform vec2 uResolution;',
    'uniform vec2 uPointer;',
    'uniform float uTime;',
    'const float PI = 3.14159265359;',
    'const float HORIZON = 1.0;',
    'const float ISCO = 3.0;',
    'const float DISK_OUTER = 9.5;',
    'float hash21(vec2 p){',
    '  vec2 q = fract(p * vec2(123.34, 456.21));',
    '  q += vec2(dot(q, q + vec2(45.32)));',
    '  return fract(q.x * q.y);',
    '}',
    'float noise(vec2 p){',
    '  vec2 i = floor(p);',
    '  vec2 f = fract(p);',
    '  vec2 u = f * f * (3.0 - 2.0 * f);',
    '  return mix(mix(hash21(i), hash21(i + vec2(1.0, 0.0)), u.x),',
    '             mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), u.x), u.y);',
    '}',
    'float fbm(vec2 p0){',
    '  vec2 p = p0;',
    '  float value = 0.0;',
    '  float amplitude = 0.5;',
    '  for (int i = 0; i < 4; i++){',
    '    value += amplitude * noise(p);',
    '    p = mat2(1.6, 1.2, -1.2, 1.6) * p;',
    '    amplitude *= 0.5;',
    '  }',
    '  return value;',
    '}',
    'vec3 geodesicAcceleration(vec3 position, vec3 velocity){',
    '  float r2 = dot(position, position);',
    '  vec3 angularMomentum = cross(position, velocity);',
    '  float h2 = dot(angularMomentum, angularMomentum);',
    '  return -1.5 * h2 * position / (r2 * r2 * sqrt(r2));',
    '}',
    'vec3 starField(vec3 direction){',
    '  vec3 d = normalize(direction);',
    '  vec2 spherical = vec2(atan(d.z, d.x) / (2.0 * PI), asin(clamp(d.y, -1.0, 1.0)) / PI);',
    '  vec2 grid = spherical * vec2(720.0, 360.0);',
    '  vec2 cell = floor(grid);',
    '  vec2 local = fract(grid) - 0.5;',
    '  float seed = hash21(cell);',
    '  float radius = mix(0.02, 0.07, seed * seed);',
    '  float point = smoothstep(radius, 0.0, length(local)) * step(0.986, seed);',
    '  float glow = smoothstep(radius * 4.0, 0.0, length(local)) * step(0.997, seed) * 0.35;',
    '  float temperature = hash21(cell + vec2(17.0, 29.0));',
    '  vec3 tint = mix(vec3(0.48, 0.65, 1.0), vec3(1.0, 0.72, 0.42), temperature);',
    '  return tint * (point * (1.5 + seed * 3.0) + glow);',
    '}',
    'vec4 volumeSample(vec3 point, vec3 rayVelocity){',
    '  float radius = length(point.xz);',
    '  float height = abs(point.y);',
    '  if (radius <= ISCO || radius >= DISK_OUTER || height > 0.42){ return vec4(0.0); }',
    '  float omega = 0.42 / pow(radius, 1.5);',
    '  float swirl = 2.2 * log(radius);',
    '  float ang = uTime * omega + swirl;',
    '  float c = cos(ang);',
    '  float s = sin(ang);',
    '  vec2 rc = vec2(c * point.x - s * point.z, s * point.x + c * point.z);',
    '  float broad = fbm(rc * 0.9 + vec2(0.0, uTime * 0.02));',
    '  float detail = fbm(rc * 2.6 + broad * 1.5);',
    '  float rings = 0.5 + 0.5 * sin(radius * 8.5 + broad * 6.0);',
    '  float clumps = smoothstep(0.26, 0.84, broad * 0.72 + detail * 0.46 + rings * 0.22);',
    '  float thickness = mix(0.05, 0.24, smoothstep(ISCO, DISK_OUTER, radius));',
    '  float vertical = exp(-pow(height / thickness, 2.0) * 3.4);',
    '  float innerFade = smoothstep(ISCO, ISCO + 0.45, radius);',
    '  float outerFade = 1.0 - smoothstep(DISK_OUTER - 2.4, DISK_OUTER, radius);',
    '  float radial = (DISK_OUTER - radius) / (DISK_OUTER - ISCO);',
    '  float radialFalloff = pow(radial, 0.36);',
    '  float density = vertical * innerFade * outerFade * radialFalloff * clumps;',
    '  float heat = pow(radial, 1.35);',
    '  vec3 thermal = mix(vec3(0.55, 0.14, 0.03), vec3(1.0, 0.55, 0.16), smoothstep(0.05, 0.55, heat));',
    '  thermal = mix(thermal, vec3(1.0, 0.94, 0.82), pow(heat, 2.4));',
    '  vec3 tangent = normalize(vec3(-point.z, 0.0, point.x));',
    '  float orbitalSpeed = min(0.64, 0.94 / sqrt(max(radius - HORIZON, 0.25)));',
    '  float towardObserver = dot(tangent, -normalize(rayVelocity));',
    '  float doppler = pow(clamp(1.0 / (1.0 - orbitalSpeed * towardObserver), 0.72, 1.55), 1.5);',
    '  float gravitationalRedshift = sqrt(1.0 - HORIZON / radius);',
    '  vec3 emission = thermal * density * doppler * gravitationalRedshift * 9.5;',
    '  return vec4(emission, density * 2.1);',
    '}',
    'void main(){',
    '  float aspect = uResolution.x / uResolution.y;',
    '  vec2 screen = (vUv * 2.0 - 1.0) * vec2(aspect, 1.0);',
    '  float yaw = uPointer.x;',
    '  float pitch = clamp(uPointer.y, -1.319, 1.319);',
    '  float orbitRadius = 21.0;',
    '  vec3 cameraPosition = vec3(',
    '    sin(yaw) * cos(pitch) * orbitRadius,',
    '    sin(pitch) * orbitRadius,',
    '    cos(yaw) * cos(pitch) * orbitRadius);',
    '  vec3 forward = normalize(-cameraPosition);',
    '  vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));',
    '  vec3 up = cross(right, forward);',
    '  vec3 position = cameraPosition;',
    '  vec3 velocity = normalize(forward * 1.72 + right * screen.x + up * screen.y);',
    '  vec3 accumulated = vec3(0.0);',
    '  float transmittance = 1.0;',
    '  bool escaped = false;',
    '  for (int stepIndex = 0; stepIndex < 256; stepIndex++){',
    '    float radius = length(position);',
    '    if (radius < HORIZON * 1.015){ break; }',
    '    if (radius > 24.0 && stepIndex > 24 && dot(position, velocity) > 0.0){ escaped = true; break; }',
    '    float stepSize = clamp((radius - HORIZON) * 0.07, 0.016, 0.24);',
    '    float rxz = length(position.xz);',
    '    if (rxz > ISCO - 0.6 && rxz < DISK_OUTER + 0.6){',
    '      float slab = mix(0.05, 0.24, smoothstep(ISCO, DISK_OUTER, rxz));',
    '      float vy = max(abs(velocity.y), 0.001);',
    '      float band = slab * 3.0;',
    '      float ay = abs(position.y);',
    '      if (ay < band){ stepSize = min(stepSize, (slab * 0.4) / vy); }',
    '      else if (position.y * velocity.y < 0.0){ stepSize = min(stepSize, (ay - band) / vy); }',
    '      stepSize = max(stepSize, 0.004);',
    '    }',
    '    vec3 previousPosition = position;',
    '    vec3 acceleration0 = geodesicAcceleration(position, velocity);',
    '    velocity += acceleration0 * (0.5 * stepSize);',
    '    position += velocity * stepSize;',
    '    vec3 acceleration1 = geodesicAcceleration(position, velocity);',
    '    velocity += acceleration1 * (0.5 * stepSize);',
    '    velocity = normalize(velocity);',
    '    vec3 samplePoint = mix(previousPosition, position, 0.5);',
    '    vec4 volume = volumeSample(samplePoint, velocity);',
    '    if (volume.a > 0.0001 && transmittance > 0.008){',
    '      float opticalDepth = volume.a * stepSize;',
    '      float absorbed = 1.0 - exp(-opticalDepth);',
    '      accumulated += volume.rgb * transmittance * absorbed / max(volume.a, 0.001);',
    '      transmittance *= exp(-opticalDepth);',
    '    }',
    '  }',
    '  if (escaped){ accumulated += starField(velocity) * transmittance; }',
    '  outColor = vec4(accumulated, 1.0);',
    '}',
  ].join('\n');

  // --- bright-pass: highlight extraction (port of bright-pass.wgsl) ---
  var BRIGHT_FRAG = [
    '#version 300 es',
    'precision highp float;',
    'in vec2 vUv;',
    'out vec4 outColor;',
    'uniform sampler2D uSrc;',
    'void main(){',
    '  vec3 color = texture(uSrc, vUv).rgb;',
    '  float luminance = dot(color, vec3(0.2126, 0.7152, 0.0722));',
    '  float knee = 0.6;',
    '  float soft = clamp((luminance - 1.0 + knee) / (2.0 * knee), 0.0, 1.0);',
    '  float contribution = max(soft * soft * knee, luminance - 1.0);',
    '  float weight = contribution / max(luminance, 0.0001);',
    '  outColor = vec4(color * weight, 1.0);',
    '}',
  ].join('\n');

  // --- blur: 9-tap gaussian (port of blur.wgsl) ---
  var BLUR_FRAG = [
    '#version 300 es',
    'precision highp float;',
    'in vec2 vUv;',
    'out vec4 outColor;',
    'uniform sampler2D uSrc;',
    'uniform vec2 uTexelSize;',
    'uniform vec2 uDirection;',
    'uniform float uRadius;',
    'void main(){',
    '  float w0 = 0.227027;',
    '  float w1 = 0.1945946;',
    '  float w2 = 0.1216216;',
    '  float w3 = 0.054054;',
    '  float w4 = 0.016216;',
    '  vec2 step = uTexelSize * uDirection * uRadius;',
    '  vec3 result = texture(uSrc, vUv).rgb * w0;',
    '  result += texture(uSrc, vUv + step).rgb * w1;',
    '  result += texture(uSrc, vUv - step).rgb * w1;',
    '  result += texture(uSrc, vUv + step * 2.0).rgb * w2;',
    '  result += texture(uSrc, vUv - step * 2.0).rgb * w2;',
    '  result += texture(uSrc, vUv + step * 3.0).rgb * w3;',
    '  result += texture(uSrc, vUv - step * 3.0).rgb * w3;',
    '  result += texture(uSrc, vUv + step * 4.0).rgb * w4;',
    '  result += texture(uSrc, vUv - step * 4.0).rgb * w4;',
    '  outColor = vec4(result, 1.0);',
    '}',
  ].join('\n');

  // --- composite: ACES + vignette + gamma (port of composite.wgsl) ---
  var COMPOSITE_FRAG = [
    '#version 300 es',
    'precision highp float;',
    'in vec2 vUv;',
    'out vec4 outColor;',
    'uniform sampler2D uScene;',
    'uniform sampler2D uBloom;',
    'vec3 aces(vec3 x){',
    '  float a = 2.51;',
    '  float b = 0.03;',
    '  float c = 2.43;',
    '  float d = 0.59;',
    '  float e = 0.14;',
    '  return clamp((x * (a * x + vec3(b))) / (x * (c * x + vec3(d)) + vec3(e)), vec3(0.0), vec3(1.0));',
    '}',
    'void main(){',
    '  vec3 hdrScene = texture(uScene, vUv).rgb;',
    '  vec3 hdrBloom = texture(uBloom, vUv).rgb;',
    '  vec3 color = hdrScene + hdrBloom * 0.9;',
    '  color *= 1.15;',
    '  color = aces(color);',
    '  vec2 centered = vUv - vec2(0.5);',
    '  float vignette = 1.0 - smoothstep(0.55, 1.15, length(centered) * 1.6);',
    '  color *= mix(0.72, 1.0, vignette);',
    '  color = pow(color, vec3(1.0 / 2.2));',
    '  outColor = vec4(color, 1.0);',
    '}',
  ].join('\n');

  /* ---------------- helpers ---------------- */

  function compile(type, source) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, source);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      throw new Error('shader: ' + gl.getShaderInfoLog(sh));
    }
    return sh;
  }

  function program(fragSource) {
    var p = gl.createProgram();
    gl.attachShader(p, compile(gl.VERTEX_SHADER, VERT));
    gl.attachShader(p, compile(gl.FRAGMENT_SHADER, fragSource));
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
    gl.texImage2D(gl.TEXTURE_2D, 0, INTERNAL, w, h, 0, gl.RGBA, halfFloat ? gl.HALF_FLOAT : gl.UNSIGNED_BYTE, null);
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

  /* ---------------- programs + uniforms ---------------- */

  var sceneProg = program(SCENE_FRAG);
  var brightProg = program(BRIGHT_FRAG);
  var blurProg = program(BLUR_FRAG);
  var compositeProg = program(COMPOSITE_FRAG);

  var sceneLoc = {
    resolution: gl.getUniformLocation(sceneProg, 'uResolution'),
    pointer: gl.getUniformLocation(sceneProg, 'uPointer'),
    time: gl.getUniformLocation(sceneProg, 'uTime'),
  };
  var brightLoc = { src: gl.getUniformLocation(brightProg, 'uSrc') };
  var blurLoc = {
    src: gl.getUniformLocation(blurProg, 'uSrc'),
    texelSize: gl.getUniformLocation(blurProg, 'uTexelSize'),
    direction: gl.getUniformLocation(blurProg, 'uDirection'),
    radius: gl.getUniformLocation(blurProg, 'uRadius'),
  };
  var compositeLoc = {
    scene: gl.getUniformLocation(compositeProg, 'uScene'),
    bloom: gl.getUniformLocation(compositeProg, 'uBloom'),
  };

  var vao = gl.createVertexArray();

  /* ---------------- orbit input (faithful port) ---------------- */

  var yaw = 0;
  var pitch = 0.05;
  var targetYaw = 0;
  var targetPitch = 0.05;
  var activePointer;

  canvas.style.touchAction = 'none';

  canvas.addEventListener('pointerdown', function (e) {
    if (!e.isPrimary || activePointer !== undefined) return;
    activePointer = e.pointerId;
    canvas.setPointerCapture && canvas.setPointerCapture(e.pointerId);
  });
  canvas.addEventListener('pointermove', function (e) {
    if (!e.isPrimary || (activePointer !== undefined && e.pointerId !== activePointer)) return;
    var rect = canvas.getBoundingClientRect();
    var x = Math.max(0, Math.min(1, (e.clientX - rect.left) / Math.max(1, rect.width)));
    var y = Math.max(0, Math.min(1, (e.clientY - rect.top) / Math.max(1, rect.height)));
    targetYaw = (0.5 - x) * Math.PI * 1.4;
    targetPitch = Math.max(-Math.PI * 0.42, Math.min(Math.PI * 0.42, (y - 0.5) * Math.PI * 0.7));
  });
  function pointerEnd(e) {
    if (e.pointerId !== activePointer) return;
    if (canvas.hasPointerCapture && canvas.hasPointerCapture(e.pointerId)) {
      canvas.releasePointerCapture(e.pointerId);
    }
    activePointer = undefined;
  }
  canvas.addEventListener('pointerup', pointerEnd);
  canvas.addEventListener('pointercancel', pointerEnd);

  function updateOrbit() {
    yaw += (targetYaw - yaw) * 0.12;
    pitch += (targetPitch - pitch) * 0.12;
    return [yaw, pitch];
  }

  /* ---------------- resize + targets ---------------- */

  var scene = null;
  var bloomA = null;
  var bloomB = null;

  function createTargets(fbW, fbH) {
    var bloomH = Math.min(360, fbH);
    var bloomW = Math.max(1, Math.round(bloomH * fbW / fbH));
    scene = makeTarget(fbW, fbH);
    bloomA = makeTarget(bloomW, bloomH);
    bloomB = makeTarget(bloomW, bloomH);
  }

  function destroyTargets() {
    if (scene) destroyTarget(scene);
    if (bloomA) destroyTarget(bloomA);
    if (bloomB) destroyTarget(bloomB);
  }

  var fbW = 0;
  var fbH = 0;

  function resize() {
    var w = Math.max(1, Math.round(canvas.clientWidth * dpr));
    var h = Math.max(1, Math.round(canvas.clientHeight * dpr));
    if (w === fbW && h === fbH) return;
    fbW = w;
    fbH = h;
    canvas.width = w;
    canvas.height = h;
    destroyTargets();
    createTargets(w, h);
  }

  var dpr = Math.min(1.6, Math.max(1, window.devicePixelRatio || 1));

  /* ---------------- render chain (faithful port) ---------------- */

  function drawFullscreen() {
    gl.bindVertexArray(vao);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }

  var CLEAR = [0, 0, 0, 1];

  function render(t) {
    resize();

    var pointer = updateOrbit();
    var time = t / 1000;

    // pass 1: scene → HDR
    gl.bindFramebuffer(gl.FRAMEBUFFER, scene.fbo);
    gl.viewport(0, 0, scene.w, scene.h);
    gl.clearColor.apply(gl, CLEAR);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(sceneProg);
    gl.uniform2f(sceneLoc.resolution, scene.w, scene.h);
    gl.uniform2f(sceneLoc.pointer, pointer[0], pointer[1]);
    gl.uniform1f(sceneLoc.time, time);
    drawFullscreen();

    // pass 2: bright → bloomA
    gl.bindFramebuffer(gl.FRAMEBUFFER, bloomA.fbo);
    gl.viewport(0, 0, bloomA.w, bloomA.h);
    gl.clearColor.apply(gl, CLEAR);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(brightProg);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, scene.tex);
    gl.uniform1i(brightLoc.src, 0);
    drawFullscreen();

    // passes 3–6: 4 gaussian blurs ping-pong (bloomA <-> bloomB)
    var blurs = [
      { dir: [1, 0], radius: 1 },
      { dir: [0, 1], radius: 1 },
      { dir: [1, 0], radius: 2.4 },
      { dir: [0, 1], radius: 2.4 },
    ];
    gl.useProgram(blurProg);
    for (var i = 0; i < blurs.length; i++) {
      var src = i % 2 === 0 ? bloomA : bloomB;
      var dst = i % 2 === 0 ? bloomB : bloomA;
      gl.bindFramebuffer(gl.FRAMEBUFFER, dst.fbo);
      gl.viewport(0, 0, dst.w, dst.h);
      gl.clearColor.apply(gl, CLEAR);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, src.tex);
      gl.uniform1i(blurLoc.src, 0);
      gl.uniform2f(blurLoc.texelSize, 1 / src.w, 1 / src.h);
      gl.uniform2f(blurLoc.direction, blurs[i].dir[0], blurs[i].dir[1]);
      gl.uniform1f(blurLoc.radius, blurs[i].radius);
      drawFullscreen();
    }

    // pass 7: composite → canvas (bloom ends in bloomA)
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.viewport(0, 0, fbW, fbH);
    gl.clearColor.apply(gl, CLEAR);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(compositeProg);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, scene.tex);
    gl.uniform1i(compositeLoc.scene, 0);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, bloomA.tex);
    gl.uniform1i(compositeLoc.bloom, 1);
    drawFullscreen();

    requestAnimationFrame(render);
  }

  var raf = 0;
  try {
    resize();
    raf = requestAnimationFrame(render);
  } catch (err) {
    console.error('black hole renderer failed:', err);
    // fall back to the Cosmos B timelapse
    gl.getExtension('WEBGL_lose_context') && gl.getExtension('WEBGL_lose_context').loseContext();
    if (canvas.parentElement) canvas.parentElement.removeChild(canvas);
    var fb = document.getElementById('cosmos-fallback');
    if (fb) fb.hidden = false;
  }

  window.addEventListener('resize', function () {
    var nd = Math.min(1.6, Math.max(1, window.devicePixelRatio || 1));
    if (nd !== dpr) {
      dpr = nd;
      fbW = 0;
      fbH = 0;
    }
  });

  window.__blackholeDispose = function () {
    cancelAnimationFrame(raf);
    destroyTargets();
  };
})();
