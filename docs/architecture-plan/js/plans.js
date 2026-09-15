/* ============================================================
   رندر SVG نقشه‌های ۲بعدی — سایت، پیلوت، طبقه تیپ (نسخه ۲)
   ============================================================ */
const S = 40; // پیکسل بر متر
function polygonArea(pts){let a=0;for(let i=0;i<pts.length;i++){const[p,q]=[pts[i],pts[(i+1)%pts.length]];a+=p[0]*q[1]-q[0]*p[1];}return Math.abs(a/2);}
function scaledParcel(){
  const P=PLAN.parcel, a0=polygonArea(P.basePts), s=Math.sqrt(P.targetArea/a0);
  return { pts:P.basePts.map(p=>[p[0]*s,p[1]*s]), scale:s, area:a0*s*s };
}
function faArea(a){ return a.toLocaleString("fa-IR",{minimumFractionDigits:1,maximumFractionDigits:1}); }
function line(x1,y1,x2,y2,cls,extra=""){return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}" ${extra}/>`;}
function rect(x,y,w,h,cls,extra=""){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}" ${extra}/>`;}
function text(x,y,str,cls="",extra=""){return `<text x="${x}" y="${y}" class="${cls}" ${extra}>${str}</text>`;}

/* دیوارها از اتاق‌ها */
function buildWalls(rooms, outer){
  const walls=[];
  for(const o of (outer||[])) walls.push({...o, ext:true});
  const tol=0.02;
  for(let i=0;i<rooms.length;i++)for(let j=i+1;j<rooms.length;j++){
    const a=rooms[i],b=rooms[j];
    const ov0=Math.max(a.y0,b.y0), ov1=Math.min(a.y1,b.y1);
    if(ov1-ov0>0.3){
      const gx=[[a.x1,b.x0],[b.x1,a.x0]].find(([r,l])=>Math.abs(r-l)<=0.46+tol);
      if(gx)walls.push({x0:(gx[0]+gx[1])/2,y0:ov0,x1:(gx[0]+gx[1])/2,y1:ov1,t:Math.max(Math.abs(gx[1]-gx[0]),0.1)});
    }
    const ox0=Math.max(a.x0,b.x0), ox1=Math.min(a.x1,b.x1);
    if(ox1-ox0>0.3){
      const gy=[[a.y1,b.y0],[b.y1,a.y0]].find(([r,l])=>Math.abs(r-l)<=0.46+tol);
      if(gy)walls.push({x0:ox0,y0:(gy[0]+gy[1])/2,x1:ox1,y1:(gy[0]+gy[1])/2,t:Math.max(Math.abs(gy[1]-gy[0]),0.1)});
    }
  }
  return walls;
}

/* ---------- پلان پیلوت / طبقه تیپ ---------- */
function floorSVG(kind){
  const B=PLAN.building;
  const isP = kind==="pilotis";
  const rooms = isP ? PLAN.pilotis.rooms : PLAN.typical.rooms;
  const doors = isP ? PLAN.pilotis.doors : PLAN.typical.doors;
  const oxL = 0, oyL = isP ? 0 : B.towerOy;         // مبدأ محلی
  const W = isP ? B.plateL : B.towerL;
  const H = isP ? B.plateW : B.towerW;
  const outer = [
    {x0:0,y0:0,x1:W,y1:0,t:B.wallExt},{x0:0,y0:H,x1:W,y1:H,t:B.wallExt},
    {x0:0,y0:0,x1:0,y1:H,t:B.wallExt},{x0:W,y0:0,x1:W,y1:H,t:B.wallExt}
  ];
  const Wpx=(W+7)*S, Hpx=(H+8)*S;
  const X=x=>(3.0+x)*S, Y=y=>(2.6+H-y)*S;
  let out="";
  out+=rect(X(0),Y(H),W*S,H*S,"floor");
  for(const r of rooms){
    if(r.aisle){ out+=rect(X(r.x0),Y(r.y1),(r.x1-r.x0)*S,(r.y1-r.y0)*S,"roomAisle"); continue; }
    const cls = r.shop?"room shop":r.parking?"room park":r.stair||r.lift?"room core":"room";
    out+=rect(X(r.x0),Y(r.y1),(r.x1-r.x0)*S,(r.y1-r.y0)*S,cls);
  }
  const walls=buildWalls(rooms, outer);
  for(const w of walls){
    const th=w.t*S;
    if(Math.abs(w.x1-w.x0)<1e-9) out+=rect(X(w.x0)-th/2,Y(Math.max(w.y0,w.y1)),th,Math.abs(w.y1-w.y0)*S,w.ext?"wext":"wint");
    else out+=rect(X(Math.min(w.x0,w.x1)),Y(w.y0)-th/2,Math.abs(w.x1-w.x0)*S,th,w.ext?"wext":"wint");
  }
  /* پنجره‌ها (طبقات مسکونی) */
  if(!isP) for(const r of rooms) for(const win of (r.win||[])){
    if(win.door) continue;
    if(win.s==="S") out+=rect(X(win.a),Y(0)-2.5,(win.b-win.a)*S,5,"win");
    if(win.s==="N") out+=rect(X(win.a),Y(H)-2.5,(win.b-win.a)*S,5,"win");
    if(win.s==="E") out+=rect(X(W)-2.5,Y(win.b),(win.b-win.a)*S,5,"win");
    if(win.s==="W") out+=rect(X(0)-2.5,Y(win.b),(win.b-win.a)*S,5,"win");
  }
  /* ویترین مغازه‌ها */
  if(isP) for(const r of rooms) if(r.shop){
    out+=rect(X(W)-2.5,Y(r.y1)+6,5,(r.y1-r.y0)*S-12,"win");
  }
  /* درها */
  for(const d of doors){
    const len=Math.hypot(d.x2-d.x1,d.y2-d.y1);
    const vert=Math.abs(d.x2-d.x1)<1e-9;
    if(d.t==="open"){ out+=line(X(d.x1),Y(d.y1),X(d.x2),Y(d.y2),"dopen"); continue; }
    if(vert) out+=rect(X(d.x1)-2.5,Y(Math.max(d.y1,d.y2)),5,len*S,"bg");
    else out+=rect(X(Math.min(d.x1,d.x2)),Y(d.y1)-2.5,len*S,5,"bg");
    const t=d.t==="entry"?"dentry":d.t==="lift"?"dlift":"dleaf";
    const mx=(d.x1+d.x2)/2, my=(d.y1+d.y2)/2;
    if(d.t==="entry"&&!vert){ /* در ورودی روی دیوار افقی */
      out+=line(X(d.x1),Y(d.y1),X(d.x1),Y(d.y1)-len*S,t);
      out+=`<path d="M ${X(d.x1)} ${Y(d.y1)-len*S} A ${len*S} ${len*S} 0 0 1 ${X(d.x2)} ${Y(d.y1)}" class="darc"/>`;
      continue;
    }
    if(vert){
      const top=Math.max(d.y1,d.y2);
      out+=line(X(d.x1),Y(top),X(d.x1)+len*S,Y(top),t);
      out+=`<path d="M ${X(d.x1)+len*S} ${Y(top)} A ${len*S} ${len*S} 0 0 1 ${X(d.x1)} ${Y(top-len*S)}" class="darc"/>`;
    } else {
      const l=Math.min(d.x1,d.x2);
      out+=line(X(l),Y(d.y1),X(l),Y(d.y1)-len*S,t);
      out+=`<path d="M ${X(l)} ${Y(d.y1)-len*S} A ${len*S} ${len*S} 0 0 1 ${X(l)+len*S} ${Y(d.y1)}" class="darc"/>`;
    }
  }
  /* بازشوهای لبه جنوبی پیلوت */
  if(isP) for(const o of PLAN.pilotis.openings){
    out+=rect(X(o.x0),Y(0)-2.5,(o.x1-o.x0)*S,5,"dopen");
    out+=text(X((o.x0+o.x1)/2),Y(0)+14,"ورود خودرو","lbl-small");
  }
  /* پله */
  for(const r of rooms) if(r.stair){
    for(let i=0;i<=10;i++){ const yy=Y(r.y0+0.2)+i*(r.y1-r.y0-0.4)*S/10; out+=line(X(r.x0)+2,yy,X(r.x1)-2,yy,"step"); }
    const midX=(X(r.x0)+X(r.x1))/2;
    out+=line(midX,Y(r.y1-0.5),midX,Y(r.y0+0.5),"sarrow","marker-end='url(#arrw)'");
    out+=text(midX,Y((r.y0+r.y1)/2)-6,isP?"بالا":"بالا/پایین","lbl-small");
  }
  /* آسانسور */
  for(const r of rooms) if(r.lift){
    out+=line(X(r.x0)+2,Y(r.y1)-2,X(r.x1)-2,Y(r.y0)+2,"lx");
    out+=line(X(r.x0)+2,Y(r.y0)+2,X(r.x1)-2,Y(r.y1)-2,"lx");
  }
  /* خودروها */
  if(isP) for(const r of rooms) if(r.parking){
    const cx=X((r.x0+r.x1)/2), cy=Y((r.y0+r.y1)/2);
    const horiz=(r.y1-r.y0)<(r.x1-r.x0);
    out+=rect(cx-(horiz?38:20),cy-(horiz?20:38),horiz?76:40,horiz?40:76,"car",`rx="7"`);
    out+=text(cx,cy+3,r.id.replace("P",""),"lbl-small");
  }
  /* برچسب اتاق‌ها */
  for(const r of rooms){
    const w=r.x1-r.x0,h=r.y1-r.y0,a=w*h;
    const cx=X((r.x0+r.x1)/2), cy=Y((r.y0+r.y1)/2);
    if(r.aisle){ out+=text(cx,cy,r.fa,"lbl-gray"); continue; }
    if(r.parking||r.stair||r.lift){ out+=text(cx,cy,r.fa,"lbl-small"); continue; }
    out+=text(cx,cy-6,r.fa,"lbl");
    out+=text(cx,cy+9,`${w.toFixed(2)}×${h.toFixed(2)} — ${faArea(a)} m²`,"lbl-2");
  }
  /* بالکن */
  if(!isP) for(const b of PLAN.typical.balconies){
    const bx0=b.x0, by0=b.y0+oyL, bx1=b.x1, by1=b.y1+oyL;
    out+=rect(X(bx0),Y(by1),(bx1-bx0)*S,(by1-by0)*S,"balc");
    out+=text(X((bx0+bx1)/2),Y((by0+by1)/2)+4,b.fa,"lbl-small");
  }
  /* اندازه‌گذاری */
  if(isP){
    out+=dimChainH(X(0),X(9.7*S),Y(-1.8),"۹٫۷۰ (برج)"); out+=dimChainH(X(9.7*S),X(18.6*S),Y(-1.8),"۸٫۹۰");
    out+=dimChainH(X(0),X(18.6*S),Y(-2.8),"۱۸٫۶۰");
    out+=dimChainV(Y(0),Y(12*S),X(-1.5),"۱۲٫۰۰");
  } else {
    out+=dimChainH(X(0),X(3.4*S),Y(-1.8),"۳٫۴۰"); out+=dimChainH(X(3.4*S),X(6.85*S),Y(-1.8),"۳٫۴۵"); out+=dimChainH(X(6.85*S),X(9.7*S),Y(-1.8),"۲٫۸۵");
    out+=dimChainH(X(0),X(9.7*S),Y(-2.8),"۹٫۷۰");
    out+=dimChainV(Y(0),Y(11.5*S),X(-1.5),"۱۱٫۵۰");
  }
  out+=northArrow(Wpx-70,80);
  out+=scaleBar(3.0*S,Hpx-30);
  out+=titleBlock(kind);
  return `<svg viewBox="0 0 ${Wpx} ${Hpx}" class="sheet" xmlns="http://www.w3.org/2000/svg">
    <defs><marker id="arrw" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,8 L4,0 L8,8" fill="none" stroke="#333" stroke-width="1.4"/></marker></defs>
    <rect class="frame" x="6" y="6" width="${Wpx-12}" height="${Hpx-12}"/>${out}</svg>`;
}

function dimChainH(xa,xb,y,label){return line(xa,y,xb,y,"dim")+line(xa,y-6,xa,y+6,"dim")+line(xb,y-6,xb,y+6,"dim")+text((xa+xb)/2,y-7,label,"dimtxt");}
function dimChainV(ya,yb,x,label){return line(x,ya,x,yb,"dim")+line(x-6,ya,x+6,ya,"dim")+line(x-6,yb,x+6,yb,"dim")+text(x+4,(ya+yb)/2,label,"dimtxt");}
function northArrow(x,y){return `<g transform="translate(${x},${y})"><circle r="26" class="ncirc"/><path d="M0,-20 L7,10 L0,4 L-7,10 Z" class="narr"/><text y="22" text-anchor="middle" class="ntxt">N</text></g>`;}
function scaleBar(x,y){
  let s=`<g transform="translate(${x},${y})">`;
  for(let i=0;i<5;i++) s+=rect(i*S/2,0,S/2,7,i%2?"sb1":"sb2");
  s+=text(0,-5,"0","sbtxt")+text(S,-5,"۱م","sbtxt")+text(2*S,-5,"۲م","sbtxt")+text(S*1.5,20,"مقیاس ۱:۱۰۰","sbtxt")+`</g>`;
  return s;
}
function titleBlock(kind){
  const names={pilotis:"پلان پیلوت (همکف) — ۳ مغازه + پارکینگ ۴ خودرو",typical:"پلان تیپ طبقات ۱ تا ۴ — واحد ۲ خوابه ۷۰ m²",site:"پلان سایت و جانمایی"};
  const Wpx=(PLAN.building.plateL+7)*S, Hpx=(PLAN.building.plateW+8)*S;
  const tbW=440,tbH=92,x=Wpx-tbW-18,y=Hpx-tbH-16;
  const lv={pilotis:"پیلوت باز — جزو مشاعات (فضای بسته: ۸۵ m²)",typical:"۴ طبقه × ۱۱۱٫۵۵ m² = ۴۴۶٫۲۰ m²",site:"اشغال ۳۷٫۲٪ — فضای باز ۶۲٫۸٪"}[kind];
  return `<g transform="translate(${x},${y})">
    <rect class="tb" width="${tbW}" height="${tbH}"/>
    <text x="${tbW-12}" y="24" text-anchor="end" class="tb1">${PLAN.meta.project} — ${names[kind]}</text>
    <text x="${tbW-12}" y="44" text-anchor="end" class="tb2">کد املاک: ${PLAN.meta.ownerCode} — ${PLAN.meta.city}</text>
    <text x="${tbW-12}" y="62" text-anchor="end" class="tb2">${lv}</text>
    <text x="${tbW-12}" y="80" text-anchor="end" class="tb2">تاریخ: ${PLAN.meta.dateFa} — ${PLAN.meta.designer}</text>
  </g>`;
}

/* ---------- سایت ---------- */
function siteSVG(){
  const pc=scaledParcel(), pts=pc.pts;
  const minX=Math.min(...pts.map(p=>p[0])), maxX=Math.max(...pts.map(p=>p[0]));
  const minY=Math.min(...pts.map(p=>p[1])), maxY=Math.max(...pts.map(p=>p[1]));
  const B=PLAN.building, Wpx=(maxX-minX+12)*S, Hpx=(maxY-minY+12)*S;
  const ox=(3.5-minX)*S, oy=(3.5+maxY)*S;
  const X=x=>ox+x*S, Y=y=>oy-y*S;
  let out="";
  out+=rect(X(maxX),Y(maxY),5*S,(maxY-minY)*S,"street");
  out+=rect(X(minX),Y(minY)-4*S,(maxX-minX)*S,4*S,"street");
  out+=rect(X(minX),Y(maxY),(maxX-minX)*S,4*S,"street");
  out+=text(X(maxX)+2.2*S,Y((minY+maxY)/2),"معبر اصلی ۲۴ متری","streetlbl");
  out+=text(X((minX+maxX)/2),Y(minY)-2*S,"کوی ۸ متری جنوبی — ورود خودرو به پارکینگ","streetlbl");
  out+=text(X((minX+maxX)/2),Y(maxY)+2.6*S,"کوی ۸ متری شمالی — ورودی پیاده ساکنین","streetlbl");
  out+=`<defs><pattern id="ph" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="9" class="hatchP"/></pattern></defs>`;
  out+=`<polygon points="${pts.map(p=>X(p[0])+","+Y(p[1])).join(" ")}" class="parcel"/>`;
  out+=`<polygon points="${pts.map(p=>X(p[0])+","+Y(p[1])).join(" ")}" fill="url(#ph)" opacity="0.55"/>`;
  for(let i=0;i<pts.length;i++){
    const p=pts[i],q=pts[(i+1)%pts.length];
    const mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2;
    const dx=q[0]-p[0],dy=q[1]-p[1],L2=Math.hypot(dx,dy);
    out+=text(X(mx+dy/L2*1.1),Y(my-dx/L2*1.1),L2.toFixed(2),"dimtxt-bold");
  }
  /* پلیت پیلوت + برج */
  out+=rect(X(B.ox),Y(B.oy+B.plateW),B.plateL*S,B.plateW*S,"pilotis");
  out+=rect(X(B.ox),Y(B.oy+B.towerOy+B.towerW),B.towerL*S,B.towerW*S,"bldg");
  out+=text(X(B.ox+B.plateL/2),Y(B.oy+B.plateW)-8,"پیلوت ۱۸٫۶۰×۱۲٫۰۰ — ۲۲۳٫۲۰ m² (۳۷٫۲٪)","lbl-bold");
  out+=text(X(B.ox+B.towerL/2),Y(B.oy+B.towerOy+B.towerW/2),"برج مسکونی","lbl-bold");
  out+=text(X(B.ox+B.towerL/2),Y(B.oy+B.towerOy+B.towerW/2)+16,"۹٫۷۰×۱۱٫۵۰","lbl-2");
  out+=text(X(B.ox+B.plateL-2.8),Y(B.oy+2),"۳ مغازه","lbl-small");
  out+=text(X(B.ox+B.plateL-2.8),Y(B.oy+10.6),"۳ مغازه","lbl-small");
  /* حریم */
  const sbN=3.17, sbS=4.2, sbW=5.4, sbE=6.0;
  out+=rect(X(B.ox-sbW),Y(B.oy+B.plateW+sbN),(B.plateL+sbW+sbE)*S,(B.plateW+sbN+sbS)*S,"setback");
  out+=text(X(B.ox+B.plateL+2.6),Y(B.oy+6.5),"حیاط شرقی","lbl-gray");
  out+=text(X(B.ox+B.plateL+2.6),Y(B.oy+7.6),"(ویترین مغازه‌ها)","lbl-small");
  out+=text(X(B.ox+B.towerL/2),Y(B.oy-0.8),"ورود خودرو ↓","lbl-small");
  out+=text(X(B.ox+11.3),Y(B.oy+B.plateW+1.2),"ورود پیاده ↑","lbl-small");
  const tw=360,tx=X(minX)+8,ty=Y(minY)-352;
  out+=`<g transform="translate(${tx},${ty})"><rect class="tb" width="${tw}" height="138"/>
   <text x="${tw-10}" y="20" text-anchor="end" class="tb1">خلاصه مساحت‌ها</text>
   <text x="${tw-10}" y="41" text-anchor="end" class="tb2">عرصه: ${faArea(pc.area)} m² — اشغال: ۲۲۳٫۲۰ (۳۷٫۲٪ ≤ ۶۰٪)</text>
   <text x="${tw-10}" y="61" text-anchor="end" class="tb2">۴ طبقه مسکونی × ۱۱۱٫۵۵ = ۴۴۶٫۲۰ m²</text>
   <text x="${tw-10}" y="81" text-anchor="end" class="tb2">مغازه‌ها ۵۵٫۶ + مشاعات پیلوت ۲۷٫۷ + بالکن ۶٫۰</text>
   <text x="${tw-10}" y="101" text-anchor="end" class="tb2">تراکم مصرفی: ۵۳۵٫۵ از ۵۴۲٫۳۸ m² (حاشیه ۶٫۹)</text>
   <text x="${tw-10}" y="121" text-anchor="end" class="tb2">۴ واحد مسکونی + ۳ واحد تجاری + ۴ پارکینگ</text></g>`;
  out+=northArrow(Wpx-70,90);
  out+=titleBlock("site");
  return `<svg viewBox="0 0 ${Wpx} ${Hpx}" class="sheet" xmlns="http://www.w3.org/2000/svg">${out}</svg>`;
}
