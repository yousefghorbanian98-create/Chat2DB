'use strict';
/**
 * COSMIC ODYSSEY ambient engine — ported from the reference design document.
 * A dependency-free WebGL scene: 3D star field (twinkling, parallax) plus a
 * full-screen black-hole shader (gravitational lensing, accretion disk, pulsar
 * beams, nebula). All effects are toggleable at runtime.
 */
(function () {
  const Cosmos = {
    opts: { blackhole: true, pulsar: true, nebula: true, starDensity: 3000, intensity: 0.85, mouseX: 0.5, mouseY: 0.5 },
    _gl: null, _canvas: null, _programs: {}, _buffers: {}, _stars: null, _raf: 0, _t0: performance.now(), _running: false
  };

  const STAR_VS = `
    attribute vec3 aPosition;
    attribute float aSize;
    attribute float aBrightness;
    attribute vec3 aColor;
    uniform mat4 uProjection;
    uniform mat4 uView;
    uniform float uTime;
    uniform float uScrollY;
    varying float vBrightness;
    varying vec3 vColor;
    void main() {
      vec3 pos = aPosition;
      pos.z += uScrollY * 0.0005;
      pos.z = mod(pos.z + 2.0, 4.0) - 2.0;
      vec4 mvPos = uView * vec4(pos, 1.0);
      gl_Position = uProjection * mvPos;
      float twinkle = sin(uTime * (1.0 + aBrightness * 3.0) + aBrightness * 100.0) * 0.3 + 0.7;
      gl_PointSize = aSize * twinkle * (300.0 / -mvPos.z);
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

  const BH_FS = `
    precision highp float;
    varying vec2 vUV;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform vec2 uMouse;
    uniform float uScrollY;
    uniform float uBH;
    uniform float uPulsar;
    uniform float uNebula;
    #define PI 3.14159265359
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453123); }
    float noise(vec2 p){
      vec2 i = floor(p); vec2 f = fract(p); f = f*f*(3.0-2.0*f);
      return mix(mix(hash(i), hash(i+vec2(1.0,0.0)), f.x),
                 mix(hash(i+vec2(0.0,1.0)), hash(i+vec2(1.0,1.0)), f.x), f.y);
    }
    float fbm(vec2 p){
      float val=0.0; float amp=0.5;
      for(int i=0;i<5;i++){ val += amp*noise(p); p*=2.0; amp*=0.5; }
      return val;
    }
    void main(){
      vec2 uv = (gl_FragCoord.xy - 0.5*uResolution)/min(uResolution.x, uResolution.y);
      vec2 mouseUV = (uMouse - 0.5) * 2.0;
      mouseUV.x *= uResolution.x/uResolution.y;

      vec2 bhPos = vec2(0.3 + sin(uTime*0.1)*0.05, 0.12 + cos(uTime*0.08)*0.05);
      bhPos.y -= uScrollY*0.0003;
      vec2 toBH = uv - bhPos;
      float dist = length(toBH);
      float angle = atan(toBH.y, toBH.x);

      float schwarzschild = 0.08;
      float lensStrength = schwarzschild/(dist*dist + 0.01);
      vec2 lensed = uv + normalize(toBH)*lensStrength*0.02;

      float diskAngle = angle + uTime*0.5 + lensStrength*2.0;
      float diskWidth = 0.15; float diskCenter = 0.25;
      float disk = smoothstep(diskWidth, 0.0, abs(dist - diskCenter));
      float diskNoise = fbm(vec2(diskAngle*3.0, dist*10.0 - uTime*0.3));
      disk *= diskNoise * 1.5;
      float doppler = sin(diskAngle)*0.5+0.5;
      vec3 diskColor = mix(vec3(0.4,0.1,0.8), vec3(1.0,0.6,0.1), doppler);
      float innerGlow = exp(-dist*8.0)*0.5;
      vec3 innerColor = vec3(0.5,0.2,1.0);
      float eventHorizon = smoothstep(0.06,0.04,dist);

      vec2 pulsarPos = vec2(-0.4, -0.2 + sin(uTime*0.15)*0.1);
      pulsarPos.y -= uScrollY*0.0002;
      vec2 toPulsar = uv - pulsarPos;
      float pulsarDist = length(toPulsar);
      float pulsarAngle = atan(toPulsar.y, toPulsar.x);
      float beamAngle = uTime*3.0;
      float beam1 = pow(max(0.0, cos(pulsarAngle - beamAngle)), 100.0);
      float beam2 = pow(max(0.0, cos(pulsarAngle - beamAngle + PI)), 100.0);
      float beams = (beam1 + beam2) * exp(-pulsarDist*2.0);
      vec3 beamColor = vec3(0.1,0.8,1.0);
      float pulsarCore = exp(-pulsarDist*20.0);
      float pulsarPulse = sin(uTime*10.0)*0.3+0.7;

      vec2 nebulaUV = uv*2.0 + uTime*0.02;
      float nebula = fbm(nebulaUV) * fbm(nebulaUV + 3.0);
      vec3 nebulaMix = mix(vec3(0.1,0.0,0.2), vec3(0.0,0.05,0.15), fbm(nebulaUV*0.5));

      vec3 color = nebulaMix * nebula * 0.3 * uNebula;
      color += diskColor * disk * (1.0-eventHorizon) * 1.5 * uBH;
      color += innerColor * innerGlow * (1.0-eventHorizon) * uBH;
      float photonSphere = smoothstep(0.01,0.0,abs(dist-0.07))*0.8;
      color += vec3(0.8,0.5,1.0)*photonSphere*(1.0-eventHorizon)*uBH;
      color *= (1.0 - eventHorizon*0.98*uBH);
      color += beamColor*beams*0.8*uPulsar;
      color += vec3(0.3,0.9,1.0)*pulsarCore*pulsarPulse*uPulsar;
      float mouseDist = length(uv - mouseUV*0.3);
      color += vec3(0.2,0.1,0.4)*exp(-mouseDist*4.0)*0.15;
      float vignette = 1.0 - dot(uv*0.5, uv*0.5);
      color *= max(0.0, vignette);
      color = color/(color+1.0);
      color = pow(color, vec3(0.85));
      gl_FragColor = vec4(color, 1.0);
    }`;

  function createShader(gl, type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    return s;
  }
  function createProgram(gl, vs, fs) {
    const p = gl.createProgram();
    gl.attachShader(p, createShader(gl, gl.VERTEX_SHADER, vs));
    gl.attachShader(p, createShader(gl, gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p);
    return p;
  }

  function buildStars(gl, count) {
    const pos = new Float32Array(count * 3);
    const size = new Float32Array(count);
    const bright = new Float32Array(count);
    const color = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      pos[i*3] = (Math.random()-0.5)*6;
      pos[i*3+1] = (Math.random()-0.5)*6;
      pos[i*3+2] = (Math.random()-0.5)*4;
      size[i] = Math.random()*3+0.5;
      bright[i] = Math.random();
      const t = Math.random();
      if (t < 0.3) { color[i*3]=0.7+Math.random()*0.3; color[i*3+1]=0.8+Math.random()*0.2; color[i*3+2]=1.0; }
      else if (t < 0.7) { color[i*3]=1.0; color[i*3+1]=0.9+Math.random()*0.1; color[i*3+2]=0.7+Math.random()*0.3; }
      else { color[i*3]=1.0; color[i*3+1]=0.5+Math.random()*0.3; color[i*3+2]=0.3+Math.random()*0.2; }
    }
    return { pos, size, bright, color };
  }

  function makeBuffer(gl, data) {
    const b = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
    return b;
  }

  function perspective(fov, aspect, near, far) {
    const f = 1 / Math.tan(fov/2);
    const nf = 1/(near-far);
    return [f/aspect,0,0,0, 0,f,0,0, 0,0,(far+near)*nf,-1, 0,0,2*far*near*nf,0];
  }
  function lookAt(eye, target, up) {
    let zx=eye[0]-target[0], zy=eye[1]-target[1], zz=eye[2]-target[2];
    let zl = Math.hypot(zx,zy,zz); zx/=zl; zy/=zl; zz/=zl;
    let xx=up[1]*zz-up[2]*zy, xy=up[2]*zx-up[0]*zz, xz=up[0]*zy-up[1]*zx;
    let xl=Math.hypot(xx,xy,xz); xx/=xl; xy/=xl; xz/=xl;
    let yx=zy*xz-zz*xy, yy=zz*xx-zx*xz, yz=zx*xy-zy*xx;
    return [xx,yx,zx,0, xy,yy,zy,0, xz,yz,zz,0,
      -(xx*eye[0]+xy*eye[1]+xz*eye[2]),
      -(yx*eye[0]+yy*eye[1]+yz*eye[2]),
      -(zx*eye[0]+zy*eye[1]+zz*eye[2]),1];
  }

  function mat4mul(a, b) {
    const o = new Array(16);
    for (let c=0;c<4;c++) for (let r=0;r<4;r++) {
      o[c*4+r] = a[r]*b[c*4] + a[4+r]*b[c*4+1] + a[8+r]*b[c*4+2] + a[12+r]*b[c*4+3];
    }
    return o;
  }

  Cosmos.init = function (canvas) {
    this._canvas = canvas;
    const gl = canvas.getContext('webgl', { alpha: false, antialias: false }) || canvas.getContext('experimental-webgl');
    if (!gl) return false;
    this._gl = gl;

    this._programs.star = createProgram(gl, STAR_VS, STAR_FS);
    this._programs.bh = createProgram(gl, QUAD_VS, BH_FS);
    this._buffers.quad = makeBuffer(gl, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]));
    this._stars = buildStars(gl, this.opts.starDensity);
    this._buffers.starPos = makeBuffer(gl, this._stars.pos);
    this._buffers.starSize = makeBuffer(gl, this._stars.size);
    this._buffers.starBright = makeBuffer(gl, this._stars.bright);
    this._buffers.starColor = makeBuffer(gl, this._stars.color);

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    this.resize();
    this._running = true;
    const loop = () => {
      this._raf = requestAnimationFrame(loop);
      this._render();
    };
    loop();
    return true;
  };

  Cosmos.resize = function () {
    const canvas = this._canvas, gl = this._gl;
    if (!gl) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = canvas.clientWidth || window.innerWidth;
    const h = canvas.clientHeight || window.innerHeight;
    canvas.width = Math.floor(w*dpr); canvas.height = Math.floor(h*dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
  };

  Cosmos.setOption = function (key, value) {
    this.opts[key] = value;
    if (key === 'starDensity') this._rebuildStars();
    if (key === 'intensity') {
      const c = this._canvas;
      if (c) c.style.opacity = String(value);
    }
  };

  Cosmos._rebuildStars = function () {
    const gl = this._gl;
    if (!gl) return;
    this._stars = buildStars(gl, Math.max(200, this.opts.starDensity));
    gl.bindBuffer(gl.ARRAY_BUFFER, this._buffers.starPos);
    gl.bufferData(gl.ARRAY_BUFFER, this._stars.pos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, this._buffers.starSize);
    gl.bufferData(gl.ARRAY_BUFFER, this._stars.size, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, this._buffers.starBright);
    gl.bufferData(gl.ARRAY_BUFFER, this._stars.bright, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, this._buffers.starColor);
    gl.bufferData(gl.ARRAY_BUFFER, this._stars.color, gl.STATIC_DRAW);
  };

  function bindAttrib(gl, prog, name, buffer, size) {
    const loc = gl.getAttribLocation(prog, name);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 0, 0);
  }

  Cosmos._render = function () {
    const gl = this._gl;
    if (!gl || !this._running) return;
    const t = (performance.now() - this._t0) / 1000;
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    gl.clearColor(0,0,0,1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // --- black hole fullscreen pass ---
    const bh = this._programs.bh;
    gl.useProgram(bh);
    gl.uniform1f(gl.getUniformLocation(bh,'uTime'), t);
    gl.uniform2f(gl.getUniformLocation(bh,'uResolution'), w, h);
    gl.uniform2f(gl.getUniformLocation(bh,'uMouse'), this.opts.mouseX, this.opts.mouseY);
    gl.uniform1f(gl.getUniformLocation(bh,'uScrollY'), 0);
    gl.uniform1f(gl.getUniformLocation(bh,'uBH'), this.opts.blackhole ? 1.0 : 0.0);
    gl.uniform1f(gl.getUniformLocation(bh,'uPulsar'), this.opts.pulsar ? 1.0 : 0.0);
    gl.uniform1f(gl.getUniformLocation(bh,'uNebula'), this.opts.nebula ? 1.0 : 0.0);
    bindAttrib(gl, bh, 'aPosition', this._buffers.quad, 2);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

    // --- star field ---
    const sp = this._programs.star;
    gl.useProgram(sp);
    const proj = perspective(60*Math.PI/180, w/h, 0.1, 100);
    const view = lookAt([0,0,3], [0,0,0], [0,1,0]);
    const pv = mat4mul(proj, view);
    gl.uniformMatrix4fv(gl.getUniformLocation(sp,'uProjection'), false, proj);
    gl.uniformMatrix4fv(gl.getUniformLocation(sp,'uView'), false, view);
    gl.uniform1f(gl.getUniformLocation(sp,'uTime'), t);
    gl.uniform1f(gl.getUniformLocation(sp,'uScrollY'), 0);
    bindAttrib(gl, sp, 'aPosition', this._buffers.starPos, 3);
    bindAttrib(gl, sp, 'aSize', this._buffers.starSize, 1);
    bindAttrib(gl, sp, 'aBrightness', this._buffers.starBright, 1);
    bindAttrib(gl, sp, 'aColor', this._buffers.starColor, 3);
    gl.drawArrays(gl.POINTS, 0, this.opts.starDensity);
  };

  window.Cosmos = Cosmos;
})();
