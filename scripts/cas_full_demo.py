"""Idempotent full-stack CAS demo generator. Run only through Odoo shell."""
import base64
import os
import traceback
from datetime import datetime, time, timedelta
from odoo import fields

P="[DEMO]"; PASSWORD=os.getenv("CAS_DEMO_PASSWORD","Demo@1405!")
TODAY=fields.Date.context_today(env.user); NOW=fields.Datetime.now(); C=env.company
R={}; U={}; E={}; D={}
def ref(x): return env.ref(x,raise_if_not_found=False)
def gids(*xs): return [x.id for x in (ref(a) for a in xs) if x]
def one(m,d,v):
    r=env[m].sudo().search(d,limit=1)
    return r or env[m].sudo().create(v)
def run(name,fn):
    try:
        with env.cr.savepoint(): R[name]=(True,fn())
        print("[CAS-DEMO] PASS",name,R[name][1],flush=True)
    except Exception as ex:
        R[name]=(False,f"{type(ex).__name__}: {ex}")
        print("[CAS-DEMO] FAIL",name,R[name][1],flush=True); traceback.print_exc()
def user(key,label,gs):
    login=f"demo.{key}@cas.local"; r=env["res.users"].sudo().with_context(active_test=False).search([("login","=",login)],limit=1)
    v={"name":f"{P} {label}","login":login,"password":PASSWORD,"active":True,"company_id":C.id,
       "company_ids":[(6,0,[C.id])],"group_ids":[(6,0,gids("base.group_user",*gs))]}
    if r:r.write(v)
    else:r=env["res.users"].sudo().with_context(no_reset_password=True).create(v)
    return r
def people():
    specs={
      "ceo":("مدیرعامل",["cas_kardex_management.group_cas_kardex_ceo","cas_correspondence.group_cas_correspondence_manager","cas_document_core.group_cas_document_manager","cas_action_hub.group_cas_action_hub_manager"]),
      "hr":("مدیر منابع انسانی",["cas_shift_management.group_cas_shift_manager","cas_attendance_core.group_cas_attendance_manager","cas_kardex_management.group_cas_kardex_manager","cas_work_report.group_cas_work_report_manager"]),
      "supervisor":("سرپرست تولید",["cas_shift_management.group_cas_shift_planner","cas_attendance_core.group_cas_attendance_supervisor","cas_kardex_management.group_cas_kardex_supervisor","cas_work_report.group_cas_work_report_supervisor","cas_approval_core.group_cas_approval_user","cas_correspondence.group_cas_correspondence_user"]),
      "designer":("طراح فرایند",["cas_form_core.group_cas_form_manager","cas_workflow_core.group_cas_workflow_manager","cas_approval_core.group_cas_approval_manager"]),
      "secretary":("مسئول دبیرخانه",["cas_correspondence.group_cas_correspondence_user","cas_document_core.group_cas_document_user"]),
      "approver":("مدیر مالی",["cas_approval_core.group_cas_approval_user","cas_action_hub.group_cas_action_hub_user"]),
      "employee1":("کارشناس تولید یک",["cas_form_core.group_cas_form_user","cas_workflow_core.group_cas_workflow_user","cas_correspondence.group_cas_correspondence_user","cas_attendance_core.group_cas_attendance_user","cas_kardex_management.group_cas_kardex_user","cas_work_report.group_cas_work_report_user","cas_action_hub.group_cas_action_hub_user","cas_document_core.group_cas_document_user"]),
      "employee2":("کارشناس تولید دو",["cas_form_core.group_cas_form_user","cas_correspondence.group_cas_correspondence_user","cas_attendance_core.group_cas_attendance_user","cas_kardex_management.group_cas_kardex_user","cas_work_report.group_cas_work_report_user","cas_action_hub.group_cas_action_hub_user"])}
    U.update({k:user(k,*v) for k,v in specs.items()})
    D["management"]=one("hr.department",[("name","=",f"{P} مدیریت")],{"name":f"{P} مدیریت","company_id":C.id})
    D["production"]=one("hr.department",[("name","=",f"{P} تولید")],{"name":f"{P} تولید","company_id":C.id,"parent_id":D["management"].id})
    D["finance"]=one("hr.department",[("name","=",f"{P} مالی")],{"name":f"{P} مالی","company_id":C.id,"parent_id":D["management"].id})
    es={"ceo":("management",None,"مدیرعامل"),"hr":("management","ceo","مدیر منابع انسانی"),
        "supervisor":("production","ceo","سرپرست"),"designer":("management","ceo","طراح"),
        "secretary":("management","ceo","دبیرخانه"),"approver":("finance","ceo","مدیر مالی"),
        "employee1":("production","supervisor","کارشناس تولید"),"employee2":("production","supervisor","کارشناس کیفیت")}
    for k,(dep,parent,job) in es.items():
        v={"name":U[k].name,"user_id":U[k].id,"company_id":C.id,"department_id":D[dep].id,"job_title":job}
        if parent:v["parent_id"]=E[parent].id
        r=env["hr.employee"].sudo().search([("user_id","=",U[k].id)],limit=1); E[k]=r or env["hr.employee"].sudo().create(v); E[k].write(v)
    D["management"].manager_id=E["ceo"];D["production"].manager_id=E["supervisor"];D["finance"].manager_id=E["approver"]
    v={}
    if "cas_ceo_user_id" in C._fields:v["cas_ceo_user_id"]=U["ceo"].id
    if "cas_correspondence_ceo_user_id" in C._fields:v["cas_correspondence_ceo_user_id"]=U["ceo"].id
    C.sudo().write(v);return "8 users, 8 employees, 3 departments"
run("people",people)

def make_form(code,name,specs):
    d=one("cas.form.definition",[("code","=",code),("company_id","=",C.id)],{"name":f"{P} {name}","code":code,"company_id":C.id,"owner_user_id":U["designer"].id})
    v=d.current_version_id or d.version_ids.filtered(lambda x:x.state=="draft")[:1]
    if not v:v=env["cas.form.version"].sudo().create({"definition_id":d.id,"name":"نسخه ۱","revision":1})
    if v.state=="draft" and not v.field_ids:
        for n,s in enumerate(specs,1):
            f=env["cas.form.field"].sudo().create({"version_id":v.id,"technical_key":s[0],"label":s[1],"field_type":s[2],"required":s[3]})
            if len(s)>4:env["cas.form.field.option"].sudo().create([{"field_id":f.id,"technical_key":a,"label":b} for a,b in s[4]])
            env["cas.form.node"].sudo().create({"version_id":v.id,"technical_key":f"node_{s[0]}","node_type":"field","field_id":f.id,"sequence":n*10})
        v.action_publish()
    return d,d.current_version_id
def forms():
    data=[
      ("demo_purchase","درخواست خرید",[("title","عنوان","short_text",True),("amount","مبلغ","decimal",True),("urgency","فوریت","dropdown",True,[("normal","عادی"),("urgent","فوری")])],{"title":"خرید قطعه","amount":85000000.0,"urgency":"urgent"}),
      ("demo_incident","گزارش حادثه",[("title","حادثه","short_text",True),("date","تاریخ","date",True),("safe","ایمن است","boolean",True)],{"title":"توقف دستگاه","date":TODAY,"safe":True}),
      ("demo_quality","کنترل کیفیت",[("product","محصول","short_text",True),("quantity","تعداد","integer",True),("result","نتیجه","dropdown",True,[("ok","تأیید"),("rework","اصلاح")])],{"product":"محصول A","quantity":12,"result":"ok"})]
    for code,name,spec,answers in data:
        d,v=make_form(code,name,spec); count=env["cas.form.submission"].sudo().search_count([("version_id","=",v.id),("owner_user_id","=",U["employee1"].id)])
        for i in range(count,3):
            s=env["cas.form.submission"].sudo().create({"version_id":v.id,"owner_user_id":U["employee1"].id});s.action_save_answers(answers)
            if i!=1:s.action_submit()
    return "3 forms, 9 draft/submitted records"
run("forms-builder-runtime",forms)

def workflow(code,name,approval):
    d=one("cas.workflow.definition",[("code","=",code),("company_id","=",C.id)],{"name":f"{P} {name}","code":code,"company_id":C.id,"owner_user_id":U["designer"].id,"target_model_id":env["ir.model"]._get("res.partner").id})
    v=d.current_version_id or d.version_ids.filtered(lambda x:x.state=="draft")[:1]
    if not v:v=env["cas.workflow.version"].sudo().create({"definition_id":d.id,"name":"نسخه ۱","revision":1})
    if v.state=="draft" and not v.state_ids:
        a=env["cas.workflow.state"].sudo().create({"version_id":v.id,"name":"در انتظار","code":"review","kind":"initial","sla_hours":24})
        b=env["cas.workflow.state"].sudo().create({"version_id":v.id,"name":"تأیید","code":"approved","kind":"final"})
        c=env["cas.workflow.state"].sudo().create({"version_id":v.id,"name":"رد","code":"rejected","kind":"cancelled"})
        t=env["cas.workflow.transition"].sudo().create({"version_id":v.id,"name":"تأیید","code":"approve","from_state_id":a.id,"to_state_id":b.id,"responsible_mode":"actor","condition_config":{"type":"always"}})
        z=env["cas.workflow.transition"].sudo().create({"version_id":v.id,"name":"رد","code":"reject","from_state_id":a.id,"to_state_id":c.id,"responsible_mode":"actor","condition_config":{"type":"always"}})
        if approval:
            p=env["cas.approval.policy"].sudo().create({"version_id":v.id,"state_id":a.id,"name":"تأیید مدیریت","code":"demo_approval","approve_transition_id":t.id,"reject_transition_id":z.id,"execution_mode":"sequential","decision_rule":"all"})
            for q,u in ((10,U["approver"]),(20,U["ceo"])):env["cas.approval.step"].sudo().create({"policy_id":p.id,"sequence":q,"name":u.name,"role_label":u.name,"approver_type":"user","approver_user_id":u.id,"deadline_hours":8})
        v.action_publish()
    return d
def workflows():
    simple=workflow("demo_process","فرایند بررسی",False); approved_flow=workflow("demo_approval_flow","فرایند تأیید خرید",True)
    for d in (simple,approved_flow):
        for i in range(1,4):
            p=one("res.partner",[("ref","=",f"DEMO-{d.code}-{i}")],{"name":f"{P} پرونده {i}","ref":f"DEMO-{d.code}-{i}"})
            if not env["cas.workflow.instance"].sudo().search_count([("definition_id","=",d.id),("resource_id","=",p.id)]):d.sudo().action_start(p.id,responsible_user_id=U["supervisor"].id)
    instance=env["cas.workflow.instance"].sudo().search([("definition_id","=",simple.id),("status","=","running")],limit=1)
    if instance:
        transition=instance.version_id.transition_ids.filtered(lambda x:x.code=="approve")[:1]
        instance.action_execute_transition(transition.id,note="بررسی نمایشی تکمیل شد")
    request=env["cas.approval.request"].sudo().search([("policy_id.code","=","demo_approval"),("status","=","pending")],limit=1)
    if request:
        line=request.line_ids.filtered(lambda x:x.status=="pending" and x.approver_user_id==U["approver"])[:1]
        if line:line.with_user(U["approver"]).action_approve("تأیید مرحله مالی در دمو")
    return "2 node workflows, 6 instances, approval inbox"
run("workflow-approval-designer",workflows)

def documents():
    b=one("cas.document.storage.backend",[("name","=",f"{P} دیتابیس"),("company_id","=",C.id)],{"name":f"{P} دیتابیس","company_id":C.id,"backend_type":"database"})
    f=one("cas.document.folder",[("code","=","DEMO-DOCS"),("company_id","=",C.id)],{"name":f"{P} اسناد","code":"DEMO-DOCS","company_id":C.id,"manager_user_id":U["secretary"].id})
    o=one("cas.document.ocr.provider",[("name","=",f"{P} OCR"),("company_id","=",C.id)],{"name":f"{P} OCR","company_id":C.id,"provider_type":"manual"})
    for i,n in enumerate(("دستورالعمل ایمنی","صورتجلسه","گزارش کیفیت"),1):
        d=one("cas.document",[("name","=",f"{P} {n}"),("company_id","=",C.id)],{"name":f"{P} {n}","company_id":C.id,"folder_id":f.id,"owner_user_id":U["secretary"].id,"authorized_user_ids":[(6,0,[U["employee1"].id,U["supervisor"].id])],"storage_backend_id":b.id})
        if not d.version_ids:
            v=d.add_version(f"demo-{i}.txt",f"محتوای سند {i}".encode(),"text/plain","نسخه اولیه");d.action_activate()
            if i==1:
                j=env["cas.document.ocr.job"].sudo().create({"version_id":v.id,"provider_id":o.id});j.action_submit_review();j.write({"extracted_text":"متن OCR نمایشی"});j.action_confirm_text()
    return "3 versioned documents and OCR"
run("documents-ocr",documents)

def letters():
    folder=env["cas.document.folder"].sudo().search([("code","=","DEMO-DOCS")],limit=1)
    t=one("cas.correspondence.template",[("code","=","DEMO-OFFICIAL"),("company_id","=",C.id)],{"name":f"{P} قالب رسمی","code":"DEMO-OFFICIAL","company_id":C.id,"body_html":"<p>متن پایه</p>","document_folder_id":folder.id})
    count=env["cas.correspondence.letter"].sudo().search_count([("subject","like",f"{P} نامه ")])
    for i in range(count+1,6):
        l=env["cas.correspondence.letter"].sudo().with_user(U["secretary"]).create({"subject":f"{P} نامه {i}","body":f"<p>نامه نمایشی {i}</p>","company_id":C.id,"template_id":t.id if i==1 else False})
        r=env["cas.correspondence.recipient"].sudo().with_user(U["secretary"]).create({"letter_id":l.id,"target_kind":"user","recipient_user_id":U["employee1"].id,"expectation":"action" if i==2 else "information","deadline":NOW+timedelta(days=i)})
        if i!=5:l.with_user(U["secretary"]).action_send()
        if i==2:r.with_user(U["employee1"]).action_mark_viewed();r.with_user(U["employee1"]).action_start();r.with_user(U["employee1"]).action_complete("انجام شد")
        if i==3:r.with_user(U["employee1"]).action_mark_viewed()
    q=one("cas.correspondence.register",[("subject","=",f"{P} وارده"),("company_id","=",C.id)],{"direction":"inbound","subject":f"{P} وارده","company_id":C.id,"owner_user_id":U["secretary"].id,"counterparty":"شرکت بیرونی","file_data":base64.b64encode("نامه وارده".encode()),"file_name":"inbound.txt","document_folder_id":folder.id})
    if q.state=="draft":
        q.with_user(U["secretary"]).action_register();s=env["cas.correspondence.signature"].sudo().create({"register_id":q.id,"signer_user_id":U["secretary"].id,"method":"organizational"});s.with_user(U["secretary"]).action_sign_organizational()
    target=env["cas.correspondence.letter"].sudo().search([("subject","=",f"{P} نامه 4"),("state","!=","draft")],limit=1)
    if target and not target.referral_ids:
        w=env["cas.correspondence.referral.wizard"].sudo().with_user(U["secretary"]).create({"letter_id":target.id,"target_kind":"user","recipient_user_id":U["supervisor"].id,"expectation":"action","priority":"urgent","note":"ارجاع فوری نمایشی"})
        w.action_confirm();rr=target.referral_ids[-1];rr.with_user(U["supervisor"]).action_mark_viewed();rr.with_user(U["supervisor"]).action_start()
    return "5 letters, template, referral, inbound register, signature"
run("correspondence-secretariat",letters)

def attendance():
    p=one("cas.attendance.policy",[("code","=","demo_simple"),("company_id","=",C.id)],{"name":f"{P} سیاست","code":"demo_simple","company_id":C.id,"attendance_mode":"simple"})
    s=one("cas.shift.template",[("code","=","demo_morning"),("company_id","=",C.id)],{"name":f"{P} صبح","code":"demo_morning","company_id":C.id,"start_hour":7.5,"end_hour":16.0,"default_break_minutes":30})
    x=one("cas.shift.pattern",[("code","=","demo_week"),("company_id","=",C.id)],{"name":f"{P} هفتگی","code":"demo_week","company_id":C.id,"cycle_length":1,"line_ids":[(0,0,{"cycle_day":1,"day_kind":"work","template_id":s.id})]})
    a=one("cas.shift.assignment",[("name","=",f"{P} برنامه"),("company_id","=",C.id)],{"name":f"{P} برنامه","company_id":C.id,"employee_ids":[(6,0,[E["employee1"].id,E["employee2"].id])],"supervisor_user_id":U["supervisor"].id,"policy_id":p.id,"pattern_id":x.id,"anchor_date":TODAY-timedelta(days=7),"date_from":TODAY-timedelta(days=7),"date_to":TODAY+timedelta(days=2),"weekly_rest_day":"none","short_day_enabled":False})
    if a.state=="draft":a.action_publish()
    site=one("cas.attendance.site",[("code","=","demo_gate"),("company_id","=",C.id)],{"name":f"{P} درب","code":"demo_gate","company_id":C.id})
    dev=one("cas.attendance.device",[("code","=","demo_device"),("company_id","=",C.id)],{"name":f"{P} دستگاه","code":"demo_device","company_id":C.id,"site_id":site.id})
    for n,k in ((1001,"employee1"),(1002,"employee2")):one("cas.attendance.identity",[("source_type","=","device"),("external_key","=",str(n)),("company_id","=",C.id)],{"source_type":"device","external_key":str(n),"employee_id":E[k].id})
    M=env["cas.attendance.event"].sudo().with_context(cas_attendance_supervisor=True)
    for off in range(1,6):
      d=TODAY-timedelta(days=off)
      for j,k in enumerate(("employee1","employee2"),1):
       for kind,at in (("work_start",datetime.combine(d,time(7,30+j*3))),("work_end",datetime.combine(d,time(17 if off==2 else 16,j*5)))):
        uid=f"DEMO:{k}:{d}:{kind}"
        if not M.search_count([("external_uid","=",uid)]):M.create({"employee_id":E[k].id,"occurred_at":at,"work_date":d,"source":"device","event_kind":kind,"site_id":site.id,"device_id":dev.id,"external_uid":uid})
    raw=("employee_id,check_in,check_out\n"+f"1001,{TODAY} 07:31,{TODAY} 16:04\n1002,{TODAY} 07:35,{TODAY} 16:08\n").encode()
    b=one("cas.attendance.import",[("name","=",f"{P} فایل دستگاه"),("company_id","=",C.id)],{"name":f"{P} فایل دستگاه","company_id":C.id,"import_type":"paired_sessions","device_id":dev.id,"site_id":site.id,"data_file":base64.b64encode(raw),"filename":"demo.csv"})
    if b.state=="draft":b.action_parse()
    if b.state=="review" and not b.unmatched_count:b.action_import_ready()
    guard=one("cas.guard.batch",[("name","=",f"{P} ثبت گروهی نگهبانی"),("company_id","=",C.id)],{"name":f"{P} ثبت گروهی نگهبانی","company_id":C.id,"site_id":site.id,"default_occurred_at":NOW,"line_ids":[(0,0,{"employee_id":E["employee1"].id,"occurred_at":NOW,"event_kind":"guard_entry"}),(0,0,{"employee_id":E["employee2"].id,"occurred_at":NOW+timedelta(minutes=2),"event_kind":"guard_entry"})]})
    if guard.state=="draft":guard.action_confirm()
    recovered=one("cas.attendance.outage",[("name","=",f"{P} خرابی رفع‌شده"),("company_id","=",C.id)],{"name":f"{P} خرابی رفع‌شده","company_id":C.id,"device_id":dev.id,"site_id":site.id,"start_at":NOW-timedelta(hours=2),"reason":"قطع ارتباط نمایشی"})
    if recovered.state=="open":recovered.action_recover()
    one("cas.attendance.outage",[("name","=",f"{P} خرابی باز"),("company_id","=",C.id)],{"name":f"{P} خرابی باز","company_id":C.id,"device_id":dev.id,"site_id":site.id,"start_at":NOW-timedelta(minutes=30),"reason":"در انتظار بررسی"})
    r=one("cas.attendance.request",[("employee_id","=",E["employee1"].id),("reason","=",f"{P} مأموریت")],{"employee_id":E["employee1"].id,"request_type":"mission","duration_type":"hourly","date_from":TODAY,"date_to":TODAY,"datetime_from":datetime.combine(TODAY,time(10)),"datetime_to":datetime.combine(TODAY,time(12)),"reason":f"{P} مأموریت"})
    if r.state=="draft":r.action_submit()
    day=env["cas.kardex.day"].sudo().search([("employee_id","=",E["employee1"].id),("work_date","=",TODAY-timedelta(days=2))],limit=1)
    if day and day.discretionary_overtime_minutes:
        ot=one("cas.overtime.request",[("kardex_day_id","=",day.id),("reason","=",f"{P} اضافه‌کاری")],{"kardex_day_id":day.id,"reason":f"{P} اضافه‌کاری"})
        if ot.state=="draft":ot.action_submit()
        if ot.state=="pending_manager":ot.write({"manager_approved_minutes":min(60,ot.actual_minutes),"manager_note":"تأیید نمایشی"});ot.action_manager_approve()
    return f"{len(a.day_ids)} shift days, events, import, guard batch, outages, kardex/request/overtime"
run("shift-attendance-kardex",attendance)

def reports():
    s=one("cas.work.station",[("code","=","demo_station"),("company_id","=",C.id)],{"name":f"{P} ایستگاه","code":"demo_station","company_id":C.id,"department_id":D["production"].id,"supervisor_user_id":U["supervisor"].id,"normal_shift_hours":8})
    for k in ("employee1","employee2"):
      for i in range(3):
       title=f"{P} گزارش {k}-{i}"
       if not env["cas.work.report"].sudo().search_count([("task_title","=",title)]):
        r=env["cas.work.report"].sudo().with_user(U[k]).create({"work_date":TODAY,"employee_id":E[k].id,"work_station_id":s.id,"shift_start":NOW-timedelta(hours=8),"shift_end":NOW-timedelta(minutes=15),"task_title":title,"description":"شرح فعالیت","result":"خروجی","issues":"بدون مانع"})
        if i!=2:r.action_submit()
    rs=env["cas.work.report"].sudo().search([("task_title","like",P)]);blob=env["cas.work.report"].sudo()._xlsx_bytes(rs)
    if not blob.startswith(b"PK"):raise RuntimeError("invalid XLSX")
    kardex_blob,kardex_rows=env["cas.kardex.report.service"].sudo().build_xlsx(TODAY-timedelta(days=7),TODAY,include_draft=True)
    if not kardex_blob.startswith(b"PK"):raise RuntimeError("invalid kardex XLSX")
    return f"{len(rs)} reports, work XLSX {len(blob)}, kardex XLSX {len(kardex_blob)} bytes/{kardex_rows} rows"
run("work-report-excel",reports)
def hub():
    one("cas.action.sla.rule",[("name","=",f"{P} SLA"),("company_id","=",C.id)],{"name":f"{P} SLA","company_id":C.id,"action_type":"action","reminder_interval_hours":4,"escalation_after_hours":12,"max_escalation_level":3,"escalation_user_id":U["supervisor"].id})
    env["cas.action.item"].sudo().action_sync_all();n=env["cas.action.item"].sudo().search_count([("company_id","=",C.id)])
    if not n:raise RuntimeError("no actions")
    return f"{n} action items"
run("action-hub-sla",hub)
def bridges():
    names=["cas_jalali","cas_jalali_hr","cas_jalali_mail","cas_jalali_qweb","cas_jalali_search","cas_jalali_suite","cas_kardex_report","cas_form_builder","cas_dynamic_form","cas_workflow_designer"]
    miss=[n for n in names if not env["ir.module.module"].sudo().search_count([("name","=",n),("state","=","installed")])]
    if miss:raise RuntimeError("missing "+",".join(miss))
    return "all Jalali/UI/report bridges installed"
run("technical-bridges",bridges)
env.cr.commit()
print("\n========== CAS DEMO COVERAGE ==========")
for k,(ok,msg) in R.items():print(("PASS" if ok else "FAIL"),"|",k,"|",msg)
bad=[k for k,v in R.items() if not v[0]]
print("Users: demo.<role>@cas.local | password:",PASSWORD,"| failures:",len(bad))
if bad:raise RuntimeError("Incomplete demo: "+",".join(bad))
