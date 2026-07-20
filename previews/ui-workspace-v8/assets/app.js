(() => {
  "use strict";
  const D = window.CAS_DATA;
  const app = document.getElementById("mainContent");
  const sidebar = document.getElementById("sidebar");
  const sidebarContent = document.getElementById("sidebarContent");
  const roleSelect = document.getElementById("roleSelect");
  const breadcrumb = document.getElementById("breadcrumb");
  const drawerRoot = document.getElementById("drawerRoot");
  const modalRoot = document.getElementById("modalRoot");
  const toastRoot = document.getElementById("toastRoot");
  const bootParams = new URLSearchParams(location.search);
  const v7Defaults = {
    fontScale: "standard",
    density: "comfortable",
    accent: "blue",
    theme: "light",
    sidebarCollapsed: false,
    widgetOrder: ["tasks","calendar","actions","conversations","activity","day-progress","notices"]
  };
  let v7Settings = Object.assign({}, v7Defaults, JSON.parse(localStorage.getItem("cas.v7.settings") || "{}"));

  function applyV7Settings(){
    const scales={compact:"0.94",standard:"1",large:"1.12"};
    const densities={compact:"0.90",comfortable:"1"};
    const accents={
      blue:{base:"#1769aa",strong:"#0b5f9c",soft:"#e8f3fb",sidebar1:"#102a43",sidebar2:"#163b58"},
      teal:{base:"#0b8f7b",strong:"#087466",soft:"#e5f7f3",sidebar1:"#103d3a",sidebar2:"#15564f"},
      purple:{base:"#6b46c1",strong:"#55359f",soft:"#f3edff",sidebar1:"#2c2344",sidebar2:"#45346a"},
      amber:{base:"#b86a08",strong:"#945405",soft:"#fff4df",sidebar1:"#473016",sidebar2:"#65451e"}
    };
    const palette=accents[v7Settings.accent]||accents.blue;
    document.documentElement.style.setProperty("--v7-font-scale",scales[v7Settings.fontScale]||"1");
    document.documentElement.style.setProperty("--v7-density",densities[v7Settings.density]||"1");
    document.documentElement.style.setProperty("--v7-accent",palette.base);
    document.documentElement.style.setProperty("--v7-accent-strong",palette.strong);
    document.documentElement.style.setProperty("--v7-accent-soft",palette.soft);
    document.documentElement.style.setProperty("--blue",palette.base);
    document.documentElement.style.setProperty("--blue-strong",palette.strong);
    document.documentElement.style.setProperty("--blue-soft",palette.soft);
    document.documentElement.style.setProperty("--sidebar-tone-1",palette.sidebar1);
    document.documentElement.style.setProperty("--sidebar-tone-2",palette.sidebar2);
    document.body.classList.toggle("theme-dark",v7Settings.theme==="dark");
    document.body.classList.toggle("sidebar-collapsed",Boolean(v7Settings.sidebarCollapsed));
    const toggle=document.getElementById("sidebarToggle");
    if(toggle){
      toggle.textContent=v7Settings.sidebarCollapsed?"›":"‹";
      toggle.title=v7Settings.sidebarCollapsed?"بازکردن منوی کناری":"جمع‌کردن منوی کناری";
    }
    localStorage.setItem("cas.v7.settings",JSON.stringify(v7Settings));
  }

  let currentUserId = bootParams.get("cas_user") || localStorage.getItem("cas.user") || "employee_demo";
  if (!D.users[currentUserId]) currentUserId = "employee_demo";
  const primaryRoleOf = userId => {
    const priorities=["system_admin","ceo","manager","supervisor","guard","secretariat","shift_planner","form_designer","workflow_designer","document_manager","employee"];
    const user=D.users[userId]; return priorities.find(r=>user.securityRoles.includes(r)) || "employee";
  };
  const landingOf = userId => {
    const role=primaryRoleOf(userId);
    return ({guard:"guard-workspace",system_admin:"admin-center",supervisor:"supervisor-dashboard",manager:"manager-dashboard",ceo:"executive-dashboard",secretariat:"secretariat-register"})[role] || "home";
  };
  let currentRole = primaryRoleOf(currentUserId);
  let currentRoute = "home";
  let selectedPerson = D.people[0];
  let guardLogs = [...D.attendanceLogs];
  let workActivities = [
    {title:"بررسی و پاسخ به مکاتبات عملیات",category:"مکاتبات",duration:45,note:"پاسخ اولیه به دو نامه داخلی",standard:true},
    {title:"تحلیل مغایرت حضور شیفت شب",category:"حضور و کاردکس",duration:70,note:"بررسی رکوردهای دستگاه و برنامه شیفت",standard:true},
    {title:"جلسه هماهنگی عملیات",category:"جلسه",duration:60,note:"هماهنگی برنامه امروز با سرپرست",standard:true}
  ];
  let personalTasks = [
    {title:"مرور درخواست خرید شماره ۴۵۱",meta:"امروز، ۱۰:۰۰",source:"تفویض‌شده",priority:"high",done:false},
    {title:"ارسال جمع‌بندی جلسه عملیات",meta:"امروز، ۱۳:۳۰",source:"شخصی",priority:"normal",done:false},
    {title:"پیگیری اصلاح گزارش شیفت شب",meta:"عقب‌افتاده از دیروز",source:"پیگیری",priority:"high",done:false},
    {title:"هماهنگی بازدید واحد تولید",meta:"فردا، ۰۹:۰۰",source:"تقویم",priority:"normal",done:false}
  ];
  let taskView = "today";
  const systemTaskCategories = ["تفویض‌شده","جلسه","اداری"];
  let personalTaskCategories = JSON.parse(localStorage.getItem("cas.personalTaskCategories") || '["شخصی","پیگیری"]');
  let activeTaskCategory = "";
  let replyingTo = null;
  const pinnedMessages = new Set();
  const pinnedConversations = new Set();
  let calendarView = "week";
  let homeCalendarView = localStorage.getItem("cas.home.calendarView") || "day";
  let homeCalendarMonthOffset = Number(localStorage.getItem("cas.home.calendarMonthOffset") || 0);
  let selectedConversation = 0;
  const eventParticipants = new Map();
  const calendarEvents = [
    {day:0,start:9,end:10,title:"مرور درخواست خرید ۴۵۱",type:"task",owner:"مهدی رضایی",location:"فضای شخصی"},
    {day:0,start:11,end:12,title:"جلسه هماهنگی عملیات",type:"meeting",owner:"تیم عملیات",location:"اتاق جلسات مدیریت"},
    {day:0,start:14.5,end:15.25,title:"مرور گزارش‌های شیفت",type:"report",owner:"رضا اسدی",location:"آنلاین"},
    {day:1,start:8.5,end:9.5,title:"بازدید واحد تولید",type:"meeting",owner:"تیم تولید",location:"سایت تولید"},
    {day:2,start:13,end:14,title:"بررسی مغایرت حضور",type:"task",owner:"منابع انسانی",location:"دفتر اداری"},
    {day:3,start:10,end:11.5,title:"جلسه کمیته بهره‌وری",type:"meeting",owner:"مدیران واحدها",location:"سالن کنفرانس"},
    {day:4,start:15,end:16,title:"پاسخ به مکاتبات باز",type:"correspondence",owner:"دبیرخانه",location:"فضای شخصی"}
  ];
  const conversations = [
    {name:"تیم عملیات",kind:"کانال واحد",avatar:"تو",unread:3,preview:"صورتجلسه امروز در همین گفتگو قرار گرفت.",time:"۰۹:۳۴",members:"۱۲ عضو"},
    {name:"مریم فلاحی",kind:"گفت‌وگوی مستقیم",avatar:"مف",unread:1,preview:"نامه تأمین قطعات برای بررسی شما ارجاع شد.",time:"۰۹:۱۰",members:"آنلاین"},
    {name:"هماهنگی مدیران",kind:"کانال سازمانی",avatar:"هم",unread:2,preview:"جلسه فردا به ساعت ۱۰ منتقل شد.",time:"دیروز",members:"۸ عضو"},
    {name:"رضا اسدی",kind:"گفت‌وگوی مستقیم",avatar:"را",unread:0,preview:"گزارش شیفت شب تکمیل شد.",time:"دیروز",members:"آخرین حضور ۰۸:۴۲"},
    {name:"فناوری اطلاعات",kind:"کانال خدمات",avatar:"IT",unread:0,preview:"تیکت دستگاه حضور در حال پیگیری است.",time:"شنبه",members:"۵ عضو"}
  ];

  const esc = value => String(value ?? "").replace(/[&<>'"]/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[ch]));
  const num = n => new Intl.NumberFormat("fa-IR").format(n);
  const toneClass = tone => ({red:"badge-red",orange:"badge-orange",green:"badge-green",purple:"badge-purple",blue:"badge-blue"}[tone] || "");
  const badge = (text, tone="") => `<span class="badge ${toneClass(tone)}">${esc(text)}</span>`;
  const initials = name => name.split(/\s+/).map(x=>x[0]).slice(0,2).join("");
  const routeMeta = route => D.routes[route] || {label:route,icon:"•"};

  function effectiveCapabilities(userId=currentUserId){
    const user=D.users[userId];
    if(!user) return new Set();
    return new Set(user.securityRoles.flatMap(role=>D.roleCapabilities[role]||[]));
  }

  function allowed(route, userId=currentUserId){
    const meta = D.routes[route];
    const user = D.users[userId];
    if(!meta) return true;
    if(!user) return false;
    if(meta.permissions?.length){
      const caps=effectiveCapabilities(userId);
      return meta.permissions.some(permission=>caps.has(permission));
    }
    if(!meta.roles) return true;
    return user.securityRoles.some(role=>meta.roles.includes(role));
  }

  function pageHeader(title, subtitle, kicker="فضای کار سازمانی CAS", actions=""){
    return `<div class="page-header">
      <div><div class="page-kicker">${esc(kicker)}</div><h1 class="page-title">${esc(title)}</h1><p class="page-subtitle">${esc(subtitle)}</p></div>
      <div class="page-actions">${actions}</div>
    </div>`;
  }

  function stat(icon,value,label,trend="",tone=""){
    return `<div class="card stat-card"><div class="stat-icon">${icon}</div><div><strong>${value}</strong><span>${label}</span></div>${trend?`<em class="stat-trend ${tone}">${trend}</em>`:""}</div>`;
  }

  function renderRoleOptions(){
    roleSelect.innerHTML = Object.entries(D.users).map(([id,u])=>`<option value="${id}" ${id===currentUserId?"selected":""}>${u.name} — ${u.job}</option>`).join("");
    const user=D.users[currentUserId];
    document.getElementById("profileName").textContent = user.name;
    document.getElementById("profileRole").textContent = `${user.job} • ${user.unit}`;
    const avatar = document.querySelector(".profile-chip .avatar");
    avatar.textContent = initials(user.name);
  }

  function renderSidebar(){
    const html = D.navGroups.map(group => {
      const items = group.items.filter(i=>allowed(i.route));
      if(!items.length) return "";
      return `<section class="nav-group"><div class="nav-group-title">${group.title}</div>${items.map(i=>`<button class="nav-item ${i.route===currentRoute?"active":""}" data-route="${i.route}"><span class="nav-icon">${i.icon}</span><span class="nav-label">${i.label}</span>${i.count?`<span class="nav-count">${num(i.count)}</span>`:""}</button>`).join("")}</section>`;
    }).join("");
    sidebarContent.innerHTML = html;
  }

  function setBreadcrumb(){
    const meta = routeMeta(currentRoute);
    breadcrumb.innerHTML = `<span>فضای کار</span><span>‹</span><strong>${esc(meta.label)}</strong>`;
    document.title = `${meta.label} | CAS`;
  }

  function getInitialRoute(){
    const params = new URLSearchParams(location.search);
    const route = params.get("cas_route") || localStorage.getItem("cas.route") || landingOf(currentUserId);
    return allowed(route) ? route : landingOf(currentUserId);
  }

  function navigate(route, push=true){
    if(!allowed(route)){
      toast("این صفحه برای نقش انتخاب‌شده در دسترس نیست.","warn");
      route = landingOf(currentUserId);
    }
    currentRoute = route;
    localStorage.setItem("cas.route",route);
    if(push){
      const u = new URL(location.href); u.searchParams.set("cas_route",route); history.pushState({route},"",u);
    }
    renderSidebar(); setBreadcrumb(); renderRoute();
    app.scrollTop = 0; app.focus({preventScroll:true});
    sidebar.classList.remove("open");
  }

  function card(title,body,subtitle="",footer="",extra=""){
    return `<section class="card ${extra}"><div class="card-header"><div><h3 class="card-title">${title}</h3>${subtitle?`<div class="card-subtitle">${subtitle}</div>`:""}</div></div><div class="card-body">${body}</div>${footer?`<div class="card-footer">${footer}</div>`:""}</section>`;
  }

  function actionRows(limit=D.actions.length){
    return `<div class="task-list">${D.actions.slice(0,limit).map((a,i)=>`<div class="task-item"><div class="task-source">${a.icon}</div><div><h4>${a.title}</h4><p>${a.subject}</p><div class="task-meta">${badge(a.source,"blue")}${badge(a.status,a.tone)}</div></div><div class="task-deadline"><strong>${a.deadline}</strong><span>اولویت ${a.priority}</span><button class="btn btn-sm btn-ghost" data-action="open-action" data-index="${i}">بررسی</button></div></div>`).join("")}</div>`;
  }

  function toFaMinutes(minutes){
    const h=Math.floor(minutes/60), m=minutes%60;
    if(h && m) return `${num(h)} ساعت و ${num(m)} دقیقه`;
    if(h) return `${num(h)} ساعت`;
    return `${num(m)} دقیقه`;
  }

  function renderTodayActivities(){
    return workActivities.map((item,i)=>`<div class="activity-row">
      <div class="activity-state">${item.standard?"✓":"+"}</div>
      <div class="activity-main"><div class="activity-title"><strong>${esc(item.title)}</strong>${item.standard?badge("استاندارد","green"):badge("در انتظار استانداردسازی","orange")}</div><p>${esc(item.note||"بدون توضیح")}</p><div class="activity-meta">${badge(item.category,"blue")}<span>◴ ${toFaMinutes(item.duration)}</span></div></div>
      <button class="mini-btn" data-action="remove-work-activity" data-index="${i}" aria-label="حذف فعالیت">×</button>
    </div>`).join("");
  }

  function renderPersonalTasks(){
    const visible=personalTasks.filter(x=>!x.done).slice(0,4);
    return visible.map((task,i)=>`<div class="personal-task ${task.priority==="high"?"is-high":""}">
      <button class="task-check" data-action="toggle-personal-task" data-index="${i}" aria-label="انجام شد"></button>
      <div class="personal-task-main"><strong>${esc(task.title)}</strong><div><span>${esc(task.meta)}</span>${badge(task.source,task.source==="تفویض‌شده"?"purple":task.source==="پیگیری"?"orange":"blue")}</div></div>
      <button class="task-more" data-action="personal-task-menu" data-index="${i}" aria-label="گزینه‌ها">•••</button>
    </div>`).join("");
  }

  function renderHomeCalendar(){
    const switcher=`<div class="calendar-view-switch">${["day","week","month"].map(v=>`<button class="${homeCalendarView===v?"active":""}" data-action="home-calendar-view" data-value="${v}">${v==="day"?"روز":v==="week"?"هفته":"ماه"}</button>`).join("")}</div>`;
    let body="";
    if(homeCalendarView==="day"){
      body=`<div class="home-calendar-day">
        <div class="home-time-row"><time>۱۱:۰۰</time><button class="home-cal-event type-meeting" data-action="calendar-event-detail"><strong>جلسه هماهنگی عملیات</strong><small>اتاق جلسات مدیریت • ۶۰ دقیقه</small></button></div>
        <div class="home-time-row"><time>۱۴:۳۰</time><button class="home-cal-event type-report" data-action="calendar-event-detail"><strong>مرور گزارش‌های شیفت</strong><small>گزارش کار • ۴۵ دقیقه</small></button></div>
        <div class="home-time-row"><time>۱۶:۰۰</time><button class="home-cal-event type-correspondence" data-action="calendar-event-detail"><strong>پاسخ به مکاتبات باز</strong><small>دبیرخانه • ۳۰ دقیقه</small></button></div>
      </div>`;
    } else if(homeCalendarView==="week"){
      const days=["ش","ی","د","س","چ","پ","ج"];
      body=`<div class="home-calendar-week">${days.map((d,i)=>`<div class="home-week-day ${i===0?"today":""}"><strong>${d}</strong><span>${num(27+i)}</span>${i===0?'<i class="home-week-event">۲ رویداد</i>':i===2?'<i class="home-week-event">۱ رویداد</i>':""}</div>`).join("")}</div>`;
    } else {
      const monthNames=["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"];
      const weekdayNames=["شنبه","یکشنبه","دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه"];
      const baseMonth=3; // تیر
      const baseYear=1405;
      const absolute=baseMonth+homeCalendarMonthOffset;
      const monthIndex=((absolute%12)+12)%12;
      const year=baseYear+Math.floor(absolute/12);
      const daysInMonth=monthIndex<6?31:monthIndex<11?30:29;
      const firstWeekday=((0+homeCalendarMonthOffset*3)%7+7)%7;
      const cells=[
        ...Array.from({length:firstWeekday},()=>null),
        ...Array.from({length:daysInMonth},(_,i)=>i+1)
      ];
      while(cells.length%7) cells.push(null);
      const currentDay=homeCalendarMonthOffset===0?27:null;
      body=`<div class="home-month-shell">
        <div class="home-month-toolbar">
          <button class="home-month-nav" data-action="home-calendar-month-prev" aria-label="ماه قبل">›</button>
          <div><strong>${monthNames[monthIndex]} ${num(year)}</strong><small>نمای ماهانه تقویم شمسی</small></div>
          <button class="home-month-nav" data-action="home-calendar-month-next" aria-label="ماه بعد">‹</button>
        </div>
        <div class="home-month-weekdays">${weekdayNames.map(d=>`<span>${d}</span>`).join("")}</div>
        <div class="home-calendar-month">${cells.map(day=>day===null
          ? `<span class="home-month-empty"></span>`
          : `<button class="${day===currentDay?"today":""}" data-action="home-calendar-day" data-day="${day}"><span>${num(day)}</span>${[5,12,18,27].includes(day)?'<i></i>':""}</button>`
        ).join("")}</div>
      </div>`;
    }
    return `<section class="card dashboard-widget calendar-compact-card widget-wide" data-widget="calendar" draggable="true" title="برای جابه‌جایی، کارت را از سربرگ بکشید">
      <div class="card-header"><div><div class="card-eyebrow">زمان‌بندی</div><h3 class="card-title">تقویم</h3><div class="card-subtitle">تغییر نما بدون خروج از میزکار</div></div>${switcher}</div>
      <div class="card-body home-calendar-body">${body}</div>
      <div class="card-footer"><button class="btn" data-route="calendar">تقویم کامل</button><button class="btn btn-primary" data-action="new-calendar-event">+ رویداد</button></div>
    </section>`;
  }

  function renderCompactActivityWidget(totalMinutes){
    const recent=workActivities.slice(0,3);
    return `<section class="card dashboard-widget compact-activity-widget widget-wide" data-widget="activity" draggable="true">
      <div class="card-header"><div><div class="card-eyebrow">گزارش کار امروز</div><h3 class="card-title">ثبت و مرور فعالیت</h3><div class="card-subtitle">فرم و آخرین رکوردها در یک ویجت فشرده</div></div><div class="activity-header-total"><span>مجموع</span><strong>${toFaMinutes(totalMinutes)}</strong></div></div>
      <div class="card-body">
        <div class="compact-activity-form">
          <select id="quickActivity"><option value="بررسی و پاسخ به مکاتبات عملیات|مکاتبات">بررسی و پاسخ به مکاتبات عملیات</option><option value="تحلیل مغایرت حضور شیفت شب|حضور و کاردکس">تحلیل مغایرت حضور شیفت شب</option><option value="پیگیری اقدام‌های باز|اقدام‌ها">پیگیری اقدام‌های باز</option><option value="جلسه هماهنگی عملیات|جلسه">جلسه هماهنگی عملیات</option><option value="__new__">فعالیت جدید...</option></select>
          <select id="quickDuration"><option value="15">۱۵ دقیقه</option><option value="30" selected>۳۰ دقیقه</option><option value="45">۴۵ دقیقه</option><option value="60">۱ ساعت</option></select>
          <input id="quickNote" placeholder="نتیجه یا توضیح کوتاه..." />
          <button class="btn btn-primary" data-action="add-quick-activity">+ ثبت</button>
        </div>
        <div class="compact-activity-list fixed-row-list">${recent.map((item,i)=>`<div class="compact-activity-row"><span class="activity-state">✓</span><div><strong>${esc(item.title)}</strong><small>${esc(item.category)} • ${toFaMinutes(item.duration)}</small></div><button class="mini-btn" data-action="remove-work-activity" data-index="${i}">×</button></div>`).join("")}${emptyWidgetRows(Math.max(0,3-recent.length),"activity")}</div>
      </div>
      <div class="card-footer"><button class="btn btn-ghost" data-route="work-report-new">مرور گزارش کامل</button></div>
    </section>`;
  }

  function renderConversationWidget(){
    return `<section class="card dashboard-widget compact-conversation-widget" data-widget="conversations" draggable="true">
      <div class="card-header"><div><div class="card-eyebrow">ارتباط سریع</div><h3 class="card-title">گفت‌وگوهای اخیر</h3></div><button class="btn btn-sm" data-route="messages">همه</button></div>
      <div class="card-body"><div class="v7-conversation-list fixed-row-list">${conversations.slice(0,4).map((x,i)=>`<button class="v7-conversation-row" data-action="open-home-conversation" data-index="${i}"><span class="avatar avatar-sm">${x.avatar}</span><div><strong>${x.name}</strong><small>${x.preview}</small></div><aside>${x.unread?`<b>${num(x.unread)}</b>`:""}<time>${x.time}</time></aside></button>`).join("")}${emptyWidgetRows(Math.max(0,4-conversations.slice(0,4).length),"conversation")}</div></div>
    </section>`;
  }

  function applySavedWidgetOrder(){
    const grid=document.querySelector(".dashboard-widget-grid");
    if(!grid) return;
    const order=Array.isArray(v7Settings.widgetOrder)?v7Settings.widgetOrder:v7Defaults.widgetOrder;
    order.forEach(id=>{
      const item=grid.querySelector(`[data-widget="${id}"]`);
      if(item) grid.appendChild(item);
    });
    enableWidgetDrag();
  }

  function enableWidgetDrag(){
    const grid=document.querySelector(".dashboard-widget-grid");
    if(!grid) return;
    let dragged=null;
    grid.querySelectorAll(".dashboard-widget").forEach(widget=>{
      widget.addEventListener("dragstart",e=>{
        if(e.target.closest("button,input,select,textarea")){e.preventDefault();return;}
        dragged=widget; widget.classList.add("dragging");
        e.dataTransfer.effectAllowed="move";
      });
      widget.addEventListener("dragend",()=>{
        widget.classList.remove("dragging");
        grid.querySelectorAll(".drag-over").forEach(x=>x.classList.remove("drag-over"));
        v7Settings.widgetOrder=[...grid.querySelectorAll(".dashboard-widget")].map(x=>x.dataset.widget);
        localStorage.setItem("cas.v7.settings",JSON.stringify(v7Settings));
        dragged=null;
      });
      widget.addEventListener("dragover",e=>{
        e.preventDefault();
        if(!dragged||dragged===widget)return;
        widget.classList.add("drag-over");
        const rect=widget.getBoundingClientRect();
        const before=(e.clientY-rect.top)<rect.height/2;
        grid.insertBefore(dragged,before?widget:widget.nextSibling);
      });
      widget.addEventListener("dragleave",()=>widget.classList.remove("drag-over"));
    });
  }

  function emptyWidgetRows(count, type="default"){
    return Array.from({length:Math.max(0,count)},()=>`<div class="widget-placeholder-row placeholder-${type}" aria-hidden="true">
      <span class="placeholder-leading"></span>
      <div class="placeholder-copy"><i></i><i></i></div>
      <span class="placeholder-trailing"></span>
    </div>`).join("");
  }

  function renderHome(){
    const user = D.users[currentUserId];
    const firstName=user.name.split(" ")[0];
    const totalMinutes=workActivities.reduce((sum,x)=>sum+x.duration,0);
    const pendingTasks=personalTasks.filter(x=>!x.done).length;
    return `<div class="page employee-workspace-v5">
      <section class="briefing-hero briefing-hero-v2">
        <div class="briefing-header-row">
          <div class="briefing-copy">
            <div class="page-kicker">شنبه ۲۷ تیر ۱۴۰۵ • مرکز فرمان شخصی</div>
            <h1>صبح بخیر، ${esc(firstName)}</h1>
            <p>امروز بهتر است ابتدا درخواست خرید شماره ۴۵۱ را بررسی کنی؛ موعد آن نزدیک است.</p>
          </div>
          <div class="presence-compact">
            <span class="presence-dot"></span>
            <div><strong>حضور فعال از ۰۷:۵۸</strong><small>شیفت صبح • ۰۷:۳۰ تا ۱۹:۳۰</small></div>
            <button class="btn btn-sm" data-route="attendance-hub">جزئیات</button>
          </div>
        </div>

        <div class="briefing-status-grid">
          <button data-route="my-actions" class="status-card urgent">
            <span class="status-icon">!</span>
            <div><strong>۳ مورد نیازمند اقدام</strong><small>یک مورد در آستانه عبور از SLA</small></div>
          </button>
          <button data-route="calendar" class="status-card">
            <span class="status-icon">◷</span>
            <div><strong>اولین جلسه ساعت ۱۱:۰۰</strong><small>جلسه هماهنگی عملیات</small></div>
          </button>
          <button data-route="work-report-new" class="status-card warning">
            <span class="status-icon">▤</span>
            <div><strong>گزارش دیروز نهایی نشده</strong><small>حدود ۳۰ دقیقه فعالیت ثبت‌نشده</small></div>
          </button>
          <button data-route="attendance-hub" class="status-card success">
            <span class="status-icon">✓</span>
            <div><strong>شیفت صبح فعال است</strong><small>ورود ثبت‌شده در ۰۷:۵۸</small></div>
          </button>
        </div>

        <button class="command-launcher command-launcher-wide" data-route="global-search-page">
          <span>⌕</span>
          <div><strong>چه کاری می‌خواهی انجام بدهی؟</strong><small>فرم، اقدام، شخص، سند یا فرایند را جست‌وجو کن</small></div>
          <kbd>Ctrl K</kbd>
        </button>
      </section>

      <section class="action-strip unified-shortcuts">
        <button data-action="new-request"><span>＋</span><div><strong>ثبت درخواست</strong><small>مرخصی، مأموریت، خرید و...</small></div></button>
        <button data-action="add-personal-task"><span>✓</span><div><strong>کار جدید</strong><small>ثبت سریع در کارهای من</small></div></button>
        <button data-action="new-calendar-event"><span>◷</span><div><strong>رویداد جدید</strong><small>جلسه یا برنامه شخصی</small></div></button>
        <button data-action="add-activity-focus"><span>▤</span><div><strong>ثبت فعالیت</strong><small>افزودن به گزارش امروز</small></div></button>
        <button data-route="correspondence-new"><span>✉</span><div><strong>نامه جدید</strong><small>مکاتبه رسمی سازمانی</small></div></button>
        <button data-route="messages"><span class="conversation-symbol mini"><i></i><i></i></span><div><strong>گفت‌وگوها</strong><small>ارتباط مستقیم و گروهی</small></div></button>
        <button data-route="attendance-hub"><span>◴</span><div><strong>حضور و شیفت</strong><small>کاردکس شخصی</small></div></button>
        <button data-route="my-documents"><span>▧</span><div><strong>اسناد مرتبط</strong><small>فایل‌ها و نسخه‌ها</small></div></button>
      </section>

      <div class="dashboard-widget-grid">
        <section class="card dashboard-widget personal-todo-card" data-widget="tasks" draggable="true">
          <div class="card-header"><div><div class="card-eyebrow">آنچه باید انجام شود</div><h3 class="card-title">کارهای من</h3><div class="card-subtitle">${num(pendingTasks)} کار باز • ۱ مورد عقب‌افتاده</div></div><button class="btn btn-sm btn-primary" data-action="add-personal-task">+ افزودن</button></div>
          <div class="todo-tabs"><button class="active">امروز <b>۳</b></button><button>آینده <b>۱</b></button><button>عقب‌افتاده <b>۱</b></button></div>
          <div class="card-body"><div class="personal-task-list fixed-row-list">${renderPersonalTasks()}${emptyWidgetRows(Math.max(0,4-personalTasks.filter(x=>!x.done).slice(0,4).length),"task")}</div></div>
          <div class="card-footer"><button class="btn btn-ghost" data-route="personal-tasks">همه کارها</button></div>
        </section>

        ${renderHomeCalendar()}

        <section class="card dashboard-widget action-center-card" data-widget="actions" draggable="true">
          <div class="card-header"><div><div class="card-eyebrow">ورودی عملیاتی</div><h3 class="card-title">نیازمند اقدام</h3></div><button class="btn btn-sm" data-route="my-actions">همه</button></div>
          <div class="card-body">${actionRows(3)}</div>
        </section>

        ${renderConversationWidget()}

        ${renderCompactActivityWidget(totalMinutes)}

        <section class="card dashboard-widget day-progress-compact" data-widget="day-progress" draggable="true">
          <div class="card-header"><div><div class="card-eyebrow">پیشرفت روز کاری</div><h3 class="card-title">گزارش امروز</h3></div><strong>${toFaMinutes(totalMinutes)}</strong></div>
          <div class="card-body"><div class="progress-track"><span style="width:${Math.min(100,Math.round(totalMinutes/480*100))}%"></span></div><div class="compact-progress-stats"><div><span>ثبت‌شده</span><strong>${num(workActivities.length)} فعالیت</strong></div><div><span>پوشش روز</span><strong>${num(Math.min(100,Math.round(totalMinutes/480*100)))}٪</strong></div></div></div>
          <div class="card-footer"><button class="btn btn-primary" data-route="work-report-new">مرور گزارش</button></div>
        </section>

        <section class="card dashboard-widget system-notices" data-widget="notices" draggable="true">
          <div class="card-header"><div><div class="card-eyebrow">اطلاع‌رسانی</div><h3 class="card-title">فقط برای اطلاع</h3></div></div>
          <div class="card-body"><div class="fixed-row-list notice-fixed-list"><div class="notice-line"><span>!</span><div><strong>کاردکس خرداد قفل شد</strong><small>اصلاح فقط از مسیر بازگشایی مجاز است.</small></div></div><div class="notice-line"><span>ش</span><div><strong>فیلترهای تاریخ شمسی به‌روزرسانی شد</strong><small>در جست‌وجوهای پیشرفته قابل استفاده است.</small></div></div>${emptyWidgetRows(2,"notice")}</div></div>
        </section>
      </div>
    </div>`;
  }

  function renderSupervisorDashboard(){
    return `<div class="page">${pageHeader("داشبورد سرپرستی","تصمیم‌های حوزه، مغایرت‌های حضور، گزارش‌های کار و وضعیت SLA تیم.","داشبورد نقش‌محور",`<button class="btn" data-route="team-work-reports">گزارش‌های تیم</button><button class="btn btn-primary" data-route="attendance-review">رسیدگی مغایرت‌ها</button>`)}
      <div class="grid grid-4">${stat("◎","۵","تصمیم باز","۲ فوری","danger")}${stat("⚠","۶","مغایرت حضور","+۱ امروز","warn")}${stat("▤","۸۷٪","ارسال گزارش کار","+۴٪")}${stat("◴","۹۱٪","رعایت SLA","هدف ۹۵٪","warn")}</div>
      <div class="grid grid-3" style="margin-top:16px"><section class="card span-2"><div class="card-header"><div><h3 class="card-title">صف تصمیم‌های سرپرست</h3><div class="card-subtitle">مرتب‌شده بر اساس ریسک SLA</div></div>${badge("به‌روزرسانی لحظه‌ای","green")}</div><div class="card-body">${actionRows(5)}</div></section>${card("وضعیت تیم",`<div class="chart-bars">${[76,92,84,100,68,89,94].map((h,i)=>`<div class="chart-bar" style="height:${h}%"><em>${h}٪</em><span>${["ش","ی","د","س","چ","پ","ج"][i]}</span></div>`).join("")}</div><div style="font-size:9px;color:var(--ink-500);margin-top:10px">نرخ تکمیل به‌موقع فعالیت‌های حوزه در هفت روز اخیر</div>`)} </div>
      <div class="grid grid-3" style="margin-top:16px">${card("حضور امروز",`<div class="donut" style="position:relative"><div class="donut-label"><strong>۸۹٪</strong>حضور کامل</div></div><div class="kv-grid" style="margin-top:15px"><div class="kv"><span>حاضر</span><strong>۳۴ نفر</strong></div><div class="kv"><span>مرخصی</span><strong>۳ نفر</strong></div><div class="kv"><span>مغایرت</span><strong>۲ نفر</strong></div></div>`)}${card("گزارش‌های کار عقب‌افتاده",`<div class="task-list">${D.people.slice(1,5).map((p,i)=>`<div class="task-item"><div class="person-photo" style="width:36px;height:36px;border-radius:11px">${p.initials}</div><div><h4>${p.name}</h4><p>${p.job}</p></div><div>${badge(i<2?"مهلت گذشته":"تا ۲ ساعت",i<2?"red":"orange")}</div></div>`).join("")}</div>`)}${card("درخواست‌های پرریسک",`<div class="timeline"><div class="timeline-item"><h5>مرخصی ساعتی همزمان دو اپراتور</h5><p>نیازمند کنترل ظرفیت شیفت</p><time>امروز</time></div><div class="timeline-item"><h5>اضافه‌کاری خارج از مجوز خودکار</h5><p>ارجاع به مدیر واحد</p><time>فردا</time></div><div class="timeline-item"><h5>اصلاح کاردکس دوره قفل‌شده</h5><p>نیازمند مجوز بازگشایی</p><time>۳۱ تیر</time></div></div>`)} </div>
    </div>`;
  }

  function renderManagerDashboard(executive=false){
    const title = executive?"داشبورد مدیرعامل":"داشبورد مدیریت واحد";
    const sub = executive?"نمای تجمیعی سازمان، روند SLA، تصمیم‌های سطح عالی و شاخص‌های حضور و کارکرد.":"روند عملیات واحد، بهره‌وری، تصمیم‌ها، منابع انسانی و ریسک‌های اجرایی.";
    return `<div class="page">${pageHeader(title,sub,"داشبورد مدیریتی",`<button class="btn">دریافت گزارش PDF</button><button class="btn btn-primary" data-route="approvals">تصمیم‌های باز</button>`)}
      <div class="grid grid-4">${stat("◈",executive?"۸۹٪":"۹۲٪","تحقق برنامه ماه","+۳.۲٪")}${stat("◴","۹۱٪","رعایت SLA","-۲٪","warn")}${stat("◎",executive?"۱۲":"۷","تصمیم سطح مدیریت","۳ فوری","danger")}${stat("▦",executive?"۸۱٪":"۸۵٪","بهره‌وری کارکرد","+۵٪")}</div>
      <div class="grid grid-3" style="margin-top:16px"><section class="card span-2"><div class="card-header"><div><h3 class="card-title">روند عملکرد ۶ ماهه</h3><div class="card-subtitle">ترکیب تکمیل اقدام، حضور مؤثر و گزارش کار</div></div><div class="segmented"><button class="active">عملکرد</button><button>حضور</button><button>SLA</button></div></div><div class="card-body"><div class="chart-bars">${[62,68,74,72,83,89,91,86,94,90,96,92].map((h,i)=>`<div class="chart-bar" style="height:${h}%"><em>${h}</em><span>${i+1}</span></div>`).join("")}</div></div></section>${card("توزیع وضعیت اقدام‌ها",`<div class="donut" style="position:relative"><div class="donut-label"><strong>۲۴۸</strong>کل اقدام‌ها</div></div><div class="kv-grid" style="margin-top:16px"><div class="kv"><span>در زمان</span><strong>۱۴۴</strong></div><div class="kv"><span>نزدیک سررسید</span><strong>۵۰</strong></div><div class="kv"><span>گذشته</span><strong>۲۲</strong></div></div>`)} </div>
      <div class="grid grid-3" style="margin-top:16px">${card("تصمیم‌های اولویت‌دار",actionRows(3),"بر اساس ریسک و سطح اختیار","<button class=\"btn btn-sm btn-primary\" data-route=\"approvals\">مشاهده صندوق تأیید</button>")}${card("واحدهای نیازمند توجه",`<div class="task-list">${[['تولید سایت','۷۸٪','orange'],['انتظامات','۸۴٪','blue'],['فنی','۸۷٪','green'],['خرید','۹۱٪','green']].map(x=>`<div class="task-item"><div class="task-source">${x[0][0]}</div><div><h4>${x[0]}</h4><p>شاخص ترکیبی عملکرد</p></div>${badge(x[1],x[2])}</div>`).join("")}</div>`)}${card("ریسک‌های سیستمی",`<div class="timeline"><div class="timeline-item"><h5>۶ مغایرت حضور حل‌نشده</h5><p>۲ مورد عبور از نیمه‌شب</p><time>ریسک متوسط</time></div><div class="timeline-item"><h5>۳ نامه محرمانه در انتظار ثبت</h5><p>دبیرخانه مرکزی</p><time>ریسک بالا</time></div><div class="timeline-item"><h5>دوره کاردکس تیر آماده قفل نیست</h5><p>۱۲ رکورد پیش‌نویس</p><time>ریسک متوسط</time></div></div>`)} </div>
    </div>`;
  }

  function renderActions(urgent=false){
    const list = urgent ? D.actions.filter(a=>a.tone==="red"||a.tone==="orange") : D.actions;
    return `<div class="page">${pageHeader(urgent?"اقدام‌های فوری":"کارتابل من",urgent?"مواردی که عبور از SLA یا اثر عملیاتی فوری دارند.":"اقدام‌های قابل انجام از همه ماژول‌ها؛ انجام کار روی رکورد منبع صورت می‌گیرد.","CAS Action Hub",`<button class="btn">همگام‌سازی</button><button class="btn btn-primary">اقدام گروهی</button>`)}
      <div class="grid grid-4">${stat("✓",num(list.length),"اقدام قابل انجام")}${stat("!","۳","سررسید امروز","+۱","warn")}${stat("◴","۱","عبور از SLA","فوری","danger")}${stat("↗","۹۲٪","تکمیل در زمان")}</div>
      <div class="toolbar" style="margin-top:18px"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="جست‌وجو در عنوان، منبع یا شخص مرتبط..." /></div><div class="segmented"><button class="active">همه</button><button>امروز</button><button>نزدیک سررسید</button></div></div><div class="toolbar-end"><select class="select"><option>همه منابع</option><option>حضور و غیاب</option><option>فرم و فرایند</option><option>مکاتبات</option></select><select class="select"><option>مرتب‌سازی: فوریت</option><option>مهلت</option><option>اولویت</option></select></div></div>
      <section class="card"><div class="card-body">${list.length?actionRows(list.length):`<div class="empty-state"><div class="empty-icon">✓</div><h3>اقدام فوری ندارید</h3><p>تمام کارهای فوری در زمان برنامه انجام شده‌اند.</p></div>`}</div></section>
    </div>`;
  }

  function renderApprovals(){
    return `<div class="page">${pageHeader("صندوق تأیید","تصمیم رسمی فقط توسط تأییدکننده منصوب یا جانشین معتبر ثبت می‌شود.","CAS Approval Core",`<button class="btn" data-route="delegations">مدیریت جانشینی</button>`)}
      <div class="split-view"><section class="list-pane"><div class="pane-head"><strong>در انتظار تصمیم</strong>${badge("۵ مورد","orange")}</div><div class="pane-body">${D.approvals.map((a,i)=>`<div class="record-row ${i===0?"active":""}" data-action="approval-select" data-index="${i}"><div class="task-source">◎</div><div><h4>${a.title}</h4><p>${a.requester} • ${a.stage}</p>${badge(a.priority,a.priority==="بالا"?"red":"orange")}</div><time>${a.deadline}</time></div>`).join("")}</div></section>
      <section class="detail-pane"><div class="detail-head"><div>${badge("نیازمند اقدام","red")}</div><h2>درخواست مرخصی ساعتی</h2><p>درخواست خروج از ساعت ۱۲:۰۰ تا ۱۶:۰۰ برای مراجعه پزشکی</p></div><div class="detail-section"><div class="kv-grid"><div class="kv"><span>درخواست‌دهنده</span><strong>سارا احمدی</strong></div><div class="kv"><span>واحد</span><strong>کنترل کیفیت</strong></div><div class="kv"><span>شماره</span><strong>APR/۱۴۰۵/۰۰۱۸۲</strong></div><div class="kv"><span>مرحله</span><strong>سرپرست مستقیم</strong></div><div class="kv"><span>مهلت تصمیم</span><strong>امروز، ۱۱:۰۰</strong></div><div class="kv"><span>جانشینی</span><strong>استفاده نشده</strong></div></div></div><div class="detail-section"><h3>اطلاعات درخواست</h3><div class="form-grid"><div class="field"><label>از ساعت</label><input value="۱۲:۰۰" readonly /></div><div class="field"><label>تا ساعت</label><input value="۱۶:۰۰" readonly /></div><div class="field full"><label>دلیل</label><textarea readonly>مراجعه پزشکی با هماهنگی سرپرست شیفت و تحویل فعالیت‌های جاری.</textarea></div></div></div><div class="detail-section"><h3>مسیر تأیید</h3><div class="timeline"><div class="timeline-item"><h5>ثبت درخواست</h5><p>توسط سارا احمدی</p><time>امروز ۰۸:۳۲</time></div><div class="timeline-item"><h5>تصمیم سرپرست</h5><p>مرحله جاری - شما</p><time>مهلت ۱۱:۰۰</time></div><div class="timeline-item"><h5>ثبت نهایی کاردکس</h5><p>پس از تأیید</p><time>خودکار</time></div></div></div><div class="decision-bar"><span style="font-size:10px;color:var(--ink-500)">رد درخواست نیازمند دلیل اجباری است.</span><div class="page-actions"><button class="btn btn-danger" data-action="reject-approval">بازگرداندن برای اصلاح</button><button class="btn btn-success" data-action="approve">تأیید و ثبت</button></div></div></section></div>
    </div>`;
  }

  function renderFormCatalog(){
    return `<div class="page">${pageHeader("فرم‌های قابل ثبت","نسخه‌های منتشرشده و مجاز برای نقش و شرکت جاری.","CAS Dynamic Form Runtime",`<button class="btn" data-route="my-submissions">ثبت‌های من</button>`)}
      <div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="نام یا کد فرم..." /></div><div class="segmented"><button class="active">همه</button><button>پرمصرف</button><button>اخیر</button></div></div><div class="toolbar-end"><select class="select"><option>همه حوزه‌ها</option><option>منابع انسانی</option><option>انتظامات</option><option>خرید</option></select></div></div>
      <div class="module-catalog">${D.forms.map((f,i)=>`<article class="module-card"><div class="module-icon">▤</div><h3>${f.title}</h3><p>${f.category} • زمان تقریبی تکمیل ${f.duration}</p><div class="module-meta"><div><span class="module-code">${f.code}</span><br>${badge(f.version,"blue")}</div><button class="btn btn-sm btn-primary" data-route="form-runtime">شروع ثبت</button></div></article>`).join("")}</div>
      <div class="grid grid-3" style="margin-top:18px">${card("آخرین پیش‌نویس‌ها",`<div class="task-list">${D.forms.slice(0,3).map(f=>`<div class="task-item"><div class="task-source">✎</div><div><h4>${f.title}</h4><p>آخرین ذخیره: امروز ۰۸:۲۴</p></div><button class="btn btn-sm" data-route="form-runtime">ادامه</button></div>`).join("")}</div>`)}${card("فرم‌های پرتکرار",`<div class="chart-bars">${[78,95,58,70,48,62].map((h,i)=>`<div class="chart-bar" style="height:${h}%"><em>${h}</em><span>${i+1}</span></div>`).join("")}</div>`)}${card("راهنمای ثبت",`<div class="timeline"><div class="timeline-item"><h5>نسخه فرم هنگام شروع تثبیت می‌شود</h5><p>تغییرات نسخه جدید روی ثبت جاری اثر ندارد.</p></div><div class="timeline-item"><h5>پیش‌نویس قابل بازیابی است</h5><p>اطلاعات را ذخیره و بعداً ادامه دهید.</p></div><div class="timeline-item"><h5>اعتبارسنجی سرور مرجع نهایی است</h5><p>کنترل مرورگر صرفاً برای تجربه بهتر است.</p></div></div>`)} </div>
    </div>`;
  }

  function renderSubmissions(){
    return `<div class="page">${pageHeader("ثبت‌های من","پیش‌نویس‌ها، موارد ارسال‌شده، بازگشایی‌ها و نسخه فرم متصل.","CAS Form Core",`<button class="btn btn-primary" data-route="form-catalog">ثبت فرم جدید</button>`)}
      <div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="شماره رهگیری یا عنوان فرم..." /></div></div><div class="toolbar-end"><select class="select"><option>همه وضعیت‌ها</option><option>پیش‌نویس</option><option>در گردش</option><option>تأییدشده</option></select></div></div>
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>شماره رهگیری</th><th>فرم</th><th>مالک ثبت</th><th>زمان ایجاد</th><th>نسخه</th><th>وضعیت</th><th></th></tr></thead><tbody>${D.submissions.map((s,i)=>`<tr><td class="title-cell"><strong>${s.number}</strong><small>pin شده به نسخه ${s.version}</small></td><td>${s.form}</td><td>${s.owner}</td><td>${s.date}</td><td>${s.version}</td><td>${badge(s.state,s.state.includes("تأیید")?"green":s.state.includes("اصلاح")?"red":"blue")}</td><td><button class="btn btn-sm" data-action="submission-detail" data-index="${i}">جزئیات</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderFormRuntime(){
    return `<div class="page">${pageHeader("درخواست خرید کالا و خدمات","فرم FR-PUR-REQ-02 • نسخه منتشرشده ۶ • ذخیره خودکار پیش‌نویس فعال است.","اجرای فرم پویا",`<button class="btn">ذخیره پیش‌نویس</button><button class="btn btn-primary" data-action="submit-form">ارسال نهایی</button>`)}
      <div class="form-shell"><section class="card form-card"><div class="form-section"><h3>اطلاعات درخواست</h3><p>مشخصات پایه و واحد درخواست‌کننده</p><div class="form-grid"><div class="field"><label class="required">عنوان درخواست</label><input value="خرید تجهیزات ایمنی کارگاه" /></div><div class="field"><label class="required">واحد درخواست‌کننده</label><select><option>مدیریت تولید سایت</option></select></div><div class="field"><label class="required">تاریخ نیاز</label><input value="۱۴۰۵/۰۵/۱۰" /></div><div class="field"><label>مرکز هزینه</label><select><option>تولید - ۱۱۰۲</option></select></div></div></div>
      <div class="form-section"><h3>اقلام موردنیاز</h3><p>حداقل یک ردیف باید ثبت شود.</p><div class="table-wrap"><table class="data-table" style="min-width:700px"><thead><tr><th>شرح کالا</th><th>تعداد</th><th>واحد</th><th>برآورد مبلغ</th><th>اولویت</th></tr></thead><tbody><tr><td><input value="کلاه ایمنی صنعتی" /></td><td><input value="۲۰" style="width:80px" /></td><td>عدد</td><td>۱۸۰,۰۰۰,۰۰۰ ریال</td><td>${badge("بالا","orange")}</td></tr><tr><td><input value="دستکش نسوز" /></td><td><input value="۵۰" style="width:80px" /></td><td>جفت</td><td>۹۵,۰۰۰,۰۰۰ ریال</td><td>${badge("متوسط","blue")}</td></tr></tbody></table></div><button class="btn btn-sm" style="margin-top:10px">＋ افزودن ردیف</button></div>
      <div class="form-section"><h3>توجیه و پیوست</h3><div class="form-grid"><div class="field full"><label class="required">شرح ضرورت</label><textarea>با توجه به فرسودگی تجهیزات موجود و الزامات HSE، تأمین اقلام پیش از شروع ماه آینده ضروری است.</textarea><small>حداقل ۵۰ و حداکثر ۱۰۰۰ نویسه</small></div><div class="field full"><div class="upload-box"><strong>فایل استعلام یا تصویر کالا را رها کنید</strong>PDF، تصویر یا فایل Office تا سقف ۲۰ مگابایت</div></div></div></div></section>
      <aside class="form-aside"><section class="card"><div class="card-header"><h3 class="card-title">پیشرفت تکمیل</h3>${badge("۷۸٪","blue")}</div><div class="card-body"><div class="progress-list"><div class="progress-item done"><span class="progress-dot">✓</span>اطلاعات درخواست</div><div class="progress-item done"><span class="progress-dot">✓</span>اقلام موردنیاز</div><div class="progress-item active"><span class="progress-dot">۳</span>توجیه و پیوست</div><div class="progress-item"><span class="progress-dot">۴</span>بازبینی و ارسال</div></div><div style="height:8px;border-radius:99px;background:var(--ink-100);margin:18px 0"><div style="width:78%;height:100%;background:var(--blue);border-radius:99px"></div></div><div class="kv"><span>شماره پیش‌نویس</span><strong>FRM/۱۴۰۵/۰۰۳۸۹</strong></div><div class="kv" style="margin-top:8px"><span>آخرین ذخیره</span><strong>امروز، ۰۹:۴۲</strong></div></div><div class="card-footer"><button class="btn btn-primary" style="width:100%" data-action="submit-form">بازبینی و ارسال</button></div></section></aside></div>
    </div>`;
  }

  function renderFormsAdmin(){
    return `<div class="page">${pageHeader("مدیریت فرم‌های سازمانی","تعریف پایدار، نسخه‌های پیش‌نویس/منتشرشده، مالک فرایند و وضعیت استفاده.","CAS Form Core",`<button class="btn">ورود از قالب</button><button class="btn btn-primary" data-action="new-form">تعریف فرم جدید</button>`)}
      <div class="grid grid-4">${stat("▤","۲۸","تعریف فعال")}${stat("✎","۶","نسخه پیش‌نویس","۲ نیازمند بازبینی","warn")}${stat("✓","۲۲","نسخه منتشرشده")}${stat("▦","۱,۸۴۲","ثبت نهایی")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>فرم</th><th>کد فنی</th><th>مالک فرایند</th><th>نسخه فعال</th><th>پیش‌نویس</th><th>آخرین تغییر</th><th></th></tr></thead><tbody>${D.forms.map((f,i)=>`<tr><td class="title-cell"><strong>${f.title}</strong><small>${f.category}</small></td><td dir="ltr">${f.code}</td><td>${["نیلوفر کریمی","امیر نادری","رضا اسدی"][i%3]}</td><td>${badge(f.version,"green")}</td><td>${i%2?badge("ندارد"):badge("بازنگری جدید","orange")}</td><td>۲${i+1} تیر ۱۴۰۵</td><td><div class="row-actions"><button class="btn btn-sm" data-route="form-builder">طراحی</button><button class="mini-btn" data-action="form-detail">⋮</button></div></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderFormBuilder(){
    const palette = [["T","متن کوتاه"],["¶","متن بلند"],["#","عدد"],["٪","درصد"],["◉","انتخاب تکی"],["☑","چندانتخاب"],["ش","تاریخ جلالی"],["◴","ساعت"],["▱","فایل"],["▦","رکورد مرتبط"],["👤","کارمند"],["ƒ","محاسبه‌شده"]];
    return `<div class="page">${pageHeader("طراح دیداری فرم","درخواست خرید کالا و خدمات • بازنگری ۷ • پیش‌نویس", "CAS Visual Form Builder",`<button class="btn">پیش‌نمایش</button><button class="btn">ذخیره تغییرات</button><button class="btn btn-primary" data-action="publish">اعتبارسنجی و انتشار</button>`)}
      <div class="builder"><aside class="builder-panel"><div class="builder-title">پالت فیلدها</div><div class="palette">${palette.map(p=>`<button class="palette-item"><strong>${p[0]}</strong>${p[1]}</button>`).join("")}</div></aside><div class="canvas"><div class="canvas-page"><div class="page-kicker">FR-PUR-REQ-02</div><h2>درخواست خرید کالا و خدمات</h2><p>لطفاً اطلاعات درخواست و اقلام موردنیاز را کامل کنید.</p><div class="canvas-field"><span class="drag-handle">⠿</span><div class="field"><label class="required">عنوان درخواست</label><input placeholder="عنوان کوتاه و مشخص" /></div></div><div class="canvas-field selected"><span class="drag-handle">⠿</span><div class="form-grid"><div class="field"><label class="required">واحد درخواست‌کننده</label><select><option>انتخاب کنید</option></select></div><div class="field"><label class="required">تاریخ نیاز</label><input placeholder="۱۴۰۵/۰۵/۱۰" /></div></div></div><div class="canvas-field"><span class="drag-handle">⠿</span><div class="field"><label>شرح ضرورت</label><textarea placeholder="توضیحات کامل..."></textarea></div></div><div class="canvas-field"><span class="drag-handle">⠿</span><div class="upload-box"><strong>پیوست درخواست</strong>فایل را اینجا رها کنید</div></div></div></div><aside class="builder-panel"><div class="builder-title">ویژگی‌های بخش انتخاب‌شده</div><div class="property-list"><div class="field"><label>عنوان</label><input value="اطلاعات درخواست" /></div><div class="field"><label>کلید فنی</label><input value="request_info" dir="ltr" /></div><div class="field"><label>تعداد ستون</label><select><option>۲ ستون</option></select></div><h4>رفتار</h4><label style="font-size:10px;display:flex;gap:7px"><input type="checkbox" checked /> نمایش عنوان بخش</label><label style="font-size:10px;display:flex;gap:7px;margin-top:8px"><input type="checkbox" /> جمع‌شونده</label><h4>اعتبارسنجی</h4><div class="field"><label>شرط نمایش</label><select><option>همیشه نمایش داده شود</option></select></div><button class="btn btn-danger btn-sm" style="width:100%;margin-top:10px">حذف بخش</button></div></aside></div>
    </div>`;
  }

  function renderWorkflowInstances(){
    return `<div class="page">${pageHeader("گردش‌کارهای من","نمونه‌های اجرایی متصل به نسخه ثابت، وضعیت جاری، مسئول و مهلت مرحله.","CAS Workflow Core",`<button class="btn">نمای کانبان</button>`)}
      <div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="شماره، فرایند یا رکورد منبع..." /></div></div><div class="toolbar-end"><select class="select"><option>همه وضعیت‌ها</option><option>درحال اجرا</option><option>تکمیل‌شده</option></select></div></div>
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>شماره</th><th>گردش‌کار</th><th>رکورد منبع</th><th>وضعیت جاری</th><th>مسئول</th><th>مهلت مرحله</th><th>وضعیت اجرا</th><th></th></tr></thead><tbody>${D.workflowInstances.map((w,i)=>`<tr><td class="title-cell"><strong>${w.no}</strong><small>نسخه ${i+2}</small></td><td>${w.title}</td><td>${w.record}</td><td>${badge(w.state,"purple")}</td><td>${w.owner}</td><td>${w.deadline}</td><td>${badge(w.status,w.status.includes("تکمیل")?"green":"blue")}</td><td><button class="btn btn-sm" data-action="workflow-detail" data-index="${i}">بازکردن</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderWorkflowAdmin(){
    return `<div class="page">${pageHeader("مدیریت گردش‌کارها","تعریف فرایند، نسخه‌ها، مدل مقصد، مسیر انتشار و نمونه‌های فعال.","CAS Workflow Core",`<button class="btn btn-primary" data-action="new-workflow">گردش‌کار جدید</button>`)}
      <div class="grid grid-4">${stat("⇄","۱۸","گردش‌کار فعال")}${stat("✎","۴","نسخه پیش‌نویس","۱ نامعتبر","warn")}${stat("◴","۹۱٪","رعایت SLA")}${stat("▦","۳۲۴","نمونه درحال اجرا")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>عنوان فرایند</th><th>کد</th><th>مدل مقصد</th><th>نسخه فعال</th><th>نمونه فعال</th><th>وضعیت طراحی</th><th></th></tr></thead><tbody>${["درخواست مرخصی و مأموریت","درخواست خرید سازمانی","گزارش کار روزانه","ثبت عدم انطباق کیفیت","اصلاح کاردکس"].map((n,i)=>`<tr><td class="title-cell"><strong>${n}</strong><small>مالک: ${["منابع انسانی","خرید","عملیات","کیفیت","منابع انسانی"][i]}</small></td><td dir="ltr">WF-${["HR-LEAVE","PUR-REQ","WR-DAILY","QC-NCR","KR-REOPEN"][i]}</td><td dir="ltr">${["cas.attendance.request","cas.form.submission","cas.work.report","cas.form.submission","cas.kardex.reopen"][i]}</td><td>${badge(`نسخه ${i+2}`,"green")}</td><td>${[48,35,129,18,7][i]}</td><td>${i===4?badge("نیازمند بازبینی","orange"):badge("معتبر","green")}</td><td><button class="btn btn-sm" data-route="workflow-designer">طراحی</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function wfLine(x,y,w,angle){return `<div class="wf-line" style="right:${x}px;top:${y}px;width:${w}px;transform:rotate(${angle}deg)"></div>`}
  function renderWorkflowDesigner(){
    return `<div class="page">${pageHeader("طراح دیداری گردش‌کار","درخواست مرخصی و مأموریت • بازنگری ۵ • پیش‌نویس", "CAS Visual Workflow Designer",`<button class="btn">بررسی مسیرها</button><button class="btn">ذخیره گراف</button><button class="btn btn-primary" data-action="publish">انتشار نسخه</button>`)}
      <div class="workflow-canvas"><div class="wf-toolbar"><button class="mini-btn">＋</button><button class="mini-btn">−</button><button class="mini-btn">↶</button><button class="mini-btn">⌗</button></div>
        <svg aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;z-index:1" viewBox="0 0 1000 650" preserveAspectRatio="none"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#7fa6bd"/></marker></defs><path d="M790 180 L710 180" stroke="#7fa6bd" stroke-width="2" marker-end="url(#arrow)"/><path d="M540 180 L460 180" stroke="#7fa6bd" stroke-width="2" marker-end="url(#arrow)"/><path d="M290 180 L210 180" stroke="#7fa6bd" stroke-width="2" marker-end="url(#arrow)"/><path d="M540 220 C540 300 500 330 470 360" stroke="#d78b61" stroke-width="2" fill="none" marker-end="url(#arrow)"/><path d="M380 405 C300 405 280 280 350 220" stroke="#7fa6bd" stroke-width="2" fill="none" marker-end="url(#arrow)"/></svg>
        <div class="wf-node start" style="right:3%;top:130px"><div class="node-type">آغاز</div><h4>ثبت درخواست</h4><p>فرم متصل: درخواست مرخصی</p></div>
        <div class="wf-node" style="right:28%;top:130px"><div class="node-type">وظیفه کاربر</div><h4>بازبینی سرپرست</h4><p>SLA: چهار ساعت • مسئول: مدیر مستقیم</p></div>
        <div class="wf-node approval" style="right:53%;top:130px"><div class="node-type">تأیید چندمرحله‌ای</div><h4>تأیید مدیریت</h4><p>قانون: همه تأییدکنندگان</p></div>
        <div class="wf-node end" style="right:78%;top:130px"><div class="node-type">پایان</div><h4>ثبت در کاردکس</h4><p>انتقال خودکار پس از تأیید</p></div>
        <div class="wf-node" style="right:39%;top:340px;border-color:#df9c75"><div class="node-type" style="color:var(--orange)">اصلاح</div><h4>بازگشت به درخواست‌دهنده</h4><p>یادداشت اجباری • مهلت ۲۴ ساعت</p></div>
        <aside class="wf-side">${card("تنظیمات گره",`<div class="field"><label>عنوان</label><input value="تأیید مدیریت" /></div><div class="field" style="margin-top:8px"><label>نوع گره</label><select><option>تأیید چندمرحله‌ای</option></select></div><div class="field" style="margin-top:8px"><label>سیاست تأیید</label><select><option>مرخصی بیش از ۴ ساعت</option></select></div><div class="field" style="margin-top:8px"><label>SLA مرحله</label><input value="۸ ساعت" /></div>`)}</aside>
      </div>
    </div>`;
  }

  function renderApprovalPolicies(){
    return `<div class="page">${pageHeader("سیاست‌های تأیید","مراحل نسخه‌پذیر، روش اجرا، حد نصاب، نقش سازمانی و انتقال نتیجه.","CAS Approval Core",`<button class="btn btn-primary">سیاست جدید</button>`)}
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>سیاست</th><th>مرحله گردش‌کار</th><th>روش اجرا</th><th>قاعده تصمیم</th><th>تأییدکنندگان</th><th>مهلت</th><th></th></tr></thead><tbody>${["مرخصی ساعتی","خرید تا ۵۰۰ میلیون","خرید بالای ۵۰۰ میلیون","اضافه‌کاری خارج از مجوز","بازگشایی کاردکس"].map((x,i)=>`<tr><td class="title-cell"><strong>${x}</strong><small>POL-${i+101}</small></td><td>${["بررسی سرپرست","تصمیم مدیر واحد","تصمیم مدیریت عالی","تصمیم مدیرعامل","مجوز بازگشایی"][i]}</td><td>${badge(i===2?"موازی":"ترتیبی","blue")}</td><td>${i===2?"حد نصاب ۲":"همه"}</td><td>${[1,1,3,1,2][i]} گام</td><td>${[4,8,12,8,12][i]} ساعت</td><td><button class="btn btn-sm">ویرایش</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderDelegations(){
    return `<div class="page">${pageHeader("جانشینی و تفویض تأیید","مجوز تاریخ‌دار، محدود به سیاست و شرکت؛ هر استفاده در تصمیم ثبت می‌شود.","CAS Approval Delegation",`<button class="btn btn-primary">ثبت جانشینی</button>`)}
      <div class="grid grid-3">${card("جانشینی فعال",`<div class="guard-selected"><div class="person-photo">ان</div><div><h3>امیر نادری ← نگار یوسفی</h3><p>از ۲۷ تیر تا ۳ مرداد ۱۴۰۵</p></div></div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>سیاست‌ها</span><strong>گزارش کار، خرید</strong></div><div class="kv"><span>شرکت</span><strong>چدن‌آرا شمال</strong></div><div class="kv"><span>استفاده شده</span><strong>۲ تصمیم</strong></div></div>`,"جایگزینی در زمان مأموریت")}${card("تقویم جانشینی",`<div class="timeline"><div class="timeline-item"><h5>۲۷ تیر - شروع جانشینی</h5><p>ثبت توسط مدیر سامانه</p></div><div class="timeline-item"><h5>۲۹ تیر - یک تصمیم خرید</h5><p>تصمیم‌گیرنده واقعی: نگار یوسفی</p></div><div class="timeline-item"><h5>۳ مرداد - پایان خودکار</h5><p>دسترسی پس از تاریخ پایان معتبر نیست.</p></div></div>`)}${card("کنترل‌های قرارداد",`<div class="status-panel" style="grid-template-columns:1fr"><div class="status-item"><span class="status-light"></span><div><strong>عدم هم‌پوشانی</strong><small>جانشینی موازی متناقض وجود ندارد</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>محدوده سیاست</strong><small>فقط سیاست‌های مشخص‌شده</small></div></div><div class="status-item"><span class="status-light warn"></span><div><strong>پایان نزدیک</strong><small>دو روز تا انقضا</small></div></div></div>`)} </div>
    </div>`;
  }

  function renderCorrespondence(){
    return `<div class="page">${pageHeader("مکاتبات سازمانی","نامه‌های رسمی داخلی، ارجاع‌ها، رسید مشاهده و سابقه ممیزی؛ مستقل از چت عمومی.","CAS Correspondence",`<button class="btn" data-route="secretariat-register">دفتر ثبت</button><button class="btn btn-primary" data-route="letter-compose">نامه جدید</button>`)}
      <div class="split-view"><section class="list-pane"><div class="pane-head"><div class="segmented"><button class="active">دریافتی</button><button>ارسالی</button><button>پیش‌نویس</button></div>${badge("۲ خوانده‌نشده","blue")}</div><div class="pane-body">${D.letters.map((l,i)=>`<div class="record-row ${i===0?"active":""}" data-action="letter-select" data-index="${i}"><div class="task-source">✉</div><div><h4>${l.subject}</h4><p>${l.from} ← ${l.to}</p><div style="display:flex;gap:5px">${badge(l.conf,l.conf==="محرمانه"?"red":"blue")}${badge(l.state,l.state.includes("دریافت")?"green":"purple")}</div></div><time>${l.date}</time></div>`).join("")}</div></section>
      <section class="detail-pane"><div class="detail-head"><div style="display:flex;gap:7px">${badge("داخلی","blue")}${badge("ارجاع شده","purple")}</div><h2>درخواست تأمین قطعات یدکی خط شات‌بلاست</h2><p>شماره ۱۴۰۵/د/۰۰۲۴ • از مدیریت تولید سایت به مدیریت خرید</p></div><div class="detail-section"><div class="kv-grid"><div class="kv"><span>فرستنده</span><strong>رضا اسدی</strong></div><div class="kv"><span>گیرنده اصلی</span><strong>مدیر خرید</strong></div><div class="kv"><span>تاریخ ارسال</span><strong>۲۷ تیر ۱۴۰۵ - ۰۸:۱۴</strong></div><div class="kv"><span>سطح محرمانگی</span><strong>داخلی</strong></div><div class="kv"><span>مهلت پاسخ</span><strong>۳۱ تیر ۱۴۰۵</strong></div><div class="kv"><span>ثبت دبیرخانه</span><strong>در انتظار ثبت</strong></div></div></div><div class="detail-section"><h3>متن نامه</h3><p style="font-size:11px;color:var(--ink-700);line-height:2">با سلام؛ با توجه به توقف‌های اخیر خط شات‌بلاست و گزارش واحد فنی، خواهشمند است نسبت به تأمین قطعات یدکی فهرست پیوست در اولویت خرید اقدام شود. موجودی فعلی برای حداکثر ده روز کاری کفایت می‌کند.</p></div><div class="detail-section"><h3>پیوست‌ها</h3><div class="log-card"><div class="log-type">▧</div><div><h5>فهرست_قطعات_شات_بلاست.pdf</h5><p>نسخه سند ۲ • ۲۷۸ KB</p></div><button class="btn btn-sm">مشاهده</button></div></div><div class="detail-section"><h3>ارجاع‌ها و سابقه</h3><div class="timeline"><div class="timeline-item"><h5>ارجاع به کارشناس تأمین و پیگیری</h5><p>مهلت: ۳۱ تیر • اقدام باز</p><time>امروز ۰۹:۰۲</time></div><div class="timeline-item"><h5>رسید مشاهده مدیر خرید</h5><p>مشاهده از Workspace</p><time>امروز ۰۸:۴۰</time></div><div class="timeline-item"><h5>نامه ارسال شد</h5><p>گیرندگان و دسترسی تثبیت شدند.</p><time>امروز ۰۸:۱۴</time></div></div></div><div class="decision-bar"><button class="btn">ثبت پاسخ</button><div class="page-actions"><button class="btn">ارجاع</button><button class="btn btn-primary">شروع اقدام</button></div></div></section></div>
    </div>`;
  }

  function renderLetterCompose(){
    return `<div class="page">${pageHeader("نامه جدید","پیش‌نویس رسمی با کنترل محرمانگی، گیرندگان مجاز، پیوست و رابطه پاسخ/اصلاح.","CAS Correspondence",`<button class="btn">ذخیره پیش‌نویس</button><button class="btn btn-primary" data-action="send-letter">ارسال نامه</button>`)}
      <div class="form-shell"><section class="card form-card"><div class="form-section"><h3>اطلاعات نامه</h3><div class="form-grid"><div class="field full"><label class="required">موضوع</label><input placeholder="موضوع روشن و کوتاه" /></div><div class="field"><label class="required">نوع مکاتبه</label><select><option>نامه داخلی</option><option>نامه صادره</option></select></div><div class="field"><label class="required">محرمانگی</label><select><option>عادی</option><option>داخلی</option><option>محرمانه</option></select></div><div class="field"><label class="required">گیرنده اصلی</label><select><option>انتخاب واحد یا شخص</option></select></div><div class="field"><label>رونوشت</label><input placeholder="افزودن گیرنده..." /></div><div class="field"><label>مهلت پاسخ</label><input value="۱۴۰۵/۰۵/۰۱" /></div><div class="field"><label>قالب رسمی</label><select><option>نامه داخلی استاندارد</option></select></div></div></div><div class="form-section"><h3>متن مکاتبه</h3><div class="field"><label class="required">متن نامه</label><textarea style="min-height:260px" placeholder="متن نامه را وارد کنید..."></textarea></div></div><div class="form-section"><h3>پیوست‌ها</h3><div class="upload-box"><strong>فایل‌های پیوست را اینجا رها کنید</strong>فایل‌ها پس از ارسال به Core Document پیوند می‌خورند.</div></div></section><aside class="form-aside"><section class="card"><div class="card-header"><h3 class="card-title">کنترل پیش از ارسال</h3></div><div class="card-body"><div class="progress-list"><div class="progress-item active"><span class="progress-dot">۱</span>موضوع و نوع نامه</div><div class="progress-item"><span class="progress-dot">۲</span>گیرندگان مجاز</div><div class="progress-item"><span class="progress-dot">۳</span>متن و پیوست</div><div class="progress-item"><span class="progress-dot">۴</span>تثبیت ارسال</div></div><div class="kv" style="margin-top:16px"><span>شماره</span><strong>پس از ثبت دبیرخانه</strong></div><div class="kv" style="margin-top:8px"><span>نسخه سند رسمی</span><strong>پس از تولید PDF</strong></div></div></section></aside></div>
    </div>`;
  }

  function renderDocuments(){
    return `<div class="page">${pageHeader("کتابخانه اسناد","نسخه فایل، پیوند کسب‌وکاری، پوشه، برچسب، OCR و رخدادهای رسمی.","CAS Document Core",`<button class="btn">پوشه جدید</button><button class="btn btn-primary" data-action="upload-document">بارگذاری سند</button>`)}
      <div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="عنوان سند، برچسب یا رکورد مرتبط..." /></div><div class="segmented"><button class="active">شبکه‌ای</button><button>فهرست</button></div></div><div class="toolbar-end"><select class="select"><option>همه پوشه‌ها</option><option>مکاتبات</option><option>فرم‌های سازمانی</option><option>کاردکس</option></select><select class="select"><option>همه وضعیت‌ها</option><option>فعال</option><option>در OCR</option><option>بایگانی</option></select></div></div>
      <div class="document-grid">${D.documents.map((d,i)=>`<article class="doc-card"><div class="doc-preview"><span class="doc-format">${d.format}</span>${d.icon}</div><h4>${d.name}</h4><p>${d.folder} • ${d.size}</p><div class="doc-footer"><div>${badge(d.version,"blue")} ${badge(d.status,d.status.includes("OCR")?"purple":d.status.includes("تأیید")||d.status.includes("منتشر")?"green":"orange")}</div><button class="mini-btn" data-action="document-detail" data-index="${i}">⋮</button></div></article>`).join("")}</div>
    </div>`;
  }

  function renderOcrQueue(){
    return `<div class="page">${pageHeader("صف پردازش OCR","ارسال، پردازش، بازبینی و تأیید متن استخراج‌شده با نگهداری رخداد خطا.","CAS Document OCR",`<button class="btn">ارسال گروهی</button>`)}
      <div class="grid grid-4">${stat("◉","۸","در انتظار پردازش")}${stat("↻","۳","در حال پردازش","میانگین ۲ دقیقه")}${stat("✓","۱۱۲","تکمیل این ماه")}${stat("!","۲","خطای نیازمند بررسی","فوری","danger")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>سند</th><th>ارائه‌دهنده</th><th>وضعیت</th><th>تلاش</th><th>زمان ارسال</th><th>کیفیت</th><th></th></tr></thead><tbody>${D.documents.slice(0,6).map((d,i)=>`<tr><td class="title-cell"><strong>${d.name}</strong><small>${d.format} • ${d.size}</small></td><td>${i%2?"Tesseract داخلی":"سرویس OCR سازمانی"}</td><td>${badge(i===1?"درحال پردازش":i===4?"خطا":"در انتظار",i===4?"red":i===1?"blue":"orange")}</td><td>${i===4?"۳ از ۳":"۱ از ۳"}</td><td>امروز ${`۰${8+i}:۲${i}`}</td><td>${i<3?`${88+i*3}٪`:"-"}</td><td><button class="btn btn-sm">بازبینی</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderSecretariatRegister(){
    return `<div class="page">${pageHeader("دفتر وارده و صادره","ثبت رسمی، تخصیص شماره، تولید PDF نسخه‌دار و اتصال به دفتر ممیزی.","CAS Correspondence Advanced",`<button class="btn">گزارش دفتر</button><button class="btn btn-primary" data-action="register-letter">ثبت نامه جدید</button>`)}
      <div class="grid grid-4">${stat("⇩","۱۸","وارده امروز")}${stat("⇧","۱۲","صادره امروز")}${stat("◴","۳","در انتظار ثبت","نزدیک SLA","warn")}${stat("✍","۷","در انتظار امضا")}</div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2 table-card"><div class="card-header"><div><h3 class="card-title">آخرین رخدادهای دفتر ثبت</h3><div class="card-subtitle">هر رخداد ثبت و ابطال به‌صورت append-only نگهداری می‌شود.</div></div><div class="segmented"><button class="active">همه</button><button>وارده</button><button>صادره</button></div></div><div class="table-wrap"><table class="data-table"><thead><tr><th>شماره ثبت</th><th>نوع</th><th>موضوع</th><th>فرستنده/گیرنده</th><th>زمان ثبت</th><th>ثبت‌کننده</th><th></th></tr></thead><tbody>${D.letters.map((l,i)=>`<tr><td class="title-cell"><strong>${i%2?`۱۴۰۵/ص/۰۳${20+i}`:`۱۴۰۵/و/۰۱${18+i}`}</strong><small>${l.no}</small></td><td>${badge(i%2?"صادره":"وارده",i%2?"purple":"blue")}</td><td>${l.subject}</td><td>${i%2?l.to:l.from}</td><td>${l.date} - ۰${8+i}:۱${i}</td><td>مریم فلاحی</td><td><button class="btn btn-sm">جزئیات</button></td></tr>`).join("")}</tbody></table></div></section>
      ${card("صف نیازمند ثبت",`<div class="task-list">${D.letters.slice(0,4).map((l,i)=>`<div class="task-item"><div class="task-source">${i%2?"⇧":"⇩"}</div><div><h4>${l.subject}</h4><p>${l.from}</p></div><button class="btn btn-sm btn-primary" data-action="register-letter">ثبت</button></div>`).join("")}</div>`,"۳ مورد نزدیک سررسید")}</div>
    </div>`;
  }

  function renderCorrespondenceTemplates(){
    return `<div class="page">${pageHeader("قالب‌های مکاتبات","قالب رسمی، سربرگ، جای‌گذاری داده، خروجی QWeb/PDF و کنترل نسخه.","CAS Correspondence Advanced",`<button class="btn btn-primary">قالب جدید</button>`)}
      <div class="module-catalog">${["نامه داخلی استاندارد","نامه صادره رسمی","ابلاغیه سازمانی","صورتجلسه رسمی","پاسخ به استعلام","نامه محرمانه"].map((x,i)=>`<article class="module-card"><div class="module-icon">▨</div><h3>${x}</h3><p>قالب QWeb نسخه ${i+1} • آخرین تغییر ${20+i} تیر ۱۴۰۵</p><div class="module-meta">${badge(i===5?"محدود":"فعال",i===5?"red":"green")}<button class="btn btn-sm">ویرایش قالب</button></div></article>`).join("")}</div>
    </div>`;
  }

  function renderSignatureLedger(){
    return `<div class="page">${pageHeader("دفتر امضا","ثبت امضا یا ابطال با دلیل، بازیگر، زمان و نسخه سند رسمی.","CAS Correspondence Signature",`<button class="btn">خروجی دفتر</button>`)}
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>سند رسمی</th><th>نامه</th><th>امضاکننده</th><th>نوع رویداد</th><th>زمان</th><th>اثر انگشت نسخه</th><th></th></tr></thead><tbody>${D.letters.map((l,i)=>`<tr><td class="title-cell"><strong>DOC/۱۴۰۵/${220+i}</strong><small>PDF رسمی نسخه ${i+1}</small></td><td>${l.subject}</td><td>${i%2?"مرتضی نظری":"علی اکبری"}</td><td>${badge(i===3?"ابطال امضا":"امضا",i===3?"red":"green")}</td><td>${l.date} - ۱${i}:۳۲</td><td dir="ltr">${`7bc${i}...a19${i}`}</td><td><button class="btn btn-sm">مشاهده سند</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderMyShifts(){
    const days = Array.from({length:35},(_,i)=>i<3?null:i-2);
    return `<div class="page">${pageHeader("تقویم شیفت من","برنامه منتشرشده و snapshot روزانه؛ تغییر سیاست آینده سابقه روزهای گذشته را عوض نمی‌کند.","CAS Shift Management",`<button class="btn" data-route="shift-swaps">درخواست جابه‌جایی</button>`)}
      <div class="grid grid-4">${stat("◷","صبح","شیفت امروز","۰۷:۳۰ تا ۱۹:۳۰")}${stat("▦","۲-۲-۲","الگوی فعال")}${stat("◫","۱۴","روز کاری ماه")}${stat("↔","۱","درخواست جابه‌جایی","در انتظار","warn")}</div>
      <section class="card" style="margin-top:18px"><div class="card-header"><div><h3 class="card-title">مرداد ۱۴۰۵</h3><div class="card-subtitle">شرکت چدن‌آرا شمال • تقویم رسمی و تعطیلات اعمال شده</div></div><div class="page-actions"><button class="mini-btn">‹</button><button class="btn btn-sm">امروز</button><button class="mini-btn">›</button></div></div><div class="calendar-head">${["شنبه","یکشنبه","دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه"].map(d=>`<div>${d}</div>`).join("")}</div><div class="calendar-grid">${days.map((d,i)=>`<div class="calendar-day ${d===1?"today":""}">${d?`<span class="day-no">${num(d)}</span>${d%6===1||d%6===2?`<span class="shift-pill">شیفت روز<br>۰۷:۳۰ - ۱۹:۳۰</span>`:d%6===3||d%6===4?`<span class="shift-pill night">شیفت شب<br>۱۹:۳۰ - ۰۷:۳۰</span>`:`<span class="shift-pill off">استراحت</span>`}`:""}</div>`).join("")}</div></section>
    </div>`;
  }

  function renderShiftPlanning(){
    return `<div class="page">${pageHeader("برنامه‌ریزی شیفت","تعریف سیاست، الگوی چرخشی، انتساب تاریخ‌دار و انتشار snapshot روزانه.","CAS Shift Management",`<button class="btn">تعطیلات رسمی</button><button class="btn btn-primary">انتساب جدید</button>`)}
      <div class="grid grid-4">${stat("▦","۹","الگوی فعال")}${stat("👤","۷۶","کارمند منتسب")}${stat("!","۴","روز بدون برنامه","نیازمند اقدام","danger")}${stat("✓","۳۱","روز منتشرشده")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><div><h3 class="card-title">انتساب‌های شیفت</h3><div class="card-subtitle">دامنه تاریخ، کارمند/حوزه، الگو و وضعیت انتشار</div></div><div class="search-box"><span>⌕</span><input placeholder="نام کارمند یا الگو..." /></div></div><div class="table-wrap"><table class="data-table"><thead><tr><th>کارمند/حوزه</th><th>الگو</th><th>بازه اعتبار</th><th>سیاست حضور</th><th>روزهای snapshot</th><th>وضعیت</th><th></th></tr></thead><tbody>${D.people.slice(0,7).map((p,i)=>`<tr><td class="title-cell"><strong>${p.name}</strong><small>${p.unit} • ${p.code}</small></td><td>${i<2?"نگهبانی ۲-۲-۲":"شیفت اداری"}</td><td>۱ تیر تا ۳۱ شهریور ۱۴۰۵</td><td>${i<2?"سیاست شیفت ۱۲ ساعته":"سیاست اداری"}</td><td>${31-i}</td><td>${badge(i===6?"پیش‌نویس":"منتشرشده",i===6?"orange":"green")}</td><td><button class="btn btn-sm">ویرایش</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderShiftSwaps(){
    return `<div class="page">${pageHeader("جابه‌جایی شیفت","انتقال کنترل‌شده بین دو روز با بررسی تداخل، الگو و تأیید مسئول.","CAS Shift Swap",`<button class="btn btn-primary">درخواست جابه‌جایی</button>`)}
      <div class="grid grid-3">${card("درخواست فعال",`<div class="guard-selected"><div class="person-photo">حم</div><div><h3>حسین مرادی</h3><p>تعویض با فرهاد محمدی</p></div>${badge("در انتظار سرپرست","orange")}</div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>روز مبدأ</span><strong>۳۰ تیر - شب</strong></div><div class="kv"><span>روز مقصد</span><strong>۱ مرداد - روز</strong></div><div class="kv"><span>تداخل</span><strong>ندارد</strong></div></div>`,"قانون انتقال دو روز")}${card("کنترل خودکار",`<div class="status-panel" style="grid-template-columns:1fr"><div class="status-item"><span class="status-light"></span><div><strong>پوشش هر دو روز</strong><small>هر دو شیفت دارای جایگزین‌اند</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>حداقل استراحت</strong><small>۱۲ ساعت رعایت شده است</small></div></div><div class="status-item"><span class="status-light warn"></span><div><strong>تأیید سرپرست</strong><small>هنوز ثبت نشده</small></div></div></div>`)}${card("سابقه درخواست‌ها",`<div class="timeline"><div class="timeline-item"><h5>جابه‌جایی ۲۳ و ۲۴ تیر</h5><p>تأیید و منتشر شد</p><time>۲۲ تیر</time></div><div class="timeline-item"><h5>جابه‌جایی ۱۵ و ۱۶ تیر</h5><p>رد به دلیل تداخل</p><time>۱۴ تیر</time></div></div>`)} </div>
    </div>`;
  }

  function renderMyAttendance(){
    return `<div class="page">${pageHeader("حضور و کارکرد من","رخدادهای خام، تطبیق با برنامه شیفت، ورود/خروج مؤثر و وضعیت روزانه.","CAS Attendance Core",`<button class="btn">اعلام مغایرت</button>`)}
      <div class="grid grid-4">${stat("⇩","۰۷:۵۸","ورود مؤثر","دستگاه درب اصلی")}${stat("⇧","-","خروج مؤثر","هنوز ثبت نشده")}${stat("◷","۰۸:۱۲","کارکرد تا اکنون")}${stat("✓","عادی","وضعیت امروز")}</div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2"><div class="card-header"><div><h3 class="card-title">خط زمانی امروز</h3><div class="card-subtitle">شیفت برنامه‌ریزی‌شده: ۰۷:۳۰ تا ۱۹:۳۰</div></div>${badge("بدون مغایرت","green")}</div><div class="card-body"><div style="height:90px;position:relative;margin:30px 20px"><div style="position:absolute;right:0;left:0;top:40px;height:8px;border-radius:99px;background:var(--ink-100)"><div style="position:absolute;right:3%;width:66%;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--teal),var(--blue))"></div></div>${[["۰۷:۳۰","شروع برنامه",0],["۰۷:۵۸","ورود دستگاه",3],["۱۲:۱۰","خروج موقت",38],["۱۲:۴۲","بازگشت",42],["۱۹:۳۰","پایان برنامه",100]].map((x,i)=>`<div style="position:absolute;right:${x[2]}%;top:27px;transform:translateX(50%);text-align:center"><span style="display:block;width:18px;height:18px;border-radius:50%;background:${i===1||i===3?'var(--blue)':'#fff'};border:3px solid ${i===1||i===3?'var(--blue-soft)':'var(--ink-200)'}"></span><strong style="font-size:9px;display:block;white-space:nowrap;margin-top:6px">${x[0]}</strong><small style="font-size:8px;color:var(--ink-500);white-space:nowrap">${x[1]}</small></div>`).join("")}</div></div></section>${card("جمع‌بندی ماه",`<div class="donut" style="position:relative"><div class="donut-label"><strong>۹۴٪</strong>حضور مؤثر</div></div><div class="kv-grid" style="margin-top:15px"><div class="kv"><span>کارکرد</span><strong>۱۷۶:۳۰</strong></div><div class="kv"><span>تاخیر</span><strong>۰۰:۴۵</strong></div><div class="kv"><span>اضافه‌کار</span><strong>۱۲:۲۰</strong></div></div>`)} </div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">روزهای اخیر</h3><button class="btn btn-sm" data-route="attendance-hub">حضور و شیفت کامل</button></div><div class="table-wrap"><table class="data-table"><thead><tr><th>تاریخ</th><th>شیفت</th><th>ورود</th><th>خروج</th><th>کارکرد</th><th>تاخیر</th><th>وضعیت تطبیق</th></tr></thead><tbody>${Array.from({length:8},(_,i)=>`<tr><td>${27-i} تیر ۱۴۰۵</td><td>${i%3===2?"شب":"روز"}</td><td>${i%4===1?"۰۷:۴۲":"۰۷:۲۹"}</td><td>${i%3===2?"۰۷:۳۳":"۱۹:۳۴"}</td><td>۱۲:${i%2?"۰۸":"۰۵"}</td><td>${i%4===1?badge("۰۰:۱۲","orange"):"-"}</td><td>${badge(i===5?"رفع تعارض شده":"قطعی",i===5?"purple":"green")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderAttendanceReview(){
    return `<div class="page">${pageHeader("رسیدگی مغایرت‌های حضور","مقایسه منبع دستگاه، ثبت نگهبانی و مقدار مؤثر با ثبت دلیل و بازیگر تصمیم.","CAS Attendance Reconciliation",`<button class="btn">محاسبه مجدد</button>`)}
      <div class="grid grid-4">${stat("⚠","۶","مغایرت باز","۲ بحرانی","danger")}${stat("◷","۲.۴ ساعت","میانگین زمان حل")}${stat("✓","۴۱","حل‌شده این ماه")}${stat("↻","۳","نیازمند محاسبه مجدد","warn")}</div>
      <div class="split-view" style="margin-top:18px"><section class="list-pane"><div class="pane-head"><strong>مغایرت‌های باز</strong>${badge("۶ مورد","red")}</div><div class="pane-body">${D.people.slice(0,6).map((p,i)=>`<div class="record-row ${i===0?"active":""}"><div class="person-photo" style="width:39px;height:39px;border-radius:11px">${p.initials}</div><div><h4>${p.name}</h4><p>${i%2?"ورود بدون خروج متناظر":"اختلاف دستگاه و ثبت نگهبانی"}</p>${badge(i<2?"بالا":"متوسط",i<2?"red":"orange")}</div><time>${27-i} تیر</time></div>`).join("")}</div></section><section class="detail-pane"><div class="detail-head">${badge("مغایرت منبع","red")}<h2>حسین مرادی - شیفت شب</h2><p>۲۶ تیر ۱۹:۳۰ تا ۲۷ تیر ۰۷:۳۰ • محل درب شمالی</p></div><div class="detail-section"><h3>منابع رخداد</h3><div class="grid grid-2"><div class="card card-pad"><div class="page-kicker">دستگاه</div><h3 style="margin:0">ورود ۱۹:۲۸</h3><p style="font-size:10px;color:var(--ink-500)">خروج ۰۷:۳۲ • Device-01</p>${badge("منبع خودکار","blue")}</div><div class="card card-pad" style="border-color:#f2b6a8"><div class="page-kicker" style="color:var(--orange)">ثبت نگهبانی</div><h3 style="margin:0">ورود ۱۹:۳۵</h3><p style="font-size:10px;color:var(--ink-500)">خروج ۰۷:۳۰ • نگهبان شیفت</p>${badge("اختلاف ۷ دقیقه","orange")}</div></div></div><div class="detail-section"><h3>تعیین مقدار مؤثر</h3><div class="form-grid"><div class="field"><label>منبع ورود</label><select><option>دستگاه - ۱۹:۲۸</option><option>نگهبانی - ۱۹:۳۵</option><option>مقدار سفارشی</option></select></div><div class="field"><label>منبع خروج</label><select><option>نگهبانی - ۰۷:۳۰</option><option>دستگاه - ۰۷:۳۲</option></select></div><div class="field full"><label class="required">دلیل تصمیم</label><textarea>بر اساس بازبینی دوربین درب شمالی، ورود ثبت‌شده دستگاه صحیح است؛ خروج نگهبانی انتخاب شد.</textarea></div></div></div><div class="decision-bar"><button class="btn">ابطال رخداد نامعتبر</button><button class="btn btn-success" data-action="resolve-attendance">ثبت تصمیم و محاسبه مجدد</button></div></section></div>
    </div>`;
  }

  function renderAttendanceEvents(){
    return `<div class="page">${pageHeader("رخدادهای تردد","دفتر append-only رخدادهای دستگاه و نگهبانی با منبع، محل و وضعیت اعتبار.","CAS Attendance Event",`<button class="btn">خروجی CSV</button>`)}
      <div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="نام، کد پرسنلی یا شناسه دستگاه..." /></div></div><div class="toolbar-end"><select class="select"><option>امروز</option><option>این هفته</option></select><select class="select"><option>همه منابع</option><option>دستگاه</option><option>نگهبانی</option></select></div></div>
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>کارمند</th><th>نوع رخداد</th><th>زمان</th><th>منبع</th><th>محل/دستگاه</th><th>شناسه خارجی</th><th>اعتبار</th><th></th></tr></thead><tbody>${guardLogs.concat(D.attendanceLogs).slice(0,12).map((l,i)=>`<tr><td class="title-cell"><strong>${l.name}</strong><small>${D.people[i%D.people.length].code}</small></td><td>${badge(l.type,l.type==="ورود"?"green":"orange")}</td><td>${l.time} - ۲۷ تیر ۱۴۰۵</td><td>${l.source}</td><td>${l.gate}</td><td dir="ltr">EV-${140500+i}</td><td>${badge(i===7?"باطل‌شده":"فعال",i===7?"red":"green")}</td><td><button class="mini-btn">⋮</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderAttendanceImport(){
    return `<div class="page">${pageHeader("ورود فایل حضور و غیاب","فایل ابتدا parse و stage می‌شود؛ فقط ردیف‌های آماده پس از بازبینی ثبت نهایی خواهند شد.","CAS Attendance Operations",`<button class="btn">دانلود قالب</button><button class="btn btn-primary" data-action="parse-import">خواندن و آماده‌سازی</button>`)}
      <div class="grid grid-3"><section class="card span-2"><div class="card-header"><h3 class="card-title">پرونده ورود IMP/۱۴۰۵/۰۰۲۱</h3>${badge("مرحله بازبینی","orange")}</div><div class="card-body"><div class="form-grid"><div class="field"><label>نوع فایل</label><select><option>خروجی دستگاه حضور</option></select></div><div class="field"><label>محل</label><select><option>درب اصلی</option></select></div><div class="field"><label>دستگاه</label><select><option>Device-01</option></select></div><div class="field"><label>فایل</label><input value="attendance_1405-04-27.xlsx" readonly /></div></div><div class="upload-box" style="margin-top:14px"><strong>فایل Excel آماده تحلیل است</strong>۲۳۴ KB • ۱۲۸ ردیف</div></div></section>${card("خلاصه مرحله‌بندی",`<div class="progress-list"><div class="progress-item done"><span class="progress-dot">✓</span>بارگذاری فایل</div><div class="progress-item done"><span class="progress-dot">✓</span>خواندن و parse</div><div class="progress-item active"><span class="progress-dot">۳</span>بازبینی و نگاشت</div><div class="progress-item"><span class="progress-dot">۴</span>ثبت نهایی</div></div><div class="kv-grid" style="margin-top:16px"><div class="kv"><span>آماده</span><strong>۱۱۲</strong></div><div class="kv"><span>ناشناخته</span><strong>۹</strong></div><div class="kv"><span>تکراری</span><strong>۵</strong></div></div>`)} </div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">ردیف‌های stage شده</h3><div class="segmented"><button class="active">همه ۱۲۸</button><button>ناشناخته ۹</button><button>خطا ۲</button></div></div><div class="table-wrap"><table class="data-table"><thead><tr><th>ردیف</th><th>شناسه خارجی</th><th>کارمند نگاشت‌شده</th><th>زمان</th><th>نوع</th><th>وضعیت</th><th>پیام</th></tr></thead><tbody>${Array.from({length:10},(_,i)=>`<tr><td>${i+1}</td><td dir="ltr">${i===3?"EXT-UNKNOWN":"EXT-00"+(41+i)}</td><td>${i===3?badge("نیازمند نگاشت","red"):D.people[i%D.people.length].name}</td><td>۱۴۰۵/۰۴/۲۷ - ۰${7+i%3}:${20+i}</td><td>${i%2?"خروج":"ورود"}</td><td>${badge(i===3?"unknown":i===7?"duplicate":"ready",i===3?"red":i===7?"orange":"green")}</td><td>${i===3?"شناسه یافت نشد":i===7?"رخداد تکراری":"آماده ثبت"}</td></tr>`).join("")}</tbody></table></div><div class="card-footer" style="display:flex;justify-content:space-between"><span style="font-size:10px;color:var(--ink-500)">ثبت نهایی فقط ۱۱۲ ردیف آماده را commit می‌کند.</span><button class="btn btn-success" data-action="commit-import">ثبت نهایی ردیف‌های آماده</button></div></section>
    </div>`;
  }

  function renderIdentityMapping(){
    return `<div class="page">${pageHeader("نگاشت شناسه‌های خارجی","هیچ شناسه دستگاه یا فایل نباید به‌صورت حدسی به کارمند نسبت داده شود.","CAS Attendance Identity",`<button class="btn btn-primary">نگاشت جدید</button>`)}
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>شناسه خارجی</th><th>سامانه/دستگاه</th><th>کارمند</th><th>کد پرسنلی</th><th>بازه اعتبار</th><th>آخرین استفاده</th><th>وضعیت</th><th></th></tr></thead><tbody>${D.people.map((p,i)=>`<tr><td dir="ltr">EXT-${String(41+i).padStart(4,'0')}</td><td>${i%2?"Device-01":"فایل نگهبانی"}</td><td class="title-cell"><strong>${p.name}</strong><small>${p.job}</small></td><td dir="ltr">${p.code}</td><td>از ۱ فروردین ۱۴۰۵</td><td>۲۷ تیر - ${p.last}</td><td>${badge(i===8?"غیرفعال":"فعال",i===8?"red":"green")}</td><td><button class="btn btn-sm">ویرایش</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderGuard(){
    const p=selectedPerson;
    return `<div class="page">${pageHeader("ثبت ورود و خروج نگهبانی","انتخاب فرد با کارت تصویری، فیلتر واحد، ثبت زمان دستی و لاگ آخرین رخدادها؛ بدون ساختار لیستی سنگین.","CAS Attendance Operations",`<button class="btn" data-route="attendance-events">دفتر رخدادها</button>`)}
      <div class="guard-layout"><section><div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input id="guardSearch" placeholder="نام، کد پرسنلی یا عنوان شغلی..." /></div></div><div class="toolbar-end"><select id="guardUnit" class="select"><option value="">همه واحدها</option>${[...new Set(D.people.map(x=>x.unit))].map(x=>`<option>${x}</option>`).join("")}</select></div></div><div id="peopleGrid" class="people-grid">${renderPeopleCards(D.people)}</div><section class="card" style="margin-top:16px"><div class="card-header"><div><h3 class="card-title">آخرین ثبت‌ها</h3><div class="card-subtitle">جریان زمانی آخرین رخدادهای نگهبانی و دستگاه</div></div><button class="btn btn-sm" data-route="attendance-events">مشاهده همه</button></div><div id="guardLogStream" class="card-body log-stream">${renderGuardLogs()}</div></section></section>
      <aside><section class="card guard-panel"><div class="guard-selected"><div class="person-photo">${p.initials}</div><div><h3>${p.name}</h3><p>${p.code} • ${p.job}</p><div>${badge(p.status==="in"?"داخل مجموعه":"خارج مجموعه",p.status==="in"?"green":"orange")}</div></div></div><div class="time-editor"><div class="time-box"><label>تاریخ ثبت</label><input id="guardDate" value="۱۴۰۵/۰۴/۲۷" /></div><div class="time-box"><label>ساعت دستی</label><input id="guardTime" type="time" value="09:15" /></div></div><div class="field"><label>محل ثبت</label><select id="guardGate"><option>درب شمالی</option><option>درب اصلی</option><option>درب جنوبی</option></select></div><div class="field" style="margin-top:10px"><label>یادداشت اختیاری</label><textarea id="guardNote" style="min-height:76px" placeholder="توضیح علت ثبت دستی یا رخداد ویژه..."></textarea></div><div class="guard-actions" style="margin-top:14px"><button class="btn btn-success" data-action="guard-entry">ثبت ورود</button><button class="btn" style="background:var(--orange-soft);color:var(--orange);border-color:#f5d6a3" data-action="guard-exit">ثبت خروج</button></div><div class="card-footer" style="margin:16px -17px -17px;border-radius:0 0 18px 18px"><span style="font-size:9px;color:var(--ink-500)">زمان دستی با بازیگر، محل و دلیل در رخداد ممیزی ثبت می‌شود و جای رخداد اصلی را حذف نمی‌کند.</span></div></section></aside></div>
    </div>`;
  }

  function renderPeopleCards(list){
    return list.map(p=>`<button class="person-card ${selectedPerson.id===p.id?"selected":""}" data-action="select-person" data-id="${p.id}"><div class="person-photo">${p.initials}</div><div><h4>${p.name}</h4><p>${p.code} • ${p.job}</p><small style="font-size:8px;color:var(--ink-400)">${p.unit} • آخرین ثبت ${p.last}</small></div><span class="person-status ${p.status==="out"?"out":""}"></span></button>`).join("");
  }
  function renderGuardLogs(){
    return guardLogs.slice(0,8).map(l=>`<div class="log-card"><div class="log-type ${l.type==="خروج"?"exit":""}">${l.type==="ورود"?"⇩":"⇧"}</div><div><h5>${l.name} • ${l.type}</h5><p>${l.source} • ${l.gate}</p></div><time>${l.time}</time></div>`).join("");
  }

  function renderDevices(){
    return `<div class="page">${pageHeader("محل‌ها، دستگاه‌ها و خرابی‌ها","مدیریت سایت تردد، دستگاه دریافت‌کننده و بازه‌های قطعی با اثر بر تطبیق.","CAS Attendance Core",`<button class="btn">ثبت خرابی</button><button class="btn btn-primary">دستگاه جدید</button>`)}
      <div class="status-panel">${[["Device-01","درب اصلی","online"],["Device-02","درب شمالی","online"],["Device-03","درب جنوبی","warn"],["Guard-Tablet-01","نگهبانی شمالی","online"],["Import-Gateway","دریافت فایل","online"],["OCR-Bridge","ارتباط اسناد","off"]].map(x=>`<div class="status-item"><span class="status-light ${x[2]==="warn"?"warn":x[2]==="off"?"off":""}"></span><div><strong>${x[0]}</strong><small>${x[1]} • ${x[2]==="online"?"فعال":x[2]==="warn"?"ناپایدار":"قطع"}</small></div><button class="mini-btn" style="margin-right:auto">⋮</button></div>`).join("")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">سوابق خرابی دستگاه</h3></div><div class="table-wrap"><table class="data-table"><thead><tr><th>دستگاه</th><th>شروع خرابی</th><th>پایان</th><th>اثر</th><th>گزارش‌دهنده</th><th>وضعیت</th></tr></thead><tbody>${Array.from({length:5},(_,i)=>`<tr><td>Device-0${(i%3)+1}</td><td>${20+i} تیر ۱۴۰۵ - ۰${8+i}:۱۰</td><td>${20+i} تیر - ۱${i}:۳۰</td><td>${i%2?"رخداد ناقص":"عدم دریافت"}</td><td>واحد انتظامات</td><td>${badge(i===0?"باز":"رفع‌شده",i===0?"orange":"green")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderMyKardex(){
    return `<div class="page">${pageHeader("کاردکس من","محاسبه دقیقه‌ای بر پایه شیفت، حضور قطعی، درخواست‌های تأییدشده و اضافه‌کاری.","CAS Kardex Management",`<button class="btn">چاپ ماه</button><button class="btn btn-primary" data-route="attendance-requests">ثبت درخواست</button>`)}
      <div class="grid grid-4">${stat("◷","۱۷۶:۳۰","کارکرد موظف")}${stat("＋","۱۲:۲۰","اضافه‌کاری")}${stat("−","۰۲:۱۵","کسری کار","-۰۰:۳۰","warn")}${stat("◫","۱ روز","مرخصی تأییدشده")}</div>
      <div class="toolbar" style="margin-top:18px"><div class="toolbar-start"><div class="segmented"><button>خرداد</button><button class="active">تیر ۱۴۰۵</button><button>مرداد</button></div></div><div class="toolbar-end">${badge("دوره باز","green")}<span style="font-size:10px;color:var(--ink-500)">مهلت اصلاح تا ۵ مرداد</span></div></div>
      <div class="kardex-matrix"><table class="kardex-table"><thead><tr><th>تاریخ</th><th>شیفت</th><th>ورود</th><th>خروج</th><th>کارکرد</th><th>موظفی</th><th>تاخیر</th><th>تعجیل</th><th>اضافه‌کار</th><th>مرخصی</th><th>ماموریت</th><th>کسری</th><th>وضعیت</th></tr></thead><tbody>${Array.from({length:18},(_,i)=>`<tr><td>${27-i} تیر ۱۴۰۵</td><td>${i%6<2?"روز":i%6<4?"شب":"استراحت"}</td><td>${i%6>=4?"-":i%4===1?"۰۷:۴۲":"۰۷:۲۹"}</td><td>${i%6>=4?"-":i%6<2?"۱۹:۳۴":"۰۷:۳۲"}</td><td class="cell-good">${i%6>=4?"۰۰:۰۰":"۱۲:۰۵"}</td><td>${i%6>=4?"۰۰:۰۰":"۱۲:۰۰"}</td><td class="${i%4===1?"cell-warn":""}">${i%4===1?"۰۰:۱۲":"-"}</td><td>-</td><td class="cell-good">${i%3===0?"۰۰:۳۵":"۰۰:۰۵"}</td><td>${i===5?"۰۴:۰۰":"-"}</td><td>${i===9?"۱۲:۰۰":"-"}</td><td class="${i%4===1?"cell-danger":""}">${i%4===1?"۰۰:۰۷":"-"}</td><td>${badge(i===7?"پیش‌نویس":"قطعی",i===7?"orange":"green")}</td></tr>`).join("")}</tbody></table></div>
    </div>`;
  }

  function renderAttendanceRequests(){
    return `<div class="page">${pageHeader("مرخصی و مأموریت","درخواست ساعتی، روزانه یا چندروزه با کنترل تقویم، شیفت و مسیر تأیید.","CAS Attendance Request",`<button class="btn btn-primary" data-action="new-request">درخواست جدید</button>`)}
      <div class="grid grid-4">${stat("◫","۳","درخواست این ماه")}${stat("◎","۱","در انتظار تأیید","امروز","warn")}${stat("✓","۲","تأییدشده")}${stat("◷","۰۴:۰۰","مرخصی ساعتی مصرف‌شده")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>شماره</th><th>نوع درخواست</th><th>بازه</th><th>مدت</th><th>دلیل</th><th>مرحله جاری</th><th>وضعیت</th><th></th></tr></thead><tbody>${[["REQ/۱۴۰۵/۰۲۴۱","مرخصی ساعتی","۲۷ تیر، ۱۲ تا ۱۶","۰۴:۰۰","مراجعه پزشکی","تأیید سرپرست","در انتظار"],["REQ/۱۴۰۵/۰۲۲۸","مأموریت روزانه","۲۲ تیر","۱۲:۰۰","بازدید تأمین‌کننده","پایان","تأییدشده"],["REQ/۱۴۰۵/۰۱۹۹","مرخصی روزانه","۱۵ تیر","۱ روز","امور شخصی","پایان","تأییدشده"]].map((x,i)=>`<tr><td>${x[0]}</td><td>${x[1]}</td><td>${x[2]}</td><td>${x[3]}</td><td>${x[4]}</td><td>${x[5]}</td><td>${badge(x[6],i?"green":"orange")}</td><td><button class="btn btn-sm">جزئیات</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderOvertime(){
    return `<div class="page">${pageHeader("اضافه‌کاری","درخواست تأیید اضافه‌کاری انجام‌شده و مجوزهای خودکار تاریخ‌دار.","CAS Overtime",`<button class="btn btn-primary">ثبت اضافه‌کاری</button>`)}
      <div class="grid grid-3">${card("خلاصه ماه",`<div class="donut" style="position:relative;background:conic-gradient(var(--teal) 0 72%,var(--orange) 72% 88%,var(--ink-100) 88%)"><div class="donut-label"><strong>۱۲:۲۰</strong>ثبت‌شده</div></div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>تأییدشده</span><strong>۰۹:۱۰</strong></div><div class="kv"><span>در انتظار</span><strong>۰۳:۱۰</strong></div><div class="kv"><span>ردشده</span><strong>۰۰:۰۰</strong></div></div>`)}${card("مجوز خودکار فعال",`<div class="guard-selected"><div class="task-source">◷</div><div><h3>شیفت تعمیرات اضطراری</h3><p>تا سقف ۲ ساعت پس از شیفت</p></div></div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>اعتبار</span><strong>تا ۳۱ شهریور</strong></div><div class="kv"><span>حوزه</span><strong>واحد فنی</strong></div><div class="kv"><span>تصمیم</span><strong>خودکار</strong></div></div>`)}${card("گردش تأیید",`<div class="timeline"><div class="timeline-item"><h5>ثبت توسط کارمند</h5><p>مقایسه با حضور قطعی</p></div><div class="timeline-item"><h5>تأیید سرپرست</h5><p>کنترل ضرورت و ساعت</p></div><div class="timeline-item"><h5>مدیرعامل در صورت عبور از سقف</h5><p>مرحله شرطی</p></div></div>`)} </div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>تاریخ</th><th>بازه</th><th>مدت</th><th>مبنای حضور</th><th>مجوز خودکار</th><th>مرحله</th><th>وضعیت</th></tr></thead><tbody>${Array.from({length:6},(_,i)=>`<tr><td>${27-i*2} تیر ۱۴۰۵</td><td>۱۹:۳۰ تا ${20+i%2}:۳۰</td><td>۰${1+i%2}:۰۰</td><td>${badge("تطبیق‌شده","green")}</td><td>${i%2?"ندارد":"شیفت تعمیرات"}</td><td>${i%3===0?"مدیر واحد":"پایان"}</td><td>${badge(i%3===0?"در انتظار":"تأییدشده",i%3===0?"orange":"green")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderKardexOperations(){
    return `<div class="page">${pageHeader("عملیات کاردکس","محاسبه، رسیدگی درخواست‌ها، اضافه‌کاری، رکوردهای پیش‌نویس و آماده‌سازی قفل دوره.","CAS Kardex Management",`<button class="btn">محاسبه گروهی</button><button class="btn btn-primary">آماده‌سازی دوره</button>`)}
      <div class="grid grid-4">${stat("↻","۱۲","نیازمند محاسبه")}${stat("!","۷","مغایرت باز","۲ بحرانی","danger")}${stat("◎","۹","درخواست در انتظار")}${stat("✓","۷۱","روز قطعی")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">کاردکس روزانه حوزه</h3><div class="toolbar-end"><select class="select"><option>مدیریت تولید سایت</option></select><select class="select"><option>تیر ۱۴۰۵</option></select></div></div><div class="table-wrap"><table class="data-table"><thead><tr><th>کارمند</th><th>روزهای محاسبه</th><th>پیش‌نویس</th><th>مغایرت</th><th>درخواست باز</th><th>جمع کارکرد</th><th>آمادگی قفل</th><th></th></tr></thead><tbody>${D.people.slice(0,8).map((p,i)=>`<tr><td class="title-cell"><strong>${p.name}</strong><small>${p.job}</small></td><td>${27-i}</td><td>${i%3}</td><td>${i%4===0?badge("۱ مورد","red"):"-"}</td><td>${i%3===1?"۲":"-"}</td><td>${160+i*3}:۳۰</td><td>${badge(i%4===0?"ناقص":"آماده",i%4===0?"orange":"green")}</td><td><button class="btn btn-sm">بازکردن</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderKardexPeriods(){
    return `<div class="page">${pageHeader("دوره‌ها، قفل و بازگشایی کاردکس","پس از قفل، اصلاح فقط از مسیر بازگشایی محدود با دلیل و دامنه مشخص ممکن است.","CAS Kardex Period",`<button class="btn">درخواست بازگشایی</button><button class="btn btn-primary">قفل دوره تیر</button>`)}
      <div class="grid grid-3">${card("تیر ۱۴۰۵",`<div class="guard-selected"><div class="task-source">▰</div><div><h3>دوره باز</h3><p>۱ تا ۳۱ تیر ۱۴۰۵</p></div>${badge("آماده‌سازی ۸۶٪","orange")}</div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>رکورد ناقص</span><strong>۱۲</strong></div><div class="kv"><span>درخواست باز</span><strong>۹</strong></div><div class="kv"><span>مهلت</span><strong>۵ مرداد</strong></div></div>`)}${card("خرداد ۱۴۰۵",`<div class="guard-selected"><div class="task-source">🔒</div><div><h3>قفل‌شده</h3><p>قفل در ۶ تیر ۱۴۰۵</p></div>${badge("قطعی","green")}</div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>بازگشایی</span><strong>۱ مورد</strong></div><div class="kv"><span>کارمند</span><strong>۸۱ نفر</strong></div><div class="kv"><span>خروجی</span><strong>نسخه ۳</strong></div></div>`)}${card("بازگشایی فعال",`<div class="timeline"><div class="timeline-item"><h5>کارمند: حسین مرادی</h5><p>بازه ۲۲ تا ۲۳ خرداد</p><time>تا امروز ۱۴:۰۰</time></div><div class="timeline-item"><h5>دلیل</h5><p>اصلاح رخداد خروج دستگاه</p></div><div class="timeline-item"><h5>اختیار</h5><p>مدیر منابع انسانی</p></div></div>`)} </div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">تاریخچه بازگشایی‌ها</h3></div><div class="table-wrap"><table class="data-table"><thead><tr><th>دوره</th><th>دامنه</th><th>بازه</th><th>دلیل</th><th>مجوزدهنده</th><th>زمان پایان</th><th>وضعیت</th></tr></thead><tbody>${Array.from({length:5},(_,i)=>`<tr><td>خرداد ۱۴۰۵</td><td>${i%2?"یک کارمند":"واحد فنی"}</td><td>${10+i} تا ${11+i} خرداد</td><td>اصلاح رخداد قطعی دستگاه</td><td>${i%2?"مدیر منابع انسانی":"مدیرعامل"}</td><td>${20+i} خرداد - ۱۴:۰۰</td><td>${badge(i===0?"فعال":"بسته‌شده",i===0?"orange":"green")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderKardexReport(){
    return `<div class="page">${pageHeader("گزارش Excel کاردکس","فیلتر امن تاریخ، کارمند و واحد؛ جمع زمان از دقیقه محاسبه و در خروجی قالب‌بندی می‌شود.","CAS Kardex Report",`<button class="btn">تاریخچه خروجی‌ها</button>`)}
      <div class="grid grid-3"><section class="card span-2"><div class="card-header"><h3 class="card-title">تنظیمات گزارش</h3></div><div class="card-body"><div class="form-grid"><div class="field"><label class="required">از تاریخ</label><input value="۱۴۰۵/۰۴/۰۱" /></div><div class="field"><label class="required">تا تاریخ</label><input value="۱۴۰۵/۰۴/۳۱" /></div><div class="field"><label>واحد سازمانی</label><select><option>همه واحدهای مجاز</option><option>مدیریت تولید سایت</option></select></div><div class="field"><label>کارمند</label><select><option>همه کارکنان مجاز</option></select></div><div class="field full"><label>محتوای فایل</label><div style="display:flex;gap:16px;flex-wrap:wrap"><label style="font-size:11px"><input type="checkbox" checked /> برگه جزئیات روزانه</label><label style="font-size:11px"><input type="checkbox" checked /> برگه خلاصه کارکنان</label><label style="font-size:11px"><input type="checkbox" /> شامل رکوردهای پیش‌نویس</label></div></div></div></div><div class="card-footer"><button class="btn btn-success" data-action="download-report">دریافت فایل Excel</button></div></section>${card("پیش‌نمایش دامنه",`<div class="kv-grid"><div class="kv"><span>کارکنان</span><strong>۸۱ نفر</strong></div><div class="kv"><span>روزها</span><strong>۳۱ روز</strong></div><div class="kv"><span>رکورد مجاز</span><strong>۲,۳۸۷</strong></div></div><div class="status-panel" style="grid-template-columns:1fr;margin-top:15px"><div class="status-item"><span class="status-light"></span><div><strong>کنترل چندشرکتی</strong><small>فقط شرکت جاری</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>Record Rule</strong><small>دامنه سازمانی اعمال شد</small></div></div></div>`,"قبل از ساخت فایل")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">آخرین خروجی‌ها</h3></div><div class="table-wrap"><table class="data-table"><thead><tr><th>فایل</th><th>بازه</th><th>دامنه</th><th>سازنده</th><th>زمان</th><th>حجم</th><th></th></tr></thead><tbody>${Array.from({length:5},(_,i)=>`<tr><td class="title-cell"><strong>kardex_1405_04_${i+1}.xlsx</strong><small>جزئیات + خلاصه</small></td><td>۱ تا ۳۱ تیر</td><td>${i%2?"همه واحدها":"تولید سایت"}</td><td>علی اکبری</td><td>${27-i} تیر - ۱${i}:۲۰</td><td>${1.8+i*.2} MB</td><td><button class="btn btn-sm">دانلود</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderWorkReports(team=false){
    return `<div class="page">${pageHeader(team?"گزارش‌های حوزه من":"گزارش‌های کار من",team?"گزارش‌های کارکنان حوزه، وضعیت ارسال، ایستگاه، ساعات و مرحله تأیید.":"گزارش فعالیت روزانه/شیفت؛ مستقل از حضور فیزیکی و محاسبه کاردکس.","CAS Work Report",`<button class="btn">خروجی Excel</button><button class="btn btn-primary" data-route="work-report-new">ثبت گزارش</button>`)}
      <div class="grid grid-4">${stat("▤",team?"۳۸":"۱۸","گزارش این ماه")}${stat("✓",team?"۳۱":"۱۶","تأییدشده")}${stat("◷",team?"۵":"۱","در انتظار تأیید","امروز","warn")}${stat("!",team?"۲":"۱","مهلت گذشته","فوری","danger")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr>${team?"<th>کارمند</th>":""}<th>تاریخ/شیفت</th><th>ایستگاه کاری</th><th>ساعات عادی</th><th>اضافه‌کاری</th><th>خلاصه فعالیت</th><th>مرحله</th><th>وضعیت</th><th></th></tr></thead><tbody>${Array.from({length:9},(_,i)=>`<tr>${team?`<td class="title-cell"><strong>${D.people[i%D.people.length].name}</strong><small>${D.people[i%D.people.length].job}</small></td>`:""}<td>${27-i} تیر • ${i%2?"روز":"شب"}</td><td>${["خط ریخته‌گری","ایستگاه کنترل کیفیت","درب شمالی","تعمیرات برق"][i%4]}</td><td>${i%3===0?"۱۰:۳۰":"۱۲:۰۰"}</td><td>${i%3===0?"۰۱:۳۰":"-"}</td><td>ثبت فعالیت‌های شیفت، توقف‌ها و اقدامات انجام‌شده</td><td>${i%4===0?"تأیید سرپرست":"پایان"}</td><td>${badge(i%4===0?"در انتظار":"تأییدشده",i%4===0?"orange":"green")}</td><td><button class="btn btn-sm">مشاهده</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderWorkReportNew(){
    return `<div class="page">${pageHeader("ثبت گزارش روزانه کار","گزارش فعالیت برای روز/شیفت و ایستگاه؛ مهلت ارسال ۱۲ ساعت پس از پایان شیفت.","CAS Work Report",`<button class="btn">ذخیره پیش‌نویس</button><button class="btn btn-primary" data-action="submit-work-report">ارسال برای تأیید</button>`)}
      <div class="form-shell"><section class="card form-card"><div class="form-section"><h3>مشخصات گزارش</h3><div class="form-grid"><div class="field"><label class="required">کارمند</label><select><option>${D.roles[currentRole].name}</option></select></div><div class="field"><label class="required">تاریخ گزارش</label><input value="۱۴۰۵/۰۴/۲۷" /></div><div class="field"><label class="required">ایستگاه کاری</label><select><option>جریان عملیات</option><option>خط ریخته‌گری</option><option>درب شمالی</option></select></div><div class="field"><label>شیفت مرتبط</label><select><option>شیفت روز - ۰۷:۳۰ تا ۱۹:۳۰</option></select></div><div class="field"><label class="required">شروع فعالیت</label><input type="time" value="07:30" /></div><div class="field"><label class="required">پایان فعالیت</label><input type="time" value="19:30" /></div><div class="field"><label>ساعات عادی</label><input value="۱۲:۰۰" /></div><div class="field"><label>اضافه‌کاری</label><input value="۰۰:۰۰" /></div></div></div><div class="form-section"><h3>شرح فعالیت</h3><div class="field"><label class="required">فعالیت‌های انجام‌شده</label><textarea style="min-height:190px" placeholder="فعالیت‌ها، خروجی‌ها، توقف‌ها و پیگیری‌ها را ثبت کنید..."></textarea></div><div class="field" style="margin-top:12px"><label>موانع و مسائل</label><textarea placeholder="مسائل نیازمند پیگیری سرپرست..."></textarea></div></div><div class="form-section"><h3>پیوست و شواهد</h3><div class="upload-box"><strong>فایل یا تصویر شاهد را اضافه کنید</strong>پیوست‌ها در هسته اسناد نگهداری و به گزارش پیوند می‌شوند.</div></div></section><aside class="form-aside"><section class="card"><div class="card-header"><h3 class="card-title">کنترل گزارش</h3></div><div class="card-body"><div class="status-panel" style="grid-template-columns:1fr"><div class="status-item"><span class="status-light"></span><div><strong>در بازه مجاز</strong><small>۸ ساعت تا پایان مهلت</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>نمایندگی</strong><small>ثبت توسط خود کارمند</small></div></div><div class="status-item"><span class="status-light warn"></span><div><strong>شرح فعالیت</strong><small>هنوز تکمیل نشده</small></div></div></div><div class="kv" style="margin-top:14px"><span>مسیر پس از ارسال</span><strong>تأیید سرپرست عملیات</strong></div></div></section></aside></div>
    </div>`;
  }

  function renderWorkStations(){
    return `<div class="page">${pageHeader("ایستگاه‌های کاری","ایستگاه مستقل از واحد سازمانی برای ثبت دقیق محل/نوع فعالیت گزارش کار.","CAS Work Station",`<button class="btn btn-primary">ایستگاه جدید</button>`)}
      <div class="module-catalog">${["خط ریخته‌گری","خط شات‌بلاست","ایستگاه کنترل کیفیت","تعمیرات برق","درب شمالی","دبیرخانه مرکزی","جریان عملیات","انبار مرکزی"].map((x,i)=>`<article class="module-card"><div class="module-icon">⌂</div><h3>${x}</h3><p>${["تولید سایت","تولید سایت","کیفیت","فنی","انتظامات","مدیریت اداری","مدیریت عملیات","انبار و لجستیک"][i]} • ${12+i*3} گزارش این ماه</p><div class="module-meta">${badge(i===6?"مشترک":"فعال",i===6?"blue":"green")}<button class="btn btn-sm">ویرایش</button></div></article>`).join("")}</div>
    </div>`;
  }

  function renderModules(){
    return `<div class="page">${pageHeader("پوشش رابط کاربری ۲۴ ماژول","هر ماژول بر اساس نقش واقعی، مرز مالکیت داده و نوع تجربه روزمره یا مدیریتی پوشش داده شده است.","فهرست ماژول‌های CAS",`<button class="btn" data-action="coverage">ماتریس کامل پوشش</button>`)}
      <div class="toolbar"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="نام فنی یا کاربرد ماژول..." /></div><div class="segmented"><button class="active">همه</button><button>روزمره</button><button>طراحی</button><button>فنی</button></div></div><div class="toolbar-end">${badge("۲۴ ماژول","blue")}${badge("۱۱ نمای نقش","purple")}</div></div>
      <div class="module-catalog">${D.modules.map(m=>`<article class="module-card ${allowed(m.route)?"":"unavailable"}"><div class="module-icon">${m.icon}</div><h3>${m.title}</h3><p>${m.purpose}</p><div class="module-meta"><div><span class="module-code">${m.code}</span><br>${badge(m.family,"blue")}</div><button class="btn btn-sm" data-route="${m.route}">${allowed(m.route)?"مشاهده صفحه":"نمای مدیر"}</button></div></article>`).join("")}</div>
    </div>`;
  }

  function renderSlaRules(){
    return `<div class="page">${pageHeader("قوانین SLA و تشدید","قواعد منبع‌محور برای مهلت، نزدیک سررسید، عبور و ثبت رخداد only-append.","CAS Action Hub",`<button class="btn btn-primary">قانون SLA جدید</button>`)}
      <div class="grid grid-4">${stat("◴","۱۴","قانون فعال")}${stat("!","۱","تشدید امروز","فوری","danger")}${stat("↻","هر ۱۵ دقیقه","اجرای Cron")}${stat("✓","۹۲٪","رعایت این ماه")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>عنوان قانون</th><th>منبع</th><th>شرط شروع</th><th>مهلت</th><th>هشدار</th><th>تشدید</th><th>وضعیت</th><th></th></tr></thead><tbody>${["تصمیم مرخصی ساعتی","رسیدگی مغایرت حضور","ارجاع نامه داخلی","تأیید گزارش کار","بازبینی OCR","اصلاح فرم بازگشتی"].map((x,i)=>`<tr><td class="title-cell"><strong>${x}</strong><small>SLA-${100+i}</small></td><td>${["تأیید","حضور","مکاتبات","گزارش کار","اسناد","فرم"][i]}</td><td>${["ایجاد line","ثبت تعارض","ایجاد ارجاع","ارسال گزارش","خطای job","بازگشایی ثبت"][i]}</td><td>${[4,8,24,12,2,24][i]} ساعت</td><td>${[1,2,6,3,.5,6][i]} ساعت قبل</td><td>${i%2?"مدیر واحد":"سرپرست"}</td><td>${badge("فعال","green")}</td><td><button class="btn btn-sm">ویرایش</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderDocumentSettings(){
    return `<div class="page">${pageHeader("ذخیره‌سازی و OCR","پیکربندی backend، ارائه‌دهنده OCR، retention، retry و پایش خطا.","CAS Document Core",`<button class="btn btn-primary">افزودن backend</button>`)}
      <div class="grid grid-3">${card("ذخیره‌سازی اصلی",`<div class="guard-selected"><div class="task-source">▱</div><div><h3>Local Secure Storage</h3><p>/var/lib/odoo/cas_documents</p></div>${badge("فعال","green")}</div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>حجم مصرف</span><strong>۱۸.۴ GB</strong></div><div class="kv"><span>رمزنگاری</span><strong>در سطح دیسک</strong></div><div class="kv"><span>آخرین بررسی</span><strong>امروز ۰۶:۰۰</strong></div></div>`)}${card("ارائه‌دهنده OCR",`<div class="guard-selected"><div class="task-source">◉</div><div><h3>OCR سازمانی</h3><p>صف پردازش داخلی</p></div>${badge("سالم","green")}</div><div class="kv-grid" style="margin-top:14px"><div class="kv"><span>Timeout</span><strong>۱۲۰ ثانیه</strong></div><div class="kv"><span>Retry</span><strong>۳ بار</strong></div><div class="kv"><span>کیفیت میانگین</span><strong>۹۱٪</strong></div></div>`)}${card("سیاست نگهداری",`<div class="field"><label>نسخه‌های سند رسمی</label><select><option>نگهداری دائمی</option></select></div><div class="field" style="margin-top:8px"><label>فایل موقت OCR</label><select><option>حذف پس از ۳۰ روز</option></select></div><div class="field" style="margin-top:8px"><label>نابودی کنترل‌شده</label><select><option>فقط مدیر اسناد + دلیل</option></select></div>`)} </div>
      <div class="status-panel" style="margin-top:18px"><div class="status-item"><span class="status-light"></span><div><strong>دسترسی مسیر ذخیره</strong><small>خواندن/نوشتن موفق</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>صف OCR</strong><small>۳ worker فعال</small></div></div><div class="status-item"><span class="status-light warn"></span><div><strong>پشتیبان‌گیری</strong><small>آخرین نسخه ۲۲ ساعت قبل</small></div></div></div>
    </div>`;
  }

  function renderJalaliCenter(){
    return `<div class="page">${pageHeader("مرکز تاریخ جلالی","پل‌های ورودی، HR، Chatter، جست‌وجو و QWeb؛ ذخیره همچنان تاریخ استاندارد Odoo و UTC است.","CAS Jalali Suite",`<button class="btn">اجرای آزمون timezone</button>`)}
      <div class="status-panel">${[["cas_jalali","Picker و field","online"],["cas_jalali_hr","Timeline کارکنان","online"],["cas_jalali_mail","Chatter و tracking","online"],["cas_jalali_search","فیلتر بازه","online"],["cas_jalali_qweb","PDF و گزارش","online"],["cas_jalali_suite","هماهنگی نصب","online"]].map(x=>`<div class="status-item"><span class="status-light"></span><div><strong dir="ltr">${x[0]}</strong><small>${x[1]} • نسخه 19.0.2.1.0</small></div><button class="mini-btn">✓</button></div>`).join("")}</div>
      <div class="grid grid-3" style="margin-top:18px">${card("آزمایش ورودی تاریخ",`<div class="field"><label>تاریخ جلالی</label><input value="۱۴۰۵/۰۴/۲۷" /></div><div class="field" style="margin-top:9px"><label>تاریخ و ساعت</label><input value="۱۴۰۵/۰۴/۲۷ ۰۹:۴۵" /></div><div class="kv" style="margin-top:12px"><span>مقدار RPC/ORM</span><strong dir="ltr">2026-07-18 06:15:00 UTC</strong></div>`)}${card("آزمایش فیلتر شمسی",`<div class="field"><label>فیلد</label><select><option>تاریخ ایجاد</option></select></div><div class="form-grid" style="margin-top:9px"><div class="field"><label>از</label><input value="۱۴۰۵/۰۴/۰۱" /></div><div class="field"><label>تا</label><input value="۱۴۰۵/۰۴/۳۱" /></div></div><div class="kv" style="margin-top:12px"><span>Domain استاندارد</span><strong dir="ltr" style="font-size:9px">[('create_date','&gt;=','2026-06-22'), ...]</strong></div>`)}${card("پیش‌نمایش QWeb",`<div style="border:1px solid var(--border);border-radius:12px;padding:15px;background:#fff"><strong style="font-size:12px">گزارش رسمی</strong><p style="font-size:10px;color:var(--ink-500)">تاریخ صدور: ۲۷ تیر ۱۴۰۵</p><p style="font-size:10px;color:var(--ink-500)">زمان: ۰۹:۴۵ به وقت تهران</p></div><div class="kv" style="margin-top:12px"><span>گزینه خروجی ماشین</span><strong dir="ltr">cas_gregorian = false</strong></div>`)} </div>
    </div>`;
  }

  function renderSystemHealth(){
    return `<div class="page">${pageHeader("سلامت، امنیت و ممیزی سامانه","وضعیت ماژول‌ها، Cron، asset، چندشرکتی، مسیرهای اختیاری و رخدادهای فنی.","CAS Core / Workspace",`<button class="btn">دریافت گزارش سلامت</button><button class="btn btn-primary" data-action="run-health">اجرای بررسی کامل</button>`)}
      <div class="grid grid-4">${stat("✓","۲۴/۲۴","ماژول نصب‌شده")}${stat("↻","۸","Cron فعال")}${stat("⚙","۰","خطای بحرانی")}${stat("◫","۲","هشدار پیکربندی","نیازمند بررسی","warn")}</div>
      <div class="status-panel" style="margin-top:18px">${[["هسته Odoo 19 Community","سالم","ok"],["Assetهای Workspace و RTL","کامپایل شده","ok"],["Record Rule چندشرکتی","پوشش کامل","ok"],["Adapterهای Action Hub","۲ مورد نیازمند تست","warn"],["Storage اسناد","فعال و قابل نوشتن","ok"],["پشتیبان OCR","عدم اتصال fallback","warn"],["Cron تشدید SLA","آخرین اجرا ۴ دقیقه قبل","ok"],["تقویم جلالی و timezone","آزمون موفق","ok"],["مسیرهای اختیاری Workspace","unavailable کنترل‌شده","ok"]].map(x=>`<div class="status-item"><span class="status-light ${x[2]==="warn"?"warn":""}"></span><div><strong>${x[0]}</strong><small>${x[1]}</small></div><button class="mini-btn">›</button></div>`).join("")}</div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2"><div class="card-header"><h3 class="card-title">آخرین رخدادهای فنی</h3><button class="btn btn-sm">مشاهده Log</button></div><div class="card-body"><div class="timeline"><div class="timeline-item"><h5>همگام‌سازی Action Hub تکمیل شد</h5><p>۳۲۴ آیتم بررسی، ۱۲ مورد به‌روزرسانی</p><time>امروز ۰۹:۴۵</time></div><div class="timeline-item"><h5>پردازش OCR با retry تکمیل شد</h5><p>سند DOC/۱۴۰۵/۲۲۴ در تلاش دوم</p><time>امروز ۰۹:۳۸</time></div><div class="timeline-item"><h5>آزمون مرز نیمه‌شب شیفت</h5><p>شیفت ۱۹:۳۰ تا ۰۷:۳۰ بدون خطا</p><time>امروز ۰۶:۱۰</time></div><div class="timeline-item"><h5>پشتیبان‌گیری پایگاه داده</h5><p>cas_odoo_dev • موفق</p><time>امروز ۰۲:۰۰</time></div></div></div></section>${card("اثر تغییر و انتشار",`<div class="progress-list"><div class="progress-item done"><span class="progress-dot">✓</span>نصب تمیز آزمایشی</div><div class="progress-item done"><span class="progress-dot">✓</span>Upgrade ماژول‌ها</div><div class="progress-item done"><span class="progress-dot">✓</span>QA دسکتاپ و موبایل</div><div class="progress-item active"><span class="progress-dot">۴</span>تست چندشرکتی</div><div class="progress-item"><span class="progress-dot">۵</span>تأیید انتشار</div></div>`)} </div>
    </div>`;
  }

  function renderWorkspaceSettings(){
    return `<div class="page">${pageHeader("تنظیمات Workspace","ناوبری نقش‌محور، صفحه آغاز، رفتار drawer، pagination و ماژول‌های اختیاری.","CAS Workspace",`<button class="btn btn-primary" data-action="save-settings">ذخیره تنظیمات</button>`)}
      <div class="grid grid-3"><section class="card span-2"><div class="card-header"><h3 class="card-title">رفتار پوسته</h3></div><div class="card-body"><div class="form-grid"><div class="field"><label>صفحه آغاز کاربران</label><select><option>خانه نقش‌محور</option></select></div><div class="field"><label>تعداد ردیف صفحه</label><select><option>۲۵ ردیف</option><option>۵۰ ردیف</option></select></div><div class="field"><label>جزئیات رکورد</label><select><option>Drawer سمت چپ</option></select></div><div class="field"><label>رفتار route اختیاری</label><select><option>نمایش حالت unavailable</option></select></div><div class="field full"><label>جست‌وجوی سراسری</label><div style="display:flex;gap:14px;flex-wrap:wrap"><label style="font-size:11px"><input type="checkbox" checked /> اقدام‌ها</label><label style="font-size:11px"><input type="checkbox" checked /> مکاتبات</label><label style="font-size:11px"><input type="checkbox" checked /> اسناد</label><label style="font-size:11px"><input type="checkbox" checked /> فرم‌ها</label></div></div></div></div></section>${card("قرارداد UX",`<div class="status-panel" style="grid-template-columns:1fr"><div class="status-item"><span class="status-light"></span><div><strong>Sidebar مستقل</strong><small>scroll جدا از محتوای اصلی</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>موبایل off-canvas</strong><small>بسته‌شدن بعد از انتخاب route</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>جدول عریض</strong><small>scroll افقی داخل container</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>RTL / LTR</strong><small>کد و شناسه‌ها جهت مستقل دارند</small></div></div></div>`)} </div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><h3 class="card-title">آداپترهای صفحه</h3></div><div class="table-wrap"><table class="data-table"><thead><tr><th>Route</th><th>مدل منبع</th><th>فیلدهای مجاز</th><th>جست‌وجو</th><th>وضعیت نصب</th><th>امنیت</th></tr></thead><tbody>${[["my-actions","cas.action.item","۸","عنوان/منبع","نصب","بدون sudo"],["correspondence","cas.correspondence.letter","۱۰","موضوع/شماره","نصب","read check"],["documents","cas.document","۹","عنوان/برچسب","نصب","منبع + سند"],["my-kardex","cas.kardex.day","۱۲","تاریخ","نصب","employee scope"],["ocr-queue","cas.document.ocr.job","۷","عنوان سند","اختیاری","manager only"]].map(x=>`<tr><td dir="ltr">${x[0]}</td><td dir="ltr">${x[1]}</td><td>${x[2]}</td><td>${x[3]}</td><td>${badge(x[4],x[4]==="نصب"?"green":"orange")}</td><td>${x[5]}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderRoleMatrix(){
    const keyRoutes = ["home","my-actions","approvals","form-catalog","forms-admin","form-builder","workflow-designer","correspondence","secretariat-register","documents","guard","shift-planning","attendance-review","my-kardex","kardex-periods","work-reports","system-health"];
    return `<div class="page">${pageHeader("ماتریس نقش و صفحه","نمایش پوشش دسترسی رابط؛ مجوز نهایی همچنان از ACL، Record Rule و کنترل متد سمت سرور می‌آید.","راهبری دسترسی Workspace")}
      <div class="kardex-matrix"><table class="kardex-table"><thead><tr><th>صفحه / نقش</th>${Object.values(D.roles).map(r=>`<th>${r.label}</th>`).join("")}</tr></thead><tbody>${keyRoutes.map(route=>`<tr><td>${routeMeta(route).label}<br><small dir="ltr">${route}</small></td>${Object.keys(D.roles).map(role=>`<td>${(D.routes[route]?.roles||[]).includes(role)?'<span class="badge badge-green">مجاز</span>':'<span style="color:var(--ink-300)">—</span>'}</td>`).join("")}</tr>`).join("")}</tbody></table></div>
      <div class="card card-pad" style="margin-top:16px"><strong style="font-size:12px">اصل امنیتی</strong><p style="font-size:10px;color:var(--ink-500);margin-bottom:0">پنهان‌کردن منو امنیت ایجاد نمی‌کند. این ماتریس فقط تجربه ناوبری را نشان می‌دهد؛ درخواست مستقیم، RPC، export و batch باید همان محدودیت‌های شرکت، مالک، مسئول و حوزه را پاس کنند.</p></div>
    </div>`;
  }


  function renderAdminCenter(){
    return `<div class="page">${pageHeader("مرکز مدیریت CAS","مدیریت متمرکز کاربران، ساختار سازمانی، نقش‌ها، انتساب‌ها و تنظیمات دامنه‌ای.","راهبری سامانه",`<button class="btn" data-route="audit-log">رویدادهای اخیر</button><button class="btn btn-primary" data-action="new-user">ایجاد کاربر</button>`)}
      <div class="admin-notice"><strong>حالت آزمایشی دسترسی پویا</strong><span>منوها از نقش‌های امنیتی کاربر انتخاب‌شده Resolve می‌شوند. در Production، اطلاعات از session و Backend دریافت خواهد شد.</span></div>
      <div class="grid grid-4">${stat("♙","۸۶","کاربر","۳ حساب ناقص","warn")}${stat("◈","۵","نقش فعال","۱ حساس")}${stat("⌘","۷","واحد سازمانی","۱ بدون مدیر","danger")}${stat("↹","۳","انتساب موقت","۱ نزدیک انقضا","warn")}</div>
      <div class="management-grid" style="margin-top:18px">
        ${[["♙","کاربران و کارکنان","اتصال حساب‌ها به پرونده پرسنلی و مدیریت وضعیت حساب","user-management"],["◈","نقش‌ها و دسترسی‌ها","تعریف نقش، حوزه و منشأ دسترسی مؤثر","access-roles"],["⌘","ساختار سازمانی","شرکت، سایت، معاونت، مدیریت، واحد و زیرواحد","organization"],["▣","سمت‌ها و جایگاه‌ها","جایگاه سازمانی، متصدی، مدیر مستقیم و نقش پیش‌فرض","positions"],["↹","انتساب و جانشینی","مسئولیت اصلی، جانبی، موقت و جانشینی تاریخ‌دار","assignments"],["⚙","مرکز تنظیمات","تنظیمات مستقل هر حوزه سامانه","settings-hub"]].map(x=>`<button class="management-card" data-route="${x[3]}"><span class="management-icon">${x[0]}</span><strong>${x[1]}</strong><small>${x[2]}</small><em>ورود به بخش ‹</em></button>`).join("")}
      </div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2"><div class="card-header"><h3 class="card-title">نیازمند توجه</h3><button class="btn btn-sm">مشاهده همه</button></div><div class="card-body"><div class="task-list">
        ${[["!","۴ کارمند حساب کاربری ندارند","منابع انسانی","orange"],["!","واحد فناوری اطلاعات مدیر مشخص ندارد","ساختار سازمانی","red"],["◷","دسترسی موقت امیر نادری سه روز دیگر منقضی می‌شود","دسترسی‌ها","orange"],["◈","نقش طراح فرم یک عضو غیرفعال دارد","نقش‌ها","purple"]].map(x=>`<div class="task-item"><div class="task-source">${x[0]}</div><div><h4>${x[1]}</h4><p>${x[2]}</p></div>${badge("بررسی",x[3])}</div>`).join("")}
      </div></section>${card("عملیات سریع",`<div class="quick-stack"><button class="btn" data-action="new-user">ایجاد کاربر</button><button class="btn" data-route="organization">تعریف واحد سازمانی</button><button class="btn" data-route="positions">ایجاد سمت</button><button class="btn" data-route="access-roles">تعریف نقش</button><button class="btn" data-route="assignments">ثبت جانشینی</button></div>`)}</div>
    </div>`;
  }

  function renderUserManagement(){
    const rows=Object.values(D.users);
    return `<div class="page">${pageHeader("مدیریت کاربران و کارکنان","حساب ورود از پرونده پرسنلی جداست و ارتباط آن‌ها به‌صورت شفاف مدیریت می‌شود.","مرکز مدیریت CAS",`<button class="btn">خروجی کاربران</button><button class="btn btn-primary" data-action="new-user">ایجاد کاربر</button>`)}
      <div class="grid grid-4">${stat("♙","۸۶","حساب فعال")}${stat("⚠","۳","بدون اتصال","نیازمند اصلاح","danger")}${stat("◈","۱۲","کاربر چندنقشی")}${stat("◷","۲","دسترسی موقت","نزدیک انقضا","warn")}</div>
      <div class="toolbar" style="margin-top:18px"><div class="toolbar-start"><div class="search-box">⌕<input placeholder="نام، کد پرسنلی، ایمیل یا نام کاربری..." /></div></div><div class="toolbar-end"><select class="select"><option>همه شرکت‌ها</option></select><select class="select"><option>همه واحدها</option></select><select class="select"><option>همه نقش‌ها</option></select><select class="select"><option>همه وضعیت‌ها</option></select></div></div>
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>کاربر</th><th>کارمند مرتبط</th><th>واحد / سمت</th><th>نقش‌های مؤثر</th><th>آخرین ورود</th><th>وضعیت</th><th>عملیات</th></tr></thead><tbody>${rows.map((u,i)=>`<tr><td class="title-cell"><strong>${u.name}</strong><small dir="ltr">${u.id}</small></td><td>${u.employee?`${u.employee}`:badge("بدون اتصال","red")}</td><td class="title-cell"><strong>${u.unit}</strong><small>${u.job}</small></td><td>${u.securityRoles.slice(0,3).map(r=>badge(D.roles[r]?.label||r,r==="system_admin"?"red":"blue")).join(" ")}</td><td>${u.lastLogin}</td><td>${badge(u.active?"فعال":"غیرفعال",u.active?"green":"red")}</td><td><button class="btn btn-sm" data-action="user-detail" data-user="${u.id}">مشاهده</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderAccessRoles(){
    return `<div class="page">${pageHeader("نقش‌ها و دسترسی‌ها","نقش امنیتی از سمت سازمانی جداست؛ مجوز مؤثر می‌تواند مستقیم، ارثی، موقت یا ناشی از جانشینی باشد.","مرکز مدیریت CAS",`<button class="btn">گزارش دسترسی مؤثر</button><button class="btn btn-primary" data-action="new-role">تعریف نقش</button>`)}
      <div class="grid grid-4">${stat("◈","۵","نقش فعال")}${stat("♙","۱۰۲","انتساب نقش")}${stat("⌘","۷","حوزه سازمانی")}${stat("!","۱","نقش حساس","بازبینی دوره‌ای","warn")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>نقش</th><th>نوع</th><th>حوزه پیش‌فرض</th><th>تعداد اعضا</th><th>منشأ</th><th>وضعیت</th><th></th></tr></thead><tbody>${D.accessRoles.map(r=>`<tr><td class="title-cell"><strong>${r.name}</strong><small dir="ltr">${r.id}</small></td><td>${badge(r.type,r.type==="سیستمی"?"purple":"blue")}</td><td>${r.scope}</td><td>${r.members}</td><td>${r.source}</td><td>${badge(r.status,r.status==="حساس"?"red":"green")}</td><td><button class="btn btn-sm" data-action="role-detail" data-role="${r.id}">جزئیات</button></td></tr>`).join("")}</tbody></table></div></section>
      <div class="grid grid-3" style="margin-top:18px">${card("اصل امنیتی",`<p class="muted-copy">پنهان‌شدن منو فقط UX است. Backend باید ACL، Record Rule، کنترل شرکت و کنترل متد را مستقل اعمال کند.</p>${badge("بدون sudo","green")}`)}${card("منابع دسترسی",`<div class="chip-cloud">${["گروه Odoo","سمت سازمانی","واحد","انتساب مستقیم","جانشینی","دسترسی موقت"].map(x=>badge(x,"blue")).join(" ")}</div>`)}${card("🔵 در آینده",`<p class="muted-copy">شبیه‌سازی دسترسی، مقایسه دو کاربر، بازبینی دوره‌ای و پیشنهاد خودکار نقش.</p>`)} </div>
    </div>`;
  }

  function renderOrganization(){
    return `<div class="page">${pageHeader("ساختار سازمانی","کنترل سلسله‌مراتب شرکت، سایت، معاونت، مدیریت، دپارتمان، واحد و زیرواحد.","مرکز مدیریت CAS",`<button class="btn">نمای درختی</button><button class="btn btn-primary" data-action="new-unit">واحد جدید</button>`)}
      <div class="grid grid-4">${stat("⌘","۷","واحد فعال")}${stat("♙","۸۶","عضو سازمانی")}${stat("!","۱","واحد بدون مدیر","نیازمند اصلاح","danger")}${stat("▣","۴","سطح سلسله‌مراتب")}</div>
      <div class="org-layout" style="margin-top:18px"><section class="card"><div class="card-header"><h3 class="card-title">درخت سازمانی</h3></div><div class="card-body"><div class="org-tree">${D.orgUnits.map((u,i)=>`<button class="org-node level-${u.parent?1:0}" data-action="unit-detail" data-unit="${u.id}"><span>${u.type}</span><strong>${u.name}</strong><small>${u.members} عضو • مدیر: ${u.manager}</small></button>`).join("")}</div></div></section><section class="card"><div class="card-header"><h3 class="card-title">فهرست واحدها</h3></div><div class="table-wrap"><table class="data-table"><thead><tr><th>واحد</th><th>نوع</th><th>مدیر</th><th>اعضا</th><th>وضعیت</th></tr></thead><tbody>${D.orgUnits.map(u=>`<tr><td>${u.name}</td><td>${u.type}</td><td>${u.manager}</td><td>${u.members}</td><td>${badge(u.status,u.status==="فعال"?"green":"red")}</td></tr>`).join("")}</tbody></table></div></section></div>
    </div>`;
  }

  function renderPositions(){
    return `<div class="page">${pageHeader("سمت‌ها و جایگاه‌های سازمانی","سمت سازمانی، متصدی، مدیر مستقیم و نقش‌های پیش‌فرض بدون آمیختن با مجوز امنیتی.","مرکز مدیریت CAS",`<button class="btn btn-primary" data-action="new-position">ایجاد جایگاه</button>`)}
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>کد</th><th>عنوان جایگاه</th><th>واحد</th><th>متصدی</th><th>مدیر مستقیم</th><th>نقش پیش‌فرض</th><th>وضعیت</th></tr></thead><tbody>${D.positions.map(p=>`<tr><td dir="ltr">${p.code}</td><td><strong>${p.title}</strong></td><td>${p.unit}</td><td>${p.holder}</td><td>${p.manager}</td><td>${p.roles}</td><td>${badge(p.status,p.status==="خالی"?"orange":p.status==="چندمتصدی"?"purple":"green")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderAssignments(){
    return `<div class="page">${pageHeader("انتساب‌ها و جانشینی‌ها","مدیریت مسئولیت‌های اصلی، جانبی، موقت و جانشینی با بازه اعتبار و حوزه روشن.","مرکز مدیریت CAS",`<button class="btn btn-primary" data-action="new-assignment">انتساب جدید</button>`)}
      <div class="grid grid-3">${stat("↹","۳","انتساب فعال")}${stat("◷","۱","نزدیک انقضا","سه روز","warn")}${stat("✓","۰","تداخل حل‌نشده")}</div>
      <section class="card table-card" style="margin-top:18px"><div class="table-wrap"><table class="data-table"><thead><tr><th>فرد</th><th>نوع</th><th>مسئولیت / نقش</th><th>حوزه</th><th>شروع</th><th>پایان</th><th>وضعیت</th></tr></thead><tbody>${D.assignments.map(a=>`<tr><td><strong>${a.person}</strong></td><td>${a.kind}</td><td>${a.target}</td><td>${a.scope}</td><td>${a.from}</td><td>${a.to}</td><td>${badge(a.status,a.status==="فعال"?"green":"orange")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderSettingsHub(){
    const domains=[["عمومی","زبان، منطقه زمانی، شرکت و رفتار عمومی"],["کاربران و امنیت","حساب، رمز، نشست و سیاست دسترسی"],["ساختار سازمانی","شرکت، سایت، واحد و سمت"],["فرم‌ها","انتشار، نسخه و اعتبارسنجی"],["گردش‌کارها","SLA، انتقال و قواعد اجرا"],["تأییدها","مراحل، جانشینی و تصمیم"],["مکاتبات","شماره‌گذاری، محرمانگی و قالب"],["اسناد و OCR","Storage، نسخه و پردازش متن"],["شیفت و حضور","سیاست شیفت، دستگاه و تطبیق"],["کاردکس","دوره، قفل و محاسبه"],["اعلان‌ها","کانال‌ها و الگوها"],["یکپارچه‌سازی‌ها","Odoo، Nextcloud و سرویس‌ها"]];
    return `<div class="page">${pageHeader("مرکز تنظیمات","تنظیمات بر اساس حوزه تفکیک شده‌اند؛ هیچ صفحه واحد شلوغی برای تمام سامانه وجود ندارد.","مرکز مدیریت CAS")}
      <div class="settings-grid">${domains.map((d,i)=>`<button class="setting-tile" data-action="domain-settings"><span>${["⚙","♙","⌘","▤","⇄","◎","✉","▱","◷","▦","◔","⌁"][i]}</span><strong>${d[0]}</strong><small>${d[1]}</small>${i>8?'<em>🔵 بخشی در آینده</em>':''}</button>`).join("")}</div>
    </div>`;
  }

  function renderAccessReport(){
    return `<div class="page">${pageHeader("گزارش دسترسی‌های مؤثر","مشاهده اینکه هر مجوز از کجا آمده و در چه حوزه‌ای اعمال می‌شود.","مرکز مدیریت CAS",`<button class="btn">خروجی Excel</button>`)}
      <div class="toolbar"><div class="search-box">⌕<input placeholder="انتخاب کاربر..." value="رضا اسدی" /></div><select class="select"><option>تمام منابع دسترسی</option></select></div>
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>قابلیت</th><th>عملیات</th><th>حوزه</th><th>منشأ</th><th>اعتبار</th><th>نتیجه</th></tr></thead><tbody>${[["گزارش‌های تیم","مشاهده","تولید سایت","سمت سرپرست تولید","دائم","مجاز"],["تأیید مرخصی","تصمیم","اعضای مستقیم","نقش سرپرست حوزه","دائم","مجاز"],["مدیریت کاربران","ویرایش","شرکت","—","—","غیرمجاز"],["ثبت تردد","ایجاد","درب شمالی","—","—","غیرمجاز"]].map(x=>`<tr>${x.map((v,i)=>`<td>${i===5?badge(v,v==="مجاز"?"green":"red"):v}</td>`).join("")}</tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderAuditLog(){
    return `<div class="page">${pageHeader("رویدادها و ممیزی","تاریخچه قابل فهم تغییرات مدیریتی و امنیتی با بازیگر، زمان و نتیجه.","مرکز مدیریت CAS",`<button class="btn">دریافت گزارش</button>`)}
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>زمان</th><th>رویداد</th><th>انجام‌دهنده</th><th>رکورد</th><th>نتیجه</th><th>IP / زمینه</th></tr></thead><tbody>${[["امروز ۱۰:۳۰","نقش سرپرست تولید ویرایش شد","مدیر سیستم","ROLE/supervisor","موفق","Workspace"],["امروز ۰۹:۱۵","کاربر جدید ایجاد شد","نیلوفر کریمی","USR/0087","موفق","HR"],["دیروز ۱۶:۴۰","دسترسی موقت ثبت شد","مدیر اداری","ASN/0042","در انتظار تأیید","CAS"],["دیروز ۱۴:۱۲","تلاش دسترسی غیرمجاز","کاربر مهمان","admin-center","مسدود","10.10.2.8"]].map(x=>`<tr><td>${x[0]}</td><td><strong>${x[1]}</strong></td><td>${x[2]}</td><td dir="ltr">${x[3]}</td><td>${badge(x[4],x[4]==="موفق"?"green":x[4]==="مسدود"?"red":"orange")}</td><td dir="ltr">${x[5]}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }


  function renderRequestCenter(){
    const requests=[
      ["مرخصی","ثبت مرخصی روزانه، ساعتی یا نیم‌روزی","◫","attendance-requests"],
      ["مأموریت","ثبت مأموریت درون‌شهری یا برون‌شهری","⌖","attendance-requests"],
      ["اضافه‌کاری","درخواست اضافه‌کاری قبل یا بعد از شیفت","＋","overtime"],
      ["خرید و تأمین","درخواست خرید کالا، قطعه یا خدمت","▤","form-runtime"],
      ["خدمات سازمانی","درخواست IT، خدمات عمومی یا حمل‌ونقل","⚙","form-runtime"],
      ["اعلام خرابی","ثبت خرابی دستگاه یا زیرساخت","!","form-runtime"]
    ];
    return `<div class="page">${pageHeader("ثبت درخواست","یک نقطه واحد برای شروع همه درخواست‌های مجاز؛ سامانه فرم و گردش‌کار مناسب را انتخاب می‌کند.","فضای شخصی")}
      <div class="toolbar"><div class="search-box" style="min-width:320px">⌕<input placeholder="چه درخواستی می‌خواهید ثبت کنید؟" /></div><select class="select"><option>همه دسته‌ها</option><option>منابع انسانی</option><option>خدمات</option><option>عملیات</option></select></div>
      <div class="grid grid-3">${requests.map(x=>`<button class="card card-pad" style="text-align:right;border:1px solid var(--ink-100);cursor:pointer" data-route="${x[3]}"><div class="stat-icon" style="margin-bottom:12px">${x[2]}</div><h3 class="card-title">${x[0]}</h3><p class="card-subtitle" style="line-height:2">${x[1]}</p><span class="badge badge-blue">شروع درخواست</span></button>`).join("")}</div>
      <section class="card" style="margin-top:18px"><div class="card-header"><div><h3 class="card-title">درخواست‌های پرتکرار شما</h3><div class="card-subtitle">بر اساس دسترسی و سابقه استفاده؛ بدون نمایش ماژول فنی پشت صحنه</div></div></div><div class="card-body"><div class="chip-cloud">${["مرخصی ساعتی","مأموریت روزانه","درخواست خدمات IT","اعلام خرابی"].map(x=>`<button class="btn" data-route="form-runtime">${x}</button>`).join("")}</div></div></section>
    </div>`;
  }

  function renderRequestTracking(){
    return `<div class="page">${pageHeader("پیگیری درخواست‌ها","همه درخواست‌های شما، مستقل از ماژول منبع، با وضعیت و اقدام بعدی.","فضای شخصی",`<button class="btn btn-primary" data-route="request-center">درخواست جدید</button>`)}
      <div class="grid grid-4">${stat("◫","۲","پیش‌نویس")}${stat("◷","۵","در جریان")}${stat("↩","۱","برگشت‌خورده","نیازمند اصلاح","warn")}${stat("✓","۱۸","تکمیل‌شده")}</div>
      <div class="toolbar" style="margin-top:18px"><div class="search-box">⌕<input placeholder="شماره، عنوان یا نوع درخواست..." /></div><select class="select"><option>همه وضعیت‌ها</option><option>در جریان</option><option>برگشت‌خورده</option></select></div>
      <section class="card table-card"><div class="table-wrap"><table class="data-table"><thead><tr><th>درخواست</th><th>شماره</th><th>تاریخ</th><th>مرحله فعلی</th><th>وضعیت</th><th>اقدام بعدی</th></tr></thead><tbody>${D.submissions.concat([{form:"مأموریت روزانه",number:"REQ-1405-0091",version:"v1",owner:"مهدی رضایی",date:"امروز",state:"برگشت‌خورده"}]).map((x,i)=>`<tr><td class="title-cell"><strong>${x.form}</strong><small>${i%2?"منابع انسانی":"خدمات سازمانی"}</small></td><td dir="ltr">${x.number}</td><td>${x.date}</td><td>${i%3===0?"تأیید سرپرست":"بررسی واحد مسئول"}</td><td>${badge(x.state,x.state.includes("برگشت")?"orange":x.state.includes("تأیید")?"green":"blue")}</td><td><button class="btn btn-sm" data-action="submission-detail" data-index="${Math.min(i,D.submissions.length-1)}">مشاهده</button></td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderAttendanceHub(){
    return `<div class="page">${pageHeader("حضور و شیفت","شیفت امروز، ورود و خروج، کارکرد ماه و درخواست‌های اصلاح در یک صفحه.","فضای شخصی",`<button class="btn" data-route="shift-swaps">جابه‌جایی شیفت</button><button class="btn btn-primary" data-route="attendance-requests">درخواست اصلاح یا مرخصی</button>`)}
      <div class="grid grid-4">${stat("◷","روز ۰۷:۳۰–۱۹:۳۰","شیفت امروز")}${stat("⇩","۰۷:۵۸","ورود ثبت‌شده")}${stat("▦","۱۷۶:۳۰","کارکرد ماه")}${stat("⚠","۱","مغایرت باز","نیازمند پیگیری","warn")}</div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2"><div class="card-header"><div><h3 class="card-title">وضعیت امروز</h3><div class="card-subtitle">تطبیق برنامه شیفت و رخدادهای حضور</div></div>${badge("عادی","green")}</div><div class="card-body"><div class="timeline"><div class="timeline-item"><h5>شروع شیفت برنامه‌ریزی‌شده</h5><p>شیفت روز</p><time>۰۷:۳۰</time></div><div class="timeline-item"><h5>ورود از دستگاه درب اصلی</h5><p>تأییدشده</p><time>۰۷:۵۸</time></div><div class="timeline-item"><h5>پایان برنامه</h5><p>خروج هنوز ثبت نشده است</p><time>۱۹:۳۰</time></div></div></div></section>${card("عملیات سریع",`<div class="grid"><button class="btn" data-route="my-attendance">جزئیات حضور</button><button class="btn" data-route="my-shifts">تقویم شیفت</button><button class="btn" data-route="shift-swaps">درخواست جابه‌جایی</button><button class="btn" data-route="my-kardex">کاردکس ماه</button></div>`)} </div>
      <section class="card" style="margin-top:18px"><div class="card-header"><div><h3 class="card-title">هفت روز آینده</h3><div class="card-subtitle">برنامه منتشرشده و آخرین تغییرات</div></div></div><div class="card-body"><div class="grid grid-4">${["امروز • روز","فردا • روز","سه‌شنبه • شب","چهارشنبه • شب","پنجشنبه • استراحت","جمعه • استراحت","شنبه • روز"].map((x,i)=>`<div class="kv"><span>${x.split(" • ")[0]}</span><strong>${x.split(" • ")[1]}</strong>${i===0?badge("فعال","green"):""}</div>`).join("")}</div></div></section>
    </div>`;
  }

  function renderGuardWorkspace(){
    return `<div class="page">${pageHeader("ثبت و پایش تردد","فضای تخصصی نگهبانی برای ثبت سریع، جست‌وجو و مشاهده آخرین رخدادها.","فضای عملیاتی انتظامات",`<button class="btn" data-route="attendance-events">همه رخدادها</button>`)}
      <div class="grid grid-4">${stat("⇩","۲۷","ورود امروز")}${stat("⇧","۱۹","خروج امروز")}${stat("⚠","۳","رکورد ناقص","نیازمند توجه","danger")}${stat("◷","شب","شیفت جاری")}</div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2"><div class="card-header"><div><h3 class="card-title">ثبت ورود و خروج</h3><div class="card-subtitle">جست‌وجوی نام، کد پرسنلی، واحد یا خودرو؛ امکان اصلاح ساعت پیش از ثبت</div></div></div><div class="card-body"><div class="toolbar"><div class="search-box" style="flex:1">⌕<input placeholder="نام، کد پرسنلی یا پلاک خودرو..." /></div><select class="select"><option>همه واحدها</option><option>تولید سایت</option><option>اداری</option></select><input class="select" type="time" value="09:15" /></div><div class="guard-selected"><div class="person-photo">حم</div><div><h3>حسین مرادی</h3><p>انتظامات • EMP-0041</p></div>${badge("خارج از مجموعه","orange")}</div><div class="grid grid-2" style="margin-top:14px"><button class="btn btn-success" data-action="guard-entry">ثبت ورود</button><button class="btn btn-danger" data-action="guard-exit">ثبت خروج</button></div></div></section>${card("جست‌وجوی سریع",`<div class="grid"><button class="btn">اشخاص داخل مجموعه</button><button class="btn">خودروهای داخل مجموعه</button><button class="btn">مجوزهای امروز</button><button class="btn" data-route="work-report-new">گزارش نگهبانی</button></div>`)} </div>
      <section class="card table-card" style="margin-top:18px"><div class="card-header"><div><h3 class="card-title">آخرین رکوردها</h3><div class="card-subtitle">لاگ زنده رخدادهای ثبت‌شده</div></div></div><div class="table-wrap"><table class="data-table"><thead><tr><th>شخص</th><th>نوع</th><th>ساعت</th><th>واحد</th><th>دروازه</th><th>وضعیت</th></tr></thead><tbody>${guardLogs.slice(0,7).map((l,i)=>`<tr><td><strong>${l.name}</strong></td><td>${badge(l.type,l.type==="ورود"?"green":"orange")}</td><td>${l.time}</td><td>${D.people[i%D.people.length].unit}</td><td>${l.gate}</td><td>${badge(i===2?"نیازمند بررسی":"ثبت قطعی",i===2?"red":"green")}</td></tr>`).join("")}</tbody></table></div></section>
    </div>`;
  }

  function renderTeamCenter(){
    return `<div class="page">${pageHeader("تیم و درخواست‌ها","افراد حوزه، درخواست‌های نیازمند تصمیم، گزارش‌های روزانه و مغایرت‌های حضور.","حوزه مسئولیت",`<button class="btn" data-route="team-work-reports">گزارش‌های روزانه</button><button class="btn btn-primary" data-route="approvals">تصمیم‌های باز</button>`)}
      <div class="grid grid-4">${stat("👥","۲۴","عضو حوزه")}${stat("◎","۵","در انتظار تصمیم","۲ فوری","danger")}${stat("▤","۳","گزارش عقب‌افتاده","warn")}${stat("⚠","۲","مغایرت حضور")}</div>
      <div class="grid grid-3" style="margin-top:18px"><section class="card span-2"><div class="card-header"><h3 class="card-title">نیازمند اقدام شما</h3><button class="btn btn-sm" data-route="my-actions">مشاهده همه</button></div><div class="card-body">${actionRows(5)}</div></section>${card("دسترسی‌های حوزه",`<div class="grid"><button class="btn" data-route="attendance-review">مغایرت‌های حضور</button><button class="btn" data-route="shift-planning">برنامه شیفت</button><button class="btn" data-route="team-work-reports">گزارش‌های تیم</button><button class="btn" data-route="attendance-requests">درخواست‌های تیم</button></div>`)} </div>
    </div>`;
  }


  function taskFilter(task, index){
    if(taskView==="done") return task.done;
    if(taskView==="overdue") return !task.done && task.meta.includes("عقب");
    if(taskView==="upcoming") return !task.done && (task.meta.includes("فردا") || task.meta.includes("هفته"));
    return !task.done && !task.meta.includes("فردا");
  }

  function renderPersonalTasksPage(){
    const filtered=personalTasks.map((t,i)=>({...t,_index:i})).filter(taskFilter).filter(t=>!activeTaskCategory || t.source===activeTaskCategory);
    return `<div class="page v6-page">${pageHeader("کارهای من","فهرست ساده و شخصی کارها؛ بدون پروژه، مرحله و Kanban.","فضای شخصی",`<button class="btn" data-action="task-quick-capture">ثبت سریع</button><button class="btn btn-primary" data-action="add-personal-task">+ کار جدید</button>`)}
      <section class="v6-command-summary">
        <div><strong>${num(personalTasks.filter(x=>!x.done).length)}</strong><span>کار باز</span></div>
        <div><strong>${num(personalTasks.filter(x=>!x.done&&x.meta.includes("عقب")).length)}</strong><span>عقب‌افتاده</span></div>
        <div><strong>${num(personalTasks.filter(x=>x.done).length)}</strong><span>انجام‌شده</span></div>
        <button data-action="task-quick-capture"><span>＋</span><div><strong>یادداشت کن، بعداً مرتب کن</strong><small>فقط عنوان کار را بنویس</small></div></button>
      </section>
      <div class="v6-task-layout">
        <aside class="card v6-filter-panel">
          <div class="card-header"><h3 class="card-title">نماها</h3></div>
          <div class="card-body v6-filter-list">
            ${[["today","امروز","۳"],["upcoming","آینده","۱"],["overdue","عقب‌افتاده","۱"],["done","انجام‌شده","۰"]].map(x=>`<button class="${taskView===x[0]?"active":""}" data-action="task-view" data-value="${x[0]}"><span>${x[1]}</span><b>${x[2]}</b></button>`).join("")}
            <hr><div class="filter-caption category-caption"><span>دسته‌ها</span><button class="category-add" data-action="add-task-category" title="افزودن دسته شخصی">＋</button></div>
            <button class="${activeTaskCategory===""?"active":""}" data-action="task-category-filter" data-value=""><span>همه دسته‌ها</span></button>
            ${systemTaskCategories.map(x=>`<button class="${activeTaskCategory===x?"active":""}" data-action="task-category-filter" data-value="${esc(x)}"><span>● ${esc(x)}</span><small class="category-lock" title="دسته سیستمی">قفل</small></button>`).join("")}
            ${personalTaskCategories.map(x=>`<div class="category-personal-row"><button class="${activeTaskCategory===x?"active":""}" data-action="task-category-filter" data-value="${esc(x)}"><span>● ${esc(x)}</span></button><button class="category-more" data-action="edit-task-category" data-value="${esc(x)}" title="ویرایش یا حذف">•••</button></div>`).join("")}
          </div>
        </aside>
        <section class="card v6-task-main">
          <div class="card-header"><div><h3 class="card-title">${({today:"امروز",upcoming:"آینده",overdue:"کارهای عقب‌افتاده",done:"انجام‌شده"})[taskView]}</h3><div class="card-subtitle">کار را انجام‌شده علامت بزن، زمان‌بندی کن یا از آن گزارش فعالیت بساز.</div></div><div class="segmented"><button class="active">فهرست</button><button disabled title="در CAS از Kanban استفاده نمی‌شود">Kanban ×</button></div></div>
          <div class="card-body">
            <div class="v6-task-create"><input id="inlineTaskTitle" placeholder="یک کار جدید بنویس و Enter بزن..." /><button class="btn btn-primary" data-action="inline-task-add">افزودن</button></div>
            <div class="v6-task-list">${filtered.length?filtered.map(t=>`<article class="v6-task-row ${t.priority==="high"?"priority-high":""}">
              <button class="v6-task-check ${t.done?"checked":""}" data-action="toggle-task-real" data-index="${t._index}">${t.done?"✓":""}</button>
              <div class="v6-task-content"><h4>${esc(t.title)}</h4><div><span>◷ ${esc(t.meta)}</span>${badge(t.source,t.source==="تفویض‌شده"?"purple":t.source==="پیگیری"?"orange":"blue")}</div></div>
              <div class="v6-task-actions"><button data-action="schedule-task" data-index="${t._index}">تقویم</button><button data-action="task-to-report" data-index="${t._index}">ثبت گزارش انجام</button><button data-action="move-tomorrow" data-index="${t._index}">فردا</button><button>•••</button></div>
            </article>`).join(""):`<div class="empty-state"><div class="empty-icon">✓</div><h3>در این نما کاری وجود ندارد</h3><p>می‌توانی یک کار جدید اضافه کنی.</p></div>`}</div>
          </div>
        </section>
      </div>
    </div>`;
  }

  function calendarHeader(){
    return `<div class="v6-calendar-toolbar">
      <div class="calendar-nav"><button data-action="calendar-prev">‹</button><button data-action="calendar-today">امروز</button><button data-action="calendar-next">›</button><strong>۲۷ تیر تا ۲ مرداد ۱۴۰۵</strong></div>
      <div class="calendar-main-switch">${[["day","روز"],["week","هفته"],["month","ماه"]].map(x=>`<button class="${calendarView===x[0]?"active":""}" data-action="calendar-view" data-value="${x[0]}">${x[1]}</button>`).join("")}</div>
      <div><button class="btn" data-action="calendar-filter">فیلتر</button><button class="btn btn-primary" data-action="new-calendar-event">+ رویداد جدید</button></div>
    </div>`;
  }

  function renderCalendarDay(){
    const hours=Array.from({length:11},(_,i)=>i+8);
    return `<div class="v6-day-calendar"><div class="day-head"><strong>شنبه ۲۷ تیر</strong><small>امروز</small></div><div class="day-grid">${hours.map(h=>`<div class="day-hour"><time>${num(h)}:۰۰</time><div>${calendarEvents.filter(e=>e.day===0&&Math.floor(e.start)===h).map(e=>`<button class="full-event type-${e.type}" data-action="calendar-event-detail"><strong>${e.title}</strong><small>${num(e.start)}:۰۰ تا ${num(e.end)}:۰۰ • ${e.location}</small></button>`).join("")}</div></div>`).join("")}</div></div>`;
  }

  function renderCalendarWeek(){
    const days=["شنبه ۲۷","یکشنبه ۲۸","دوشنبه ۲۹","سه‌شنبه ۳۰","چهارشنبه ۳۱","پنجشنبه ۱","جمعه ۲"];
    const hours=Array.from({length:10},(_,i)=>i+8);
    return `<div class="v6-week-calendar"><div class="week-corner"></div>${days.map((d,i)=>`<div class="week-head ${i===0?"today":""}"><strong>${d}</strong><small>${i===0?"امروز":""}</small></div>`).join("")}${hours.map(h=>`<div class="week-time">${num(h)}:۰۰</div>${days.map((_,day)=>`<div class="week-cell">${calendarEvents.filter(e=>e.day===day&&Math.floor(e.start)===h).map(e=>`<button class="week-event type-${e.type}" data-action="calendar-event-detail"><strong>${e.title}</strong><small>${num(e.start)}:۰۰</small></button>`).join("")}</div>`).join("")}`).join("")}</div>`;
  }

  function renderCalendarMonth(){
    const cells=Array.from({length:35},(_,i)=>i-2);
    return `<div class="v6-month-calendar">${["شنبه","یکشنبه","دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه"].map(d=>`<div class="month-head">${d}</div>`).join("")}${cells.map((n,i)=>`<div class="month-cell ${n<1||n>31?"muted":""} ${n===27?"today":""}"><span>${num(n<1?30+n:n>31?n-31:n)}</span>${n===27?`<button class="month-event type-meeting">جلسه هماهنگی</button><button class="month-event type-task">درخواست خرید</button>`:""}${n===28?`<button class="month-event type-meeting">بازدید تولید</button>`:""}${n===30?`<button class="month-event type-meeting">کمیته بهره‌وری</button>`:""}</div>`).join("")}</div>`;
  }

  function renderCalendarPage(){
    const body=calendarView==="day"?renderCalendarDay():calendarView==="month"?renderCalendarMonth():renderCalendarWeek();
    return `<div class="page v6-page">${pageHeader("تقویم","برنامه شخصی، جلسات، کارهای زمان‌بندی‌شده و رویدادهای سازمانی.","زمان‌بندی CAS")}
      <section class="card v6-calendar-page">${calendarHeader()}<div class="calendar-filter-bar"><span class="filter-chip active">همه رویدادها</span><span class="filter-chip meeting">جلسه</span><span class="filter-chip task">کار شخصی</span><span class="filter-chip report">گزارش</span><span class="filter-chip org">سازمانی</span><label><input type="checkbox" checked> نمایش ساعات غیرکاری</label></div><div class="calendar-full-body">${body}</div></section>
    </div>`;
  }

  function chatMessages(name){
    const samples=[
      ["مریم فلاحی","نامه تأمین قطعات برای بررسی شما ارجاع شد. لطفاً تا قبل از ساعت ۱۲ نتیجه را اعلام کنید.","۰۹:۱۰","other"],
      ["مهدی رضایی","دریافت شد. ابتدا پیوست فنی را مرور می‌کنم و نتیجه را همین‌جا می‌فرستم.","۰۹:۱۸","me"],
      ["مریم فلاحی","ممنون. فایل صورتجلسه قبلی را هم به گفتگو پیوست کردم.","۰۹:۲۱","other"],
      ["مهدی رضایی","بسیار خوب، بررسی شد. مورد اول نیازمند اصلاح مقدار سفارش است.","۰۹:۳۱","me"]
    ];
    return samples.map((m,i)=>`<div class="chat-message ${m[3]} ${pinnedMessages.has(i)?"is-pinned":""}" data-message-index="${i}">
      <div class="avatar avatar-sm">${initials(m[0])}</div>
      <div class="message-bubble">
        ${pinnedMessages.has(i)?'<div class="message-pin-label">📌 پیام سنجاق‌شده</div>':""}
        ${replyingTo===i?'<div class="message-reply-preview">در حال پاسخ به این پیام</div>':""}
        <div class="message-meta"><strong>${m[0]}</strong><time>${m[2]}</time></div><p>${m[1]}</p>
        ${m[2]==="۰۹:۲۱"?`<button class="chat-attachment"><span>▧</span><div><strong>صورتجلسه-عملیات.pdf</strong><small>۱.۲ MB • PDF</small></div></button>`:""}
        <div class="message-reactions"><button data-action="react-message" data-index="${i}" data-emoji="👍">👍 <span>${i===0?2:1}</span></button><button data-action="react-message" data-index="${i}" data-emoji="✅">✅</button><button class="reaction-add" data-action="reaction-picker" data-index="${i}">＋</button></div>
      </div>
    </div>`).join("");
  }

  function renderMessagesPage(){
    const c=conversations[selectedConversation];
    return `<div class="page v6-page messenger-page">
      <section class="v6-messenger">
        <aside class="conversation-panel">
          <div class="conversation-search"><span class="conversation-symbol mini"><i></i><i></i></span><input placeholder="جست‌وجوی گفتگو و پیام..." /></div>
          <div class="conversation-tabs"><button class="active">همه</button><button>خوانده‌نشده</button><button>سنجاق‌شده</button><button>کانال‌ها</button></div>
          <div class="conversation-list">${conversations.map((x,i)=>`<button class="conversation-item ${i===selectedConversation?"active":""} ${pinnedConversations.has(i)?"is-pinned":""}" data-action="select-conversation" data-index="${i}" data-conversation-index="${i}"><span class="avatar">${x.avatar}</span><div><strong>${pinnedConversations.has(i)?"📌 ":""}${x.name}</strong><p>${x.preview}</p></div><aside><time>${x.time}</time>${x.unread?`<b>${num(x.unread)}</b>`:""}</aside></button>`).join("")}</div>
          <button class="floating-new-conversation" data-action="new-conversation" title="گفت‌وگوی جدید"><span class="conversation-symbol"><i></i><i></i></span><b>＋</b></button>
        </aside>
        <main class="chat-panel">
          <header class="chat-header"><div class="avatar">${c.avatar}</div><div><strong>${c.name}</strong><small>${c.kind} • ${c.members}</small></div><div class="chat-header-actions"><button title="جست‌وجو در همین گفتگو">⌕</button><button data-action="chat-files" title="فایل‌های مشترک">▧</button><button data-action="chat-info" title="اطلاعات گفتگو">ⓘ</button></div></header>
          <div class="chat-body"><div class="chat-date">امروز، ۲۷ تیر</div>${chatMessages(c.name)}</div>
          <footer class="chat-compose">${replyingTo!==null?`<div class="compose-reply"><span>پاسخ به پیام انتخاب‌شده</span><button data-action="cancel-reply">×</button></div>`:""}<div class="compose-row"><div class="compose-tools"><button title="پیوست">＋</button><button data-action="composer-emoji" title="شکلک">☺</button><button title="فایل">▧</button></div><textarea id="chatInput" placeholder="پیام خود را بنویسید..."></textarea><button class="send-button" data-action="send-chat-message">ارسال</button></div></footer>
        </main>
      </section>
      <div id="messageContextMenu" class="cas-context-menu" hidden></div>
    </div>`;
  }

  function showEmojiPicker(anchor, targetType, index=null){
    document.querySelectorAll('.emoji-picker-popover').forEach(x=>x.remove());
    const pop=document.createElement('div'); pop.className='emoji-picker-popover';
    pop.innerHTML=['👍','✅','❤️','😂','👏','🎉','😮','😢','🙏','🔥','👌','🤝'].map(e=>`<button data-emoji-choice="${e}" data-target-type="${targetType}" ${index!==null?`data-index="${index}"`:''}>${e}</button>`).join('');
    document.body.appendChild(pop); const r=anchor.getBoundingClientRect();
    pop.style.left=Math.max(8,Math.min(window.innerWidth-pop.offsetWidth-8,r.left))+'px';
    pop.style.top=Math.max(8,r.top-pop.offsetHeight-8)+'px';
  }

  function renderGlobalSearchPage(){
    return `<div class="page v6-page">${pageHeader("جست‌وجوی سازمان","یک نقطه ورود برای اقدام، شخص، فرم، سند، درخواست، پیام و رکوردهای اخیر.","CAS Command Search")}
      <section class="search-hero-page"><div class="search-box-mega">⌕<input id="globalSearchInputPage" value="خرید" placeholder="مثلاً ثبت درخواست خرید، علی رضایی یا شماره سند..." autofocus/><kbd>Enter</kbd></div><div class="search-suggestions"><span>پیشنهادها:</span><button>ثبت مرخصی</button><button>گزارش امروز</button><button>درخواست خرید</button><button>کاردکس من</button></div></section>
      <div class="v6-search-layout"><aside class="card v6-filter-panel"><div class="card-header"><h3 class="card-title">نوع نتیجه</h3></div><div class="card-body v6-filter-list"><button class="active"><span>همه</span><b>۱۲</b></button><button><span>اقدام‌ها</span><b>۳</b></button><button><span>افراد</span><b>۲</b></button><button><span>فرم و درخواست</span><b>۴</b></button><button><span>اسناد</span><b>۲</b></button><button><span>پیام‌ها</span><b>۱</b></button></div></aside>
      <section class="search-results">
        <div class="result-group"><h3>اقدام‌های مستقیم</h3><button class="command-result" data-route="request-center"><span class="result-icon">＋</span><div><strong>ثبت درخواست خرید</strong><p>فرم درخواست خرید کالا و خدمات</p></div><kbd>بازکردن</kbd></button><button class="command-result" data-route="request-tracking"><span class="result-icon">◫</span><div><strong>پیگیری درخواست‌های خرید</strong><p>مشاهده وضعیت درخواست‌های ثبت‌شده</p></div><kbd>بازکردن</kbd></button></div>
        <div class="result-group"><h3>رکوردها</h3>${D.submissions.filter(x=>x.form.includes("خرید")).map(x=>`<button class="command-result"><span class="result-icon">▤</span><div><strong>${x.form}</strong><p>${x.number} • ${x.state}</p></div>${badge(x.state,"blue")}</button>`).join("")}<button class="command-result"><span class="result-icon">▧</span><div><strong>فرم درخواست خرید تجهیزات ایمنی</strong><p>اسناد • PDF • نسخه ۲</p></div>${badge("منتشرشده","green")}</button></div>
        <div class="result-group"><h3>افراد و گفتگوها</h3><button class="command-result"><span class="avatar">عر</span><div><strong>علی رستمی</strong><p>کارشناس خرید داخلی • واحد خرید</p></div><kbd>پروفایل</kbd></button><button class="command-result" data-route="messages"><span class="result-icon">✉</span><div><strong>گفت‌وگوی تیم خرید</strong><p>۳ پیام دارای عبارت «خرید»</p></div><kbd>مشاهده</kbd></button></div>
      </section></div>
    </div>`;
  }

  function renderNotificationsCenter(){
    const items=[
      ["فوری","درخواست مرخصی تا ۲۵ دقیقه دیگر از SLA عبور می‌کند.","امروز ۰۹:۳۵","red"],
      ["اقدام","گزارش شیفت شب برای تأیید شما ارسال شد.","امروز ۰۹:۱۲","blue"],
      ["پیام","مریم فلاحی در گفت‌وگوی مستقیم برای شما پیام فرستاد.","امروز ۰۹:۱۰","purple"],
      ["اطلاع","جلسه فردا از ساعت ۹ به ۱۰ منتقل شد.","دیروز","green"]
    ];
    return `<div class="page v6-page">${pageHeader("مرکز اعلان‌ها","اعلان‌های قابل اقدام از پیام‌های صرفاً اطلاع‌رسان جدا شده‌اند.","فضای شخصی",`<button class="btn">علامت‌گذاری همه به‌عنوان خوانده‌شده</button>`)}
      <div class="v6-notification-layout"><aside class="card v6-filter-panel"><div class="card-body v6-filter-list"><button class="active"><span>همه اعلان‌ها</span><b>۴</b></button><button><span>نیازمند اقدام</span><b>۲</b></button><button><span>پیام‌ها</span><b>۱</b></button><button><span>فقط اطلاع</span><b>۱</b></button></div></aside><section class="card"><div class="card-body notification-stream">${items.map((x,i)=>`<article class="notification-card tone-${x[3]}"><span class="notification-symbol">${i===0?"!":i===1?"✓":i===2?"✉":"◷"}</span><div><div>${badge(x[0],x[3])}<time>${x[2]}</time></div><h4>${x[1]}</h4><p>${i<2?"این اعلان مستقیماً به رکورد منبع متصل است و از همین‌جا قابل اقدام خواهد بود.":"برای مشاهده جزئیات، اعلان را باز کنید."}</p></div><div><button class="btn btn-sm">${i<2?"اقدام":"مشاهده"}</button><button class="mini-btn">•••</button></div></article>`).join("")}</div></section></div>
    </div>`;
  }

  function renderRecentHistory(){
    const history=[
      ["۰۹:۳۸","مشاهده درخواست خرید FRM/۱۴۰۵/۰۰۳۶۶","فرم و فرایند","▤"],
      ["۰۹:۳۱","ارسال پیام به مریم فلاحی","گفت‌وگوها","✉"],
      ["۰۹:۱۸","ثبت فعالیت «تحلیل مغایرت حضور»","گزارش کار","✎"],
      ["۰۸:۵۵","بازکردن گزارش کاردکس تیر","حضور و کارکرد","▦"],
      ["دیروز","تأیید گزارش روزانه نگهبانی","تأییدها","✓"]
    ];
    return `<div class="page v6-page">${pageHeader("تاریخچه اخیر","دسترسی سریع به رکوردها و عملیات اخیر شما؛ نه گزارش ممیزی رسمی.","فضای شخصی",`<button class="btn">پاک‌کردن تاریخچه شخصی</button>`)}
      <section class="card"><div class="card-header"><div><h3 class="card-title">فعالیت‌های اخیر</h3><div class="card-subtitle">مرتب‌شده از جدیدترین به قدیمی‌ترین</div></div><div class="search-box">⌕<input placeholder="جست‌وجو در تاریخچه..." /></div></div><div class="card-body recent-timeline">${history.map(x=>`<button><time>${x[0]}</time><span class="recent-icon">${x[3]}</span><div><strong>${x[1]}</strong><small>${x[2]}</small></div><span>‹</span></button>`).join("")}</div></section>
    </div>`;
  }

  const renderers = {
    home:renderHome,
    "personal-tasks":renderPersonalTasksPage,
    calendar:renderCalendarPage,
    messages:renderMessagesPage,
    "global-search-page":renderGlobalSearchPage,
    "notifications-center":renderNotificationsCenter,
    "recent-history":renderRecentHistory,
    "request-center":renderRequestCenter,
    "request-tracking":renderRequestTracking,
    "attendance-hub":renderAttendanceHub,
    "guard-workspace":renderGuardWorkspace,
    "team-center":renderTeamCenter,
    "supervisor-dashboard":renderSupervisorDashboard,
    "manager-dashboard":()=>renderManagerDashboard(false),
    "executive-dashboard":()=>renderManagerDashboard(true),
    "my-actions":()=>renderActions(false),
    "urgent-actions":()=>renderActions(true),
    approvals:renderApprovals,
    "form-catalog":renderFormCatalog,
    "my-submissions":renderSubmissions,
    "form-runtime":renderFormRuntime,
    "forms-admin":renderFormsAdmin,
    "form-builder":renderFormBuilder,
    "workflow-instances":renderWorkflowInstances,
    "workflow-admin":renderWorkflowAdmin,
    "workflow-designer":renderWorkflowDesigner,
    "approval-policies":renderApprovalPolicies,
    delegations:renderDelegations,
    correspondence:renderCorrespondence,
    "letter-compose":renderLetterCompose,
    documents:renderDocuments,
    "ocr-queue":renderOcrQueue,
    "secretariat-register":renderSecretariatRegister,
    "correspondence-templates":renderCorrespondenceTemplates,
    "signature-ledger":renderSignatureLedger,
    "my-shifts":renderMyShifts,
    "shift-planning":renderShiftPlanning,
    "shift-swaps":renderShiftSwaps,
    "my-attendance":renderMyAttendance,
    "attendance-review":renderAttendanceReview,
    "attendance-events":renderAttendanceEvents,
    "attendance-import":renderAttendanceImport,
    "identity-mapping":renderIdentityMapping,
    guard:renderGuard,
    devices:renderDevices,
    "my-kardex":renderMyKardex,
    "attendance-requests":renderAttendanceRequests,
    overtime:renderOvertime,
    "kardex-operations":renderKardexOperations,
    "kardex-periods":renderKardexPeriods,
    "kardex-report":renderKardexReport,
    "work-reports":()=>renderWorkReports(false),
    "team-work-reports":()=>renderWorkReports(true),
    "work-report-new":renderWorkReportNew,
    "work-stations":renderWorkStations,
    "admin-center":renderAdminCenter,
    "user-management":renderUserManagement,
    "access-roles":renderAccessRoles,
    organization:renderOrganization,
    positions:renderPositions,
    assignments:renderAssignments,
    "settings-hub":renderSettingsHub,
    "access-report":renderAccessReport,
    "audit-log":renderAuditLog,
    modules:renderModules,
    "sla-rules":renderSlaRules,
    "document-settings":renderDocumentSettings,
    "jalali-center":renderJalaliCenter,
    "system-health":renderSystemHealth,
    "workspace-settings":renderWorkspaceSettings,
    "role-matrix":renderRoleMatrix
  };

  function renderRoute(){
    const fn = renderers[currentRoute] || renderHome;
    app.innerHTML = fn();
    if(currentRoute==="home") requestAnimationFrame(applySavedWidgetOrder);
    bindDynamicInputs();
  }

  function bindDynamicInputs(){
    const guardSearch = document.getElementById("guardSearch");
    const guardUnit = document.getElementById("guardUnit");
    if(guardSearch) guardSearch.addEventListener("input",filterPeople);
    if(guardUnit) guardUnit.addEventListener("change",filterPeople);
  }
  function filterPeople(){
    const q=(document.getElementById("guardSearch")?.value||"").trim().toLowerCase();
    const unit=document.getElementById("guardUnit")?.value||"";
    const filtered=D.people.filter(p=>(!unit||p.unit===unit)&&(!q||[p.name,p.code,p.job,p.unit].join(" ").toLowerCase().includes(q)));
    const grid=document.getElementById("peopleGrid");
    if(grid) grid.innerHTML=filtered.length?renderPeopleCards(filtered):`<div class="empty-state" style="grid-column:1/-1"><div class="empty-icon">⌕</div><h3>فردی پیدا نشد</h3><p>عبارت جست‌وجو یا فیلتر واحد را تغییر دهید.</p></div>`;
  }

  function openDrawer(title,body,footer=""){
    drawerRoot.className="drawer-root open nested-layer";
    drawerRoot.innerHTML=`<div class="overlay" data-action="close-layer"></div><section class="drawer"><div class="drawer-head"><strong>${title}</strong><button class="icon-button" data-action="close-layer">×</button></div><div class="drawer-body">${body}</div>${footer?`<div class="drawer-foot">${footer}</div>`:""}</section>`;
  }
  function quickConversationsDrawer(){
    openDrawer("گفت‌وگوهای اخیر",`<div class="v7-drawer-conversations">${conversations.map((x,i)=>`<button class="v7-conversation-row" data-action="open-drawer-conversation" data-index="${i}"><span class="avatar avatar-sm">${x.avatar}</span><div><strong>${x.name}</strong><small>${x.preview}</small></div><aside><time>${x.time}</time>${x.unread?`<b>${num(x.unread)}</b>`:""}</aside></button>`).join("")}</div>`,`<button class="btn btn-primary" data-route="messages">مشاهده همه گفت‌وگوها</button>`);
  }

  function conversationInfoDrawer(){
    const c=conversations[selectedConversation];
    openDrawer("اطلاعات گفت‌وگو",`<div class="v7-conversation-info"><div class="avatar avatar-lg">${c.avatar}</div><h3>${c.name}</h3><p>${c.kind} • ${c.members}</p><div class="chat-info-actions"><button>بی‌صدا</button><button>سنجاق</button><button>اعضا</button></div><hr><h4>فایل‌های مشترک</h4><div class="shared-file"><span>PDF</span><div><strong>صورتجلسه عملیات</strong><small>امروز</small></div></div><div class="shared-file"><span>XLS</span><div><strong>گزارش شیفت شب</strong><small>دیروز</small></div></div></div>`);
  }

  function appearanceSettingsDrawer(){
    const choice=(key,value,label)=>`<button class="v7-setting-choice ${v7Settings[key]===value?"active":""}" data-action="set-v7-setting" data-setting="${key}" data-value="${value}">${label}</button>`;
    openDrawer("ظاهر و خوانایی",`
      <div class="v7-settings-block"><strong>اندازه متن</strong><small>حالت استاندارد پیش‌فرض است و هیچ متن کاربردی زیر ۱۲ پیکسل نیست.</small><div>${choice("fontScale","compact","فشرده")}${choice("fontScale","standard","استاندارد")}${choice("fontScale","large","بزرگ")}</div></div>
      <div class="v7-settings-block"><strong>تراکم رابط</strong><small>فاصله‌های کنترل‌ها و ردیف‌ها</small><div>${choice("density","compact","فشرده")}${choice("density","comfortable","راحت")}</div></div>
      <div class="v7-settings-block"><strong>رنگ اصلی</strong><small>رنگ‌بندی کنترل‌شده بدون از بین‌رفتن هویت سازمانی</small><div>${choice("accent","blue","آبی")}${choice("accent","teal","سبزآبی")}${choice("accent","purple","بنفش")}${choice("accent","amber","کهربایی")}</div></div>
      <div class="v7-settings-block"><strong>حالت نمایش</strong><small>تم روشن یا تاریک برای تمام محیط</small><div>${choice("theme","light","روشن")}${choice("theme","dark","تاریک")}</div></div>
      <div class="v7-settings-block"><strong>منوی کناری</strong><small>وضعیت انتخاب‌شده در مرورگر ذخیره می‌شود.</small><div><button class="v7-setting-choice" data-action="toggle-sidebar">${v7Settings.sidebarCollapsed?"بازکردن منو":"جمع‌کردن منو"}</button></div></div>
    `);
  }

  function openModal(title,body,footer=""){
    modalRoot.className="modal-root open";
    modalRoot.innerHTML=`<div class="overlay" data-action="close-layer"></div><section class="modal"><div class="drawer-head"><strong>${title}</strong><button class="icon-button" data-action="close-layer">×</button></div><div class="drawer-body">${body}</div>${footer?`<div class="drawer-foot">${footer}</div>`:""}</section>`;
  }
  function closeLayers(){drawerRoot.className="drawer-root";drawerRoot.innerHTML="";modalRoot.className="modal-root";modalRoot.innerHTML="";}
  function toast(message,type="success"){
    const el=document.createElement("div"); el.className=`toast ${type}`; el.textContent=message; toastRoot.appendChild(el); setTimeout(()=>el.remove(),3200);
  }

  function actionDetail(index=0){
    const a=D.actions[index]||D.actions[0];
    openDrawer(a.title,`<div style="display:flex;gap:7px;margin-bottom:12px">${badge(a.source,"blue")}${badge(a.status,a.tone)}</div><h2 style="font-size:18px;margin:0 0 5px">${a.subject}</h2><p style="font-size:10px;color:var(--ink-500)">مهلت: ${a.deadline} • اولویت ${a.priority}</p><div class="detail-section" style="padding-right:0;padding-left:0"><div class="kv-grid"><div class="kv"><span>کد اقدام</span><strong>ACT/۱۴۰۵/۰۰۸۲</strong></div><div class="kv"><span>مسئول</span><strong>${D.roles[currentRole].name}</strong></div><div class="kv"><span>منبع</span><strong>${a.source}</strong></div></div></div><div class="detail-section" style="padding-right:0;padding-left:0"><h3>شرح</h3><p style="font-size:11px;color:var(--ink-700)">این اقدام از رکورد منبع همگام شده است. برای انجام نهایی، باید رکورد اصلی بررسی و عملیات دامنه‌ای همان ماژول اجرا شود.</p></div><div class="timeline"><div class="timeline-item"><h5>اقدام به شما تخصیص یافت</h5><p>همگام‌سازی Action Hub</p><time>۱۰:۴۵</time></div><div class="timeline-item"><h5>بازبینی خودکار انجام شد</h5><p>قانون SLA فعال</p><time>۱۰:۴۲</time></div><div class="timeline-item"><h5>رکورد منبع ایجاد شد</h5><p>${a.source}</p><time>۱۰:۳۰</time></div></div>`,`<button class="btn" data-action="close-layer">بستن</button><button class="btn btn-primary" data-action="go-source">بازکردن رکورد منبع</button>`);
  }

  function submissionDetail(index=0){
    const s=D.submissions[index]||D.submissions[0];
    openDrawer("جزئیات ثبت فرم",`<div>${badge(s.state,s.state.includes("تأیید")?"green":"blue")}</div><h2 style="font-size:18px">${s.form}</h2><div class="kv-grid"><div class="kv"><span>شماره رهگیری</span><strong>${s.number}</strong></div><div class="kv"><span>نسخه فرم</span><strong>${s.version}</strong></div><div class="kv"><span>مالک</span><strong>${s.owner}</strong></div></div><div class="detail-section" style="padding-right:0;padding-left:0"><h3>Snapshot پاسخ‌های نهایی</h3><div class="kv-grid"><div class="kv"><span>تاریخ درخواست</span><strong>۲۷ تیر ۱۴۰۵</strong></div><div class="kv"><span>واحد</span><strong>عملیات</strong></div><div class="kv"><span>نوع</span><strong>ساعتی</strong></div></div></div><div class="timeline"><div class="timeline-item"><h5>ثبت ایجاد شد</h5><p>${s.date}</p></div><div class="timeline-item"><h5>ارسال نهایی</h5><p>Snapshot غیرقابل تغییر ثبت شد</p></div><div class="timeline-item"><h5>گردش‌کار آغاز شد</h5><p>نسخه فرایند pin شده است</p></div></div>`,`<button class="btn" data-action="close-layer">بستن</button><button class="btn btn-primary" data-route="workflow-instances">مشاهده گردش‌کار</button>`);
  }

  function documentDetail(index=0){
    const d=D.documents[index]||D.documents[0];
    openDrawer("جزئیات سند",`<div class="doc-preview" style="height:180px"><span class="doc-format">${d.format}</span>${d.icon}</div><h2 style="font-size:17px">${d.name}</h2><div style="display:flex;gap:7px;flex-wrap:wrap">${badge(d.version,"blue")}${badge(d.status,"green")}${badge(d.folder,"purple")}</div><div class="detail-section" style="padding-right:0;padding-left:0"><div class="kv-grid"><div class="kv"><span>حجم</span><strong>${d.size}</strong></div><div class="kv"><span>نسخه‌ها</span><strong>۳ نسخه</strong></div><div class="kv"><span>پیوندها</span><strong>۲ رکورد</strong></div></div></div><div class="timeline"><div class="timeline-item"><h5>نسخه جدید بارگذاری شد</h5><p>توسط مریم فلاحی</p><time>۲۷ تیر ۱۴۰۵</time></div><div class="timeline-item"><h5>OCR تأیید شد</h5><p>کیفیت ۹۴٪</p><time>۲۶ تیر ۱۴۰۵</time></div><div class="timeline-item"><h5>پیوند به نامه رسمی</h5><p>۱۴۰۵/د/۰۰۲۴</p><time>۲۵ تیر ۱۴۰۵</time></div></div>`,`<button class="btn">نسخه جدید</button><button class="btn btn-primary">دانلود نسخه جاری</button>`);
  }

  function newRequestModal(){
    openModal("ثبت درخواست مرخصی یا مأموریت",`<div class="form-grid"><div class="field"><label class="required">نوع درخواست</label><select><option>مرخصی ساعتی</option><option>مرخصی روزانه</option><option>مأموریت</option></select></div><div class="field"><label class="required">تاریخ</label><input value="۱۴۰۵/۰۴/۲۹" /></div><div class="field"><label class="required">از ساعت</label><input type="time" value="12:00" /></div><div class="field"><label class="required">تا ساعت</label><input type="time" value="16:00" /></div><div class="field full"><label class="required">دلیل</label><textarea placeholder="شرح درخواست..."></textarea></div></div><div class="status-item" style="margin-top:14px"><span class="status-light"></span><div><strong>کنترل برنامه شیفت</strong><small>برای بازه انتخابی تداخل بحرانی یافت نشد.</small></div></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="confirm-request">ارسال درخواست</button>`);
  }

  function newActivityProposalModal(){
    openModal("ثبت فعالیت جدید",`<div class="proposal-note"><strong>ثبت گزارش متوقف نمی‌شود.</strong><p>عنوان واردشده بلافاصله به گزارش امروز اضافه می‌شود و همزمان برای استانداردسازی ارسال خواهد شد.</p></div><div class="form-grid"><div class="field full"><label class="required">عنوان فعالیت</label><input id="proposalTitle" placeholder="مثلاً بررسی مشکل چاپگر واحد مالی" /></div><div class="field"><label class="required">دسته‌بندی</label><select id="proposalCategory"><option>پشتیبانی</option><option>عملیات</option><option>مکاتبات</option><option>جلسه</option><option>گزارش و تحلیل</option><option>سایر</option></select></div><div class="field"><label class="required">مدت</label><select id="proposalDuration"><option value="15">۱۵ دقیقه</option><option value="30" selected>۳۰ دقیقه</option><option value="45">۴۵ دقیقه</option><option value="60">۱ ساعت</option><option value="90">۱ ساعت و ۳۰ دقیقه</option></select></div><div class="field full"><label>توضیح کوتاه</label><textarea id="proposalNote" placeholder="نتیجه یا جزئیات ضروری..."></textarea></div></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="confirm-new-activity">افزودن و ارسال پیشنهاد</button>`);
  }

  function addPersonalTaskModal(){
    openModal("افزودن کار شخصی",`<div class="proposal-note"><strong>ساده و سریع</strong><p>برای ساخت یک کار، فقط عنوان کافی است. زمان، دسته و جزئیات اختیاری‌اند.</p></div><div class="form-grid"><div class="field full"><label class="required">عنوان کار</label><input id="personalTaskTitle" placeholder="مثلاً پیگیری قرارداد سرویس دستگاه" /></div><div class="field"><label>زمان انجام</label><select id="personalTaskTime"><option>امروز</option><option>فردا</option><option>این هفته</option><option>بدون تاریخ</option></select></div><div class="field"><label>دسته‌بندی</label><select id="personalTaskSource">${[...personalTaskCategories,...systemTaskCategories].map(x=>`<option>${esc(x)}</option>`).join("")}</select></div><div class="field full"><label>توضیح</label><textarea placeholder="اختیاری..."></textarea></div></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="confirm-personal-task">افزودن کار</button>`);
  }

  function participantSummaryHtml(){
    const items=[...eventParticipants.entries()];
    if(!items.length) return `<div class="participant-empty-summary"><span>هنوز کسی انتخاب نشده است.</span><small>شرکت‌کنندگان را با جست‌وجو، واحد یا محدوده سازمانی انتخاب کنید.</small></div>`;
    return `<div class="participant-summary"><div class="participant-summary-head"><strong>${num(items.length)} نفر انتخاب‌شده</strong><button class="link-button" data-action="open-participant-selector">ویرایش</button></div><div class="participant-chips">${items.map(([name,v])=>`<span class="participant-chip"><span class="avatar avatar-xs">${esc(v.initials)}</span>${esc(name)}<small>${v.mode==='task'?'وظیفه':v.mode==='both'?'دعوت و وظیفه':'دعوت'}</small><button data-action="remove-event-participant" data-name="${esc(name)}" aria-label="حذف">×</button></span>`).join('')}</div></div>`;
  }

  function renderParticipantResults(){
    const host=document.getElementById('participantResults'); if(!host)return;
    const q=(document.getElementById('participantLookup')?.value||'').trim().toLowerCase();
    const unit=document.getElementById('participantUnit')?.value||'all';
    const scope=document.getElementById('participantScope')?.value||'suggested';
    let people=D.people.map((p,i)=>({...p,subordinate:i<4,recent:i<3}));
    if(scope==='subordinates') people=people.filter(p=>p.subordinate);
    if(unit!=='all') people=people.filter(p=>p.unit===unit);
    if(q.length>=2) people=people.filter(p=>(`${p.name} ${p.job} ${p.unit}`).toLowerCase().includes(q));
    else if(unit==='all' && scope==='suggested') people=people.filter(p=>p.subordinate||p.recent);
    const visible=people.slice(0,20);
    host.innerHTML=visible.length?visible.map(p=>{
      const selected=eventParticipants.get(p.name);
      return `<article class="participant-result ${selected?'selected':''}"><label class="participant-person"><input type="checkbox" data-action="toggle-event-participant" data-name="${esc(p.name)}" ${selected?'checked':''}><span class="avatar avatar-sm">${esc(p.initials)}</span><span><strong>${esc(p.name)}</strong><small>${esc(p.job)} • ${esc(p.unit)}</small><em class="relation-badge ${p.subordinate?'subordinate':'invite-only'}">${p.subordinate?'زیرمجموعه مجاز':'فقط دعوت'}</em></span></label>${selected?(p.subordinate?`<select class="participant-row-mode" data-participant-mode="${esc(p.name)}"><option value="invite" ${selected.mode==='invite'?'selected':''}>دعوت‌نامه</option><option value="task" ${selected.mode==='task'?'selected':''}>وظیفه</option><option value="both" ${selected.mode==='both'?'selected':''}>دعوت و وظیفه</option></select>`:`<span class="readonly-mode">دعوت‌نامه</span>`):''}</article>`;
    }).join(''):`<div class="participant-no-results"><strong>نتیجه‌ای پیدا نشد</strong><small>حداقل دو حرف جست‌وجو کنید یا واحد و محدوده را تغییر دهید.</small></div>`;
    const count=document.getElementById('participantResultCount'); if(count)count.textContent=`${num(visible.length)} نتیجه`;
  }

  function participantSelectorDrawer(){
    openDrawer('انتخاب شرکت‌کنندگان',`<div class="participant-selector-intro"><strong>انتخاب مقیاس‌پذیر و مبتنی بر دسترسی</strong><p>در حالت عادی فقط افراد پیشنهادی نمایش داده می‌شوند. جست‌وجو در پیاده‌سازی واقعی به‌صورت Server-side و صفحه‌بندی‌شده انجام خواهد شد.</p></div><div class="participant-selector-controls"><div class="search-box"><span>⌕</span><input id="participantLookup" placeholder="حداقل دو حرف از نام، سمت یا واحد..." autocomplete="off"></div><select id="participantUnit"><option value="all">همه واحدهای قابل دعوت</option>${[...new Set(D.people.map(p=>p.unit))].map(u=>`<option value="${esc(u)}">${esc(u)}</option>`).join('')}</select><select id="participantScope"><option value="suggested">پیشنهادی و اخیر</option><option value="subordinates">فقط زیرمجموعه‌های من</option><option value="all">همه افراد قابل دعوت</option></select></div><div class="participant-selected-strip" id="participantSelectedStrip">${participantSummaryHtml()}</div><div class="participant-results-head"><strong>نتایج</strong><span id="participantResultCount"></span></div><div class="participant-results" id="participantResults"></div>`,`<button class="btn" data-action="close-drawer-only">انصراف</button><button class="btn btn-primary" data-action="confirm-event-participants">تأیید شرکت‌کنندگان</button>`);
    setTimeout(renderParticipantResults,0);
  }

  function newCalendarEventModal(){
    openModal("رویداد جدید",`<div class="form-grid event-form-grid"><div class="field full"><label class="required">عنوان رویداد</label><input id="calendarEventTitle" placeholder="عنوان جلسه یا برنامه..." /></div><div class="field"><label class="required">تاریخ</label><input value="۱۴۰۵/۰۴/۲۷" /></div><div class="field"><label class="required">زمان شروع</label><input type="time" value="15:00" /></div><div class="field"><label>زمان پایان</label><input type="time" value="16:00" /></div><div class="field"><label>نوع</label><select><option>جلسه</option><option>کار زمان‌بندی‌شده</option><option>یادآوری</option><option>رویداد سازمانی</option></select></div><div class="field full participant-field"><div class="field-title-row"><label>شرکت‌کنندگان</label><button class="btn btn-sm" data-action="open-participant-selector">${eventParticipants.size?'ویرایش انتخاب‌ها':'انتخاب شرکت‌کنندگان'}</button></div><div id="eventParticipantSummary">${participantSummaryHtml()}</div><small class="field-help">برای افراد خارج از زنجیره مدیریتی فقط دعوت‌نامه مجاز است. برای زیرمجموعه مجاز می‌توانید دعوت، وظیفه یا هر دو را انتخاب کنید.</small></div><div class="field full"><label>توضیحات</label><textarea placeholder="اختیاری..."></textarea></div></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="save-calendar-event">ثبت و ارسال</button>`);
  }

  function rejectModal(){
    openModal("بازگرداندن برای اصلاح",`<div class="field"><label class="required">دلیل بازگرداندن</label><textarea placeholder="دلیل باید روشن، عملیاتی و قابل پیگیری باشد..."></textarea><small>این دلیل در تاریخچه رسمی تصمیم ذخیره می‌شود.</small></div><div class="field" style="margin-top:12px"><label>مهلت اصلاح</label><input value="۱۴۰۵/۰۴/۲۸ - ۱۰:۰۰" /></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-danger" data-action="confirm-reject">ثبت بازگرداندن</button>`);
  }

  function helpModal(){
    openModal("راهنمای نمونه رابط کاربری",`<h3 style="font-size:13px">این بسته چه چیزی را پوشش می‌دهد؟</h3><p style="font-size:11px;color:var(--ink-600)">نمونه تعاملی، فارسی، راست‌چین و نقش‌محور برای ۲۴ ماژول CAS. نقش را از نوار بالا تغییر دهید تا صفحات و منوهای ویژه همان نقش نمایش داده شوند.</p><div class="status-panel" style="grid-template-columns:1fr"><div class="status-item"><span class="status-light"></span><div><strong>داده نمایشی</strong><small>در پیاده‌سازی Odoo از مدل‌های منبع و بدون sudo خوانده می‌شود.</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>صفحات تخصصی</strong><small>فرم‌ساز، گردش‌کار، دبیرخانه، نگهبانی، کاردکس و گزارش‌ها قالب اختصاصی دارند.</small></div></div><div class="status-item"><span class="status-light"></span><div><strong>بدون وابستگی خارجی</strong><small>فایل index.html را می‌توان مستقیم یا با وب‌سرور محلی اجرا کرد.</small></div></div></div><p style="font-size:10px;color:var(--ink-500)">جزئیات قرارداد Odoo، ماتریس پوشش و فهرست routeها در پوشه docs بسته قرار دارد.</p>`,`<button class="btn btn-primary" data-action="close-layer">متوجه شدم</button>`);
  }

  function globalSearch(){
    openModal("جست‌وجوی سراسری",`<div class="search-box" style="width:100%;height:48px"><span>⌕</span><input autofocus placeholder="اقدام، نامه، سند، فرم یا کارمند..." /></div><div style="margin-top:16px"><div class="page-kicker">نتایج پیشنهادی</div>${D.actions.slice(0,3).map((a,i)=>`<button class="record-row" style="width:100%;border:0;background:transparent;text-align:right" data-action="open-action" data-index="${i}"><div class="task-source">${a.icon}</div><div><h4>${a.title}</h4><p>${a.source} • ${a.subject}</p></div></button>`).join("")}${D.letters.slice(0,2).map(l=>`<button class="record-row" style="width:100%;border:0;background:transparent;text-align:right" data-route="correspondence"><div class="task-source">✉</div><div><h4>${l.subject}</h4><p>${l.no} • مکاتبات</p></div></button>`).join("")}</div>`);
  }

  function notifications(){
    openDrawer("اعلان‌ها",`<div class="task-list"><div class="task-item"><div class="task-source">!</div><div><h4>یک اقدام از SLA عبور کرد</h4><p>رفع مغایرت حضور نگهبانی</p></div><time>۵ دقیقه قبل</time></div><div class="task-item"><div class="task-source">◎</div><div><h4>درخواست جدید برای تأیید</h4><p>مرخصی ساعتی سارا احمدی</p></div><time>۲۱ دقیقه قبل</time></div><div class="task-item"><div class="task-source">✉</div><div><h4>نامه جدید دریافت شد</h4><p>ابلاغ برنامه ممیزی داخلی</p></div><time>۴۰ دقیقه قبل</time></div><div class="task-item"><div class="task-source">▱</div><div><h4>OCR سند تکمیل شد</h4><p>قرارداد سرویس دستگاه حضور</p></div><time>۱ ساعت قبل</time></div></div>`);
  }

  function profileDrawer(){
    const r=D.users[currentUserId];
    openDrawer("پروفایل و زمینه کار",`<div class="guard-selected"><div class="person-photo" style="width:68px;height:68px">${initials(r.name)}</div><div><h3>${r.name}</h3><p>${r.job} • ${r.unit}</p>${badge(r.company,"blue")}</div></div><div class="detail-section" style="padding-right:0;padding-left:0"><div class="kv-grid"><div class="kv"><span>زبان</span><strong>فارسی</strong></div><div class="kv"><span>منطقه زمانی</span><strong>Asia/Tehran</strong></div><div class="kv"><span>تقویم</span><strong>جلالی</strong></div></div></div><button class="btn" style="width:100%" data-route="home">بازگشت به خانه نقش</button>`);
  }

  function handleGuard(type){
    const time=(document.getElementById("guardTime")?.value||"09:15").replace(/^0/,"۰");
    const normalized=time.split("").map(c=>"0123456789".includes(c)?"۰۱۲۳۴۵۶۷۸۹"[Number(c)]:c).join("");
    const gate=document.getElementById("guardGate")?.value||"درب شمالی";
    guardLogs.unshift({name:selectedPerson.name,type, time:normalized,source:"ثبت نگهبانی دستی",gate});
    selectedPerson.status=type==="ورود"?"in":"out";
    toast(`${type} ${selectedPerson.name} در ساعت ${normalized} ثبت شد.`);
    renderRoute();
  }

  function handleAction(action,target){
    switch(action){
      case "toggle-sidebar":
        v7Settings.sidebarCollapsed=!v7Settings.sidebarCollapsed; applyV7Settings(); break;
      case "quick-conversations":
        quickConversationsDrawer(); break;
      case "appearance-settings":
        appearanceSettingsDrawer(); break;
      case "set-v7-setting":
        v7Settings[target.dataset.setting]=target.dataset.value; applyV7Settings(); appearanceSettingsDrawer(); break;
      case "home-calendar-view":
        homeCalendarView=target.dataset.value||"day"; localStorage.setItem("cas.home.calendarView",homeCalendarView); renderRoute(); break;
      case "home-calendar-month-prev":
        homeCalendarMonthOffset-=1; localStorage.setItem("cas.home.calendarMonthOffset",String(homeCalendarMonthOffset)); renderRoute(); break;
      case "home-calendar-month-next":
        homeCalendarMonthOffset+=1; localStorage.setItem("cas.home.calendarMonthOffset",String(homeCalendarMonthOffset)); renderRoute(); break;
      case "home-calendar-day":
        toast(`روز ${target.dataset.day} انتخاب شد.`); break;
      case "open-home-conversation":
      case "open-drawer-conversation":
        selectedConversation=Number(target.dataset.index)||0; closeLayers(); navigate("messages"); break;
      case "close-layer": closeLayers(); break;
      case "open-help": helpModal(); break;
      case "global-search": globalSearch(); break;
      case "notifications": notifications(); break;
      case "profile": profileDrawer(); break;
      case "open-action": actionDetail(Number(target.dataset.index||0)); break;
      case "submission-detail": submissionDetail(Number(target.dataset.index||0)); break;
      case "document-detail": documentDetail(Number(target.dataset.index||0)); break;
      case "new-request": newRequestModal(); break;
      case "reject-approval": rejectModal(); break;
      case "approve": toast("تصمیم تأیید ثبت و انتقال گردش‌کار فعال شد."); break;
      case "confirm-reject": closeLayers(); toast("بازگرداندن برای اصلاح با دلیل ثبت شد.","warn"); break;
      case "confirm-request": closeLayers(); toast("درخواست ثبت و گردش‌کار تأیید آغاز شد."); break;
      case "submit-form": toast("فرم اعتبارسنجی و برای گردش‌کار ارسال شد."); break;
      case "submit-work-report": toast("گزارش امروز مرور و برای تأیید سرپرست ارسال شد."); break;
      case "task-view": taskView=target.dataset.value||"today"; renderRoute(); break;
      case "task-category-filter": activeTaskCategory=target.dataset.value||""; renderRoute(); break;
      case "add-task-category": openModal("افزودن دسته شخصی",`<div class="field"><label class="required">نام دسته</label><input id="taskCategoryName" placeholder="مثلاً پیگیری مشتری" /></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="confirm-add-task-category">افزودن دسته</button>`); break;
      case "confirm-add-task-category": {
        const name=document.getElementById("taskCategoryName")?.value.trim();
        if(!name){toast("نام دسته را وارد کنید.","warn");break;}
        if([...systemTaskCategories,...personalTaskCategories].includes(name)){toast("این دسته از قبل وجود دارد.","warn");break;}
        personalTaskCategories.push(name); localStorage.setItem("cas.personalTaskCategories",JSON.stringify(personalTaskCategories)); closeLayers(); toast("دسته شخصی افزوده شد."); renderRoute(); break;
      }
      case "edit-task-category": {
        const name=target.dataset.value||"";
        openModal("ویرایش دسته شخصی",`<div class="field"><label class="required">نام دسته</label><input id="taskCategoryEditName" value="${esc(name)}" /></div><div class="proposal-note"><strong>دسته‌های سیستمی قابل حذف نیستند.</strong><p>حذف این دسته، کارهای موجود را حذف نمی‌کند و آن‌ها را به دسته «شخصی» منتقل می‌کند.</p></div>`,`<button class="btn btn-danger" data-action="delete-task-category" data-value="${esc(name)}">حذف دسته</button><button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="confirm-edit-task-category" data-value="${esc(name)}">ذخیره</button>`); break;
      }
      case "confirm-edit-task-category": {
        const oldName=target.dataset.value||""; const newName=document.getElementById("taskCategoryEditName")?.value.trim();
        if(!newName){toast("نام دسته را وارد کنید.","warn");break;}
        personalTaskCategories=personalTaskCategories.map(x=>x===oldName?newName:x); personalTasks.forEach(t=>{if(t.source===oldName)t.source=newName;}); localStorage.setItem("cas.personalTaskCategories",JSON.stringify(personalTaskCategories)); closeLayers(); toast("دسته ویرایش شد."); renderRoute(); break;
      }
      case "delete-task-category": {
        const name=target.dataset.value||""; personalTaskCategories=personalTaskCategories.filter(x=>x!==name); personalTasks.forEach(t=>{if(t.source===name)t.source="شخصی";}); if(activeTaskCategory===name)activeTaskCategory=""; localStorage.setItem("cas.personalTaskCategories",JSON.stringify(personalTaskCategories)); closeLayers(); toast("دسته شخصی حذف شد."); renderRoute(); break;
      }
      case "inline-task-add": {
        const input=document.getElementById("inlineTaskTitle"); const title=input?.value.trim();
        if(!title){toast("عنوان کار را وارد کنید.","warn");break;}
        personalTasks.unshift({title,meta:"امروز",source:"شخصی",priority:"normal",done:false}); toast("کار اضافه شد."); renderRoute(); break;
      }
      case "task-quick-capture": addPersonalTaskModal(); break;
      case "toggle-task-real": {
        const i=Number(target.dataset.index); if(personalTasks[i]){personalTasks[i].done=!personalTasks[i].done;toast(personalTasks[i].done?"کار انجام شد.":"کار دوباره باز شد.");renderRoute();} break;
      }
      case "move-tomorrow": {
        const i=Number(target.dataset.index); if(personalTasks[i]){personalTasks[i].meta="فردا";toast("کار به فردا منتقل شد.");renderRoute();} break;
      }
      case "schedule-task": calendarView="week"; navigate("calendar"); toast("کار برای زمان‌بندی انتخاب شد."); break;
      case "task-to-report": {
        const i=Number(target.dataset.index); if(personalTasks[i]){workActivities.unshift({title:personalTasks[i].title,category:"کار شخصی",duration:30,note:"از کارهای من ثبت شد",standard:false});toast("پیش‌نویس گزارش انجام ساخته شد.");navigate("work-report-new");} break;
      }
      case "calendar-view": calendarView=target.dataset.value||"week"; renderRoute(); break;
      case "calendar-prev": toast("بازه قبلی نمایش داده شد."); break;
      case "calendar-next": toast("بازه بعدی نمایش داده شد."); break;
      case "calendar-today": toast("تقویم به امروز برگشت."); break;
      case "calendar-event-detail": openModal("جزئیات رویداد",`<div class="detail-hero"><div><h2>جلسه هماهنگی عملیات</h2><p>شنبه ۲۷ تیر • ۱۱:۰۰ تا ۱۲:۰۰</p></div>${badge("جلسه","blue")}</div><div class="detail-section"><h3>اطلاعات</h3><div class="kv-grid"><div class="kv"><span>مکان</span><strong>اتاق جلسات مدیریت</strong></div><div class="kv"><span>برگزارکننده</span><strong>تیم عملیات</strong></div><div class="kv"><span>یادآوری</span><strong>۱۵ دقیقه قبل</strong></div></div></div>`,`<button class="btn" data-action="close-layer">بستن</button><button class="btn btn-primary" data-action="demo-save">ویرایش رویداد</button>`); break;
      case "select-conversation": selectedConversation=Number(target.dataset.index)||0; renderRoute(); break;
      case "send-chat-message": {
        const input=document.getElementById("chatInput"); if(!input?.value.trim()){toast("متن پیام خالی است.","warn");break;} input.value=""; replyingTo=null; toast("پیام ارسال شد."); renderRoute(); break;
      }
      case "reply-message": replyingTo=Number(target.dataset.index); document.getElementById("messageContextMenu")?.setAttribute("hidden",""); renderRoute(); setTimeout(()=>document.getElementById("chatInput")?.focus(),0); break;
      case "cancel-reply": replyingTo=null; renderRoute(); break;
      case "forward-message": document.getElementById("messageContextMenu")?.setAttribute("hidden",""); toast("پیام برای ارسال به گفت‌وگوی دیگر آماده شد."); break;
      case "delete-message": document.getElementById("messageContextMenu")?.setAttribute("hidden",""); toast("پیام خودتان حذف شد.","warn"); break;
      case "pin-message": { const i=Number(target.dataset.index); pinnedMessages.has(i)?pinnedMessages.delete(i):pinnedMessages.add(i); renderRoute(); break; }
      case "pin-conversation": { const i=Number(target.dataset.index); pinnedConversations.has(i)?pinnedConversations.delete(i):pinnedConversations.add(i); renderRoute(); break; }
      case "mute-conversation": document.getElementById("messageContextMenu")?.setAttribute("hidden",""); toast("اعلان‌های این گفتگو بی‌صدا شد."); break;
      case "archive-conversation": document.getElementById("messageContextMenu")?.setAttribute("hidden",""); toast("گفتگو بایگانی شد."); break;
      case "react-message": toast(`واکنش ${target.dataset.emoji||"👍"} ثبت شد.`); break;
      case "reaction-picker": showEmojiPicker(target,"message",target.dataset.index); break;
      case "composer-emoji": showEmojiPicker(target,"composer"); break;
      case "open-participant-selector": participantSelectorDrawer(); break;
      case "close-drawer-only": {
        drawerRoot.className="drawer-root"; drawerRoot.innerHTML="";
        const trigger=document.querySelector('[data-action="open-participant-selector"]'); if(trigger) trigger.focus();
        break;
      }
      case "confirm-event-participants": {
        drawerRoot.className="drawer-root"; drawerRoot.innerHTML="";
        const summary=document.getElementById('eventParticipantSummary'); if(summary)summary.innerHTML=participantSummaryHtml();
        const button=document.querySelector('[data-action="open-participant-selector"]'); if(button)button.textContent=eventParticipants.size?'ویرایش انتخاب‌ها':'انتخاب شرکت‌کنندگان';
        toast(`${num(eventParticipants.size)} شرکت‌کننده انتخاب شد.`); break;
      }
      case "toggle-event-participant": {
        const name=target.dataset.name; const p=D.people.find(x=>x.name===name); if(!p)break;
        const i=D.people.indexOf(p), subordinate=i<4;
        if(target.checked) eventParticipants.set(name,{initials:p.initials,unit:p.unit,job:p.job,subordinate,mode:'invite'}); else eventParticipants.delete(name);
        renderParticipantResults();
        const strip=document.getElementById('participantSelectedStrip'); if(strip)strip.innerHTML=participantSummaryHtml();
        break;
      }
      case "remove-event-participant": {
        eventParticipants.delete(target.dataset.name); renderParticipantResults();
        const strip=document.getElementById('participantSelectedStrip'); if(strip)strip.innerHTML=participantSummaryHtml();
        const summary=document.getElementById('eventParticipantSummary'); if(summary)summary.innerHTML=participantSummaryHtml();
        break;
      }
      case "save-calendar-event": {
        if(!eventParticipants.size) toast("رویداد بدون شرکت‌کننده ثبت شد."); else toast(`${num(eventParticipants.size)} شرکت‌کننده با قواعد دعوت و وظیفه افزوده شدند.`);
        eventParticipants.clear(); closeLayers(); break;
      }
      case "new-conversation": openModal("گفت‌وگوی جدید",`<div class="field"><label>جست‌وجوی شخص یا کانال</label><input placeholder="نام همکار، واحد یا کانال..." /></div><div class="people-select">${D.people.slice(0,5).map(p=>`<button><span class="avatar avatar-sm">${p.initials}</span><div><strong>${p.name}</strong><small>${p.job} • ${p.unit}</small></div></button>`).join("")}</div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="demo-save">شروع گفتگو</button>`); break;
      case "chat-files": toast("پنل فایل‌های مشترک در سمت چپ نمایش داده شده است."); break;
      case "chat-info": conversationInfoDrawer(); break;
      case "message-search": document.querySelector(".conversation-search input")?.focus(); break;
      case "add-personal-task": addPersonalTaskModal(); break;
      case "confirm-personal-task": {
        const title=document.getElementById("personalTaskTitle")?.value.trim();
        if(!title){toast("عنوان کار را وارد کنید.","warn");break;}
        const meta=document.getElementById("personalTaskTime")?.value||"امروز";
        const source=document.getElementById("personalTaskSource")?.value||"شخصی";
        personalTasks.unshift({title,meta,source,priority:"normal",done:false});
        closeLayers(); toast("کار به فهرست شخصی اضافه شد."); renderRoute(); break;
      }
      case "toggle-personal-task": {
        const visibleIndexes=personalTasks.map((x,i)=>({x,i})).filter(o=>!o.x.done).slice(0,4);
        const actual=visibleIndexes[Number(target.dataset.index||0)]?.i;
        if(actual!==undefined){personalTasks[actual].done=true;toast("کار انجام‌شده علامت خورد.");renderRoute();}
        break;
      }
      case "personal-task-menu": toast("گزینه‌های انتقال به فردا، زمان‌بندی، ثبت گزارش انجام و بایگانی در نسخه کامل نمایش داده می‌شوند."); break;
      case "all-personal-tasks": toast("صفحه کامل «کارهای من» در نسخه بعدی طراحی می‌شود."); break;
      case "open-calendar-day": toast("نمای کامل روز/هفته/ماه تقویم در صفحه مستقل باز می‌شود."); break;
      case "new-calendar-event": newCalendarEventModal(); break;
      case "add-activity-focus": document.getElementById("quickActivity")?.focus(); document.getElementById("quickActivity")?.scrollIntoView({behavior:"smooth",block:"center"}); break;
      case "add-quick-activity": {
        const selected=document.getElementById("quickActivity")?.value||"";
        if(selected==="__new__"){newActivityProposalModal();break;}
        const [title,category]=selected.split("|");
        const duration=Number(document.getElementById("quickDuration")?.value||30);
        const note=document.getElementById("quickNote")?.value.trim()||"ثبت سریع از میزکار";
        workActivities.unshift({title,category,duration,note,standard:true});
        toast("فعالیت به گزارش امروز اضافه شد."); renderRoute(); break;
      }
      case "quick-pick": { const input=document.getElementById("quickActivity"); if(input) input.value=target.dataset.value; break; }
      case "confirm-new-activity": {
        const title=document.getElementById("proposalTitle")?.value.trim();
        if(!title){toast("عنوان فعالیت را وارد کنید.","warn");break;}
        const category=document.getElementById("proposalCategory")?.value||"سایر";
        const duration=Number(document.getElementById("proposalDuration")?.value||30);
        const note=document.getElementById("proposalNote")?.value.trim()||"عنوان اولیه کاربر حفظ شده است.";
        workActivities.unshift({title,category,duration,note,standard:false}); closeLayers(); toast("فعالیت ثبت و درخواست استانداردسازی ایجاد شد."); renderRoute(); break;
      }
      case "remove-work-activity": workActivities.splice(Number(target.dataset.index||0),1); toast("فعالیت از گزارش امروز حذف شد.","warn"); renderRoute(); break;
      case "customize-workspace": toast("حالت شخصی‌سازی میزکار فعال شد؛ در نسخه Odoo چیدمان و میانبرها ذخیره می‌شوند."); break;
      case "send-letter": toast("نامه ارسال شد؛ گیرندگان و سابقه رسمی تثبیت شدند."); break;
      case "publish": toast("اعتبارسنجی نسخه موفق بود و نسخه منتشر شد."); break;
      case "resolve-attendance": toast("مغایرت حل و کاردکس روزانه برای محاسبه مجدد علامت‌گذاری شد."); break;
      case "parse-import": toast("فایل تحلیل و ردیف‌ها stage شدند."); break;
      case "commit-import": toast("فقط ردیف‌های آماده با موفقیت ثبت نهایی شدند."); break;
      case "download-report": toast("فایل Excel با اعمال Record Rule ساخته شد."); break;
      case "register-letter": toast("رخداد ثبت دبیرخانه و شماره رسمی ایجاد شد."); break;
      case "run-health": toast("بررسی سلامت کامل شد؛ ۲ هشدار پیکربندی باقی است.","warn"); break;
      case "save-settings": toast("تنظیمات Workspace ذخیره شد."); break;
      case "upload-document": toast("پنجره بارگذاری سند آماده است."); break;
      case "guard-entry": handleGuard("ورود"); break;
      case "guard-exit": handleGuard("خروج"); break;
      case "new-user": openModal("ایجاد کاربر",`<div class="progress-list"><div class="progress-item active"><span class="progress-dot">۱</span>انتخاب کارمند</div><div class="progress-item"><span class="progress-dot">۲</span>اطلاعات حساب</div><div class="progress-item"><span class="progress-dot">۳</span>جایگاه سازمانی</div><div class="progress-item"><span class="progress-dot">۴</span>نقش‌ها و مرور</div></div><div class="field" style="margin-top:16px"><label>کارمند موجود</label><select>${D.people.map(p=>`<option>${p.name} — ${p.code}</option>`).join("")}</select></div>`,`<button class="btn" data-action="close-layer">انصراف</button><button class="btn btn-primary" data-action="demo-save">ادامه</button>`); break;
      case "user-detail": { const u=D.users[target.dataset.user]; openDrawer("جزئیات کاربر",`<div class="guard-selected"><div class="person-photo">${initials(u.name)}</div><div><h3>${u.name}</h3><p>${u.job} • ${u.unit}</p>${badge(u.active?"فعال":"غیرفعال","green")}</div></div><div class="detail-section"><h3>منشأ دسترسی‌ها</h3><div class="chip-cloud">${u.securityRoles.map(r=>badge(D.roles[r]?.label||r,"blue")).join(" ")}</div></div><div class="detail-section"><h3>فضاهای کاری</h3><p>${u.workspaces.join("، ")}</p></div>`); break; }
      case "role-detail": toast("جزئیات نقش و منشأ انتساب در Drawer باز می‌شود."); break;
      case "new-role": case "new-unit": case "new-position": case "new-assignment": case "domain-settings": toast("فرم مدیریتی نمونه آماده و قابل اتصال به Backend است."); break;
      case "demo-save": closeLayers(); toast("اطلاعات نمونه ذخیره شد."); break;
      case "select-person": selectedPerson=D.people.find(p=>p.id===Number(target.dataset.id))||selectedPerson; renderRoute(); break;
      case "go-source": closeLayers(); navigate("attendance-review"); break;
      case "coverage": navigate("role-matrix"); break;
      default: if(action) toast("این کنترل در نمونه نمایشی قابل مشاهده است.");
    }
  }

  document.addEventListener("click",e=>{
    if(!e.target.closest('.cas-context-menu')) document.querySelectorAll('.cas-context-menu').forEach(m=>m.hidden=true);
    if(!e.target.closest('.emoji-picker-popover') && !e.target.closest('[data-action="reaction-picker"],[data-action="composer-emoji"]')) document.querySelectorAll('.emoji-picker-popover').forEach(x=>x.remove());
    const emojiBtn=e.target.closest('[data-emoji-choice]');
    if(emojiBtn){ const em=emojiBtn.dataset.emojiChoice; if(emojiBtn.dataset.targetType==='composer'){ const input=document.getElementById('chatInput'); if(input){input.value+=em; input.focus();} } else toast(`واکنش ${em} ثبت شد.`); emojiBtn.closest('.emoji-picker-popover')?.remove(); return; }
    const routeTarget=e.target.closest("[data-route]");
    if(routeTarget){ e.preventDefault(); navigate(routeTarget.dataset.route); return; }
    const actionTarget=e.target.closest("[data-action]");
    if(actionTarget){ e.preventDefault(); handleAction(actionTarget.dataset.action,actionTarget); }
  });
  roleSelect.addEventListener("change",e=>{
    currentUserId=e.target.value; localStorage.setItem("cas.user",currentUserId);
    currentRole=primaryRoleOf(currentUserId); renderRoleOptions();
    const landing=landingOf(currentUserId); navigate(allowed(currentRoute)?currentRoute:landing);
    toast(`کاربر آزمایشی به «${D.users[currentUserId].name}» تغییر کرد.`);
  });
  document.getElementById("mobileMenuButton").addEventListener("click",()=>sidebar.classList.toggle("open"));

  function showCasContextMenu(event, type, index){
    event.preventDefault();
    const menu=document.getElementById("messageContextMenu"); if(!menu)return;
    const isMessage=type==="message";
    const isMine=isMessage && document.querySelector(`[data-message-index="${index}"]`)?.classList.contains("me");
    menu.innerHTML=isMessage
      ? `<button data-action="reply-message" data-index="${index}">↩ پاسخ</button><button data-action="forward-message" data-index="${index}">➜ ارسال مجدد</button><button data-action="pin-message" data-index="${index}">📌 ${pinnedMessages.has(index)?"برداشتن سنجاق":"سنجاق پیام"}</button><button data-action="reaction-picker" data-index="${index}">☺ واکنش</button>${isMine?`<button class="danger" data-action="delete-message" data-index="${index}">حذف پیام</button>`:""}`
      : `<button data-action="pin-conversation" data-index="${index}">📌 ${pinnedConversations.has(index)?"برداشتن سنجاق":"سنجاق گفتگو"}</button><button data-action="mute-conversation" data-index="${index}">بی‌صدا کردن</button><button data-action="archive-conversation" data-index="${index}">بایگانی گفتگو</button>`;
    menu.hidden=false; menu.style.left=`${Math.min(event.clientX,window.innerWidth-190)}px`; menu.style.top=`${Math.min(event.clientY,window.innerHeight-220)}px`;
  }

  document.addEventListener("input",event=>{
    if(["participantLookup","participantUnit","participantScope"].includes(event.target.id)) renderParticipantResults();
  });
  document.addEventListener("change",event=>{
    if(["participantUnit","participantScope"].includes(event.target.id)) renderParticipantResults();
    if(event.target.matches('[data-participant-mode]')){
      const item=eventParticipants.get(event.target.dataset.participantMode); if(item){item.mode=event.target.value; eventParticipants.set(event.target.dataset.participantMode,item);}
      const strip=document.getElementById('participantSelectedStrip'); if(strip)strip.innerHTML=participantSummaryHtml();
    }
  });

  document.addEventListener("contextmenu",event=>{
    const message=event.target.closest("[data-message-index]");
    if(message){showCasContextMenu(event,"message",Number(message.dataset.messageIndex));return;}
    const conversation=event.target.closest("[data-conversation-index]");
    if(conversation){showCasContextMenu(event,"conversation",Number(conversation.dataset.conversationIndex));}
  });
  document.addEventListener("click",event=>{
    const menu=document.getElementById("messageContextMenu");
    if(menu && !event.target.closest("#messageContextMenu") && !event.target.closest("[data-message-index]") && !event.target.closest("[data-conversation-index]")) menu.hidden=true;
  },true);
  window.addEventListener("popstate",e=>{currentRoute=e.state?.route||getInitialRoute();renderSidebar();setBreadcrumb();renderRoute();});
  document.addEventListener("keydown",e=>{if(e.key==="Escape")closeLayers(); if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){e.preventDefault();globalSearch();} if(e.altKey&&e.key.toLowerCase()==="a"&&currentRoute==="home"){e.preventDefault();document.getElementById("quickActivity")?.focus();}});

  applyV7Settings();
  renderRoleOptions(); currentRoute=getInitialRoute();
  if(!allowed(currentRoute)) currentRoute=landingOf(currentUserId);
  renderSidebar(); setBreadcrumb(); renderRoute();
})();
