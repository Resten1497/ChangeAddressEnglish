import urllib.parse

import requests
from pyproj import Proj, Transformer
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
    "admCd": "",
    "rnMgtSn": "",
    "udrtYn": "",
    "buldMnnm": "",
    "buldSlno": "",
}


def main():
    address = input()
    enAddressResult = requestAPI(setEnAddress(address))
    positionResult = requestAPI(setPositionAddress(enAddressResult))
    if positionResult is not None :
        print(positionResult['results']['juso'][0]['entX'], positionResult['results']['juso'][0]['entY'])
        print(project_array())

def setEnAddress(address):
    searchEnglishAddressParam['keyword'] = address
    parameter = urllib.parse.urlencode(searchEnglishAddressParam)
    # query = parse.parse_qs(url.query)
    return searchEnglishAddress + "?" + parameter


def requestAPI(url):
    res = requests.get(url)
    json_object = json.loads(res.text)
    return json_object


def setPositionAddress(item):
    #print(item['results']['juso'][0]['admCd'])
    if len(item['results']['juso']) > 1:
        for i in searchPositionAddressParam:
            searchPositionAddressParam[i] = item['results']['juso'][0][i]
        searchPositionAddressParam['confmKey'] = searchPositionAddressKey
        searchPositionAddressParam['resultType'] = 'json'
        print(searchPositionAddressParam)

        parameter = urllib.parse.urlencode(searchPositionAddressParam)

        return searchPositionAddress + "?" + parameter

    return None


def project_array( ):

    transformer = Transformer.from_crs("epsg:5179","epsg:4326")
    result = transformer.transform('1985581.651174346', '1019968.41192052')

    print(result[0],result[1])


if __name__ == '__main__':
    main()
