from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mole.models import Question
# Create your views here.
def index(request):

    if request.method == 'POST':
        print(request.POST)
        questions=Question.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'result.html',context)
    else:
        questions=Question.objects.all()
        page_num = request.GET.get('page', 1)

        paginator = Paginator(questions, 1) # 6 employees per page


        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        context = {
            'quest':questions,
            'page_obj':page_obj
        }

        return render(request,'questions.html',context)

