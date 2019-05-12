from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from house.models import User
from house.models import House
from elasticsearch import Elasticsearch

import json
import time

es_client = Elasticsearch(hosts=["localhost"])
todate = time.strftime('%Y.%m.%d', time.localtime(time.time()))
#index_name = 'house_' + todate
index_name = 'house_2019.05.09'

def index(request):
    #return HttpResponse("Hello, you're at the house index.")
    is_login = False
    if request.session.get("username"):
        is_login = True
    print("session:", request.session.get("username"))
    return render(request, "house/index.html", {"is_login": is_login, "username": request.session.get("username")})


def register(request):
    return render(request, "house/reg.html")


def login(request):
    return render(request, "house/login.html")


def logout(request):
    try:
        del request.session["username"]
    except KeyError:
        pass
    return render(request, "house/index.html")


def user(request):
    return render(request, "house/user.html")


def house(request):
    return render(request, "house/pro.html")


def detail(request):
    return render(request, "house/proinfo.html")


def ranking(request):
    return render(request, "house/pro_ranking.html")


def new(request):
    return render(request, "house/pro_new.html")


def reg_user(request):
    info = {"code": 200}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        res = User.objects.filter(username=username)
        
        if res:
            info["status"] = False
            info["msg"] = "该用户名已被注册,请更换用户名后重试"
        else:
            user = User(username=username, password=password)
            user.save()
            info["status"] = True
            info["msg"] = "success"
    
    return HttpResponse(json.dumps(info))


def login_user(request):
    info = {"code": 200}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')

        res = User.objects.filter(username=username)
        if not res:
            info["status"] = False
            info["msg"] = "该用户不存在,请检查后重新登录"
        elif password == res[0].password:
            info["status"] = True
            info["msg"] = "success"

            request.session["username"] = res[0].username
        else:
            info["status"] = False
            info["msg"] = "密码不正确,请检查后重新登录"
        print(info)
    return HttpResponse(json.dumps(info))


def search_suggest(request):
    key_words = request.GET.get('s', '')
    re_datas = []
    if key_words:
        s = House.search()
        s = s.suggest('my_suggest', key_words, completion={
            "field": "region_suggest", 
            "fuzzy": {
                "fuzziness": 2
            },
            "size": 8
        })
        res = s.execute()
        for match in res.suggest.my_suggest[0].options:
            source = match._source
            re_datas.append(source["region"])
        print(re_datas)
    return HttpResponse(json.dumps(re_datas), content_type="application/json")


def house_search(request):
    key_words = request.GET.get("q", "")
    page = request.GET.get("p", "1")
    try:
        page = int(page)
    except:
        page = 1
    if key_words == "":
	    res = es_client.search(
		    index=index_name,
			body={
			    "query": {
				    "match_all":{}
				},
				"from": (page-1)*10,
				"size": 10
			}
		)
    else:
        res = es_client.search(
			index=index_name,
			body={
				"query": {
					"multi_match":{
						"query": key_words,
						"fields": ["title", "region"]
					}
				},
				"from": (page-1)*10,
				"size": 10
			}
		)
    total_nums = res["hits"]["total"]
    if page % 10 > 0:
        page_nums = int(total_nums/10) + 1
    else:
        page_nums = int(total_nums/10)
    hit_list = []
    for hit in res["hits"]["hits"]:
        hit_dict = {}
        hit_dict["title"] = hit["_source"]["title"]
        hit_dict["detail"] = hit["_source"]["detail"]
        hit_dict["region"] = hit["_source"]["region"]
        hit_dict["price"] = hit["_source"]["price"]
        hit_dict["scale"] = hit["_source"]["scale"]
        hit_dict["direction"] = hit["_source"]["direction"]
        hit_dict["floor"] = hit["_source"]["floor"]
        hit_dict["pubdate"] = hit["_source"]["pubdate"]
        hit_dict["picture"] = hit["_source"]["picture"]
        hit_dict["source"] = hit["_source"]["source"]
        hit_dict["id"] = hit["_id"]
        
        hit_list.append(hit_dict)
    print(hit_list)
    print(key_words)
    is_login = False
    if request.session.get("username"):
        is_login = True
    print("session:", request.session.get("username"))
    return render(request, "house/pro.html", {"is_login":is_login, "username": request.session.get("username"), "page": page, "all_hits": hit_list, "key_words": key_words, "total_nums": total_nums, "page_nums": page_nums})

