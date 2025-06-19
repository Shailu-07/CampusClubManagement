from django.http import HttpResponse
from  django.shortcuts import render
from . import models
import random
import mysql.connector as mycon
from datetime import date,timedelta
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from . import sendMail
from . import sentiment   
import json 
import calendar
from .models import fetch_events_for_month
def index(request):
    data= models.getStates()
    data1=models.getUpcomingEvents()
    branches= models.getBranches()
    return render(request, "index.html",{"list":data,"lstbr":branches,"lstevents":data1})
def event_detail(request):
    data= models.getStates()
    data1=models.getUpcomingEvents()
    branches= models.getBranches()
    return render(request, "event_detail.html",{"list":data,"lstbr":branches,"lstevents":data1})

def event_calendar(request):
    # Get the current month and year
    now = datetime.now()
    year, month = now.year, now.month
    try:
        # Get the month and year from the query parameter
        month_year=request.GET.get("dt")
        # Parse the month_year (format: YYYY-MM)
        year, month = map(int, month_year.split('-'))
    except:
        print("Invalid")
    
    # Fetch events from the model
    events = fetch_events_for_month(year, month)

    # Convert events into a dictionary with the day as the key
    event_dates = {}
    for event in events:
        try:
            # Parse event date and extract the day
            event_date = datetime.strptime(event['event_dt'], "%d/%m/%Y").date()
            if event_date.month == month:
                event_dates[event_date.day] = {
                    "id": event["event_id"],
                    "name": event["event_name"],
                    "details": event["details"],
                }
        except ValueError:
            continue  # Skip invalid date formats

    # Generate calendar days for the current month
    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)
    print(event_dates)
    # Get the first and last day of the given month
    first_day = datetime(year, month, 1)
    last_day = (first_day + timedelta(days=calendar.monthrange(year, month)[1] - 1))

    # Calculate previous and next months
    prev_month = (first_day - timedelta(days=1)).strftime('%Y-%m')
    next_month = (last_day + timedelta(days=1)).strftime('%Y-%m')

    # Pass the data to the template
    context = {
        "month": calendar.month_name[month],
        "year": year,
        "month_days": month_days,
        "event_dates": event_dates,
        'prev_month': prev_month,
        'next_month': next_month,
    }
    print(context)
    return render(request, "event_calendar.html", context)

def sendotp1(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")  
        email=request.POST.get("email")  
        val=models.login1(userid,email) 
        if val=='success':
            otp=str(random.randint(1111,9999))
            print("otp="+otp)
            request.session['otp']=otp
            sendMail.sendotp(otp,email)
            return render(request, "otpverification2.html",{"userid":userid,"email":email})
        else:
            return render(request, "Success.html",{"mess":"Authentication Failed!!"})
def otpverification1(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")  
        email=request.POST.get("email")  
        seckey=request.POST.get("seckey")  
        otp=request.POST.get("otp")  
        otp1=request.session['otp']
        pass1="club@"+str(random.randint(1111,9999))
        if otp==otp1:
            models.updatePass(userid,pass1)
            sendMail.sendotp1(pass1,email)
            return render(request, "Success.html",{"mess":"Password Sent on Email Successully..."}) 
        else:
            return render(request, "Success.html",{"mess":"OTP Authentication Failed!!"})
             
def forgot(request): 
    return render(request, "passwordRecovery.html")
def regpage(request):
    data= models.getStates()
    branches= models.getBranches()
    return render(request, "registration.html",{"list":data,"lstbr":branches})
def loginpage(request):
    return render(request, "login.html")
def admin(request):
    data= models.getPendingStudents()
    return render(request, "admin.html",{"list":data})
    getStudReport
def logout(request):
    del request.session["user"]  
    data= models.getStates()
    data1=models.getUpcomingEvents()
    branches= models.getBranches()
    return render(request, "index.html",{"list":data,"lstbr":branches,"lstevents":data1})
   
def viewEventsStaff(request):
    clubname=request.GET.get("club_name") 
    sts=request.GET.get("sts") 
    data= models.getEvents(clubname) 
    print(data)
    return render(request, "viewEventsStaff.html",{"list":data,"sts":sts})   
def viewEvents(request):
    clubname=request.GET.get("club_name") 
    sts=request.GET.get("sts") 
    data= models.getEvents(clubname) 
    print(data)
    return render(request, "viewEvents.html",{"list":data,"sts":sts})   
def viewDocs_event(request):
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("event") 
    
    data= models.getEventDocs(clubname,eventname) 
    print(data)
    return render(request, "viewEventsDocs.html",{"list":data,"clubname":clubname,"eventname":eventname})  

def approveDocs(request):
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("event") 
    docid=request.GET.get("docid")
    models.approveDoc(docid)
    data= models.getEventDocsPending(clubname,eventname) 
    print(data)
    return render(request, "viewEventsDocsPending.html",{"list":data,"clubname":clubname,"eventname":eventname})  
def deleteDocs(request):
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("event") 
    docid=request.GET.get("docid")
    docpath=request.GET.get("docpath")
    
    models.deleteDoc(docid)
    data= models.getEventDocsPending(clubname,eventname) 
    print(data)
    return render(request, "viewEventsDocsPending.html",{"list":data,"clubname":clubname,"eventname":eventname})  

def viewDocs_eventPending(request):
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("event") 
    
    data= models.getEventDocsPending(clubname,eventname) 
    print(data)
    return render(request, "viewEventsDocsPending.html",{"list":data,"clubname":clubname,"eventname":eventname})  
def viewReviewsEvent(request):
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("eventname") 
    
    data= models.getEventReviews(clubname,eventname) 
    data1=models.viewReviewsGraph(clubname,eventname)
    print(data)
    return render(request, "viewEventsReviews.html",{"list":data,"clubname":clubname,"eventname":eventname,"list1":data1})  
def viewEvents_pending(request):
    clubname=request.GET.get("clubname") 
    data= models.getEvents_pending(clubname) 
    print(data)
    return render(request, "viewEvents_pending.html",{"list":data})  
def viewclubs(request):
    data= models.getClubs() 
    print(data)
    return render(request, "viewclubs.html",{"list":data})
def viewclubs_approved(request):
    data= models.getClubs() 
     
    print(data)
    return render(request, "viewclubs.html",{"list":data})
def viewstudents(request):
    data= models.getStudents()
    branches= models.getBranches()
    print(data)
    return render(request, "viewstudents.html",{"list":data,"lstbr":branches})
def viewstaff(request):
    data= models.getStaff() 
    print(data)
    return render(request, "viewstaff.html",{"list":data})
    
def pending_participant_req(request):
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("eventname") 
    data= models.getmembership_reqs_event(clubname,eventname) 
    print(data)
    return render(request, "viewEventMembershipReq.html",{"list":data})
def pending_membership_req(request):
    clubname=request.GET.get("clubname") 
    data= models.getmembership_reqs(clubname) 
    print(data)
    return render(request, "viewClubMembershipReq.html",{"list":data})
def getStudReport(request):
    branch="na"
    sem=0
    if request.method == 'GET':
        branch=request.GET.get("branch") 
        sem=request.GET.get("sem") 
    data= models.getStudents(branch,int(sem))
    branches= models.getBranches()
    print(data)
    return render(request, "viewstudents1.html",{"list":data,"lstbr":branches})
def student(request):
    userid= request.session['userid']
    data= models.getClubs_stud(userid) 
    return render(request, "student.html",{"list":data})
def staff(request):
    userid= request.session['userid']
    data= models.getClubs_staff(userid)
    return render(request, "staff.html",{"list":data})
def clubadmin(request):
    return render(request, "clubadmin.html")
def principal(request): 
    data= models.getClubs_pending()
    return render(request, "principal.html",{"list":data})
def regStaff(request):
    branches= models.getBranches()
    data= models.getStates()
    return render(request, "regStaff.html",{"list":data,"lstbr":branches})
def regClubs(request):
    data= models.getStaffNames() 
    print("data="+str(data))
    return render(request, "regClubs.html",{"lststaff":data})
def uploadDocs_event(request):
    eventid=request.GET.get("eventId") 
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("event") 
    print("data="+str(eventid))
    return render(request, "UploadDocsEvents.html",{"eventid":eventid,"clubname":clubname,"eventname":eventname})
def regReviews(request):
    eventid=request.GET.get("eventId") 
    clubname=request.GET.get("clubname") 
    eventname=request.GET.get("eventname") 
    print("data="+str(eventid))
    return render(request, "regReviews.html",{"eventid":eventid,"clubname":clubname,"eventname":eventname})
def login(request):
    if request.method == 'POST':
        userid=request.POST.get("userid") 
        pass1=request.POST.get("pass") 
        val=models.login(userid,pass1)
        print("in login="+str(val) )
        if len(val)> 0 :
            request.session["user"]={"userid":val[0][0],"utype":val[0][3],"username":val[0][2]}    
            request.session["userid"]=val[0][0] 
            request.session["utype"]=val[0][3]
            request.session["username"]=val[0][2]
            request.session["emailid"]=models.getEmail(val[0][0])   
            if val[0][3]=="admin":
                data= models.getPendingStudents()
                return render(request, "admin.html",{"list":data})    
            elif val[0][3]=="principal":           
                data= models.getClubs_pending()
                return render(request, "principal.html",{"list":data})
            elif val[0][3]=="staff": 
                data= models.getClubs_staff(userid)
                return render(request, "staff.html",{"list":data}) 
            elif val[0][3]=="student": 
                data= models.getClubs_stud(userid) 
                return render(request, "student.html",{"list":data})
        else:
            return render(request, "Success.html",{"mess":"Authentication Failed!!"}) 
            
def UseridVali(request):
    msg= models.checkUserid(request.GET.get("userid")) 
    color1="green"
    if msg=='NA':
        msg="Userid is available.."   
    else:
        color1="red"
        msg="Userid is Not available, Please try another!!"
    print("color="+color1)    
    return render(request, "useridvali.html",{"msg":msg,"color":color1})
def ClubVali(request):
    msg= models.checkClubName(request.GET.get("clubname")) 
    color1="green"
    if msg=='NA':
        msg="Club Name is available.."   
    else:
        color1="red"
        msg="This Club Name is already Exists, Please try another!!"
    print("color="+color1)    
    return render(request, "clubvali.html",{"msg":msg,"color":color1})
def Cities(request):
    data= models.getCities(request.GET.get("state"))    
    return render(request, "cities.html",{"list":data})
def getUsers():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select usernm,mobileno,emailid,addr,pincode from userdetails;')
    data=cursor.fetchall()
    return data
def approveMembership(request):
    clubname="NA"
    if request.method == 'POST':
        reqid=request.POST.get("reqid")  
        email=request.POST.get("email") 
        name=request.POST.get("name") 
        clubname=request.POST.get("clubname")
        print(reqid) 
        models.updateMembershipSts(reqid,"approved")
        msg='Subject: Club Membership Approval \n \n\n' + "Dear "+name+", Membership Request for club "+clubname+" has been approved by club admin"
        print(msg)
        sendMail.sendmsg(msg,email)
    return render(request, "Success1.html",{"mess":"Membership Request Approved Successfully...","link": "pending_membership_req/?clubname="+clubname}) 
def AttendanceReg(request):
    if request.method == 'POST':
        students=request.POST.getlist("stud")
        clubname=request.POST.get("clubname")
        eventname=request.POST.get("eventname")
        strlst = ','.join(map(str, students)) 
        print("lst="+(strlst))
        models.insertAttendance(clubname,eventname,strlst)
    return render(request, "Success1.html",{"mess":"Attendance Registered Successfully...","link": "staff"}) 
def markAttendance(request):
    clubname="NA"
    eventname="NA"
    if request.method == 'GET':
        clubname=request.GET.get("clubname")
        eventname=request.GET.get("eventname")
    data=models.getMembers(clubname,eventname)
    print(data)
    return render(request, "MarkAttendance.html",{"list":data,"clubname":clubname,"eventname":eventname})
def viewAttendance(request):
    clubname="NA"
    if request.method == 'GET':
        clubname=request.GET.get("clubname")
        eventname=request.GET.get("eventname")
    data=models.viewAttendance(clubname,eventname)
    data1=models.viewAttendanceGraph(clubname,eventname)
    return render(request, "ViewAttendance.html",{"list":data,"list1":data1})
def approveEventMembership(request):
    clubname="NA"
    if request.method == 'POST':
        reqid=request.POST.get("reqid")  
        email=request.POST.get("email") 
        name=request.POST.get("name") 
        clubname=request.POST.get("clubname")
        eventname=request.POST.get("eventname")
        print(reqid) 
        models.updateMembershipStsEvent(reqid,"approved")
        msg='Subject: Event Participant Approval \n \n\n' + "Dear "+name+", Participation Request for event "+eventname+" of club "+clubname+"  has been approved by club admin"
        print(msg)
        sendMail.sendmsg(msg,email)
        clubname=clubname+"&eventname="+eventname
        print(clubname)
    return render(request, "Success1.html",{"mess":"Membership Request Approved Successfully...","link": "staff"}) 
def approveEvent(request):
    clubname="NA"
    if request.method == 'GET':
        reqid=request.GET.get("eventId")  
        event=request.GET.get("event")  
        clubname=request.GET.get("clubname")  
        msg11=models.getEmail_clubadmin(reqid) 
        email=msg11.split('|')[0]
        staffnm=msg11.split('|')[1]
         
        print(reqid) 
        models.updateEventSts(reqid,request.session["userid"],"approved")
        msg='Subject: Event Approval \n \n\n' + "Dear "+staffnm+", event having title "+event+" has been approved by principal"
        print(msg)
        sendMail.sendmsg(msg,email)
    return render(request, "Success1.html",{"mess":"Event Approved Successfully...","link": "viewEvents_pending/?clubname="+clubname}) 
def rejectEvent(request):
    clubname="NA"
    if request.method == 'GET':
        reqid=request.GET.get("eventId")  
        event=request.GET.get("event")  
        clubname=request.GET.get("clubname")  
        msg11=getEmail_clubadmin(reqid) 
        email=msg11.split('|')[0]
        staffnm=msg11.split('|')[1]
         
        print(reqid) 
        models.updateEventSts(reqid,request.session["userid"],"rejected")
        msg='Subject: Event Request Rejection \n \n\n' + "Dear "+staffnm+", event having title "+event+" has been rejected by principal"
        print(msg)
        sendMail.sendmsg(msg,email)
    return render(request, "Success1.html",{"mess":"Membership Request Approved Successfully...","link": "viewEvents_pending/?clubname="+clubname}) 
def rejectMembership(request):
    if request.method == 'POST':
        reqid=request.POST.get("reqid")  
        email=request.POST.get("email") 
        name=request.POST.get("name") 
        clubname=request.POST.get("clubname") 
        print(reqid) 
        models.updateMembershipSts(reqid,"rejected")        
    return render(request, "Success1.html",{"mess":"Membership Request Rejected Successfully...","link": "staff"})
def rejectEventMembership(request):
    if request.method == 'POST':
        reqid=request.POST.get("reqid")  
        email=request.POST.get("email") 
        name=request.POST.get("name") 
        clubname=request.POST.get("clubname") 
        eventname=request.POST.get("eventname") 
        print(reqid) 
        models.updateMembershipStsEvent(reqid,"rejected")        
    return render(request, "Success1.html",{"mess":"Participation Request Rejected Successfully...","link": "staff"})
def approve(request):
    utype="admin"
    utype= request.session['utype']
    if request.method == 'GET':
        userid=request.GET.get("userid")  
        print(userid) 
        models.updatests(userid,"active")
        print(userid)
        
        print(utype) 
        
    return render(request, "Success1.html",{"mess":"Student Approved Successfully...","link": utype})
def approve_club(request):
    utype="principal" 
    if request.method == 'GET':
        club_name=request.GET.get("club_name")  
        print(club_name)
        userid= request.session['userid']
        models.updatests_club(club_name,"active",userid) 
    return render(request, "Success1.html",{"mess":"Club Approved Successfully...","link": utype})
def decline(request):
    if request.method == 'GET':
        userid=request.GET.get("userid")   
        print("stud="+userid)
        models.deleteStud(userid)
        print(userid)         
    return render(request, "Success1.html",{"mess":"Student Declined Successfully...","link": "admin"})
def decline_club(request):
    if request.method == 'GET':
        club_name=request.GET.get("club_name")  
        print(club_name) 
        models.deleteClub(club_name)      
    return render(request, "Success1.html",{"mess":"Club Declined Successfully...","link": "principal"})

def send_participant_req(request):
    clubname=request.GET.get("clubname")
    eventname=request.GET.get("eventname")
    fees=request.GET.get("fees")
    return render(request, "sendParticipantReq.html",{"clubname":clubname,"eventname":eventname,"fees":fees})
def send_membership_req(request):
    clubname=request.GET.get("clubname")
    fees=request.GET.get("fees")
    return render(request, "sendMembershipReq.html",{"clubname":clubname,"fees":fees})
def registerStud(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")   
        usernm=request.POST.get("usernm")
        pswd=request.POST.get("pswd")
        emailid=request.POST.get("emailid")
        mobileno=request.POST.get("mobileno")
        gender=request.POST.get("gender")
        pincode=request.POST.get("pincode")
        addr=request.POST.get("addr")
        state=request.POST.get("state")
        cities=request.POST.get("cities")
        dob=request.POST.get("dob")
        branch=request.POST.get("branch")
        sem=request.POST.get("sem")
        print(userid)
        print(usernm)
        print(pswd)
        print(emailid)
        photo=models.handle_uploaded_file2(request.FILES['file'],userid)
                 
        models.insertStud(userid,pswd,usernm,addr,pincode,mobileno,emailid,gender,dob,state,cities,photo,branch,sem)
    return render(request, "Success.html",{"mess":"Your Registration Done Successfully..."})

def registerStaff(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")   
        usernm=request.POST.get("usernm")
        pswd=request.POST.get("pswd")
        emailid=request.POST.get("emailid")
        mobileno=request.POST.get("mobileno")
        gender=request.POST.get("gender")
        pincode=request.POST.get("pincode")
        addr=request.POST.get("addr")
        state=request.POST.get("state")
        cities=request.POST.get("cities")
        dob=request.POST.get("dob")
        branch=request.POST.get("branch")
        utype=request.POST.get("utype")
        print(userid)
        print(usernm)
        print(pswd)
        print(emailid)
        photo=models.handle_uploaded_file3(request.FILES['file'],userid)
                 
        models.insertStaff(userid,pswd,usernm,addr,pincode,mobileno,emailid,gender,dob,state,cities,photo,branch,utype)
    return render(request, "Success1.html",{"mess":"New Staff Registration Done Successfully...","link": "admin"})

def sendParticipantRequest(request):
    if request.method == 'POST':
        clubname=request.POST.get("clubname")  
        eventname=request.POST.get("eventname")
        fees=request.POST.get("fees")
         
        userid= request.session['userid'] 
        photo=models.handle_uploaded_file51(request.FILES['file'],clubname+"_"+userid)
                 
        models.insertEvent_Membership(clubname,photo,userid,fees,eventname)
    return render(request, "Success1.html",{"mess":"Event Participation Request Sent Successfully...","link": "student"})
def pending_membership_req1(request):
    clubname=request.GET.get("clubname") 
    data= models.getmembership_reqs1(clubname) 
    print(data)
    return render(request, "viewClubMembershipReq1.html",{"list":data})
def sendMembershipRequest(request):
    if request.method == 'POST':
        clubname=request.POST.get("clubname")  
        fees=request.POST.get("fees")
         
        userid= request.session['userid'] 
        try:
            photo=models.handle_uploaded_file5(request.FILES['file'],clubname+"_"+userid)
        except:
            photo="NA"
        #photo=models.handle_uploaded_file5(request.FILES['file'],clubname+"_"+userid)
                 
        models.insertClubs_Membership(clubname,photo,userid,fees)
    return render(request, "Success1.html",{"mess":"Membership Request Sent Successfully...","link": "student"})
def regEvents(request):
    clubname="NA"
    if request.method == 'GET':
        clubname=request.GET.get("club_name")   
          
    return render(request, "regEvents.html",{"clubname":clubname})
def registerEvent(request):
    if request.method == 'POST':
        clubname=request.POST.get("clubname")   
        details=request.POST.get("details")
        venue=request.POST.get("venue")
        eventTitle=request.POST.get("eventTitle")
        eventDt=request.POST.get("eventDt")
        eventdt1=eventDt.split("-")
        eventDt=eventdt1[2]+"/"+eventdt1[1]+"/"+eventdt1[0]
        eventTm=request.POST.get("eventTm")
        fees=request.POST.get("fees") 
        userid= request.session['userid']
        photo=models.handle_uploaded_file6(request.FILES['file'],eventTitle)
                 
        models.insertEvents1(eventTitle,userid,clubname,eventDt, eventTm,venue,photo ,fees,details)
    return render(request, "Success1.html",{"mess":"Event Registration Done Successfully...","link": "staff"})

def registerReviews(request):
    clubname="NA"
    if request.method == 'POST':
        clubname=request.POST.get("clubname")   
        eventname=request.POST.get("eventname")
        eventId=request.POST.get("eventId")
        review=request.POST.get("review")
        polarity=sentiment.sentimentAnalysis(review)    
        sentiTxt="Neutral"      
        if polarity > 0 :
            sentiTxt="Positive"
        elif polarity < 0 :
            sentiTxt="Negative"
        userid=request.session["userid"]
        username=request.session["username"]
        models.insertReviews(userid,review,username,eventname,clubname,sentiTxt,polarity)
         
        clubname=clubname.replace(" ", "%20")
    return render(request, "Success1.html",{"mess":"Review Submitted Successfully...","link": "viewEvents/?club_name="+clubname})
def UploadDocsEvents(request):
    clubname="NA"
    if request.method == 'POST':
        clubname=request.POST.get("clubname")   
        eventname=request.POST.get("eventname")
        eventId=request.POST.get("eventId")
        title=request.POST.get("title")
        userid=request.session["userid"]
        username=request.session["username"]
        utype=request.session["utype"]
        photo=models.handle_uploaded_file7(request.FILES['file'],title+"_"+eventname) 
        models.insertContent(clubname,photo,eventname, title,userid,username, utype,'pending')

        
        clubname=clubname.replace(" ", "%20")
    return render(request, "Success1.html",{"mess":"Content Uploaded Successfully...","link": "viewEvents/?club_name="+clubname})

def registerClubs(request):
    if request.method == 'POST':
        clubname=request.POST.get("clubname")   
        details=request.POST.get("details")
        clubadmin=request.POST.get("clubadmin")
        fees=request.POST.get("fees")
       
        photo=models.handle_uploaded_file4(request.FILES['file'],clubname)
                 
        models.insertClubs(clubname,photo,details,clubadmin,fees)
    return render(request, "Success1.html",{"mess":"New Club Registration Done Successfully...","link": "admin"})
def compose_message(request):
    if request.method == 'POST':
        userid= request.session['userid']
        expertUserid = request.POST.get("expertUserid")
        msg = request.POST.get("msg")
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cid=models.get_max_comm_id()
        attach1=models.handle_uploaded_file_comm(request.FILES.get("attach1"),cid)
        models.insert_communication(userid, expertUserid, msg, dt, attach1)

        return render(request, "Success1.html",{"mess":"Message Sent Successfully...","link":""+str(request.session['utype'])})
    expuid=request.GET.get("expuid")
    return render(request, "compose_message.html",{"msg":"test","expuid":expuid})
def reply(request):
    if request.method == 'POST':
        expertUserid= request.session['userid']
        cid = request.POST.get("cid")
        msg = request.POST.get("msg")
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         
        attach1=models.handle_uploaded_file_comm_reply(request.FILES.get("attach1"),cid)
        models.update_comm(cid, reply, attach1)

        return render(request, "Success1.html",{"mess":"Reply Sent Successfully...","link":""+str(request.session['utype'])})
    else:
        cid = request.GET.get("cid")
        return render(request, "reply.html",{"cid":cid})
def sent_items(request):
    userid = request.session.get('userid', 'NA')
    expertUserid = request.GET.get("expertUserid")
    messages = models.get_sent_items(userid,expertUserid)
    return render(request, "sent_items.html", {"messages": messages})

def inbox(request):
    userid = request.session.get('userid', 'NA')
    expertUserid = request.GET.get("expertUserid")
    print(expertUserid)
    messages = models.get_inbox(expertUserid)
    return render(request, "inbox.html", {"messages": messages})
def inbox1(request):
    userid = request.session.get('userid', 'NA')
    expertUserid = request.GET.get("expertUserid")
    print(expertUserid)
    messages = models.get_inbox(expertUserid)
    return render(request, "inbox1.html", {"messages": messages})

def reply_message(request):
    if request.method == 'POST':
        expertUserid= request.session['userid']
        cid = request.POST.get("cid")
        reply = request.POST.get("msg")
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         
        attach2=models.handle_uploaded_file_comm_reply(request.FILES.get("attach1"),cid)
        models.update_comm(cid, reply, attach2)

        return render(request, "Success1.html",{"mess":"Reply Sent Successfully...","link":""+str(request.session['utype'])})
