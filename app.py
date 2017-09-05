# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

   
    res = processRequest(req)    
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "SearchProductInTarget":
        return {}
    responseT = makeTargetQuery(req)
    if responseT is None:
        return {}
    res = makeWebhookResult(responseT)
    return res

#import requests
from collections import defaultdict
import json 

def SearchAPICaller(search_string):
    base_url = "http://10.63.77.129/v1/target/select?authKey=0a81a798b7fea7908b14cff9d95eaa75&q=%s&rows=10"    
    url=base_url % search_string
    #resp = requests.get(url).json()
    resp1=urlopen(url).read()
    #encoding = webURL.info().get_content_charset('utf-8')
    
    resp=json.loads(resp1.decode("utf-8"))
    returnVal=defaultdict(dict)
    for x in range (0,9):
        returnVal["sku"][x]=resp['response']['docs'][x]['sku'] 
        returnVal['desc'][x]=resp['response']['docs'][x]['NAME']
        #returnVal['image'][x] = resp['response']['docs'][x]['IMGURL']   
    return json.dumps(returnVal)
    
def makeTargetQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    things = parameters.get("Things")
    search_string=things    
    return SearchAPICaller(search_string)


def makeWebhookResult(data):
    data1=json.loads(data)
    speech = "Hey, I am confused, did you buy " + data1["sku"]['0'] +" or "+ data1["sku"]['1']   
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-TargetSearch-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
