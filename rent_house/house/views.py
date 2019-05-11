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
    return render(request, "house/index.html")


def register(request):
    return render(request, "house/reg.html")


def login(request):
    return render(request, "house/login.html")


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
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = User(username=username, password=password)
        user.save()

    return render(request, "house/login.html")


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')

        print(username)
        print(password)

    return render(request, "index.html")


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
    return render(request, "house/pro.html", {"page": page, "all_hits": hit_list, "key_words": key_words, "total_nums": total_nums, "page_nums": page_nums})

