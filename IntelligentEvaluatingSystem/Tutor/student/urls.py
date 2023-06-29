from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('studentclick', views.studentclick_view),
path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('studentsignup', views.student_signup_view,name='studentsignup'),
path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
path('student-exam', views.student_exam_view,name='student-exam'),
# path('student-exam-new', views.student_exam_view_new,name='student-exam-new'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('exam-summ', views.exam_summ,name='exam-summ'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),
# path('start-exam', views.start_exam_view,name='start-exam'),
path('exam-comp', views.exam_comp_view,name='exam-comp'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
# path('view-result', views.view_result_view,name='view-result'),
path('view-result/<int:pk>', views.view_result,name='view-result'), # my result
path('check-result', views.check_result,name='check-result'),
# path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
path("delete", views.delete_session,name="dlt_session")
]   
