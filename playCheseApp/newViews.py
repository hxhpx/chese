import operator
from urllib import response
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import numpy as np

from .models import History

@require_http_methods(["GET"])
#将某一局游戏保存到数据库
def keep(request):
    response = {}
    try:
        n = request.GET.get('name')
        s = int(request.GET.get('size'))
        l = request.GET.get('list')
        c = int(request.GET.get('stepCnt'))

        history = History(name=n, size=s, list=l, stepCnt=c)
        history.save()

        response['error_num'] = 0
    except Exception as e:
        response['error_num'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)


#从数据库获取所有棋局信息
def getID(request):
    response={}
    try:
        history = History.objects.filter()
        allList = json.loads(serializers.serialize("json", history))

        response['allList'] = []
        for i in range(len(allList)):
            dic = {}
            dic['id'] = allList[i]['pk']
            dic['name'] = allList[i]['fields']['name']
            dic['time'] = str(allList[i]['fields']['time']).split('.')[0]
            response['allList'].append(dic)

        print(response['allList'])
        response['error_num'] = 0
    except Exception as e:
        response['error_num'] = 1
        response['msg'] = str(e)
        print(str(e))
    return JsonResponse(response)

#回放选定的棋局
def review(request):
    response = {}
    try:
        idx = int(request.GET.get('id').split()[0])
        history = History.objects.filter(pk=idx)
        lst = json.loads(serializers.serialize("json", history))
        print(lst[0])

        response['size'] = lst[0]['fields']['size']
        response['stepCnt'] = lst[0]['fields']['stepCnt']
        response['list'] = lst[0]['fields']['list']
        response['error_num'] = 0
    except Exception as e:
        response['error_num'] = 1
        response['msg'] = str(e)
        print(str(e))
    return JsonResponse(response)

#搞定排行榜
def board(request):
    response = {}
    try:
        filter = History.objects.filter()
        allHis = json.loads(serializers.serialize("json", filter))
        all = []

        for i in range(len(allHis)):
            cur = {}
            cur['id'] = allHis[i]['pk']
            cur['name'] = allHis[i]['fields']['name']
            cur['size'] = allHis[i]['fields']['size']
            cur['time'] = allHis[i]['fields']['time']
            left = int(cur['size']) * int(cur['size']) - allHis[i]['fields']['stepCnt'] - 2
            cur['left'] = left
            all.append(cur)

        all2 = sorted(all, key=operator.itemgetter('size'))
        all3 = sorted(all2, key=operator.itemgetter('left'))
        for i in range(len(all3)):
            all3[i]['position'] = i+1

        response['board'] = all3
        print(response['board'])
        response['error_num'] = 0

    except Exception as e:
        response['error_num'] = 1
        response['msg'] = str(e)

    return JsonResponse(response)

'''
def keepTest(request):
    response = {}
    try:
        list = request.GET.get('list')
        c = int(request.GET.get('stepCnt'))

        print("list:   ",list)
        response['error_num'] = 0
        response['stepCnt'] = c
        response['msg'] = list
    except Exception as e:
        response['error_num'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)
'''