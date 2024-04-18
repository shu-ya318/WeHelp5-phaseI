#S零、載入 所有模組
import urllib.request as request
import json 
import csv
# S一、網路資料 (一)下載+(二)解析--JSON格式
URL1="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
URL2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
with request.urlopen(URL1) as response:
    data1 = json.loads(response.read())
with request.urlopen(URL2) as response:
    data2 = json.loads(response.read())
      
#處理spot.csv檔案    
    # S二、各自解析/取得 並整理成 指定的一個整體資料
    #(一)初始化
spotData = { }     #不用[ ] ，{ }快速比對相同鍵值對
    #(二)更新值 為整理後指定資料 
    #(之1)遍歷data1特定鍵值對，每次都 整理成 1個鍵SERIAL_NO : 值為1個列表[stitle,longitude,latitude,filelist首URL]
                                                      #值放列表，因需順序性
for spot in data1['data']['results']:  
    spotData[spot['SERIAL_NO']] = [  
        spot['stitle'],
        spot['longitude'],
        spot['latitude'],
        'https://' + spot['filelist'].split('https://')[1]  #分割後，開頭加回https://    
        ]    
    #(之2)遍歷data2，條件語句: 若 比對spotData有 同鍵&值者，就操作(V): 取得data特定值，加入spotData指定序位
for spot in data2['data']:  
    if spot['SERIAL_NO'] in spotData:
        spotData[spot['SERIAL_NO']].insert(1, spot['address'][5:8])  #列表方法insert #第2位[索引1] #切片方法: 字串[取出首索引值 含:尾索引值 不含]    

    # S三、資料 轉成整理好的CSV檔
    #(一)寫入/新增
with open('spot.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #csv.writer() 函數  用,隔開 且會換行
    writer = csv.writer(csvfile)   
    # writerow() 寫入單筆資料 --適用產生 一個標題欄 
    writer.writerow(['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL'])
    # 字典:items() 方法 ，回傳鍵&值  #遍歷，用變數key、變數value來分別儲存 取得每輪資料
    for key, value in spotData.items():
        #只顯示寫入 value 意即spotData的列表值 內含5個元素
        writer.writerow(value)


