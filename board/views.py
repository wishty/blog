from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("안녕하세요, 게시판 페이지에 오신 것을 환영합니다. ^^")

# def index(request):
#     return render(
#         request,
#         'board/index.html'
#     )

