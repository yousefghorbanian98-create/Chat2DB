/* ============================================================
   main.js — ناوبری، گزارش انطباق (نسخه ۲: پیلوت + ۴ طبقه)
   ============================================================ */
const $=id=>document.getElementById(id);
const TABS=["site","pilotis","typical","v3d","report"];

function renderTab(key){
  TABS.forEach(t=>$("tab-"+t).classList.toggle("active",t===key));
  document.querySelectorAll(".view").forEach(v=>v.classList.remove("show"));
  $("view-"+key).classList.add("show");
  if(key==="v3d" && !window._v3dInit){ window._v3dInit=true; setTimeout(()=>init3D(),50); }
}
function downloadSVG(id,name){
  const svg=document.querySelector("#"+id+" svg"); if(!svg)return;
  const s=new XMLSerializer().serializeToString(svg);
  const blob=new Blob(['<?xml version="1.0" encoding="UTF-8"?>\n'+s],{type:"image/svg+xml"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=name; a.click();
}
/* ---- محاسبات مالی/مساحتی طرح ---- */
function compute(){
  const B=PLAN.building;
  const pc=scaledParcel(), area=pc.area;
  const plate=B.plateL*B.plateW, tower=B.towerL*B.towerW;
  const shops=PLAN.pilotis.rooms.filter(r=>r.shop).reduce((s,r)=>s+(r.x1-r.x0)*(r.y1-r.y0),0);
  const coreP=PLAN.pilotis.rooms.filter(r=>!r.parking&&!r.aisle&&!r.shop).reduce((s,r)=>s+(r.x1-r.x0)*(r.y1-r.y0),0);
  const floors=B.nRes*tower;
  const balc=PLAN.typical.balconies.reduce((s,b)=>s+(b.x1-b.x0)*(b.y1-b.y0),0)*B.nRes*0.5;
  const usedNoBalc=floors+shops+coreP, used=usedNoBalc+balc;
  const unit=PLAN.typical.rooms.filter(r=>r.id.startsWith("U-")).reduce((s,r)=>s+(r.x1-r.x0)*(r.y1-r.y0),0);
  return {area, plate, tower, shops, coreP, floors, balc, usedNoBalc, used, unit,
          occ:plate/area*100, open:(area-plate)/area*100, margin:PLAN.meta.allowedArea-used};
}
function renderReport(){
  const c=compute();
  const ok='<span class="ok">✔ منطبق</span>', note='<span class="warn">◐ با تایید مهندس</span>';
  const rows=[
    ["عرصه (پلی‌گون کاداستر مقیاس‌شده)","۶۰۰٫۰۰ m²","هدف ≈ ۶۰۰",ok],
    ["سطح اشغال (پلیت پیلوت ۱۸٫۶×۱۲)","۲۲۳٫۲۰ m² — ۳۷٫۲٪","حداکثر ۶۰٪",ok],
    ["فضای باز","۳۷۶٫۸۰ m² — ۶۲٫۸٪","حداقل ۲۰٪",ok],
    ["۴ طبقه مسکونی × ۱۱۱٫۵۵","۴۴۶٫۲۰ m²","—","—"],
    ["مغازه‌ها: ۳ × ۱۸٫۵۴","۵۵٫۶۱ m²","فضای بسته پیلوت",ok],
    ["مشاعات بسته پیلوت (پله/آسانسور/لابی/شفت)","۲۷٫۷۳ m²","≤ ۳۰٪ مساحت پیلوت = ۶۷ m²",ok],
    ["بالکن‌ها ۴×۳٫۰۰ (با ضریب ۵۰٪)","۶٫۰۰ m²","واحد < ۱۰۰ m² اصفهان: ≥ ۳ m²",ok],
    ["<b>تراکم مصرفی (بدون فضای باز پیلوت)</b>","<b>۵۳۵٫۵۴ m²</b>","مجاز دستور نقشه: ۵۴۲٫۳۸",ok+" حاشیه ۶٫۸۴"],
    ["سناریوی خوش‌بینانه (پیلوت باز معاف؛ فقط مغازه‌ها)","۵۲۹٫۵۴ m²","—",ok],
    ["تعداد واحدها","۴ مسکونی (هر طبقه ۱ واحد ۲خوابه) + ۳ تجاری","درخواست کارفرما",ok],
    ["مساحت مفید هر واحد","۷۰٫۳ m² + بالکن ۳٫۰","—","—"],
    ["عرض مفید راه‌پله","۲٫۵۲۵ m (دو بازو ۲×۱٫۲)","حداقل ۱٫۱۰ (مبحث ۳)",ok],
    ["کف‌پا/کف پله","۱۷٫۶ / ۲۹ cm — ۱۷ عدد در هر طبقه","≤۱۸ / ≥۲۸",ok],
    ["باکس آسانسور","۱٫۶۵×۲٫۰۰ m","حداقل ۱٫۶۰×۲٫۰۰",ok],
    ["لابی طبقات","۲٫۵۲۵×۳٫۲ = ۸٫۱ m²","حداقل ۱٫۵×۱٫۵",ok],
    ["پارکینگ","۴ قطعه سرپوشیده در پیلوت","۴ واحد مسکونی",ok+" (+۳ تجاری: ◐ کنترل شود)"],
    ["عرض مسیر مانور پیلوت","۴٫۱۵ m","حداقل ۳٫۰",ok],
    ["ارتفاع مفید پیلوت","۲٫۶۰ m","پارکینگ ≥ ۲٫۲۰",ok],
    ["بالکن هر واحد","۳٫۰۰ m² جنوبی","≥ ۳٫۰ برای واحد < ۱۰۰ m²",ok],
    ["نورگیری اتاق‌ها","همه اتاق‌ها نور طبیعی S/N/E/W","مبحث ۴: شیشه ≥ ۱/۸ کف",ok],
    ["ارتفاع کل از تراز کوچه","۱۵٫۸۰ m (۵ تراز × ۳ + جان‌پناه)","ضوابط ارتفاع منطقه ۱ — ◐ کنترل",note],
    ["عقب‌نشینی‌ها","جنوب ۴٫۲ | شمال ۳٫۱۷ | غرب ۵٫۴ | شرق ۶٫۰–۹٫۲","طبق تفصیلی — ◐ کنترل",note],
    ["سازه","ستون‌های ۴۰×۴۰ پیلوت + دیوار برشی هسته","طراحی سازه توسط مهندس محاسب",note]
  ];
  const srcs=[
    ["ضوابط شهرداری در طراحی معماری (اشغال ۶۰٪، پیلوت، ارتفاع، پارکینگ)","https://doctorjavaz.com/ضوابط-شهرداری-در-طراحی-معماری/"],
    ["ضوابط مشرفیت و زیربنا — اصفهان (پیلوت ≤۳۰٪، زیرزمین خارج از زیربنا)","https://mojavezisfahan.ir/building-overlooking/"],
    ["ضوابط بالکن اصفهان (واحد < ۱۰۰ م: ≥ ۳ m²)","https://www.markazeahan.com/definition-construction-balconies-building/"],
    ["ضوابط پله و آسانسور — مبحث سوم بند ۳-۱-۴-۴-۴","https://planyab.com/ضوابط-طراحی-پله-و-آسانسور/"],
    ["الزامات عمومی فضاها — مبحث چهارم (شیشه ۱/۸ کف)","https://omranpooya.com/construction/procedure/general-requirements/gr-5"],
    ["ضوابط پارکینگ (۲٫۵×۵، رامپ ۱۵٪، ارتفاع ۲٫۲)","https://ahanjam.com/parking-regulations/"],
    ["ابعاد و شیب رامپ و ارتفاع پارکینگ","https://tka-eng.com/parking-ordinary/"]
  ];
  $("report-body").innerHTML=`
   <h3>خلاصه طرح (نسخه ۲ — پیلوت + ۴ طبقه + ۳ مغازه)</h3>
   <p>طبق درخواست کارفرما: ساختمان <b>۴ طبقه مسکونی روی پیلوت</b> طراحی شد و در همکف (پیلوت) <b>۳ مغازه</b> + پارکینگ سرپوشیده ۴ خودرو + هسته پله/آسانسور جانمایی شد. پیلوت در ضلع جنوب و شرق کاملاً باز است؛ مغازه‌ها رو به معبر اصلی ۲۴ متری (شرق) و ورودی پیاده ساکنین از کوی شمالی است — تفکیک کامل تردد تجاری/مسکونی/سواره.</p>
   <h3>جدول انطباق با ضوابط</h3>
   <table class="chk"><thead><tr><th>موضوع</th><th>طراحی</th><th>ضابطه</th><th>وضعیت</th></tr></thead>
   <tbody>${rows.map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join("")}</tbody></table>
   <h3>جدول فضاهای هر ردیف</h3>
   <table class="chk"><thead><tr><th>تراز</th><th>فضاها</th><th>مساحت</th></tr></thead><tbody>
   <tr><td>پیلوت (همکف)</td><td>۳ مغازه (هر یک ۴٫۹×۳٫۹) + پارکینگ ۴ خودرو + پله/آسانسور/لابی + مانور</td><td>اشغال ۲۲۳٫۲۰ (بسته: ۸۵٫۱)</td></tr>
   <tr><td>اول تا چهارم × ۴</td><td>نشیمن ۲۵٫۵ + آشپزخانه ۷٫۷ + مستر ۹٫۵ + خواب۲ ۸٫۹ + سرویس ۶٫۷ + ورودی ۵٫۰ + راهرو ۷٫۰ + پله/آسانسور/لابی</td><td>۱۱۱٫۵۵ هر طبقه (مفید واحد ۷۰٫۳)</td></tr>
   <tr><td>بام</td><td>باکس پله + جان‌پناه ۸۵ cm</td><td>—</td></tr>
   </tbody></table>
   <h3>مبانی و فرضیات (نیازمند کنترل مهندس ناظر)</h3>
   <ol class="assume">
    <li><b>چرا برج کوچک‌تر شد؟</b> مجاز ساخت ۵۴۲٫۳۸ m² ثابت است؛ با ۵ تراز مسکونی + تجاری، فوتریت هر طبقه باید کاهش می‌یافت (۵ تراز × اشغال قبلی ۲۷۰ = ۱۳۵۰ ≫ ۵۴۲). طرح فعلی حداکثر استفاده از تراکم را با حفظ استاندارد واحدها می‌کند.</li>
    <li><b>محاسبه محافظه‌کارانه تراکم:</b> فضای بسته پیلوت (مغازه‌ها + هسته) نیز لحاظ شد؛ فقط گذر/مانور باز پیلوت معاف فرض شد. اگر شهرداری مغازه‌ها را خارج از تراکم مسکونی محاسبه کند، حاشیه بیشتری خواهد بود.</li>
    <li><b>پارکینگ تجاری:</b> ضوابط کاربری تجاری ممکن است به ازای هر مغازه پارکینگ جدا بخواهد؛ کنترل نهایی با کمیسیون ماده ۵. حیاط شرقی برای پارک مهمان قابل استفاده است.</li>
    <li><b>ابعاد زمین:</b> از چاپ کاداستر خوانده و به ۶۰۰ m² مقیاس شد؛ قبل از اجرا توسط نقشه‌بردار کنترل و در <code>js/data.js → parcel.basePts</code> جایگزین شود.</li>
    <li>نقشه سازه، تاسیسات، برق و جزئیات اجرایی توسط مهندسان مربوطه تکمیل شود؛ این بسته پیش‌طرح فاز ۲ است.</li>
   </ol>
   <h3>منابع ضوابط (اوپن‌سورس)</h3>
   <ul class="srcs">${srcs.map(s=>`<li><a target="_blank" href="${s[1]}">${s[0]}</a></li>`).join("")}</ul>
   <h3>ابزار اوپن‌سورس استفاده‌شده</h3>
   <p>Three.js (نمای ۳بعدی + خروجی GLB) — ezdxf (خروجی DXF اتوکد) — matplotlib (رندر PNG) — SVG خالص. بدون نرم‌افزار تجاری.</p>`;
}
window.addEventListener("DOMContentLoaded",()=>{
  $("view-site").innerHTML=siteSVG();
  $("view-pilotis").innerHTML=floorSVG("pilotis");
  $("view-typical").innerHTML=floorSVG("typical");
  renderReport();
  TABS.forEach(t=>{const b=$("btn-"+t); if(b)b.onclick=()=>renderTab(t);});
  ["f-pilotis","f-floors","f-roof"].forEach(id=>$(id).addEventListener("change",applyVisibility));
  $("btn-reset").onclick=resetView; $("btn-top").onclick=topView; $("btn-glb").onclick=exportGLB;
  ["site","pilotis","typical"].forEach(k=>{
    const b=$("dl-"+k); if(b) b.onclick=()=>downloadSVG("view-"+k,"plan-"+k+".svg");
  });
  $("btn-print").onclick=()=>window.print();
});
