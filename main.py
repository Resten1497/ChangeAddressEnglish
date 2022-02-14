import urllib.parse

import requests
import pyproj
import json
from urllib import parse

searchEnglishAddress = "https://www.juso.go.kr/addrlink/addrEngApi.do"
searchEnglishAddressKey = "devU01TX0FVVEgyMDIyMDIxNDE1MDUzNTExMjI0MjA="
searchEnglishAddressParam = {"confmKey": searchEnglishAddressKey,
                             "keyword": "",
                             "resultType": "json"
                             }

searchPositionAddress = "https://www.juso.go.kr/addrlink/addrCoordApi.do"
searchPositionAddressKey = "devU01TX0FVVEgyMDIyMDIxNDE1MDYzNjExMjI0MjE="
searchPositionAddressParam = {
    "confmKey": searchPositionAddressKey,
    "resultType": "json",
    "admCd": "",
    "rnMgtSn": "",
    "udrtYn": "",
    "buldMnnm": "",
    "buldSlno": "",

}


def main():
    enAddressResult = requestEnAddress(setEnAddress())
    print(requestEnAddress(setPositionAddress(enAddressResult)))


def setEnAddress():
    searchEnglishAddressParam['keyword'] = '강원 춘천시 공지로 353'
    parameter = urllib.parse.urlencode(searchEnglishAddressParam)
    # query = parse.parse_qs(url.query)
    return searchEnglishAddress + "?" + parameter


def requestEnAddress(url):
    print(url)
    res = requests.get(url)
    json_object = json.loads(res.text)
    return json_object


def setPositionAddress(item):
    #print(item['results']['juso'][0]['admCd'])
    for i in searchPositionAddressParam:
        if i != "confmKey" and i != "resultType":
            searchPositionAddressParam[i] = item['results']['juso'][0][i]
    parameter = urllib.parse.urlencode(searchPositionAddressParam)
    return searchPositionAddress + "?" + parameter





if __name__ == '__main__':
    main()
