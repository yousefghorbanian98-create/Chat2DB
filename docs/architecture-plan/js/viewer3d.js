/* ============================================================
   نمای سه‌بعدی — Three.js r128: پیلوت + ۴ طبقه مسکونی + بام
   ============================================================ */
let renderer, scene3, camera3, controls3, groups={};

function init3D(){
  const box=document.getElementById("view3d");
  const W=box.clientWidth, H=box.clientHeight;
  scene3=new THREE.Scene();
  scene3.background=new THREE.Color(0xdfe9f2);
  scene3.fog=new THREE.Fog(0xdfe9f2, 100, 260);
  camera3=new THREE.PerspectiveCamera(46, W/H, 0.1, 500);
  camera3.position.set(30, 26, 40);
  renderer=new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
  renderer.setSize(W,H);
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.shadowMap.enabled=true;
  renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  box.appendChild(renderer.domElement);
  controls3=new THREE.OrbitControls(camera3, renderer.domElement);
  controls3.enableDamping=true; controls3.dampingFactor=0.08;
  controls3.target.set(14, 4, -10);
  const hemi=new THREE.HemisphereLight(0xffffff, 0x8899aa, 0.75); scene3.add(hemi);
  const sun=new THREE.DirectionalLight(0xfff2dd, 1.05);
  sun.position.set(40, 50, -28); sun.castShadow=true;
  sun.shadow.mapSize.set(2048,2048);
  const d=50; Object.assign(sun.shadow.camera,{left:-d,right:d,top:d,bottom:-d,far:160});
  scene3.add(sun);
  buildSite3D(); buildPilotis(); buildFloors(); buildRoof();
  applyVisibility();
  const ax=new THREE.AxesHelper(4); ax.position.set(-3,0.02,3); scene3.add(ax);
  animate3D();
  window.addEventListener("resize",()=>{
    camera3.aspect=box.clientWidth/box.clientHeight; camera3.updateProjectionMatrix();
    renderer.setSize(box.clientWidth,box.clientHeight);
  });
}
function mat(c,o){ return new THREE.MeshLambertMaterial({color:c, transparent:!!o, opacity:o==null?1:o}); }
function addBox(g,w,h,d,x,y,z,m){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), m||mat(0xe8e2d6));
  mesh.position.set(x,y,z); mesh.castShadow=true; mesh.receiveShadow=true; g.add(mesh); return mesh;
}
function buildSite3D(){
  const g=new THREE.Group(); groups.site=g;
  const pc=scaledParcel(), pts=pc.pts;
  const shape=new THREE.Shape(pts.map(p=>new THREE.Vector2(p[0],-p[1])));
  const ground=new THREE.Mesh(new THREE.ShapeGeometry(shape), mat(0xb8c9a3));
  ground.rotation.x=-Math.PI/2; ground.position.y=-0.06; ground.receiveShadow=true; g.add(ground);
  const st=new THREE.Mesh(new THREE.PlaneGeometry(8,26), mat(0x9aa2ab));
  st.rotation.x=-Math.PI/2; st.position.set(pc.pts[2][0]+4.2, -0.04, -12); g.add(st);
  scene3.add(g);
}
/* ---------- پیلوت ---------- */
function buildPilotis(){
  const B=PLAN.building, P=PLAN.pilotis;
  const g=new THREE.Group(); groups.pilotis=g;
  const ox=B.ox, oz=-B.oy; // y شمال → -z
  const L=B.plateL, W=B.plateW, FH=B.pilotisH;
  addBox(g, L+0.5, 0.15, W+0.5, ox+L/2, 0.075, oz+W/2, mat(0xc9c2b6)); // کف پیلوت
  /* ستون‌ها ۴۰×۴۰ */
  const colXs=[0.45,4.8,6.9,9.45,12.85,15.4,18.15], colYs=[0.45,6.0,11.55];
  for(const cx of colXs) for(const cy of colYs){
    if(cx>6.6&&cx<9.9) continue; /* هسته پله/آسانسور */
    addBox(g,0.4,FH,0.4, ox+cx, FH/2, oz-cy, mat(0xbfb8ac));
  }
  /* مغازه‌ها: دیوار + ویترین شرقی */
  const shopW=mat(0xe3dccb);
  for(const r of P.rooms) if(r.shop){
    const w=r.x1-r.x0, d=r.y1-r.y0, cx=ox+(r.x0+r.x1)/2, cz=oz-(r.y0+r.y1)/2;
    const h=2.7, y0=h/2+0.15;
    addBox(g,w,h,0.15, cx, y0, oz-r.y0-0.075, shopW);
    addBox(g,w,h,0.15, cx, y0, oz-r.y1+0.075, shopW);
    addBox(g,0.15,h,d, ox+r.x0+0.075, y0, cz, shopW);
    addBox(g,0.12,h,d, ox+r.x1-0.06, y0, cz, mat(0x7fb4d8,0.8)); /* ویترین */
    addBox(g,w+0.2,0.18,d+0.2, cx, 0.24+h, cz, mat(0xb0a89c)); /* سرستون */
  }
  /* هسته مشاعات */
  const core=mat(0xf0d9b8);
  addBox(g,0.15,FH,11.65, ox+7.0-0.075, FH/2, oz-5.9125, core);
  addBox(g,2.85,FH,0.15, ox+8.2625, FH/2, oz-11.75, core);
  addBox(g,0.15,FH,2.25, ox+9.45, FH/2, oz-1.3, mat(0xbfb8ac)); /* دیوار شرقی هسته (با در) */
  /* تابلوی مغازه‌ها */
  addLabel(ox+15.6, 3.35, oz-6.0, "۳ مغازه — رو به معبر ۲۴ متری");
  addLabel(ox+3.4, 3.35, oz-3.0, "پیلوت: پارکینگ ۴ خودرو");
  scene3.add(g);
}
/* ---------- ۴ طبقه مسکونی ---------- */
function buildFloors(){
  const B=PLAN.building, T=PLAN.typical;
  const ox=B.ox, oz=-B.oy-B.towerOy;
  const L=B.towerL, W=B.towerW, FH=B.floorH;
  const walls=buildWalls(T.rooms, [
    {x0:0,y0:0,x1:L,y1:0,t:B.wallExt},{x0:0,y0:W,x1:L,y1:W,t:B.wallExt},
    {x0:0,y0:0,x1:0,y1:W,t:B.wallExt},{x0:L,y0:0,x1:L,y1:W,t:B.wallExt}
  ]);
  const wallM=mat(0xe8e2d6), glass=mat(0x7fb4d8,0.85);
  for(let i=0;i<B.nRes;i++){
    const g=new THREE.Group(); groups["f"+i]=g;
    const y0=B.pilotisH + i*FH;
    addBox(g, L+0.5, 0.22, W+0.5, ox+L/2, y0-0.11, oz+W/2, mat(0xc9c2b6)); /* دال */
    const h=FH-0.28;
    addBox(g,L+0.35,h,0.35, ox+L/2, y0+0.15+h/2, oz+0.175, wallM);
    addBox(g,L+0.35,h,0.35, ox+L/2, y0+0.15+h/2, oz+W+0.175, wallM);
    addBox(g,0.35,h,W+0.35, ox+0.175, y0+0.15+h/2, oz+W/2, wallM);
    addBox(g,0.35,h,W+0.35, ox+L+0.175, y0+0.15+h/2, oz+W/2, wallM);
    for(const w of walls){
      if(w.ext) continue;
      const t=Math.max(w.t,0.1), hh=FH-0.3;
      const coreC = (Math.abs(w.x1-w.x0)<1e-9 && w.x0>6.6 && w.x0<7.2) || (Math.abs(w.y1-w.y0)<1e-9 && w.y0>2.3 && w.y0<6.0);
      const mm = coreC?mat(0xf0d9b8):mat(0xdcd6cb);
      if(Math.abs(w.x1-w.x0)<1e-9) addBox(g,t,hh,w.y1-w.y0, ox+w.x0, y0+0.15+hh/2, oz+w.y0+ (w.y1-w.y0)/2 - 0, mm);
      else addBox(g,w.x1-w.x0,hh,t, ox+(w.x0+w.x1)/2, y0+0.15+hh/2, oz+w.y0, mm);
    }
    for(const r of T.rooms) for(const win of (r.win||[])){
      if(win.door) continue;
      const yC=y0+0.95+win.h/2;
      if(win.s==="S") addBox(g,win.b-win.a,win.h,0.1, ox+(win.a+win.b)/2, yC, oz+0.2, glass);
      if(win.s==="N") addBox(g,win.b-win.a,win.h,0.1, ox+(win.a+win.b)/2, yC, oz+W+0.2, glass);
      if(win.s==="E") addBox(g,0.1,win.h,win.b-win.a, ox+L+0.2, yC, oz+(win.a+win.b)/2, glass);
      if(win.s==="W") addBox(g,0.1,win.h,win.b-win.a, ox-0.2, yC, oz+(win.a+win.b)/2, glass);
    }
    /* در ورودی واحد از لابی (شرقی) */
    addBox(g,0.1,2.1,0.9, ox+6.925, y0+1.2, oz-4.75, mat(0x6b4f35));
    /* بالکن جنوبی */
    addBox(g,3.0,0.16,1.0, ox+2.7, y0+0.08, oz-0.5, mat(0xbfb8ac));
    addBox(g,3.0,0.9,0.06, ox+2.7, y0+0.6, oz-0.97, mat(0x99a3ad,0.6));
    scene3.add(g);
  }
  addLabel(ox+L+4.2, B.pilotisH+FH*2+1, oz+W/2, "۴ طبقه مسکونی — هر طبقه ۱ واحد ۲ خوابه (۷۰ m²)");
}
/* ---------- بام ---------- */
function buildRoof(){
  const B=PLAN.building;
  const g=new THREE.Group(); groups.roof=g;
  const ox=B.ox, oz=-B.oy-B.towerOy;
  const L=B.towerL, W=B.towerW, yTop=B.pilotisH+B.nRes*B.floorH;
  addBox(g,L+0.5,0.24,W+0.5, ox+L/2, yTop+0.12, oz+W/2, mat(0xb5aea2));
  const pp=0.85;
  addBox(g,L+0.5,pp,0.2, ox+L/2, yTop+0.24+pp/2, oz+0.1, mat(0xd8d2c6));
  addBox(g,L+0.5,pp,0.2, ox+L/2, yTop+0.24+pp/2, oz+W+0.1, mat(0xd8d2c6));
  addBox(g,0.2,pp,W+0.5, ox+0.1, yTop+0.24+pp/2, oz+W/2, mat(0xd8d2c6));
  addBox(g,0.2,pp,W+0.5, ox+L+0.1, yTop+0.24+pp/2, oz+W/2, mat(0xd8d2c6));
  addBox(g,2.85,1.7,5.65, ox+8.2625, yTop+0.24+0.85, oz-8.75, mat(0xc2bbb0)); /* باکس پله */
  scene3.add(g);
}
function addLabel(x,y,z,str){
  const cv=document.createElement("canvas"); cv.width=512; cv.height=96;
  const c=cv.getContext("2d");
  c.fillStyle="rgba(30,40,55,0.82)"; c.fillRect(0,0,512,96);
  c.fillStyle="#fff"; c.font="bold 34px Vazirmatn, Tahoma"; c.textAlign="center"; c.textBaseline="middle";
  c.fillText(str,256,50);
  const tex=new THREE.CanvasTexture(cv);
  const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tex}));
  sp.scale.set(10.5,1.95,1); sp.position.set(x,y,z); scene3.add(sp);
}
function applyVisibility(){
  groups.pilotis.visible=document.getElementById("f-pilotis").checked;
  for(let i=0;i<PLAN.building.nRes;i++) groups["f"+i].visible=document.getElementById("f-floors").checked;
  groups.roof.visible=document.getElementById("f-roof").checked;
}
function animate3D(){ requestAnimationFrame(animate3D); controls3.update(); renderer.render(scene3,camera3); }
function resetView(){ camera3.position.set(30,26,40); controls3.target.set(14,4,-10); }
function topView(){ camera3.position.set(14,58,-9.8); controls3.target.set(14,0,-9.8); }
function exportGLB(){
  const exp=new THREE.GLTFExporter();
  const out=new THREE.Group();
  ["site","pilotis","f0","f1","f2","f3","roof"].forEach(k=>{ if(groups[k]) out.add(groups[k].clone()); });
  exp.parse(out, res=>{
    const blob=new Blob([res],{type:"model/gltf-binary"});
    const a=document.createElement("a"); a.href=URL.createObjectURL(blob);
    a.download="residential-commercial-4floors.glb"; a.click();
  }, {binary:true});
}
