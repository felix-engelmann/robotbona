from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from urllib.parse import parse_qs

from urllib import request as rq


import json

# Create your views here.

@csrf_exempt
def getToken(request):
    if request.method == 'POST':
        print(request.body)

        #req = rq.Request("http://47.91.67.181/baole-web/common/getToken.do", data = request.body,
        #                 headers={"Content - Type": "application/x-www-form-urlencoded; charset=utf-8",
        #                            'Accept': '*/*'}
        #)  # this will make the method "POST"
        #resp = rq.urlopen(req)
        #token = resp.read()

        #cookie=resp.getheader("Set-Cookie")


        #print(token)
        #data = json.loads(token)
        #rcv = json.loads(request.body)
        #print(data)
        response = JsonResponse({"msg":"ok",
                                    "result":"0",
                                    "data":{"appKey":"67ce4fabe562405d9492cad9097e09bf",
                                         "deviceNo":"3230aea4433f1c",
                                            "token":"1oe13ie0X8ST3L0FO844426484884489"},
                                        "version":"1.0.0"})
        #response.set_cookie("SERVERID", "2423aa26fbdf3112bc4aa0453e825ac8|1549668141|1549668141")
        response["Content-Type"] = "application/json;charset=UTF-8"
        #response["Set-Cookie"] = cookie
        return response

    pass
