import urllib.request as request
import json 
import csv
URL1="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
URL2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with request.urlopen(URL1) as response:
    data1 = json.loads(response.read())
with request.urlopen(URL2) as response:
    data2 = json.loads(response.read())
    
#處理mrt.csv檔案 
    #(一)取出只需要的資料 &整理
mrtData = { }
for spot in data1['data']['results']:  
    mrtData[spot['SERIAL_NO']] = [                  
        spot['stitle']   
    ]                          
for spot in data2['data']:  
    if spot['SERIAL_NO'] in mrtData:
	    mrtData[spot['SERIAL_NO']].insert(0,spot['MRT']) 
       
    #(二) 對相同MRT值的元素，重整資料  
groupedData = {}
#@好難想@  遍歷的主體:  只抓值['MRT','stitle'] ，因鍵SERIAL_NO沒使用
           #思考新{ }  為 { 鍵 放同MRT名1 : 值放 同MRT名1 , 同MRT名的元素1的stitle值, 同MRT名的元素2的stitle值... }
                    #取值寫values[0]或values[1]
                    #拆成 { 鍵 放同MRT名1 : 值放 同MRT名1 } 跟   值第2個元素起 如何讓同MRT名的元素們的stitle值 依序自動塞入同鍵?
                      ##X~x 每輪value[0]不一定要放(因會重複) ，但value[1]必放
                      ##每輪利用條件式 檢查['MRT','stitle']，#第1種結果-MRT名還沒出現，在指定位置塞入該元素的值'MRT','stitle'  
                                                           #第2種結果-MRT名已出現(重複)，只 在指定位置塞入該元素的'stitle'
for values in mrtData.values():
    mrt = values[0]
    if mrt not in groupedData:
        groupedData[mrt] = [mrt]
    groupedData[mrt].extend(values[1:])
#改形式，列表中所有元素以,和空格連接成一個字串  #如  "新北投": ["新北投", "新北投溫泉區", "北投圖書館"] 變成 新北投, 新北投溫泉區, 北投圖書館
for values in groupedData.values():
    print(', '.join(values))


with open('mrt.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['MRTStation', 'SpotTitles'])
    for values in groupedData.values():
        writer.writerow(values)
