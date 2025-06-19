"""
URL configuration for campusClubManagementApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin),
    path('',views.index),
    path('home/',views.index),
    path('loginpage/',views.loginpage),
    path('regpage/',views.regpage),
    path('Cities/',views.Cities),
    path('registerStud/',views.registerStud),
    path('login/',views.login),
    path('student/',views.student),
    path('staff/',views.staff),
    
    path('viewclubs_principal_pending/',views.principal),
    path('principal/',views.principal),
    path('clubadmin/',views.clubadmin),
    path('viewstudents/',views.viewstudents),
    path('viewstaff/',views.viewstaff),
    path('viewclubs/',views.viewclubs),
    path('viewclubs_approved/',views.viewclubs_approved),
    path('getStudReport/',views.getStudReport),
    path('clubadmin/',views.clubadmin),
    path('approve/',views.approve),
    path('decline/',views.decline),
    path('decline_club/',views.decline_club),
    path('logout/',views.logout),
    path('regStaff/',views.regStaff),
    path('registerStaff/',views.registerStaff),
    path('UseridVali/',views.UseridVali),
    path('ClubVali/',views.ClubVali),
    path('regClubs/',views.regClubs),
    path('registerClubs/',views.registerClubs),
    path('approve_club/',views.approve_club),
    path('send_membership_req/',views.send_membership_req),
    path('send_participant_req/',views.send_participant_req),
    path('sendParticipantRequest/',views.sendParticipantRequest),
    path('sendMembershipRequest/',views.sendMembershipRequest),
    path('forgot/',views.forgot),
    path('pending_participant_req/',views.pending_participant_req),
    path('pending_membership_req/',views.pending_membership_req),
    path('pending_membership_req1/',views.pending_membership_req1),
    path('approveMembership/',views.approveMembership),
    path('approveEventMembership/',views.approveEventMembership),
    path('rejectMembership/',views.rejectMembership),
    path('rejectEventMembership/',views.rejectEventMembership),
    path('markAttendance/',views.markAttendance),
    path('viewAttendance/',views.viewAttendance),
    path('sendotp1/',views.sendotp1),
    path('otpverification1/',views.otpverification1),

    path('regEvents/',views.regEvents),
    path('registerEvent/',views.registerEvent),
    path('viewEvents/',views.viewEvents),
    path('viewEvents_pending/',views.viewEvents_pending),
    path('approve_event/',views.approveEvent),
    path('regReviews/',views.regReviews),
    path('registerReviews/',views.registerReviews),
    path('viewReviewsEvent/',views.viewReviewsEvent),
    path('uploadDocs_event/',views.uploadDocs_event),
    path('UploadDocsEvents/',views.UploadDocsEvents),
    path('viewDocs_event/',views.viewDocs_event),
    path('viewDocs_eventPending/',views.viewDocs_eventPending),
    path('approveDocs/',views.approveDocs),
    path('deleteDocs/',views.approveDocs),
    path('viewEventsStaff/',views.viewEventsStaff),
    path('AttendanceReg/',views.AttendanceReg),
    path('event_calendar/',views.event_calendar), 
    path("event_detail/", views.event_detail, name="event_detail"),
    path("compose_message/", views.compose_message, name="compose_message"),
    path("sent_items/", views.sent_items, name="sent_items"),
    path("inbox/", views.inbox, name="inbox"),
    path("inbox1/", views.inbox1, name="inbox1"),
    path("reply_message/", views.reply_message, name="reply_message"),
    path("reply/", views.reply, name="reply"),
]
