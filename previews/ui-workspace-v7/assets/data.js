window.CAS_DATA = {
  routes: [
    {id:"home",label:"میزکار",icon:"⌂",group:"روز کاری"},
    {id:"tasks",label:"کارهای من",icon:"✓",group:"روز کاری",count:4},
    {id:"calendar",label:"تقویم",icon:"▦",group:"روز کاری"},
    {id:"conversations",label:"گفت‌وگوها",icon:"💬",group:"روز کاری",count:4},
    {id:"actions",label:"نیازمند اقدام",icon:"!",group:"پیگیری",count:5},
    {id:"notifications",label:"مرکز اعلان‌ها",icon:"◔",group:"پیگیری"},
    {id:"history",label:"تاریخچه اخیر",icon:"↶",group:"پیگیری"},
    {id:"requests",label:"درخواست‌ها",icon:"◇",group:"سازمان"},
    {id:"activity",label:"گزارش فعالیت",icon:"▤",group:"سازمان"},
    {id:"attendance",label:"حضور و شیفت",icon:"◴",group:"سازمان"},
    {id:"correspondence",label:"مکاتبات",icon:"✉",group:"سازمان"},
    {id:"settings",label:"تنظیمات",icon:"⚙",group:"سیستم"}
  ],
  conversations: [
    {id:1,name:"تیم عملیات",kind:"گروه واحد",avatar:"تو",unread:3,last:"صورتجلسه امروز در همین گفتگو قرار گرفت.",time:"۰۹:۳۴",online:true},
    {id:2,name:"مریم فلاحی",kind:"گفت‌وگوی مستقیم",avatar:"مف",unread:1,last:"نامه تأمین قطعات برای بررسی شما ارجاع شد.",time:"۰۹:۱۰",online:true},
    {id:3,name:"هماهنگی مدیران",kind:"گروه سازمانی",avatar:"هم",unread:0,last:"جلسه فردا به ساعت ۱۰ منتقل شد.",time:"دیروز",online:false},
    {id:4,name:"رضا اسدی",kind:"گفت‌وگوی مستقیم",avatar:"را",unread:0,last:"گزارش شیفت شب تکمیل شد.",time:"دیروز",online:false}
  ],
  messages: {
    1:[
      {me:false,name:"مریم فلاحی",time:"۰۹:۱۲",text:"صورتجلسه جلسه عملیات را بارگذاری کردم. دو مورد نیازمند تصمیم شماست."},
      {me:true,name:"من",time:"۰۹:۱۸",text:"ممنون. مورد مربوط به برنامه شیفت را امروز بررسی می‌کنم."},
      {me:false,name:"رضا اسدی",time:"۰۹:۳۴",text:"نسخه اصلاح‌شده گزارش شیفت شب هم به رکورد مربوط متصل شد."}
    ],
    2:[
      {me:false,name:"مریم فلاحی",time:"۰۹:۱۰",text:"نامه تأمین قطعات برای بررسی شما ارجاع شد."},
      {me:true,name:"من",time:"۰۹:۲۱",text:"دریافت شد. تا قبل از جلسه امروز پاسخ می‌دهم."}
    ]
  },
  tasks:[
    {title:"مرور درخواست خرید شماره ۴۵۱",meta:"امروز، ۱۰:۰۰",source:"تفویض‌شده",high:true},
    {title:"ارسال جمع‌بندی جلسه عملیات",meta:"امروز، ۱۳:۳۰",source:"شخصی"},
    {title:"پیگیری اصلاح گزارش شیفت شب",meta:"عقب‌افتاده از دیروز",source:"پیگیری",high:true},
    {title:"هماهنگی بازدید واحد تولید",meta:"فردا، ۰۹:۰۰",source:"تقویم"}
  ],
  actions:[
    {title:"تأیید درخواست مرخصی ساعتی",subject:"سارا احمدی • کنترل کیفیت",deadline:"تا ۱۱:۰۰",tone:"danger"},
    {title:"بررسی مغایرت حضور شیفت شب",subject:"دو رکورد عبور از نیمه‌شب",deadline:"امروز",tone:"warning"},
    {title:"پاسخ به نامه تأمین قطعات",subject:"دبیرخانه مرکزی",deadline:"تا ۱۴:۰۰",tone:"warning"},
    {title:"تکمیل گزارش فعالیت دیروز",subject:"یک گزارش نهایی نشده",deadline:"گذشته",tone:"danger"}
  ]
};