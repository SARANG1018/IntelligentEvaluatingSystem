from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from student import models as SMODEL
from student import forms as SFORM
from django.contrib.auth.models import User
from django.http import JsonResponse
from quiz import models as QMODEL 
import json, math


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    # return render(request,'quiz/index.html')
    # return JsonResponse({'text': 'Just rendering some JSON :)'})
    return render(request,'quiz/index.html')


    

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
        print*=("mai aya hi nahi")
    else:
        return redirect('admin-dashboard')
        print("mai aya")
    
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    # 'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'quiz/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student.html',{'students':students})

@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)

@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')

@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'quiz/admin_course.html')

@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'quiz/admin_add_course.html',{'courseForm':courseForm})

@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')

@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'quiz/admin_question.html')

@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'quiz/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'quiz/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'quiz/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student_marks.html',{'students':students})

# @login_required(login_url='adminlogin')
# def admin_view_marks_view(request,pk):
#     courses = models.Course.objects.all()
#     response =  render(request,'quiz/admin_view_marks.html',{'courses':courses})
#     response.set_cookie('student_id',str(pk))
#     return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    print("IN RESUKT VIEEW")

    result=QMODEL.Result.objects.get(id=pk)
    parent_list=result.parent_list
    num_levels = len(parent_list)
    if(num_levels==0):
        return render(request, 'student/no_result.html')

    num_categories = len(parent_list[0])
    
    # count the number of times each category was attempted
    attempts_count = {}
    for level in range(num_levels):
        for category in parent_list[level]:
            if category not in attempts_count:
                attempts_count[category] = 0
            attempts_count[category] += 1
    
    # determine the feedback based on the number of levels completed
    if num_levels == 1:
        feedback = "Brilliant! You have mastered all courses in level 1."
    elif num_levels == 2:
        feedback = "Good job! You have completed all courses in level 2."
    else:
        feedback = "Keep practicing! It took you {} levels to complete all courses.".format(num_levels)
    
    # add comments on courses attempted multiple times
    comments = []
    for category in attempts_count:
        if attempts_count[category] > 1:
            # comments.append("You had to attempt {} multiple times in different levels.".format(category))
            comments.append("You have attempted {} multiple times throughout different levels. You may want to practice this category more to improve your understanding.".format(category))
    
    return render(request, 'quiz/result.html', {'feedback': feedback, 'comments': comments,'courses':parent_list})

