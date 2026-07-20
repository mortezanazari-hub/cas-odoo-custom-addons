(() => {
"use strict";
const D=window.CAS_DATA;
const main=document.getElementById("main"),nav=document.getElementById("nav"),breadcrumb=document.getElementById("breadcrumb");
let route=localStorage.getItem("cas.route")||"home";
let activeConversation=1;
const settings=Object.assign({font:"standard",density:"comfortable",theme:"light",accent:"#1769aa",sidebar:"open"},JSON.parse(localStorage.getItem("cas.settings")||"{}"));

function esc(v){return String(v??"").replace(/[&<>'"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]))}
function applySettings(){
  const scales={compact:.9,standard:1,large:1.14};
  document.documentElement.style.setProperty("--font-scale",scales[settings.font]||1);
  document.documentElement.style.setProperty("--density",settings.density==="compact"?.86:1);
  document.documentElement.style.setProperty("--accent",settings.accent);
  document.body.classList.toggle("theme-dark",settings.theme==="dark");
  document.body.classList.toggle("sidebar-collapsed",settings.sidebar==="collapsed");
  localStorage.setItem("cas.settings",JSON.stringify(settings));
}
function renderNav(){
  const groups=[...new Set(D.routes.map(x=>x.group))];
  nav.innerHTML=groups.map(g=>`<div class="nav-group"><div class="nav-title">${g}</div>${D.routes.filter(x=>x.group===g&&x.id!=="settings").map(x=>`<button class="nav-item ${route===x.id?"active":""}" data-route="${x.id}" title="${x.label}"><span class="nav-icon">${x.icon}</span><span class="nav-text">${x.label}</span>${x.count?`<span class="nav-count">${x.count}</span>`:""}</button>`).join("")}</div>`).join("");
}
function header(title,sub,kicker="فضای کار سازمانی CAS",actions=""){return `<div class="page-header"><div><div class="page-kicker">${kicker}</div><h1 class="page-title">${title}</h1><p class="page-subtitle">${sub}</p></div><div>${actions}</div></div>`}
function card(title,body,sub=""){return `<section class="card"><div class="card-header"><div><h3 class="card-title">${title}</h3>${sub?`<div class="card-subtitle">${sub}</div>`:""}</div></div><div class="card-body">${body}</div></section>`}
function badge(text,tone=""){return `<span class="badge ${tone?`badge-${tone}`:""}">${text}</span>`}
function taskRows(limit=99){return D.tasks.slice(0,limit).map(t=>`<div class="task-row ${t.high?"high":""}"><button class="task-check"></button><div class="task-main"><strong>${t.title}</strong><small>${t.meta} • ${t.source}</small></div></div>`).join("")}
function actionRows(limit=99){return D.actions.slice(0,limit).map(a=>`<div class="action-row"><div class="action-main"><strong>${a.title}</strong><small>${a.subject}</small></div>${badge(a.deadline,a.tone)}<button class="btn">بررسی</button></div>`).join("")}
function convPreview(c){return `<div class="conversation-preview" data-open-conversation="${c.id}"><div class="person-avatar">${c.avatar}</div><div class="conv-meta"><strong>${c.name}</strong><p>${c.last}</p></div><span class="conv-time">${c.time}</span>${c.unread?`<span class="unread-dot">${c.unread}</span>`:""}</div>`}

function home(){
 return `<div class="page">
 <section class="briefing"><div><h1>صبح بخیر مهدی</h1><p>اولین جلسه شما ساعت ۱۰:۳۰ است. سه مورد به تصمیم شما نیاز دارد.</p></div><div class="briefing-points"><span class="briefing-point">۲ کار عقب‌افتاده</span><span class="briefing-point">۴ گفت‌وگوی خوانده‌نشده</span><span class="briefing-point">۱ گزارش نهایی‌نشده</span></div></section>
 <div class="grid grid-3">
   <section class="card span-2"><div class="card-header"><div><h3 class="card-title">اولویت‌های امروز</h3><div class="card-subtitle">کاری که بهتر است از اینجا شروع شود</div></div><button class="btn" data-route="tasks">همه کارها</button></div><div class="card-body">${taskRows(4)}</div></section>
   ${card("جلسه بعدی",`<strong style="font-size:var(--fs-lg)">جلسه هماهنگی عملیات</strong><p style="color:var(--muted)">امروز، ۱۰:۳۰ تا ۱۱:۳۰<br>اتاق جلسات مدیریت</p><button class="btn btn-primary" data-route="calendar">مشاهده در تقویم</button>`)}
 </div>
 <div class="grid grid-3" style="margin-top:16px">
   <section class="card quick-conversations"><div class="card-header"><div><h3 class="card-title">گفت‌وگوهای اخیر</h3><div class="card-subtitle">دسترسی سریع؛ بدون ترک میزکار</div></div><button class="btn btn-ghost" data-route="conversations">مشاهده همه</button></div><div class="card-body">${D.conversations.slice(0,3).map(convPreview).join("")}</div></section>
   ${card("نیازمند اقدام",actionRows(3),"مرتب‌شده بر اساس فوریت")}
   ${card("وضعیت امروز",`<div class="record-row"><div><strong>حضور</strong><p>ثبت ورود ساعت ۰۷:۴۸</p></div>${badge("عادی","success")}</div><div class="record-row"><div><strong>گزارش فعالیت</strong><p>سه فعالیت ثبت‌شده</p></div>${badge("پیش‌نویس","warning")}</div><div class="record-row"><div><strong>درخواست‌ها</strong><p>دو درخواست در جریان</p></div>${badge("در حال بررسی")}</div>`)}
 </div></div>`;
}
function tasks(){return `<div class="page">${header("کارهای من","فهرست ساده کارهای شخصی، تفویض‌شده و ناشی از گردش‌کار.","مدیریت روز کاری",`<button class="btn btn-primary">+ کار جدید</button>`)}${card("امروز",taskRows())}</div>`}
function conversations(){
 const c=D.conversations.find(x=>x.id===activeConversation)||D.conversations[0];
 const msgs=D.messages[c.id]||[{me:false,name:c.name,time:c.time,text:c.last}];
 return `<div class="page">${header("گفت‌وگوها","ارتباط سریع و سبک با همکاران و گروه‌های سازمانی؛ جزئیات فقط هنگام نیاز نمایش داده می‌شود.","ارتباط سازمانی",`<button class="btn">+ گفت‌وگوی جدید</button>`)}
 <div class="chat-layout">
  <aside class="chat-list"><div class="chat-list-head"><input class="search" placeholder="جست‌وجو در گفت‌وگوها..."></div><div class="chat-list-body">${D.conversations.map(x=>`<button class="chat-item ${x.id===c.id?"active":""}" data-conversation="${x.id}"><div class="person-avatar">${x.avatar}</div><div class="conv-meta"><strong>${x.name}</strong><p>${x.last}</p></div>${x.unread?`<span class="unread-dot">${x.unread}</span>`:""}</button>`).join("")}</div></aside>
  <section class="chat-pane"><header class="chat-head"><div class="chat-title"><div class="person-avatar">${c.avatar}</div><div><strong>${c.name}</strong><small>${c.kind}${c.online?" • آنلاین":""}</small></div></div><button class="icon-button" data-action="conversation-info" title="اطلاعات گفتگو">⋯</button></header>
  <div class="chat-messages">${msgs.map(m=>`<div class="message ${m.me?"me":""}"><div class="bubble"><p>${m.text}</p><time>${m.time}</time></div></div>`).join("")}</div>
  <form class="composer" id="composer"><button type="button" class="icon-button">＋</button><input name="message" placeholder="پیام خود را بنویسید..."><button class="btn btn-primary">ارسال</button></form></section>
 </div></div>`;
}
function calendar(){
 const days=["شنبه","یکشنبه","دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه"];
 return `<div class="page">${header("تقویم","برنامه روز، هفته و ماه؛ ساختار نسخه ۶ حفظ شده و خوانایی اصلاح شده.","برنامه‌ریزی",`<button class="btn btn-primary">+ رویداد جدید</button>`)}
 <div class="calendar-toolbar"><div class="segmented"><button>روز</button><button class="active">هفته</button><button>ماه</button></div><div><button class="btn">امروز</button> <button class="btn">‹</button> <button class="btn">›</button></div></div>
 <section class="card calendar-card"><div class="card-body"><div class="week-grid"><div class="head">ساعت</div>${days.map(d=>`<div class="head">${d}</div>`).join("")}${[8,9,10,11,12,13,14,15,16].map((h,ri)=>`<div>${h}:۰۰</div>${days.map((d,di)=>`<div>${(ri===2&&di===0)?'<div class="event">جلسه هماهنگی عملیات</div>':(ri===5&&di===2)?'<div class="event">بررسی مغایرت حضور</div>':""}</div>`).join("")}`).join("")}</div></div></section></div>`;
}
function actions(){return `<div class="page">${header("نیازمند اقدام","مواردی که واقعاً منتظر تصمیم یا انجام کار شما هستند.","CAS Action Center")}${card("صف اقدام‌ها",actionRows())}</div>`}
function generic(id){
 const meta={notifications:["مرکز اعلان‌ها","اطلاع‌رسانی‌های سیستمی و سازمانی"],history:["تاریخچه اخیر","دسترسی سریع به رکوردهای اخیر"],requests:["درخواست‌ها","ثبت و پیگیری درخواست‌های سازمانی"],activity:["گزارش فعالیت","ثبت کارهای واقعاً انجام‌شده"],attendance:["حضور و شیفت","وضعیت حضور، شیفت و کارکرد"],correspondence:["مکاتبات","نامه‌ها، ارجاع‌ها و مهلت‌های پاسخ"]}[id]||["صفحه",""];
 return `<div class="page">${header(meta[0],meta[1])}${card("نمای کلی",`<div class="record-row"><div><strong>نمونه رکورد فعال</strong><p>این بخش در نسخه ۷ از ساختار نسخه ۶ پیروی می‌کند و مقیاس خوانایی جدید روی آن اعمال شده است.</p></div><button class="btn">باز کردن</button></div><div class="record-row"><div><strong>رکورد دوم</strong><p>اطلاعات نمونه برای ارزیابی UX و سلسله‌مراتب بصری.</p></div>${badge("در جریان","warning")}</div>`)}</div>`;
}
function settingsPage(){
 return `<div class="page">${header("تنظیمات محیط","ظاهر و خوانایی فضای کار را متناسب با نیاز خود تنظیم کنید.","شخصی‌سازی")}
 <div class="settings-grid"><aside class="card settings-nav"><button class="active">ظاهر و خوانایی</button><button>چیدمان میزکار</button><button>اعلان‌ها</button><button>حریم خصوصی</button></aside>
 <section class="card setting-section">
  <div class="setting-row"><div><strong>اندازه متن</strong><small>هیچ متن کاربردی در CAS کمتر از ۱۲ پیکسل نیست.</small></div><div class="choice-group">${[["compact","فشرده"],["standard","استاندارد"],["large","بزرگ"]].map(x=>`<button class="choice ${settings.font===x[0]?"active":""}" data-setting="font" data-value="${x[0]}">${x[1]}</button>`).join("")}</div></div>
  <div class="setting-row"><div><strong>تراکم رابط</strong><small>فاصله سطرها، کارت‌ها و کنترل‌ها</small></div><div class="choice-group">${[["compact","فشرده"],["comfortable","راحت"]].map(x=>`<button class="choice ${settings.density===x[0]?"active":""}" data-setting="density" data-value="${x[0]}">${x[1]}</button>`).join("")}</div></div>
  <div class="setting-row"><div><strong>نمایش</strong><small>حالت روشن یا تاریک</small></div><div class="choice-group">${[["light","روشن"],["dark","تاریک"]].map(x=>`<button class="choice ${settings.theme===x[0]?"active":""}" data-setting="theme" data-value="${x[0]}">${x[1]}</button>`).join("")}</div></div>
  <div class="setting-row"><div><strong>رنگ اصلی</strong><small>رنگ کنترل‌شده رابط؛ برند سازمانی حفظ می‌شود.</small></div><div class="choice-group">${["#1769aa","#0b8f7b","#6b46c1","#b45309"].map(c=>`<button class="color-choice" data-setting="accent" data-value="${c}" style="background:${c}" title="${c}"></button>`).join("")}</div></div>
  <div class="setting-row"><div><strong>وضعیت منوی کناری</strong><small>انتخاب شما برای ورود بعدی حفظ می‌شود.</small></div><div class="choice-group">${[["open","باز"],["collapsed","جمع‌شده"]].map(x=>`<button class="choice ${settings.sidebar===x[0]?"active":""}" data-setting="sidebar" data-value="${x[0]}">${x[1]}</button>`).join("")}</div></div>
 </section></div></div>`;
}
function render(){
 const meta=D.routes.find(x=>x.id===route); breadcrumb.textContent=`فضای کار ‹ ${meta?.label||""}`; document.title=`${meta?.label||"CAS"} | CAS v7`;
 renderNav();
 const pages={home,tasks,conversations,calendar,actions,settings:settingsPage};
 main.innerHTML=(pages[route]||(()=>generic(route)))();
}
function go(r){route=r;localStorage.setItem("cas.route",r);render();main.scrollTop=0}
function openQuickChat(){
 document.getElementById("drawerRoot").innerHTML=`<div class="drawer-backdrop" data-action="close-drawer"><aside class="drawer" onclick="event.stopPropagation()"><div class="drawer-head"><div><strong style="font-size:var(--fs-lg)">گفت‌وگوهای اخیر</strong><div class="card-subtitle">چهار پیام خوانده‌نشده</div></div><button class="drawer-close" data-action="close-drawer">×</button></div>${D.conversations.map(convPreview).join("")}<button class="btn btn-primary" style="width:100%;margin-top:14px" data-route="conversations">مشاهده همه گفت‌وگوها</button></aside></div>`;
}
document.addEventListener("click",e=>{
 const r=e.target.closest("[data-route]")?.dataset.route;if(r){go(r);document.getElementById("drawerRoot").innerHTML="";return}
 const a=e.target.closest("[data-action]")?.dataset.action;
 if(a==="toggle-sidebar"){settings.sidebar=settings.sidebar==="collapsed"?"open":"collapsed";applySettings()}
 if(a==="mobile-menu")document.getElementById("sidebar").classList.add("open");
 if(a==="quick-chat")openQuickChat();
 if(a==="close-drawer")document.getElementById("drawerRoot").innerHTML="";
 if(a==="conversation-info")document.getElementById("drawerRoot").innerHTML=`<div class="drawer-backdrop" data-action="close-drawer"><aside class="drawer" onclick="event.stopPropagation()"><div class="drawer-head"><strong>اطلاعات گفت‌وگو</strong><button class="drawer-close" data-action="close-drawer">×</button></div><p>اعضا، فایل‌ها و ارتباط با رکوردهای سازمانی فقط هنگام نیاز در این Drawer نمایش داده می‌شوند.</p></aside></div>`;
 const cid=e.target.closest("[data-conversation]")?.dataset.conversation||e.target.closest("[data-open-conversation]")?.dataset.openConversation;
 if(cid){activeConversation=Number(cid);go("conversations");document.getElementById("drawerRoot").innerHTML=""}
 const setting=e.target.closest("[data-setting]");
 if(setting){settings[setting.dataset.setting]=setting.dataset.value;applySettings();render()}
});
document.addEventListener("submit",e=>{if(e.target.id==="composer"){e.preventDefault();const input=e.target.message;if(input.value.trim()){(D.messages[activeConversation] ||= []).push({me:true,name:"من",time:"اکنون",text:input.value.trim()});input.value="";render()}}});
window.addEventListener("keydown",e=>{if(e.key==="Escape")document.getElementById("drawerRoot").innerHTML=""});
applySettings();render();
})();