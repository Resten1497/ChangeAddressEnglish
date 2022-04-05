import time
import urllib.parse

import requests
from openpyxl import load_workbook
from pyproj import Proj, Transformer
import json
import openpyxl
import pymysql
from urllib import parse
db = pymysql.connect(user='root', passwd='sa720315', host='127.0.0.1', db='awesome_beer',  charset='utf8')
cursor = db.cursor()


searchEnglishAddress = "https://www.juso.go.kr/addrlink/addrEngApi.do"
searchEnglishAddressKey = "devU01TX0FVVEgyMDIyMDMwODE3MDkyODExMjMyNTI="
searchEnglishAddressParam = {"confmKey": searchEnglishAddressKey,
                             "keyword": "",
                             "resultType": "json"
                             }
searchPositionAddress = "https://www.juso.go.kr/addrlink/addrCoordApi.do"
searchPositionAddressParam = {
    "admCd": "",
    "rnMgtSn": "",
    "udrtYn": "",
    "buldMnnm": "",
    "buldSlno": "",
}

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
    searchPositionAddressKey = "devU01TX0FVVEgyMDIyMDMwODE3MTQzMjExMjMyNTM="
    if len(item['results']['juso']) >= 1:
        searchPositionAddressParam = {
            "admCd": "",
            "rnMgtSn": "",
            "udrtYn": "",
            "buldMnnm": "",
            "buldSlno": "",
        }
        for i in searchPositionAddressParam:

            searchPositionAddressParam[i] = item['results']['juso'][0][i]
        searchPositionAddressParam['confmKey'] = searchPositionAddressKey
        searchPositionAddressParam['resultType'] = 'json'
        parameter = urllib.parse.urlencode(searchPositionAddressParam)

        return searchPositionAddress + "?" + parameter

    return None
def project_array(x,y):

    transformer = Transformer.from_crs("epsg:5179","epsg:4326")
    result = transformer.transform(y, x)

    return result[1],result[0]

def main():
    sql = "SELECT idx,address, x, y FROM awesome_beer.tb_beer where x is null;"
    update_sql = "UPDATE awesome_beer.tb_beer SET x=%s, y=%s where idx = %s;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for i in rows :
        enAddressResult = requestAPI(setEnAddress(i[1]))
        #print(i[1])
        #print(enAddressResult)
        if enAddressResult['results']['common']['totalCount'] != '0':
            positionResult = requestAPI(setPositionAddress(enAddressResult))
            if positionResult is not None:
                # print(positionResult['results']['juso'][0]['entX'], positionResult['results']['juso'][0]['entY'])
                x,y = project_array(positionResult['results']['juso'][0]['entX'], positionResult['results']['juso'][0]['entY'])
                cursor.execute(update_sql,(x,y,i[0]))
                db.commit()
                print(x,y)
        else:
            print(enAddressResult['results']['common']['totalCount'])
        time.sleep(0.3)


    # load_wb = load_workbook("data.xlsx", data_only=True)
    # load_ws = load_wb['Sheet1']
    # for i in load_ws['A']:
    #     enAddressResult = requestAPI(setEnAddress(i.value))
    #     if enAddressResult['results']['common']['totalCount'] == '1':
    #         positionResult = requestAPI(setPositionAddress(enAddressResult))
    #         if positionResult is not None:
    #             # print(positionResult['results']['juso'][0]['entX'], positionResult['results']['juso'][0]['entY'])
    #             project_array(positionResult['results']['juso'][0]['entX'], positionResult['results']['juso'][0]['entY'])
    #     else:
    #         print("None")
    #     time.sleep(0.3)


if __name__ == '__main__':
    main()
