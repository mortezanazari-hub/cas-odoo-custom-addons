window.CAS_DATA = (() => {
  const ALL = ["employee","supervisor","manager","ceo","guard","secretariat","shift_planner","form_designer","workflow_designer","document_manager","system_admin"];
  const OPS = ["supervisor","manager","ceo","shift_planner","system_admin"];
  const MANAGERS = ["manager","ceo","system_admin"];
  const ADMIN = ["system_admin"];

  const roles = {
    employee:{label:"کاربر عادی",name:"مهدی رضایی",unit:"عملیات",landing:"home",accent:"blue"},
    supervisor:{label:"سرپرست",name:"مهدی رضایی",unit:"سرپرست عملیات",landing:"supervisor-dashboard",accent:"teal"},
    manager:{label:"مدیر واحد",name:"علی اکبری",unit:"مدیریت تولید سایت",landing:"manager-dashboard",accent:"blue"},
    ceo:{label:"مدیرعامل",name:"مرتضی نظری",unit:"مدیریت عالی",landing:"executive-dashboard",accent:"purple"},
    guard:{label:"نگهبان",name:"حسین مرادی",unit:"انتظامات - درب شمالی",landing:"guard",accent:"orange"},
    secretariat:{label:"دبیرخانه",name:"مریم فلاحی",unit:"دبیرخانه مرکزی",landing:"secretariat-register",accent:"purple"},
    shift_planner:{label:"برنامه‌ریز شیفت",name:"سارا محمدی",unit:"منابع انسانی",landing:"shift-planning",accent:"teal"},
    form_designer:{label:"طراح فرم",name:"نگار یوسفی",unit:"سیستم‌ها و روش‌ها",landing:"forms-admin",accent:"blue"},
    workflow_designer:{label:"طراح گردش‌کار",name:"امیر نادری",unit:"سیستم‌ها و روش‌ها",landing:"workflow-admin",accent:"purple"},
    document_manager:{label:"مدیر اسناد",name:"مریم فلاحی",unit:"دبیرخانه و اسناد",landing:"documents",accent:"teal"},
    system_admin:{label:"مدیر سامانه",name:"مدیر سیستم",unit:"فناوری اطلاعات",landing:"admin-center",accent:"red"}
  };

  const legacyNavGroups = [
    {title:"فضای من",items:[
      {route:"home",label:"خانه",icon:"⌂",roles:ALL},
      {route:"my-actions",label:"کارتابل من",icon:"✓",roles:ALL,count:12},
      {route:"urgent-actions",label:"اقدام‌های فوری",icon:"!",roles:ALL,count:3},
      {route:"approvals",label:"تأییدهای من",icon:"◎",roles:["supervisor","manager","ceo","secretariat","system_admin"],count:5},
      {route:"supervisor-dashboard",label:"داشبورد سرپرستی",icon:"◫",roles:["supervisor","manager","system_admin"]},
      {route:"manager-dashboard",label:"داشبورد مدیریت",icon:"▦",roles:["manager","ceo","system_admin"]},
      {route:"executive-dashboard",label:"داشبورد مدیرعامل",icon:"◈",roles:["ceo","system_admin"]}
    ]},
    {title:"فرم و فرایند",items:[
      {route:"form-catalog",label:"فرم‌های قابل ثبت",icon:"▤",roles:ALL},
      {route:"my-submissions",label:"ثبت‌های من",icon:"▥",roles:ALL},
      {route:"form-runtime",label:"اجرای فرم نمونه",icon:"✎",roles:ALL},
      {route:"workflow-instances",label:"گردش‌کارهای من",icon:"⇄",roles:ALL},
      {route:"forms-admin",label:"مدیریت فرم‌ها",icon:"▣",roles:["form_designer","system_admin"]},
      {route:"form-builder",label:"طراح دیداری فرم",icon:"✥",roles:["form_designer","system_admin"]},
      {route:"workflow-admin",label:"مدیریت گردش‌کار",icon:"⌘",roles:["workflow_designer","system_admin"]},
      {route:"workflow-designer",label:"طراح دیداری گردش‌کار",icon:"⌁",roles:["workflow_designer","system_admin"]},
      {route:"approval-policies",label:"سیاست‌های تأیید",icon:"◇",roles:["manager","workflow_designer","system_admin"]},
      {route:"delegations",label:"جانشینی تأیید",icon:"↹",roles:["manager","ceo","system_admin"]}
    ]},
    {title:"مکاتبات و اسناد",items:[
      {route:"correspondence",label:"مکاتبات",icon:"✉",roles:ALL,count:7},
      {route:"letter-compose",label:"نامه جدید",icon:"＋",roles:ALL},
      {route:"documents",label:"اسناد",icon:"▱",roles:ALL},
      {route:"ocr-queue",label:"صف پردازش OCR",icon:"◉",roles:["document_manager","secretariat","system_admin"]},
      {route:"secretariat-register",label:"دفتر وارده و صادره",icon:"▧",roles:["secretariat","manager","ceo","system_admin"]},
      {route:"correspondence-templates",label:"قالب‌های مکاتبات",icon:"▨",roles:["secretariat","document_manager","system_admin"]},
      {route:"signature-ledger",label:"دفتر امضا",icon:"✍",roles:["secretariat","ceo","system_admin"]}
    ]},
    {title:"شیفت و حضور",items:[
      {route:"my-shifts",label:"تقویم شیفت من",icon:"◷",roles:ALL},
      {route:"shift-planning",label:"برنامه‌ریزی شیفت",icon:"▦",roles:["shift_planner","manager","system_admin"]},
      {route:"shift-swaps",label:"جابه‌جایی شیفت",icon:"↔",roles:ALL},
      {route:"my-attendance",label:"حضور و کارکرد من",icon:"◴",roles:ALL},
      {route:"attendance-review",label:"رسیدگی مغایرت‌ها",icon:"⚠",roles:OPS,count:6},
      {route:"attendance-events",label:"رخدادهای تردد",icon:"⋮",roles:["guard","supervisor","manager","system_admin"]},
      {route:"attendance-import",label:"ورود فایل دستگاه",icon:"⇩",roles:["shift_planner","manager","system_admin"]},
      {route:"identity-mapping",label:"نگاشت شناسه‌ها",icon:"⌗",roles:["shift_planner","manager","system_admin"]},
      {route:"guard",label:"ثبت نگهبانی",icon:"⬙",roles:["guard","supervisor","manager","system_admin"]},
      {route:"devices",label:"محل‌ها و دستگاه‌ها",icon:"▣",roles:["manager","system_admin"]}
    ]},
    {title:"کاردکس و گزارش",items:[
      {route:"my-kardex",label:"کاردکس من",icon:"▦",roles:ALL},
      {route:"attendance-requests",label:"مرخصی و مأموریت",icon:"◫",roles:ALL},
      {route:"overtime",label:"اضافه‌کاری",icon:"＋",roles:ALL},
      {route:"kardex-operations",label:"عملیات کاردکس",icon:"⌑",roles:OPS},
      {route:"kardex-periods",label:"دوره‌ها و قفل ماه",icon:"▰",roles:MANAGERS},
      {route:"kardex-report",label:"گزارش Excel کاردکس",icon:"⇲",roles:["supervisor","manager","ceo","system_admin"]},
      {route:"work-reports",label:"گزارش کار",icon:"▤",roles:ALL},
      {route:"team-work-reports",label:"گزارش‌های حوزه من",icon:"▥",roles:OPS},
      {route:"work-report-new",label:"ثبت گزارش روزانه",icon:"✎",roles:ALL},
      {route:"work-stations",label:"ایستگاه‌های کاری",icon:"⌂",roles:["manager","system_admin"]}
    ]},
    {title:"مدیریت سامانه",items:[
      {route:"modules",label:"پوشش ۲۴ ماژول",icon:"◩",roles:["manager","ceo","form_designer","workflow_designer","document_manager","system_admin"]},
      {route:"sla-rules",label:"قوانین SLA",icon:"◴",roles:MANAGERS},
      {route:"document-settings",label:"ذخیره‌سازی و OCR",icon:"⚙",roles:["document_manager","system_admin"]},
      {route:"jalali-center",label:"مرکز تاریخ جلالی",icon:"◉",roles:ADMIN},
      {route:"system-health",label:"سلامت و ممیزی",icon:"⚙",roles:ADMIN},
      {route:"admin-center",label:"مرکز مدیریت CAS",icon:"⌘",roles:ADMIN},
      {route:"user-management",label:"کاربران و کارکنان",icon:"♙",roles:ADMIN},
      {route:"access-roles",label:"نقش‌ها و دسترسی‌ها",icon:"◈",roles:ADMIN},
      {route:"organization",label:"ساختار سازمانی",icon:"⌘",roles:ADMIN},
      {route:"positions",label:"سمت‌ها و جایگاه‌ها",icon:"▣",roles:ADMIN},
      {route:"assignments",label:"انتساب و جانشینی",icon:"↹",roles:ADMIN},
      {route:"settings-hub",label:"مرکز تنظیمات",icon:"⚙",roles:ADMIN},
      {route:"access-report",label:"گزارش دسترسی‌ها",icon:"▦",roles:ADMIN},
      {route:"audit-log",label:"رویدادها و ممیزی",icon:"≋",roles:ADMIN},
      {route:"workspace-settings",label:"تنظیمات Workspace",icon:"☷",roles:ADMIN},
      {route:"role-matrix",label:"ماتریس نقش و صفحه",icon:"▦",roles:ADMIN}
    ]}
  ];

  // منوی تجربه‌محور: نمایش بر اساس capability مؤثر، نه نام نقش یا ماژول فنی.
  const roleCapabilities = {
    employee:["workspace.home","personal.tasks","calendar.use","discuss.use","action.read","request.create","request.track","report.daily.create","attendance.self","correspondence.self","search.global","notification.read","history.read"],
    supervisor:["team.dashboard","team.actions","team.reports","attendance.team.review","shift.team.read","approval.decide","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    manager:["management.dashboard","team.actions","team.reports","attendance.team.review","shift.manage","approval.decide","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    ceo:["executive.dashboard","approval.decide","organization.analytics","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    guard:["guard.workspace","guard.event.create","guard.event.read","shift.self","report.daily.create","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    secretariat:["secretariat.workspace","correspondence.manage","document.manage","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    shift_planner:["shift.manage","attendance.import","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    form_designer:["form.design","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    workflow_designer:["workflow.design","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    document_manager:["document.manage","ocr.manage","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"],
    system_admin:["admin.center","admin.users","admin.roles","admin.organization","admin.positions","admin.assignments","admin.settings","admin.audit","admin.health","technical.tools","personal.tasks","calendar.use","discuss.use","search.global","notification.read","history.read"]
  };

  const navGroups = [
    {title:"فضای کاری",items:[
      {route:"home",label:"میزکار",icon:"⌂",permissions:["workspace.home"]},
      {route:"personal-tasks",label:"کارهای من",icon:"✓",permissions:["personal.tasks"],count:4},
      {route:"calendar",label:"تقویم",icon:"◷",permissions:["calendar.use"]},
      {route:"messages",label:"گفت‌وگوها",icon:"✉",permissions:["discuss.use"],count:6},
      {route:"my-actions",label:"نیازمند اقدام",icon:"!",permissions:["action.read"],count:12},
      {route:"global-search-page",label:"جست‌وجوی سازمان",icon:"⌕",permissions:["search.global"]},
      {route:"notifications-center",label:"مرکز اعلان‌ها",icon:"◔",permissions:["notification.read"],count:4},
      {route:"recent-history",label:"تاریخچه اخیر",icon:"↶",permissions:["history.read"]},
      {route:"request-center",label:"ثبت درخواست",icon:"＋",permissions:["request.create"]},
      {route:"request-tracking",label:"پیگیری درخواست‌ها",icon:"◫",permissions:["request.track"]},
      {route:"work-report-new",label:"گزارش روزانه",icon:"✎",permissions:["report.daily.create"]},
      {route:"attendance-hub",label:"حضور و شیفت",icon:"◷",permissions:["attendance.self"]},
      {route:"correspondence",label:"مکاتبات",icon:"▧",permissions:["correspondence.self"]}
    ]},
    {title:"حوزه مسئولیت",items:[
      {route:"supervisor-dashboard",label:"مرکز سرپرستی",icon:"◫",permissions:["team.dashboard"]},
      {route:"team-center",label:"تیم و درخواست‌ها",icon:"▦",permissions:["team.actions"]},
      {route:"manager-dashboard",label:"داشبورد مدیریت",icon:"▦",permissions:["management.dashboard"]},
      {route:"executive-dashboard",label:"داشبورد مدیرعامل",icon:"◈",permissions:["executive.dashboard"]},
      {route:"guard-workspace",label:"ثبت و پایش تردد",icon:"⬙",permissions:["guard.workspace"]},
      {route:"secretariat-register",label:"دبیرخانه مرکزی",icon:"▧",permissions:["secretariat.workspace"]},
      {route:"shift-planning",label:"برنامه‌ریزی شیفت",icon:"▦",permissions:["shift.manage"]}
    ]},
    {title:"مدیریت سامانه",items:[
      {route:"admin-center",label:"مرکز مدیریت CAS",icon:"⌘",permissions:["admin.center"]},
      {route:"user-management",label:"کاربران و کارکنان",icon:"♙",permissions:["admin.users"]},
      {route:"access-roles",label:"نقش‌ها و دسترسی‌ها",icon:"◈",permissions:["admin.roles"]},
      {route:"organization",label:"ساختار سازمانی",icon:"⌘",permissions:["admin.organization"]},
      {route:"positions",label:"سمت‌ها و جایگاه‌ها",icon:"▣",permissions:["admin.positions"]},
      {route:"assignments",label:"انتساب و جانشینی",icon:"↹",permissions:["admin.assignments"]},
      {route:"settings-hub",label:"مرکز تنظیمات",icon:"⚙",permissions:["admin.settings"]},
      {route:"audit-log",label:"رویدادها و ممیزی",icon:"≋",permissions:["admin.audit"]},
      {route:"system-health",label:"سلامت سامانه",icon:"◉",permissions:["admin.health"]}
    ]},
    {title:"ابزارهای تخصصی",items:[
      {route:"forms-admin",label:"مدیریت فرم‌ها",icon:"▣",permissions:["form.design"]},
      {route:"workflow-admin",label:"مدیریت گردش‌کار",icon:"⌘",permissions:["workflow.design"]},
      {route:"documents",label:"مدیریت اسناد",icon:"▱",permissions:["document.manage"]},
      {route:"ocr-queue",label:"صف OCR",icon:"◉",permissions:["ocr.manage"]},
      {route:"modules",label:"پوشش ماژول‌ها",icon:"◩",permissions:["technical.tools"]}
    ]}
  ];

  const modules = [
    {code:"cas_core",title:"هسته فنی CAS",family:"پایه",purpose:"نقطه اتکای مشترک افزونه‌ها و مرز وابستگی فنی.",ui:"فاقد منوی مستقل؛ صفحه سلامت فقط برای مدیر سامانه.",roles:["system_admin"],route:"system-health",icon:"C"},
    {code:"cas_jalali",title:"تقویم جلالی",family:"بومی‌سازی",purpose:"ورودی و نمایش جلالی بدون تغییر ذخیره استاندارد Odoo.",ui:"در همه فیلدهای تاریخ و انتخابگرها.",roles:ALL,route:"jalali-center",icon:"ش"},
    {code:"cas_jalali_hr",title:"پل جلالی کارکنان",family:"بومی‌سازی",purpose:"تاریخ‌های جلالی timeline کارکنان و قرارداد.",ui:"داخل پروفایل و timeline کارمند.",roles:["manager","system_admin"],route:"jalali-center",icon:"HR"},
    {code:"cas_jalali_mail",title:"پل جلالی پیام‌ها",family:"بومی‌سازی",purpose:"نمایش تاریخ جلالی در پیام و تاریخچه تغییرات.",ui:"در Chatter و timeline همه رکوردها.",roles:ALL,route:"jalali-center",icon:"✉"},
    {code:"cas_jalali_search",title:"فیلتر جلالی",family:"بومی‌سازی",purpose:"فیلتر بازه تاریخ شمسی و تبدیل به domain استاندارد.",ui:"در جست‌وجو و فیلتر صفحات داده.",roles:ALL,route:"jalali-center",icon:"⌕"},
    {code:"cas_jalali_qweb",title:"گزارش جلالی",family:"بومی‌سازی",purpose:"رندر جلالی تاریخ در PDF، QWeb و ایمیل.",ui:"در پیش‌نمایش و خروجی رسمی.",roles:ALL,route:"jalali-center",icon:"PDF"},
    {code:"cas_jalali_suite",title:"بسته یکپارچه جلالی",family:"بومی‌سازی",purpose:"نصب هماهنگ همه bridgeهای جلالی.",ui:"فاقد صفحه روزمره؛ وضعیت نصب در مرکز جلالی.",roles:["system_admin"],route:"jalali-center",icon:"JS"},
    {code:"cas_form_core",title:"هسته فرم",family:"فرم و فرایند",purpose:"فرم نسخه‌دار، ساختار منطقی، پاسخ تایپ‌شده و submission.",ui:"تعاریف، نسخه‌ها، ثبت‌ها و جزئیات پاسخ.",roles:ALL,route:"form-catalog",icon:"▤"},
    {code:"cas_form_builder",title:"طراح دیداری فرم",family:"فرم و فرایند",purpose:"طراحی drag-and-drop نسخه پیش‌نویس فرم.",ui:"پالت فیلد، بوم، پنل ویژگی‌ها و کنترل انتشار.",roles:["form_designer","system_admin"],route:"form-builder",icon:"✥"},
    {code:"cas_dynamic_form",title:"اجرای فرم پویا",family:"فرم و فرایند",purpose:"اجرای RTL فرم منتشرشده، ذخیره پیش‌نویس و ارسال.",ui:"کاتالوگ فرم و runtime تخصصی.",roles:ALL,route:"form-runtime",icon:"✎"},
    {code:"cas_workflow_core",title:"هسته گردش‌کار",family:"فرم و فرایند",purpose:"حالت، گذار، مسئول، SLA، نمونه اجرایی و تاریخچه.",ui:"کارتابل نمونه‌ها، تعریف، نسخه و تاریخچه.",roles:ALL,route:"workflow-instances",icon:"⇄"},
    {code:"cas_workflow_designer",title:"طراح گردش‌کار",family:"فرم و فرایند",purpose:"طراحی node-based و اتصال گره‌ها به فرم.",ui:"بوم گراف، تنظیم گره و binding فرم.",roles:["workflow_designer","system_admin"],route:"workflow-designer",icon:"⌁"},
    {code:"cas_approval_core",title:"تأیید چندمرحله‌ای",family:"فرم و فرایند",purpose:"سیاست، مرحله، جانشینی، تصمیم و تاریخچه رسمی.",ui:"صندوق تأیید، جزئیات تصمیم، سیاست و نمایندگی.",roles:["supervisor","manager","ceo","system_admin"],route:"approvals",icon:"◎"},
    {code:"cas_action_hub",title:"کارتابل و SLA",family:"فضای کار",purpose:"تجمیع اقدام‌های قابل انجام با مهلت و لینک منبع.",ui:"کارتابل من، فوری، همه اقدامات و قوانین SLA.",roles:ALL,route:"my-actions",icon:"✓"},
    {code:"cas_document_core",title:"هسته اسناد",family:"مکاتبات و اسناد",purpose:"سند نسخه‌دار، پیوند رکورد، پوشه، برچسب، storage و OCR.",ui:"کتابخانه سند، نسخه‌ها، صف OCR و تنظیم backend.",roles:ALL,route:"documents",icon:"▱"},
    {code:"cas_correspondence",title:"مکاتبات سازمانی",family:"مکاتبات و اسناد",purpose:"نامه رسمی، گیرنده، ارجاع، رسید، پاسخ و محرمانگی.",ui:"صندوق‌ها، پیش‌نویس، نامه‌خوان و ارجاع.",roles:ALL,route:"correspondence",icon:"✉"},
    {code:"cas_correspondence_advanced",title:"دبیرخانه پیشرفته",family:"مکاتبات و اسناد",purpose:"دفتر وارده/صادره، قالب، PDF رسمی و امضا.",ui:"دفتر ثبت، قالب‌ها و دفتر امضا.",roles:["secretariat","manager","ceo","system_admin"],route:"secretariat-register",icon:"▧"},
    {code:"cas_shift_management",title:"مدیریت شیفت",family:"شیفت و حضور",purpose:"سیاست، شیفت، الگوی چرخشی، انتساب، snapshot و جابه‌جایی.",ui:"تقویم من، برنامه‌ریزی، swap، تعطیلات و سیاست‌ها.",roles:ALL,route:"my-shifts",icon:"◷"},
    {code:"cas_attendance_core",title:"هسته حضور",family:"شیفت و حضور",purpose:"رخداد خام append-only و تطبیق با روز شیفت.",ui:"حضور من، مغایرت‌ها، رخدادها، دستگاه و خرابی.",roles:ALL,route:"my-attendance",icon:"◴"},
    {code:"cas_attendance_operations",title:"عملیات حضور",family:"شیفت و حضور",purpose:"ورود Excel مرحله‌ای، نگاشت هویت و batch نگهبانی.",ui:"ورود فایل، staging، نگاشت و ثبت نگهبانی.",roles:["guard","shift_planner","manager","system_admin"],route:"guard",icon:"⇩"},
    {code:"cas_kardex_management",title:"مدیریت کاردکس",family:"کاردکس و گزارش",purpose:"محاسبه دقیقه‌ای، درخواست، اضافه‌کاری، قفل و بازگشایی.",ui:"کاردکس من، درخواست‌ها، عملیات، دوره و بازگشایی.",roles:ALL,route:"my-kardex",icon:"▦"},
    {code:"cas_kardex_report",title:"گزارش کاردکس",family:"کاردکس و گزارش",purpose:"خروجی Excel جزئی و خلاصه با فیلتر امن.",ui:"سازنده گزارش و تاریخچه خروجی‌ها.",roles:["supervisor","manager","ceo","system_admin"],route:"kardex-report",icon:"⇲"},
    {code:"cas_work_report",title:"گزارش کار روزانه",family:"کاردکس و گزارش",purpose:"گزارش فعالیت، ایستگاه، نمایندگی، مهلت و تأیید.",ui:"ثبت روزانه، گزارش‌های من/حوزه، ایستگاه و Excel.",roles:ALL,route:"work-reports",icon:"▤"},
    {code:"cas_workspace",title:"پوسته اختصاصی CAS",family:"فضای کار",purpose:"shell واحد RTL، route داخلی، dashboard، صفحه و drawer.",ui:"همین تجربه یکپارچه و صفحات نقش‌محور.",roles:ALL,route:"home",icon:"CAS"}
  ];

  const people = [
    {id:1,name:"حسین مرادی",code:"EMP-0041",job:"نگهبان",unit:"انتظامات",status:"in",initials:"حم",last:"۰۷:۲۹"},
    {id:2,name:"سارا احمدی",code:"EMP-0088",job:"کارشناس کنترل کیفیت",unit:"کیفیت",status:"out",initials:"سا",last:"۱۷:۰۳"},
    {id:3,name:"رضا اسدی",code:"EMP-0026",job:"سرپرست تولید",unit:"تولید سایت",status:"in",initials:"را",last:"۰۶:۵۸"},
    {id:4,name:"مریم فلاحی",code:"EMP-0062",job:"مسئول دبیرخانه",unit:"مدیریت اداری",status:"in",initials:"مف",last:"۰۸:۰۶"},
    {id:5,name:"امیر نادری",code:"EMP-0094",job:"کارشناس سیستم‌ها",unit:"برنامه‌ریزی و توسعه",status:"in",initials:"ان",last:"۰۸:۱۲"},
    {id:6,name:"فرهاد محمدی",code:"EMP-0013",job:"اپراتور خط تولید",unit:"تولید سایت",status:"out",initials:"فم",last:"۱۹:۳۴"},
    {id:7,name:"نیلوفر کریمی",code:"EMP-0101",job:"کارشناس منابع انسانی",unit:"منابع انسانی",status:"in",initials:"نک",last:"۰۸:۱۸"},
    {id:8,name:"کاظم صالحی",code:"EMP-0037",job:"تکنیسین برق صنعتی",unit:"فنی",status:"in",initials:"کس",last:"۰۷:۰۴"},
    {id:9,name:"علی رستمی",code:"EMP-0072",job:"کارشناس خرید داخلی",unit:"خرید",status:"out",initials:"عر",last:"۱۶:۴۵"}
  ];

  const actions = [
    {title:"رفع مغایرت حضور نگهبانی",source:"حضور و غیاب",subject:"حسین مرادی - شیفت شب",deadline:"امروز، ۱۰:۰۰",priority:"بالا",status:"SLA در خطر",tone:"red",icon:"⚠"},
    {title:"تصمیم درباره درخواست مرخصی ساعتی",source:"منابع انسانی",subject:"سارا احمدی - از ساعت ۱۲ تا ۱۶",deadline:"امروز، ۱۱:۰۰",priority:"بالا",status:"در انتظار تصمیم",tone:"orange",icon:"◷"},
    {title:"تأیید گزارش کار شیفت ریخته‌گری",source:"گزارش کار",subject:"رضا اسدی - گزارش تولید و توقفات",deadline:"امروز، ۱۲:۰۰",priority:"بالا",status:"در انتظار تأیید",tone:"blue",icon:"▤"},
    {title:"پیگیری ارجاع نامه ۱۴۰۵/د/۰۰۲۴",source:"مکاتبات",subject:"درخواست تأمین قطعات",deadline:"۳۱ تیر، ۱۰:۰۰",priority:"متوسط",status:"در زمان",tone:"green",icon:"✉"},
    {title:"بازبینی فرم درخواست خرید",source:"فرم و فرایند",subject:"درخواست انبار مرکزی",deadline:"۳۰ تیر، ۱۶:۰۰",priority:"متوسط",status:"در زمان",tone:"green",icon:"▤"},
    {title:"تعیین تکلیف ردیف‌های ناشناخته ورود فایل",source:"حضور و غیاب",subject:"فایل دستگاه درب جنوبی",deadline:"امروز، ۱۴:۳۰",priority:"متوسط",status:"نیازمند نگاشت",tone:"purple",icon:"⇩"}
  ];

  const letters = [
    {id:1,no:"۱۴۰۵/د/۰۰۲۴",subject:"درخواست تأمین قطعات یدکی خط شات‌بلاست",from:"مدیریت تولید سایت",to:"مدیریت خرید",date:"۲۷ تیر ۱۴۰۵",conf:"داخلی",state:"ارجاع شده",unread:true},
    {id:2,no:"۱۴۰۵/و/۰۱۲۱",subject:"ابلاغ برنامه ممیزی داخلی فصل دوم",from:"مدیریت کیفیت",to:"مدیران واحدها",date:"۲۶ تیر ۱۴۰۵",conf:"عادی",state:"دریافت شده",unread:true},
    {id:3,no:"۱۴۰۵/د/۰۰۱۹",subject:"گزارش خرابی دستگاه حضور و غیاب درب جنوبی",from:"انتظامات",to:"فناوری اطلاعات",date:"۲۵ تیر ۱۴۰۵",conf:"داخلی",state:"در حال اقدام",unread:false},
    {id:4,no:"پیش‌نویس",subject:"پیشنهاد اصلاح شیوه‌نامه ثبت اضافه‌کاری",from:"مدیریت منابع انسانی",to:"مدیرعامل",date:"۲۴ تیر ۱۴۰۵",conf:"محرمانه",state:"پیش‌نویس",unread:false},
    {id:5,no:"۱۴۰۵/ص/۰۳۳۰",subject:"پاسخ به استعلام تأمین‌کننده مواد اولیه",from:"مدیریت خرید",to:"شرکت فولاد پارس",date:"۲۳ تیر ۱۴۰۵",conf:"عادی",state:"صادر شده",unread:false}
  ];

  const documents = [
    {name:"گزارش رسمی مغایرت حضور - تیر ۱۴۰۵",format:"PDF",size:"۱.۸ MB",version:"نسخه ۳",folder:"حضور و کارکرد",status:"تأییدشده",icon:"▧"},
    {name:"روش اجرایی ثبت و ارجاع مکاتبات",format:"DOCX",size:"۸۴۰ KB",version:"نسخه ۵",folder:"روش‌های اجرایی",status:"در بازبینی",icon:"▤"},
    {name:"خروجی کاردکس خرداد ۱۴۰۵",format:"XLSX",size:"۲.۳ MB",version:"نسخه ۱",folder:"گزارش‌های کاردکس",status:"قفل‌شده",icon:"▦"},
    {name:"فرم درخواست خرید تجهیزات ایمنی",format:"PDF",size:"۴۹۰ KB",version:"نسخه ۲",folder:"فرم‌های سازمانی",status:"منتشرشده",icon:"▧"},
    {name:"قرارداد سرویس دستگاه حضور و غیاب",format:"PDF",size:"۳.۱ MB",version:"نسخه ۱",folder:"قراردادها",status:"OCR شده",icon:"▧"},
    {name:"صورتجلسه کمیته بهره‌وری",format:"DOCX",size:"۶۷۰ KB",version:"نسخه ۴",folder:"صورتجلسات",status:"در گردش",icon:"▤"},
    {name:"دستورالعمل شیفت ۲-۲-۲ نگهبانی",format:"PDF",size:"۱.۱ MB",version:"نسخه ۲",folder:"شیفت و نگهبانی",status:"منتشرشده",icon:"▧"},
    {name:"نقشه گردش‌کار درخواست مأموریت",format:"PNG",size:"۵۳۰ KB",version:"نسخه ۱",folder:"معماری فرایند",status:"فعال",icon:"◩"}
  ];

  const forms = [
    {title:"درخواست مرخصی ساعتی",code:"FR-HR-LEAVE-01",category:"منابع انسانی",duration:"۳ دقیقه",version:"نسخه ۴",status:"فعال"},
    {title:"گزارش روزانه نگهبانی",code:"FR-ADM-SEC-DR-01",category:"انتظامات",duration:"۵ دقیقه",version:"نسخه ۳",status:"فعال"},
    {title:"درخواست خرید کالا و خدمات",code:"FR-PUR-REQ-02",category:"خرید",duration:"۸ دقیقه",version:"نسخه ۶",status:"فعال"},
    {title:"گزارش خرابی تجهیزات",code:"FR-MNT-FAIL-01",category:"فنی",duration:"۶ دقیقه",version:"نسخه ۲",status:"فعال"},
    {title:"ثبت عدم انطباق کیفیت",code:"FR-QC-NCR-01",category:"کیفیت",duration:"۷ دقیقه",version:"نسخه ۵",status:"فعال"},
    {title:"درخواست مأموریت",code:"FR-HR-MIS-01",category:"منابع انسانی",duration:"۴ دقیقه",version:"نسخه ۳",status:"فعال"}
  ];

  const submissions = [
    {number:"FRM/۱۴۰۵/۰۰۳۸۱",form:"درخواست مرخصی ساعتی",date:"۲۷ تیر ۱۴۰۵ - ۰۸:۲۲",owner:"مهدی رضایی",state:"در گردش",version:"۴"},
    {number:"FRM/۱۴۰۵/۰۰۳۷۲",form:"گزارش روزانه نگهبانی",date:"۲۶ تیر ۱۴۰۵ - ۱۹:۴۴",owner:"حسین مرادی",state:"تأییدشده",version:"۳"},
    {number:"FRM/۱۴۰۵/۰۰۳۶۶",form:"درخواست خرید کالا و خدمات",date:"۲۶ تیر ۱۴۰۵ - ۱۲:۱۰",owner:"رضا اسدی",state:"نیازمند اصلاح",version:"۶"},
    {number:"FRM/۱۴۰۵/۰۰۳۴۹",form:"ثبت عدم انطباق کیفیت",date:"۲۵ تیر ۱۴۰۵ - ۱۰:۳۵",owner:"سارا احمدی",state:"بسته‌شده",version:"۵"},
    {number:"FRM/۱۴۰۵/۰۰۳۲۸",form:"گزارش خرابی تجهیزات",date:"۲۴ تیر ۱۴۰۵ - ۰۷:۴۵",owner:"کاظم صالحی",state:"در انتظار تأیید",version:"۲"}
  ];

  const workflowInstances = [
    {no:"WF/۱۴۰۵/۰۰۱۹۱",title:"درخواست مرخصی ساعتی",record:"FRM/۱۴۰۵/۰۰۳۸۱",state:"تأیید سرپرست",owner:"مهدی رضایی",deadline:"امروز ۱۱:۰۰",status:"درحال اجرا"},
    {no:"WF/۱۴۰۵/۰۰۱۸۹",title:"درخواست خرید",record:"FRM/۱۴۰۵/۰۰۳۶۶",state:"اصلاح درخواست",owner:"رضا اسدی",deadline:"فردا ۱۰:۰۰",status:"درحال اجرا"},
    {no:"WF/۱۴۰۵/۰۰۱۸۱",title:"ثبت عدم انطباق",record:"FRM/۱۴۰۵/۰۰۳۴۹",state:"اقدام اصلاحی",owner:"سارا احمدی",deadline:"۳۱ تیر",status:"درحال اجرا"},
    {no:"WF/۱۴۰۵/۰۰۱۷۰",title:"گزارش کار روزانه",record:"WR/۱۴۰۵/۰۹۲۱",state:"پایان",owner:"حسین مرادی",deadline:"-",status:"تکمیل‌شده"}
  ];

  const approvals = [
    {title:"درخواست مرخصی ساعتی",requester:"سارا احمدی",role:"سرپرست مستقیم",deadline:"امروز ۱۱:۰۰",stage:"مرحله ۱ از ۲",status:"در انتظار تصمیم",priority:"بالا"},
    {title:"خرید تجهیزات ایمنی",requester:"رضا اسدی",role:"مدیر واحد",deadline:"امروز ۱۵:۰۰",stage:"مرحله ۲ از ۳",status:"در انتظار تصمیم",priority:"بالا"},
    {title:"اضافه‌کاری شیفت تعمیرات",requester:"کاظم صالحی",role:"مدیرعامل",deadline:"فردا ۱۰:۰۰",stage:"مرحله ۲ از ۲",status:"در انتظار تصمیم",priority:"متوسط"},
    {title:"گزارش کار شیفت ریخته‌گری",requester:"رضا اسدی",role:"سرپرست",deadline:"امروز ۱۲:۰۰",stage:"مرحله ۱ از ۱",status:"در انتظار تصمیم",priority:"بالا"}
  ];

  const attendanceLogs = [
    {name:"نیلوفر کریمی",type:"ورود",time:"۰۸:۱۸",source:"ثبت نگهبانی",gate:"درب شمالی"},
    {name:"امیر نادری",type:"ورود",time:"۰۸:۱۲",source:"دستگاه",gate:"درب اصلی"},
    {name:"مریم فلاحی",type:"ورود",time:"۰۸:۰۶",source:"ثبت نگهبانی",gate:"درب شمالی"},
    {name:"کاظم صالحی",type:"ورود",time:"۰۷:۰۴",source:"دستگاه",gate:"درب جنوبی"},
    {name:"رضا اسدی",type:"ورود",time:"۰۶:۵۸",source:"دستگاه",gate:"درب اصلی"},
    {name:"فرهاد محمدی",type:"خروج",time:"۱۹:۳۴",source:"ثبت نگهبانی",gate:"درب جنوبی"}
  ];


  const users = {
    employee_demo:{id:"employee_demo",name:"مهدی رضایی",employee:"EMP-0054",job:"کارشناس عملیات",unit:"عملیات",company:"چدن‌آرا شمال",securityRoles:["employee"],workspaces:["فضای شخصی"],active:true,lastLogin:"امروز ۰۸:۰۲"},
    supervisor_demo:{id:"supervisor_demo",name:"رضا اسدی",employee:"EMP-0026",job:"سرپرست تولید",unit:"تولید سایت",company:"چدن‌آرا شمال",securityRoles:["employee","supervisor"],workspaces:["فضای شخصی","سرپرستی تولید"],active:true,lastLogin:"امروز ۰۷:۱۲"},
    guard_demo:{id:"guard_demo",name:"حسین مرادی",employee:"EMP-0041",job:"نگهبان",unit:"انتظامات",company:"چدن‌آرا شمال",securityRoles:["employee","guard"],workspaces:["فضای شخصی","ثبت تردد"],active:true,lastLogin:"امروز ۰۶:۵۵"},
    secretariat_demo:{id:"secretariat_demo",name:"مریم فلاحی",employee:"EMP-0062",job:"مسئول دبیرخانه",unit:"مدیریت اداری",company:"چدن‌آرا شمال",securityRoles:["employee","secretariat","document_manager"],workspaces:["فضای شخصی","دبیرخانه"],active:true,lastLogin:"امروز ۰۸:۰۶"},
    admin_demo:{id:"admin_demo",name:"مدیر سیستم",employee:null,job:"مدیر سامانه",unit:"فناوری اطلاعات",company:"چدن‌آرا شمال",securityRoles:["employee","manager","system_admin","form_designer","workflow_designer","document_manager","shift_planner"],workspaces:["مرکز مدیریت","فضای شخصی"],active:true,lastLogin:"اکنون"}
  };

  const orgUnits = [
    {id:"HQ",name:"شرکت چدن‌آرا شمال",type:"شرکت",parent:null,manager:"مرتضی نظری",members:86,status:"فعال"},
    {id:"OPS",name:"معاونت اجرایی",type:"معاونت",parent:"HQ",manager:"علی اکبری",members:48,status:"فعال"},
    {id:"PROD",name:"مدیریت تولید سایت",type:"مدیریت",parent:"OPS",manager:"علی اکبری",members:24,status:"فعال"},
    {id:"SEC",name:"انتظامات",type:"واحد",parent:"OPS",manager:"حسن مرادی",members:7,status:"فعال"},
    {id:"ADM",name:"مدیریت اداری",type:"مدیریت",parent:"HQ",manager:"مریم احمدی",members:16,status:"فعال"},
    {id:"IT",name:"فناوری اطلاعات",type:"واحد",parent:"ADM",manager:"—",members:2,status:"بدون مدیر"},
    {id:"DEV",name:"برنامه‌ریزی و توسعه",type:"مدیریت",parent:"HQ",manager:"امیر نادری",members:8,status:"فعال"}
  ];

  const accessRoles = [
    {id:"employee",name:"کاربر پایه",type:"سیستمی",scope:"رکوردهای شخصی",members:82,source:"گروه Odoo",status:"فعال"},
    {id:"supervisor",name:"سرپرست حوزه",type:"سازمانی",scope:"واحد و زیرواحد",members:9,source:"سمت سازمانی",status:"فعال"},
    {id:"guard",name:"اپراتور تردد",type:"سفارشی",scope:"دروازه‌های مجاز",members:6,source:"انتساب مستقیم",status:"فعال"},
    {id:"secretariat",name:"دبیرخانه",type:"سفارشی",scope:"دفتر مرکزی",members:3,source:"سمت سازمانی",status:"فعال"},
    {id:"system_admin",name:"مدیر سامانه",type:"سیستمی",scope:"تمام شرکت‌های مجاز",members:2,source:"گروه Odoo",status:"حساس"}
  ];

  const positions = [
    {code:"POS-001",title:"مدیر تولید سایت",unit:"مدیریت تولید سایت",holder:"علی اکبری",manager:"معاونت اجرایی",roles:"مدیر حوزه",status:"اشغال‌شده"},
    {code:"POS-014",title:"سرپرست تولید",unit:"مدیریت تولید سایت",holder:"رضا اسدی",manager:"علی اکبری",roles:"سرپرست حوزه",status:"اشغال‌شده"},
    {code:"POS-031",title:"مسئول فناوری اطلاعات",unit:"فناوری اطلاعات",holder:"—",manager:"مدیر اداری",roles:"کاربر پایه",status:"خالی"},
    {code:"POS-044",title:"نگهبان",unit:"انتظامات",holder:"۶ متصدی",manager:"سرپرست انتظامات",roles:"اپراتور تردد",status:"چندمتصدی"}
  ];

  const assignments = [
    {person:"رضا اسدی",kind:"سمت اصلی",target:"سرپرست تولید",scope:"تولید سایت",from:"۱۴۰۴/۰۱/۰۱",to:"—",status:"فعال"},
    {person:"مریم فلاحی",kind:"جانشینی",target:"مسئول دبیرخانه",scope:"دفتر مرکزی",from:"۱۴۰۵/۰۴/۲۵",to:"۱۴۰۵/۰۵/۰۵",status:"فعال"},
    {person:"امیر نادری",kind:"دسترسی موقت",target:"طراح گردش‌کار",scope:"شرکت",from:"۱۴۰۵/۰۴/۲۰",to:"۱۴۰۵/۰۴/۳۰",status:"نزدیک انقضا"}
  ];
  const routes = {};
  legacyNavGroups.forEach(group => group.items.forEach(item => routes[item.route] = item));
  navGroups.forEach(group => group.items.forEach(item => routes[item.route] = {...(routes[item.route]||{}),...item}));

  return {roles,users,orgUnits,accessRoles,positions,assignments,navGroups,legacyNavGroups,roleCapabilities,modules,people,actions,letters,documents,forms,submissions,workflowInstances,approvals,attendanceLogs,routes,ALL,OPS,MANAGERS,ADMIN};
})();
