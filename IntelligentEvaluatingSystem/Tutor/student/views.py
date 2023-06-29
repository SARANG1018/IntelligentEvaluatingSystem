from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from algorithm import original_function
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json,math
import random

# Create your views here.

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def student_exam_view_new(request):
#     return render(request,'student/student_exam_new.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def exam_summ(request):    
    return render(request,'student/exam_summ.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def exam_comp_view(request):    
    return render(request,'student/exam_comp.html')

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def take_exam_view(request,pk):
#     courses = QMODEL.Course.objects.all()
#     questions = []
#     total_questions = 0
#     total_marks = 0
#     for course in courses:
#         course_questions = QMODEL.Question.objects.filter(course=course)
#         questions.extend(course_questions)
#         total_questions += course_questions.count()
#         for q in course_questions:
#             total_marks += q.marks
#     return render(request, 'student/take_exam.html', {'courses': courses, 'questions': questions, 'total_questions': total_questions, 'total_marks': total_marks})

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def start_exam_view(request):
#     courses = QMODEL.Course.objects.all()
#     questions = []
#     for course in courses:
#         course_questions = QMODEL.Question.objects.filter(course=course)
#         questions.extend(course_questions)
#     if request.method == 'POST':
#         pass
#     response = render(request, 'student/startexam.html', {'courses': courses, 'questions': questions})
#     return response

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def start_exam_view(request,pk):
#     course=QMODEL.Course.objects.get(id=pk)
#     questions=QMODEL.Question.objects.all().filter(course=course)
#     if request.method=='POST':
#         pass
#     response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
#     response.set_cookie('course_id',course.id)
#     return response


# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def start_exam_view(request):
#     all_courses = QMODEL.Course.objects.all().order_by('id')
#     num_courses = len(all_courses)

#     course_id = request.COOKIES.get('course_id')
#     if course_id:
#         current_course = QMODEL.Course.objects.get(id=course_id)
#     else:
#         current_course = all_courses[0]

#     questions = QMODEL.Question.objects.filter(course=current_course)

#     if request.method == 'POST':
#         # Save answers
#         pass

#         # Get next course
#         next_course = None
#         for i, c in enumerate(all_courses):
#             if c == current_course and i < num_courses - 1:
#                 next_course = all_courses[i+1]
#                 break

#         if next_course:
#             response = render(request, 'student/start_exam.html', {'course': next_course, 'questions': QMODEL.Question.objects.filter(course=next_course)})
#             response.set_cookie('course_id', next_course.id)
#             return response
#         else:
#             return redirect('exam_summary')

#     else:
#         response = render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})
#         return response


# final_answers = []
# final_course_ids = []
# shortest_path_courses=[]
# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):

#     global shortest_path_courses

#     current_course = QMODEL.Course.objects.get(pk=pk)
#     questions = QMODEL.Question.objects.filter(course=current_course)

#     if request.method == 'POST':
#         # Save the user's answers for the current page of questions
#         answers = json.loads(request.COOKIES.get('answers'))
#         course_answers = []
#         print("outside")
#         for question in questions:
#             answer = None
#             for user_answer in answers:
#                 if user_answer['question_id'] == str(question.id):
#                     answer = user_answer['answer']
#                     break
#             if answer == question.answer:
#                 course_answers.append(1)
#             else:
#                 print("zero")
#                 course_answers.append(0)
#         print("outside(1)")
#         final_answers.append(course_answers)
#         final_course_ids.append(current_course)
#         print("final_answers:",final_answers)
#         print("final_course_ids:",final_course_ids)
#         if shortest_path_courses:
#             if shortest_path_courses:
#                 print("Hello baahar Ka")
#                 # current_course_id = shortest_path_courses[0][0].id
#                 # current_course = QMODEL.Course.objects.get(id=current_course_id)
#                 short_course_id = shortest_path_courses[0][0].id
#                 short_course = QMODEL.Course.objects.get(id=short_course_id)
#                 print("short_course",short_course)
#                 short_questions = QMODEL.Question.objects.filter(course=short_course)
#                 print("short_id",short_course_id)
#                 print(short_questions)
#                 final_answers.clear()
#                 final_course_ids.clear()
#                 # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
#                 return redirect('start-exam', pk=short_course_id)
#             else:
#                 return redirect('exam-comp')
#         else:   
#             # Check if there's a next course and redirect to its questions or summary page
#             all_courses = list(QMODEL.Course.objects.all())
#             current_course_index = all_courses.index(current_course)
#             print("length: ",len(all_courses))
#             print("current_course_index: ",current_course_index)
#             if current_course_index + 1 < len(all_courses):
#                 next_course = all_courses[current_course_index + 1]
#                 print("pk",next_course.pk)
#                 print("next course",next_course)
#                 return redirect('start-exam', pk=next_course.pk)
#             else:
#                 # Store the user's answers for all courses in the session variable
#                 if 'course_answers' not in request.session:
#                     request.session['course_answers'] = []
#                 request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})
#                 shortest_path_courses = shortest_path(final_answers, final_course_ids)

#                 if shortest_path_courses:
#                     print("Hello")
#                     # current_course_id = shortest_path_courses[0][0].id
#                     # current_course = QMODEL.Course.objects.get(id=current_course_id)
#                     short_course_id = shortest_path_courses[0][0].id
#                     short_course = QMODEL.Course.objects.get(id=short_course_id)
#                     print("short_course",short_course)
#                     short_questions = QMODEL.Question.objects.filter(course=short_course)
#                     print("short_id",short_course_id)
#                     print(short_questions)
#                     final_answers.clear()
#                     final_course_ids.clear()
#                     # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
#                     return redirect('start-exam', pk=short_course_id)
#                 else:
#                     return redirect('exam-comp')

#     else:
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})

# The Code to be used for present

# final_answers = []
# final_course_ids = []
# shortest_path_courses = []

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     global shortest_path_courses

#     current_course = QMODEL.Course.objects.get(pk=pk)
#     # questions = QMODEL.Question.objects.filter(course=current_course).order_by('?')[:3]
#     questions = QMODEL.Question.objects.filter(course=current_course).order_by('pk')[:3]
#     # questions = QMODEL.Question.objects.filter(course=current_course)
#     print("quests",questions)

#     if request.method == 'POST':
#         # Save the user's answers for the current page of questions
#         answers = json.loads(request.COOKIES.get('answers'))
#         course_answers = []
#         print("outside")
#         for question in questions:
#             answer = None
#             for user_answer in answers:
#                 print("in user")
#                 print(answers)
#                 print("Mera",user_answer['question_id'],"....",str(question.id))
#                 if user_answer['question_id'] == str(question.id):
#                     print("innnssside")
#                     answer = user_answer['answer']
#                     break
#             print("answer =",answer,"....", question.answer)
#             if answer == question.answer:
#                 course_answers.append(1)
#             else:
#                 print("zero")
#                 course_answers.append(0)
#         print("outside(1)")
#         final_answers.append(course_answers)
#         final_course_ids.append(current_course)
#         print("final_answers:",final_answers)
#         print("final_course_ids:",final_course_ids)

        
#         # Check if there's a next course and redirect to its questions or summary page
#         # all_courses = list(QMODEL.Course.objects.all())
#         # current_course_index = all_courses.index(current_course)
#         if shortest_path_courses:
#             all_courses = [course[0] for course in shortest_path_courses]
#             current_course_index = all_courses.index(current_course)
#         else:
#             all_courses = list(QMODEL.Course.objects.all())
#             current_course_index = all_courses.index(current_course)
#         print("length: ",len(all_courses))
#         print("current_course_index: ",current_course_index)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             print("pk",next_course.pk)
#             print("next course",next_course)
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             # Store the user's answers for all courses in the session variable
#             if 'course_answers' not in request.session:
#                 request.session['course_answers'] = []
#             request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})
#             shortest_path_courses = shortest_path(final_answers, final_course_ids)

#             if shortest_path_courses:
#                 print("Hello")
#                 # current_course_id = shortest_path_courses[0][0].id
#                 # current_course = QMODEL.Course.objects.get(id=current_course_id)
#                 short_course_id = shortest_path_courses[0][0].id
#                 short_course = QMODEL.Course.objects.get(id=short_course_id)
#                 print("short_course",short_course)
#                 short_questions = QMODEL.Question.objects.filter(course=short_course)
#                 print("short_id",short_course_id)
#                 print(short_questions)
#                 final_answers.clear()
#                 final_course_ids.clear()
#                 # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
#                 return redirect('start-exam', pk=short_course_id)
#             else:
#                 return redirect('exam-comp')

#     else:
#         # Render the start_exam.html template with the current course's questions
#         print("Outer Else")
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})


# final_answers = []
# final_course_ids = []
# shortest_path_courses = []
# short_questions= []

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     global shortest_path_courses
#     global short_questions

#     current_course = QMODEL.Course.objects.get(pk=pk)
#     print(current_course)
#     # questions = QMODEL.Question.objects.filter(course=current_course).order_by('?')[:3]
#     questions = QMODEL.Question.objects.filter(course=current_course).order_by('pk')[:3]
#     # questions = QMODEL.Question.objects.filter(course=current_course)
#     print("quests",questions)

#     if request.method == 'POST':
#         # Save the user's answers for the current page of questions
#         answers = json.loads(request.COOKIES.get('answers'))
#         course_answers = []
#         print("outside")
#         for question in questions:
#             answer = None
#             for user_answer in answers:
#                 print("in user")
#                 print(answers)
#                 print("Mera",user_answer['question_id'],"....",str(question.id))
#                 if user_answer['question_id'] == str(question.id):
#                     print("innnssside")
#                     answer = user_answer['answer']
#                     break
#             print("answer =",answer,"....", question.answer)
#             if answer == question.answer:
#                 course_answers.append(1)
#             else:
#                 print("zero")
#                 course_answers.append(0)
#         print("outside(1)")
#         final_answers.append(course_answers)
#         final_course_ids.append(current_course)
#         print("final_answers:",final_answers)
#         print("final_course_ids:",final_course_ids)

        
#         # Check if there's a next course and redirect to its questions or summary page
#         # all_courses = list(QMODEL.Course.objects.all())
#         # current_course_index = all_courses.index(current_course)
#         if shortest_path_courses:
#             all_courses = [course[0] for course in shortest_path_courses]
#             current_course_index = all_courses.index(current_course)
#         else:
#             all_courses = list(QMODEL.Course.objects.all())
#             current_course_index = all_courses.index(current_course)
#         print("length: ",len(all_courses))
#         print("current_course_index: ",current_course_index)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             print("pk",next_course.pk)
#             print("next course",next_course)
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             # Store the user's answers for all courses in the session variable
#             if 'course_answers' not in request.session:
#                 request.session['course_answers'] = []
#             request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})
#             shortest_path_courses = shortest_path(final_answers, final_course_ids)

#             # if shortest_path_courses:
#             #     print("Hello")
#             #     # current_course_id = shortest_path_courses[0][0].id
#             #     # current_course = QMODEL.Course.objects.get(id=current_course_id)
#             #     short_course_id = shortest_path_courses[0][0].id
#             #     short_course = QMODEL.Course.objects.get(id=short_course_id)
#             #     print("short_course",short_course)
#             #     short_questions = QMODEL.Question.objects.filter(course=short_course)
#             #     print("short_id",short_course_id)
#             #     print(short_questions)
#             #     final_answers.clear()
#             #     final_course_ids.clear()
#             #     # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
#             #     return redirect('start-exam', pk=short_course_id)
#             # else:
#             #     return redirect('exam-comp')
            
#             if shortest_path_courses:
#                 short_course_id = shortest_path_courses[0][0].id
#                 short_course = QMODEL.Course.objects.get(id=short_course_id)
#                 response_combinations = generate_responses(shortest_path_courses)
#                 print("response comb: ",response_combinations)
#                 short_questions = []
#                 seen_indices = set()
#                 seen_combinations = set()
#                 for response_combination in response_combinations:
#                     print("res combi: ",response_combination)
#                     # Check if this combination has already been processed
#                     combination = tuple(response_combination[2])
#                     if combination in seen_combinations:
#                         continue
#                     seen_combinations.add(combination)

#                     # Check if any course has used this combination of difficulty levels before
#                     index = tuple([response_combination[0], combination])
#                     if index in seen_indices:
#                         continue
#                     seen_indices.add(index)

#                     # # Check if this index has already been processed
#                     # index = tuple(response_combination[2])
#                     # if index in seen_indices:
#                     #     continue
#                     # seen_indices.add(index)

#                     e_count = response_combination[2].count('E')
#                     m_count = response_combination[2].count('M')
#                     h_count = response_combination[2].count('H')
#                     e_questions = QMODEL.Question.objects.filter(course=short_course, difficulty='E').order_by('pk')[:e_count]
#                     print("easy: ",e_questions)
#                     m_questions = QMODEL.Question.objects.filter(course=short_course, difficulty='M').order_by('pk')[:m_count]
#                     print("medium: ",m_questions)
#                     h_questions = QMODEL.Question.objects.filter(course=short_course, difficulty='H').order_by('pk')[:h_count]
#                     print("hard: ",h_questions)
#                     short_questions.extend(list(e_questions))   
#                     short_questions.extend(list(m_questions))
#                     short_questions.extend(list(h_questions))
#                 # for difficulty_level in ['E', 'M', 'H']:
#                 #     # Count how many questions are needed for this difficulty level
#                 #     count = sum(response_combination[2].count(difficulty_level) for response_combination in response_combinations)
#                 #     print(difficulty_level,": ",count)
#                 #     # Randomly select questions for this difficulty level
#                 #     questions = QMODEL.Question.objects.filter(course=short_course, difficulty=difficulty_level).order_by('pk')[:count]
#                 #     print(difficulty_level,": ",questions)
    
#                 #     # Add the selected questions to the list
#                 #     short_questions.extend(list(questions))
#                 #     print(difficulty_level,": ",short_questions)

#                 random.shuffle(short_questions)
#                 print("list quest: ",short_questions)
#                 # return render(request, 'exam.html', {'questions': short_questions})
#                 final_answers.clear()
#                 final_course_ids.clear()
#                 # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
#                 return redirect('start-exam', pk=short_course_id)
#             else:
#                 return redirect('exam-comp')
#     else:
#         # Render the start_exam.html template with the current course's questions
#         print("Outside Else")
#         print("short: ",short_questions)
#         if short_questions:
#             # If there are questions in short_questions, use those questions for the current course
#             questions = short_questions
#             # Clear the short_questions list so that it is not used again by mistake
#             short_questions = []
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})
#         # return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})

#Use this code
final_answers = []
final_course_ids = []
shortest_path_courses = []
short_questions= []
short_question_sets=[]
questions=[]
#parent_list=[]

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def start_exam_view(request, pk):
    print("outside request session",request.session.get('parent_list', []))
    global shortest_path_courses
    global short_questions
    global short_question_sets
    global questions

    # result=models.Student.objects.prefetch_related("result_set").filter(user_id=request.user.id)
    # print("RESULT",result)
    # print("RESULT PAREMT",result.parent_list)


    # parent_list = request.session.get('parent_list',[])
    # print("outside parent list",parent_list)
    
    current_course = QMODEL.Course.objects.get(pk=pk)
    print(current_course)
    # questions = QMODEL.Question.objects.filter(course=current_course).order_by('?')[:3]
    # questions = QMODEL.Question.objects.filter(course=current_course).order_by('pk')[:3]
    # questions = QMODEL.Question.objects.filter(course=current_course)
    if (short_question_sets):
        print("IN Short")
        if(short_question_sets[0]==0):
            short_question_sets=[]
        # if(len(short_question_sets)==1):
        #     questions=short_question_sets.pop(0)
        # questions = short_question_sets[0] 
    # else:
    #     print("IN NOrmal")
    #     questions = QMODEL.Question.objects.filter(course=current_course).order_by('pk')[:3]
    print("outside  quests",questions)

    if request.method == 'POST':
        # Save the user's answers for the current page of questions
        answers = json.loads(request.COOKIES.get('answers'))
        course_answers = []
        print("outside")
        for question in questions:
            answer = None
            for user_answer in answers:
                print("in user")
                # print(answers)
                # print("Mera",user_answer['question_id'],"....",str(question.id))
                if user_answer['question_id'] == str(question.id):
                    print("innnssside")
                    answer = user_answer['answer']
                    break
            # print("answer =",answer,"....", question.answer)
            if answer == question.answer:
                course_answers.append(1)
            else:
                print("zero")
                course_answers.append(0)
        print("outside(1)")
        final_answers.append(course_answers)
        final_course_ids.append(current_course)
        print("final_answers:",final_answers)
        print("final_course_ids:",final_course_ids) 
        
        
        # Check if there's a next course and redirect to its questions or summary page
        # all_courses = list(QMODEL.Course.objects.all())
        # current_course_index = all_courses.index(current_course)
        if shortest_path_courses:
            all_courses = [course[0] for course in shortest_path_courses]
            current_course_index = all_courses.index(current_course)
        else:
            all_courses = list(QMODEL.Course.objects.all())
            current_course_index = all_courses.index(current_course)
        print("length: ",len(all_courses))
        print("current_course_index: ",current_course_index)
        if current_course_index + 1 < len(all_courses):
            next_course = all_courses[current_course_index + 1]
            print("pk",next_course.pk)
            print("next course",next_course)
            print(type(next_course.pk))
            return redirect('start-exam', pk=next_course.pk)
        else:
            # Store the user's answers for all courses in the session variable
            if 'course_answers' not in request.session:
                request.session['course_answers'] = []
            request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})
            if 'parent_list' not in request.session:
                request.session['parent_list'] = []
            course_ids = [course.id for course in final_course_ids]
            request.session['parent_list'].append(course_ids)
            print("Course.IDs",course_ids)
            # request.session['parent_list'].append(final_course_ids)
            # parent_list=request.session.get('parent_list',[])
            # parent_list.append(final_course_ids)
            # parent_list.append(final_course_ids.copy())
            # print("parent_list: ",parent_list)
            print("parent_list REQUEST SESSION: ",request.session.get('parent_list',[]))
            # request.session['parent_list'] = parent_list
            print("request.session:: ",request.session['parent_list'])
            shortest_path_courses = shortest_path(final_answers, final_course_ids)
            print("Over the error")
            if shortest_path_courses:
                print("In shortest path: ",request.session.get('parent_list',[]))

                print("outside else OVER ERROR")
                short_course_id = shortest_path_courses[0][0].id
                print("short_course_id: ",short_course_id)
                short_course = QMODEL.Course.objects.get(id=short_course_id)
                response_combinations = generate_responses(shortest_path_courses)
                print("response comb: ",response_combinations)
                short_questions = []
                seen_indices = set()
                seen_combinations = set()
                for response_combination in response_combinations:
                    print("res combi: ",response_combination)
                    print(response_combination[0].id)
                    # Check if this combination has already been processed
                    # combination = tuple(response_combination[2])
                    # if combination in seen_combinations:
                    #     continue
                    # seen_combinations.add(combination)

                    # Check if any course has used this combination of difficulty levels before
                    # index = tuple([response_combination[0], combination])
                    # if index in seen_indices:
                    #     continue
                    # seen_indices.add(index)


                    e_count = response_combination[2].count('E')
                    m_count = response_combination[2].count('M')
                    h_count = response_combination[2].count('H')
                    e_questions = QMODEL.Question.objects.filter(course=response_combination[0].id, difficulty='E').order_by('?')[:e_count]
                    # print("easy: ",e_questions)
                    m_questions = QMODEL.Question.objects.filter(course=response_combination[0].id, difficulty='M').order_by('?')[:m_count]
                    # print("medium: ",m_questions)
                    h_questions = QMODEL.Question.objects.filter(course=response_combination[0].id, difficulty='H').order_by('?')[:h_count]
                    # print("hard: ",h_questions)
                    short_questions.extend(list(e_questions))   
                    short_questions.extend(list(m_questions))
                    short_questions.extend(list(h_questions))
                    # print("short_quest: ",short_questions)
                    random.shuffle(short_questions)
                    short_question_sets.append(short_questions)
                    # print("sets: ",short_question_sets)
                    short_questions=[]
 

                # random.shuffle(short_questions)
                # print("list quest: ",short_questions)
                # print("list quest: ",short_question_sets)
                # return render(request, 'exam.html', {'questions': short_questions})
                print("BEFORE FINAL: ",request.session.get('parent_list',[]))

                final_answers.clear()
                final_course_ids.clear()
                print("AFTER FINAL: ",request.session.get('parent_list',[]))
                # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
                print(type(short_course_id))
                
                return redirect('start-exam', pk=short_course_id)
            else:
                final_answers.clear()
                final_course_ids.clear()
                # return redirect('exam-comp')
                print("Inside else OVER ERROR")
                student = models.Student.objects.get(user_id=request.user.id)
                res_list=request.session.get('parent_list',[])
                print("RESULT_LIST",res_list)
                result = QMODEL.Result()
                result.student=student
                result.parent_list=res_list
                result.save()
                print("Result is saved")
                del request.session['parent_list']
                return redirect('check-result')
    else:
        # Render the start_exam.html template with the current course's questions
        print("Outside Else")
        print("short: ",short_question_sets)
        # if short_questions:
        #     # If there are questions in short_questions, use those questions for the current course
        #     questions = short_questions
        #     # Clear the short_questions list so that it is not used again by mistake
        #     short_questions = []
        if short_question_sets:
            # If there are questions in short_questions, use those questions for the current course
            # questions = short_question_sets[0]
            # Clear the short_questions list so that it is not used again by mistake
            # parent_list = request.session.get('parent_list', [])
            # print("inside parent list",parent_list)
            print("inside request session",request.session.get('parent_list', []))
            if(len(short_question_sets)==1):
                questions = short_question_sets.pop(0)
                short_question_sets.append(0)
                print("length 1")
            else:
                questions = short_question_sets.pop(0)
                print("lenght 1 nahi hai")
        else:
            print("IN NOrmal")
            questions = QMODEL.Question.objects.filter(course=current_course).order_by('?')[:3]
        print("inside quests: ",questions)
        # # Render the start_exam.html template with the current course's questions
        return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})
        # return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})

def delete_session(request):
    try:
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")


# final_answers = []
# final_course_ids = []
# shortest_path_courses = []

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     global shortest_path_courses

#     current_course = QMODEL.Course.objects.get(pk=pk)
#     print(current_course)
#     questions = QMODEL.Question.objects.filter(course=current_course).order_by('pk')[:3]
#     print("quests",questions)

#     if request.method == 'POST':
#         answers = json.loads(request.COOKIES.get('answers'))
#         course_answers = []
#         print("outside")
#         for question in questions:
#             answer = None
#             for user_answer in answers:
#                 print("in user")
#                 print(answers)
#                 print("Mera",user_answer['question_id'],"....",str(question.id))
#                 if user_answer['question_id'] == str(question.id):
#                     print("innnssside")
#                     answer = user_answer['answer']
#                     break
#             print("answer =",answer,"....", question.answer)
#             if answer == question.answer:
#                 course_answers.append(1)
#             else:
#                 print("zero")
#                 course_answers.append(0)
#         print("outside(1)")
#         final_answers.append(course_answers)
#         final_course_ids.append(current_course)
#         print("final_answers:",final_answers)
#         print("final_course_ids:",final_course_ids)
#         if shortest_path_courses:
#             all_courses = [course[0] for course in shortest_path_courses]
#             current_course_index = all_courses.index(current_course)
#         else:
#             all_courses = list(QMODEL.Course.objects.all())
#             current_course_index = all_courses.index(current_course)
#         print("length: ",len(all_courses))
#         print("current_course_index: ",current_course_index)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             print("pk",next_course.pk)
#             print("next course",next_course)
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             if 'course_answers' not in request.session:
#                 request.session['course_answers'] = []
#             request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})
#             shortest_path_courses = shortest_path(final_answers, final_course_ids)
#             if shortest_path_courses:
#                 short_course_id = shortest_path_courses[0][0].id
#                 short_course = QMODEL.Course.objects.get(id=short_course_id)
#                 response_combinations = generate_responses(shortest_path_courses)
#                 print("response comb: ",response_combinations)
#                 short_questions = []
#                 seen_indices = set()
#                 seen_combinations = set()
#                 for response_combination in response_combinations:
#                     # Check if this combination has already been processed
#                     combination = tuple(response_combination[2])
#                     if combination in seen_combinations:
#                         continue
#                     seen_combinations.add(combination)

#                     # Check if any course has used this combination of difficulty levels before
#                     index = tuple([response_combination[0], combination])
#                     if index in seen_indices:
#                         continue
#                     seen_indices.add(index)
#                     e_count = response_combination[2].count('E')
#                     m_count = response_combination[2].count('M')
#                     h_count = response_combination[2].count('H')
#                     e_questions = QMODEL.Question.objects.filter(course=short_course, difficulty='E').order_by('pk')[:e_count]
#                     print("easy: ",e_questions)
#                     m_questions = QMODEL.Question.objects.filter(course=short_course, difficulty='M').order_by('pk')[:m_count]
#                     print("medium: ",m_questions)
#                     h_questions = QMODEL.Question.objects.filter(course=short_course, difficulty='H').order_by('pk')[:h_count]
#                     print("hard: ",h_questions)
#                     short_questions.extend(list(e_questions))   
#                     short_questions.extend(list(m_questions))
#                     short_questions.extend(list(h_questions))
#                 random.shuffle(short_questions)
#                 print("list quest: ",short_questions)
#                 final_answers.clear()
#                 final_course_ids.clear()
#                 # return render(request, 'student/start_exam.html', {'course': short_course, 'questions': short_questions})
#                 return redirect('start-exam', pk=short_course_id)
#             else:
#                 return redirect('exam-comp')
#     else:
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})

    

def calculate_total_responses(categories):
    return [sum(category) for category in categories]


def calculate_ability_parameter(total_responses, num_categories, num_questions):
    try:
        return math.log(sum(total_responses) / (num_categories * num_questions) / (1 - sum(total_responses) / (num_categories * num_questions)))
    except:
        if(sum(total_responses)==0):
            return -4
        else:
            return 4

def calculate_lesson_difficulty(category_responses, num_questions: int):
    try:
        return math.log((1 - (sum(category_responses) / num_questions)) / (sum(category_responses) / num_questions))
    except:
            if all(response == 0 for response in category_responses):
                return 4
            else:
                return -4


def calculate_correctness_prob(a, lesson_difficulty):
    return ((math.e) ** (a - lesson_difficulty)) / (1 + (math.e) ** (a - lesson_difficulty))


def filter_categories(correctness_prob):

    return [i for i in range(len(correctness_prob)) if correctness_prob[i] < 0.40]


def sort_categories(filtered_categories, category_names, correctness_prob):
    info = []
    for j in filtered_categories:
        info.append((category_names[j], correctness_prob[j] * (1 - correctness_prob[j])))
    info.sort(key=lambda x: x[1])
    return info


def shortest_path(categories, category_names):
    total_responses = calculate_total_responses(categories)
    print("total responses",total_responses)
    print(sum(total_responses))
    num_categories = len(categories)
    print("num_categories",num_categories)
    num_questions = len(categories[0])
    print("num_questions",num_questions)
    a = calculate_ability_parameter(total_responses, num_categories, num_questions)
    print("printing a",a)
    lesson_difficulty = [calculate_lesson_difficulty(categories[i], num_questions) for i in range(num_categories)]
    print("lessond difficulty",lesson_difficulty)
    correctness_prob = [calculate_correctness_prob(a, lesson_difficulty[i]) for i in range(num_categories)]
    print("correctness prob",correctness_prob)
    filtered_categories = filter_categories(correctness_prob)
    print("filtered categories",filtered_categories)
    shortest_path = sort_categories(filtered_categories, category_names, correctness_prob)
    print("shortest path",shortest_path)
    return shortest_path

def generate_responses(shortest_path_results):
    response_combinations = []
    for course_info in shortest_path_results:
        course_name = course_info[0]
        course_info_factor = course_info[1]
        if course_info_factor < 0.05:
            response_combinations.append((course_name, course_info_factor, ["E"]*3))
        elif course_info_factor < 0.2:
            response_combinations.append((course_name, course_info_factor, ["E"]*2 + ["M"]*1))
        elif course_info_factor < 0.5:
            response_combinations.append((course_name, course_info_factor, ["E"]*1 + ["M"]*1 + ["H"]*1))
        else:
            response_combinations.append((course_name, course_info_factor, ["M", "M", "H"]))
    return response_combinations




















# This is the best view until now

# final_answers = []
# final_course_ids=[]
# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     current_course = QMODEL.Course.objects.get(pk=pk)
#     questions = QMODEL.Question.objects.filter(course=current_course)
    
#     print("body: ",request.body)
#     print("post: ",request.POST)
#     if request.method == 'POST':
#         # Save the user's answers for the current page of questions
#         # answers = json.loads(request.POST.get('1'))
#         answers = json.loads(request.COOKIES.get('answers'))
#         print("answers are :",answers)
#         course_answers=[]
#         for question in questions:
#             answer = None
#             for user_answer in answers:
#                 if user_answer['question_id'] == str(question.id):
#                     answer = user_answer['answer']
#                     break
#             if answer == question.answer:
#                 course_answers.append(1)
#             else:
#                 course_answers.append(0)
#         final_answers.append(course_answers)
#         final_course_ids.append(current_course)
#         print("course_answers:", course_answers)
#         print("final_answers:", final_answers)
#         print("final_course_ids:", final_course_ids)

#         # Check if there's a next course and redirect to its questions or summary page
#         all_courses = list(QMODEL.Course.objects.all())
#         current_course_index = all_courses.index(current_course)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             # Store the user's answers for all courses in the session variable
#             if 'course_answers' not in request.session:
#                 request.session['course_answers'] = []
#             request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})
#             final_answers=[]
#             return redirect('exam-comp')
#     else:   
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})




# This is saving answere for whole course
# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     current_course = QMODEL.Course.objects.get(pk=pk)
#     questions = QMODEL.Question.objects.filter(course=current_course)
#     course_answers = []
#     print("body: ",request.body)
#     print("post: ",request.POST)
#     if request.method == 'POST':
#         # Save the user's answers for the current page of questions
#         print(request.COOKIES.get('answers'))
#         # answers = json.loads(request.POST.get('1'))
#         answers = json.loads(request.COOKIES.get('answers'))
#         print("answers are :",answers)
#         course_answers.extend(answers)
#         print("course::",course_answers)

#         # Check if there's a next course and redirect to its questions or summary page
#         all_courses = list(QMODEL.Course.objects.all())
#         current_course_index = all_courses.index(current_course)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             # Store the user's answers for all courses in the session variable
#             if 'course_answers' not in request.session:
#                 request.session['course_answers'] = []
#             request.session['course_answers'].append({'course_id': pk, 'answers': course_answers})

#             return redirect('calculate-marks')
#     else:
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})

# This is saving ans for each question 

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     current_course = QMODEL.Course.objects.get(pk=pk)
#     print(pk)
#     questions = QMODEL.Question.objects.filter(course=current_course)

#     if request.method == 'POST':
#         # Save the answers submitted by the user in a list
#         course_answers = []
#         for question in questions:
#             answer = request.POST.get(str(question.id), 'hel')
#             print("answer",answer)
#             print("cuur_ans",question.answer)
#             if answer == question.answer:
#                 course_answers.append(1)
#             else:
#                 course_answers.append(0)
#             print(course_answers)

#         # Save the course answers in a list of course lists
#         if 'course_answers' in request.session:
#             request.session['course_answers'].append(course_answers)
#         else:
#             request.session['course_answers'] = [course_answers]

#         # Check if there's a next course and redirect to its questions or summary page
#         print("hello")
#         all_courses = list(QMODEL.Course.objects.all())
#         current_course_index = all_courses.index(current_course)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             print(course_answers)
#             # return redirect('exam-comp')
#             # response = redirect('calculate-marks')
#             # response.set_cookie('course_answers', json.dumps(request.session['course_answers']), max_age=3600)
#             return redirect('calculate-marks')
#             # return response
#     else:
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})

#NEXT BEST VIEW

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     current_course = QMODEL.Course.objects.get(pk=pk)
#     questions = QMODEL.Question.objects.filter(course=current_course)

#     if request.method == 'POST':
#         # Save the answers submitted by the user in the session
#         for question in questions:
#             answer = request.POST.get(str(question.id), '')
#             request.session[str(question.id)] = answer

#         # Check if there's a next course and redirect to its questions or summary page
#         all_courses = list(QMODEL.Course.objects.all())
#         current_course_index = all_courses.index(current_course)
#         if current_course_index + 1 < len(all_courses):
#             next_course = all_courses[current_course_index + 1]
#             return redirect('start-exam', pk=next_course.pk)
#         else:
#             # return redirect('exam-comp')
#             return redirect('calculate-marks')
#     else:
#         # Render the start_exam.html template with the current course's questions
#         return render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})


#BEST AVAILABLE DJANGO VIEW

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     current_course = QMODEL.Course.objects.get(pk=pk)
#     print(pk)
#     print(current_course)
#     print(current_course.id)
#     questions = QMODEL.Question.objects.filter(course=current_course)
#     print(questions[0])
#     print(request.method)

#     # Get the ID of the next course
#     def get_next_course_id(current_course_id, all_courses):
#         current_course_index = next((i for i, course in enumerate(all_courses) if course.id == current_course_id), None)
#         if current_course_index is None or current_course_index == len(all_courses) - 1:
#             return None
#         else:
#             return all_courses[current_course_index + 1].id
            
#     if request.method == 'POST':
#         # Save the answers submitted by the user in the cookies
#         for question in questions:
#             answer = request.POST.get(str(question.id), '')
#             response = HttpResponse()
#             response.set_cookie(str(question.id), answer)

        
#         print(current_course.id)
#         next_course_id = get_next_course_id(current_course.id, list(QMODEL.Course.objects.all()))
#         print(next_course_id)
#         if next_course_id is not None:
#             print("Next is Known")
#             # If there is a next course, get its object and questions, render the start_exam.html template with the next course and questions, set the course_id cookie to the ID of the next course, and return the response
#             next_course = QMODEL.Course.objects.get(pk=next_course_id)
#             print(next_course)
#             response = render(request, 'student/start_exam.html', {'course': next_course, 'questions': QMODEL.Question.objects.filter(course=next_course), 'has_next_course': next_course_id is not None})
#             response.set_cookie('course_id', next_course.id)
#             print(response)
#             return response
#         else:
#             print("Next Is Not Known")
#             # If there are no more courses, redirect to the exam summary page
#             return redirect('exam_summary')
#     else:
#         print("Not Submitted")
#         # If the form was not submitted, render the start_exam.html template with the current course and questions and the "Next" button
#         all_courses = list(QMODEL.Course.objects.all())
#         next_course_id = get_next_course_id(current_course.id, all_courses)
#         has_next_course = next_course_id is not None

#         response = render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions, 'has_next_course': has_next_course, 'all_courses': all_courses})
#         response.set_cookie('course_id', current_course.id)
#         return response

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# @csrf_exempt
# def start_exam_view(request, pk):
#     current_course = QMODEL.Course.objects.get(pk=pk)
#     questions = QMODEL.Question.objects.filter(course=current_course)
#     print(request.method)
#     if request.method == 'POST' and 'next' in request.POST:
#         # Save the answers submitted by the user in the cookies
#         for question in questions:
#             answer = request.POST.get(str(question.id), '')
#             response = HttpResponse()
#             response.set_cookie(str(question.id), answer)

#         # Get the ID of the next course
#         def get_next_course_id(current_course_id):
#             courses = list(QMODEL.Course.objects.all())
#             current_course_index = next((i for i, course in enumerate(courses) if course.id == current_course_id), None)
#             if current_course_index is None or current_course_index == len(courses) - 1:
#                 return None
#             else:
#                 return courses[current_course_index + 1].id

#         next_course_id = get_next_course_id(current_course.id)

#         if next_course_id is not None:
#             print("Next is Known")
#             # If there is a next course, get its object and questions, render the start_exam.html template with the next course and questions, set the course_id cookie to the ID of the next course, and return the response
#             next_course = QMODEL.Course.objects.get(pk=next_course_id)
#             response = render(request, 'student/start_exam.html', {'course': next_course, 'questions': QMODEL.Question.objects.filter(course=next_course)})
#             response.set_cookie('course_id', next_course.id)
#             return response
#         else:
#             print("Next Is Not Known")
#             # If there are no more courses, redirect to the exam summary page
#             return redirect('exam_summary')
#     else:
#         print("Not Submitted")
#         # If the form was not submitted with the "next" button, render the start_exam.html template with the current course and questions
#         response = render(request, 'student/start_exam.html', {'course': current_course, 'questions': questions})
#         return response


# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def start_exam_view(request,pk):
#     course = QMODEL.Course.objects.get(id=pk)
#     questions = QMODEL.Question.objects.all().filter(course=course)

#     if request.method == 'POST':
#         print("Pass")
#         pass

#     # Get the current course ID from the cookie
#     current_course_id = request.COOKIES.get('course_id')
#     print(current_course_id)
#     if current_course_id is None:
#         print("IF loop")
#         # If there is no current course ID in the cookie, set it to the ID of the first course
#         course_ids = [c.id for c in QMODEL.Course.objects.all()]
#         current_course_id = course_ids[0]
#         response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
#     else:
#         print("Else")
#         print("str: ",str(course.id))
#         print("curr: ",current_course_id)
#         if str(course.id) != current_course_id:
#             print("INner If")
#             # If the current course ID in the cookie is not the same as the ID of the current course,
#             # redirect to the next course
#             course_ids = [c.id for c in QMODEL.Course.objects.all()]
#             current_course_index = course_ids.index(int(current_course_id))
#             next_course_index = (current_course_index + 1) % len(course_ids)
#             next_course_id = course_ids[next_course_index]
#             response = redirect('start-exam', pk=next_course_id)
#         else:
#             print("Inner else")
#             # If the current course ID in the cookie is the same as the ID of the current course,
#             # render the exam page as usual
#             response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
#     print(response)
#     # Set the cookie to the ID of the current course
#     # response.set_cookie('course_id', course.id)
#     return response

# def start_exam_view(request, pk):
#     course = QMODEL.Course.objects.get(id=pk)
#     # categories = QMODEL.Category.objects.all().filter(course=course)
#     categories = QMODEL.Course.objects.all().filter(course=course)
#     questions = {}

#     # Create a dictionary of questions grouped by category
#     for category in categories:
#         questions[category.id] = QMODEL.Question.objects.filter(category=category)

#     if request.method == 'POST':
#         # Get the submitted answers
#         submitted_answers = []
#         for category_id, qs in questions.items():
#             for q in qs:
#                 answer = request.POST.get(str(q.id))
#                 if answer:
#                     submitted_answers.append((q, answer))

#         # Analyze the submitted answers to get failed categories
#         failed_categories = set()
#         for category_id, qs in questions.items():
#             incorrect_count = 0
#             for q in qs:
#                 submitted = next((ans for ans in submitted_answers if ans[0] == q), None)
#                 if submitted and submitted[1] != q.answer:
#                     incorrect_count += 1
#             # If the majority of questions in this category were answered incorrectly,
#             # it is considered a failed category
#             if incorrect_count / len(qs) >= 0.5:
#                 failed_categories.add(category_id)

#         # Redirect to the results page with failed categories
#         return redirect('exam_result', pk=course.id, failed_categories=list(failed_categories))

#     # Get the current category to show in the template
#     current_category_id = int(request.GET.get('category', questions.keys()[0]))

#     # Filter questions based on the current category
#     current_questions = questions.get(current_category_id, [])

#     # Set cookies to remember the current category and selected answers
#     response = render(request, 'student/start_exam.html', {
#         'course': course,
#         'categories': categories,
#         'current_category': current_category_id,
#         'current_questions': current_questions
#     })
#     response.set_cookie('course_id', course.id)
#     response.set_cookie('current_category', current_category_id)
#     return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def calculate_marks_view(request):
    print("i am out")
    if request.COOKIES.get('course_id') is not None:
        print("I am in ")
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        print(course)
        total_marks=0
        answers = []
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            print(i)
            selected_ans = request.COOKIES.get(str(i+1))
            print(selected_ans)
            actual_answer = questions[i].answer
            print(actual_answer)
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
                answers.append(1)
            else:   
                answers.append(0)
        print(answers)
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course 
        result.student=student
        result.save()
        # #Syntax
        

        return HttpResponseRedirect('view-result')
        # return render(request,'student/view_result.html',{'course':course})
    
# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def view_result_view(request):
#     courses=QMODEL.Course.objects.all()
#     return render(request,'student/view_result.html',{'courses':courses})

# My result page
# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def view_result(request):
#     parent_list = [
#     ["category 1", "category 2", "category 3"],
#     ["category 1", "category 3"],
#     ["category 1"]
# ]
    
#     return render(request,'student/result.html',{'courses':parent_list})

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def view_result(request):
#     # parent_list = [
#     # ["category 1", "category 2", "category 3"],
#     # ["category 1", "category 3"],
#     # ["category 1"],
#     # ["category 1"]
#     # ]
#     # parent_list = [
#     # ["Triangle", "Equilateral", "Circle","Cone"],
#     # ["Circle", "Triangle", "Equilateral"],
#     # ["Circle"]
#     # ]
#     student = models.Student.objects.get(user_id=request.user.id)
#     result= QMODEL.Result.objects.filter(student=student)
#     print("RESULT QUERY SET",result)
#     print("RESULT FROM DATABASE: ",result.last().parent_list)
#     print("IN RESUKT VIEEW")
#     parent_list= request.session.get('parent_list', [])
#     # print(parent_list)
#     final_course_ids = [[QMODEL.Course.objects.get(id=course_id) for course_id in course_ids] for course_ids in parent_list]
#     print(final_course_ids)
#     parent_list=final_course_ids
#     print("NEW PARENT LIST",parent_list)

#     num_levels = len(parent_list)
#     if(num_levels==0):
#         return render(request, 'student/no_result.html')

#     num_categories = len(parent_list[0])
    
#     # count the number of times each category was attempted
#     attempts_count = {}
#     for level in range(num_levels):
#         for category in parent_list[level]:
#             if category not in attempts_count:
#                 attempts_count[category] = 0
#             attempts_count[category] += 1
    
#     # determine the feedback based on the number of levels completed
#     if num_levels == 1:
#         feedback = "Brilliant! You have mastered all courses in level 1."
#     elif num_levels == 2:
#         feedback = "Good job! You have completed all courses in level 2."
#     else:
#         feedback = "Keep practicing! It took you {} levels to complete all courses.".format(num_levels)
    
#     # add comments on courses attempted multiple times
#     comments = []
#     for category in attempts_count:
#         if attempts_count[category] > 1:
#             # comments.append("You had to attempt {} multiple times in different levels.".format(category))
#             comments.append("You have attempted {} multiple times throughout different levels. You may want to practice this category more to improve your understanding.".format(category))
    
#     return render(request, 'student/result.html', {'feedback': feedback, 'comments': comments,'courses':parent_list})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result(request,pk):
    # parent_list = [
    # ["category 1", "category 2", "category 3"],
    # ["category 1", "category 3"],
    # ["category 1"],
    # ["category 1"]
    # ]
    # parent_list = [
    # ["Triangle", "Equilateral", "Circle","Cone"],
    # ["Circle", "Triangle", "Equilateral"],
    # ["Circle"]
    # ]
    # student = models.Student.objects.get(user_id=request.user.id)
    # result= QMODEL.Result.objects.filter(student=student)
    # print("RESULT QUERY SET",result)
    # print("RESULT FROM DATABASE: ",result.last().parent_list)
    print("IN RESUKT VIEEW")
    # parent_list= request.session.get('parent_list', [])
    # # print(parent_list)
    # final_course_ids = [[QMODEL.Course.objects.get(id=course_id) for course_id in course_ids] for course_ids in parent_list]
    # print(final_course_ids)
    # parent_list=final_course_ids
    # print("NEW PARENT LIST",parent_list)(
    result=QMODEL.Result.objects.get(id=pk)
    parent_list=result.parent_list
    num_levels = len(parent_list)
    if(num_levels==0):
        return render(request, 'student/no_result.html')

    num_categories = len(parent_list[0])

#   Changing course ids to course names
    resultant_list = []
    for child_list in parent_list:
        course_names = []
        for course_id in child_list:
            course = QMODEL.Course.objects.get(id=course_id)
            course_names.append(course.course_name)
        resultant_list.append(course_names)
    print(parent_list)
    print(resultant_list)

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
    
    # return render(request, 'student/result.html', {'feedback': feedback, 'comments': comments,'courses':parent_list})
    return render(request, 'student/result.html', {'feedback': feedback, 'comments': comments,'courses':resultant_list})
    

# @login_required(login_url='studentlogin')
# @user_passes_test(is_student)
# def check_marks_view(request,pk):
#     course=QMODEL.Course.objects.get(id=pk)
#     student = models.Student.objects.get(user_id=request.user.id)
#     results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
#     return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_result(request):
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.filter(student=student)
    print("RESULT QUERY SET",results)
    return render(request,'student/check_result.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})