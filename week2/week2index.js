/*Q1*/ 
function findAndPrint(messages, currentStation) { // 要放參數，比較 "目前站"跟 "朋友所在站"
                                                  /* @@參數沒寫messages物件，則let friend in messages為undefined
                                                     @@參數沒寫currentStation字串，則const currentStationIndex = stations.indexOf(currentStation); 返回-1*/
                                                 /*參數位置: 非絕對,看慣例 如:一般性、頻繁使用者 優先*/
    let minDistance = Infinity;   //初始值Infinity:可直接用於數學運算。 //確保後續計算的距離 < 初始值
    let closestFriend = null;    // 因未知狀態

    const currentStationIndex = stations.indexOf(currentStation); //儲存索引值，後續計算站間距離
                                                                  /* @@寫for迴圈之前的外部，因只找一次*/

    for (let friend in messages) {    /*遍歷: 每次迴圈迭代中，變數station值改變為 messages物件的一個新屬性
                                              新變數friend 儲值 為當輪屬性(友名)*/
        let friendStation = extractStation(messages[friend]);  /*呼叫輔助函式，把特定友名的對應值 傳入 來過濾出站名
                                                            如:friend 變數值為"Bob"，傳入輔函參數為"I'm at Ximen MRT station."
                                                               執行輔函參數 返回值Ximen 並賦值給新變數*/
        if (friendStation === null) {
            continue;
        }

        let friendStationIndex = stations.indexOf(friendStation);

        // 支線例外判斷&處理
        if (currentStationIndex === stations.indexOf("Qizhang") && friendStation === "Xiaobitan") {
            closestFriend = friend;  // 滿足此條件(目前位置為唯一達支線的主站) ，友站直接賦值 在支線站的友名。
            break;                   //毋庸遍歷它友
        }
        if (currentStationIndex === stations.indexOf("Xindian City Hall") && friendStation === "Xiaobitan") {
            continue;                //滿足此條件，跳過支線站的友名(因設定站名有順序，先跑回能達支線的唯一主站 再到支線)  繼續遍歷它友名
        }

        let distance = Math.abs(currentStationIndex - friendStationIndex); // Math.abs 函數  取得差值的絕對值
        if (distance < minDistance) {  //當計算結果 為最近，則一起更新變數的值 (否則仍為初始值)
            minDistance = distance;
            closestFriend = friend;
        }
    }
    console.log(closestFriend);
}
function extractStation(message) {
    for (let station of stations) {   //變數station : 每輪迴圈中，stations 陣列中 當前遍歷的元素
        if (message.includes(station)) {  
            return station; 
        }                            /*  過濾參數中資料 ，若含符合陣列元素值的資料(x逕寫陣列名，變成檢查包含整個陣列) 
                                         返回            "被賦要找值 的變數station"(x返回字串) */ 
    }
    return null;                      // 遍歷全部都無，才返回  未知/空值
                                     /* @@勿寫for迴圈內部，否則 一找到不含就停 、漏後續仍包含的資料*/
}
const stations = [
    "Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", 
    "Songjiang Nanjing", "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", 
    "Chiang Kai-shek Memorial Hall", "Guting", "Taipower Building", 
    "Gongguan", "Wanlong", "Jingmei", "Dapinglin", "Qizhang", 
    "Xiaobitan", "Xindian City Hall", "Xindian"
];
const messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
};
findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian

/*Q2*/ 
function book(consultants, hour, duration, criteria) { //@@consultants物件作為參數，特性為傳址--值變會被保存 
    for (let consultant of consultants) {  // 變數consultant :每次迴圈中，在consultants物件中 當前遍歷的元素
        if (!consultant.schedule) {       
            consultant.schedule = new Array(24).fill(true); // 
        }  
    } /* 若 該元素不存在schedule屬性，就在原陣列 新增此屬性 且值為 有24個true 的陣列  
                                    出現 "schedule": [true, true, true, ..., true]},*/
    let availableConsultants = consultants.filter(consultant => {
        for (let i = hour; i < hour + duration; i++) {
            if (!consultant.schedule[i]) {
                return false;
            }
        }
        return true;
    });
       /* 過濾產出新陣列+不影原始陣列 : 每次迴圈都檢查 從 hour 開始、持續 duration 個小時的每小時，若其值false 就返回false
          新陣列 值隨傳入的hour+duration而改變*/

    // 優先處理無法預約情形，中斷跑程式
    if (availableConsultants.length === 0) {
        console.log("No Service");
        return;
    }

    // 從多個可預約者 篩選出唯一最能符條件者
    if (criteria === "price") {
        availableConsultants.sort((a, b) => a.price - b.price);
    } else if (criteria === "rate") {
        availableConsultants.sort((a, b) => b.rate - a.rate);
    }
    let chosenConsultant = availableConsultants[0];

    // 更新 被預約特定時段的顧問 屬性值
    for (let i = hour; i < hour + duration; i++) {
        chosenConsultant.schedule[i] = false;  //@@因傳址，連帶修改原陣列對應屬性的值
    }

    console.log(chosenConsultant.name);
}
const consultants=[
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
];
book(consultants, 15, 1, "price"); // Jenny
book(consultants, 11, 2, "price"); // Jenny
book(consultants, 10, 2, "price"); // John
book(consultants, 20, 2, "rate"); // John
book(consultants, 11, 1, "rate"); // Bob
book(consultants, 11, 2, "rate"); // No Service
book(consultants, 14, 3, "price"); // John

/*Q3*/ 
function func(...data){         // 參數寫...data，讓所有參數傳入同一陣列
    let middleNames = {};       // 空物件 賦值給全域變數 ，確保值可變動

    for(let name of data){
        let middleName= null;  //@@每輪迴圈都是一個新的局部變數 
        if(name.length === 2 || name.length === 3){
            middleName = name[1];
        } else if(name.length === 4 || name.length === 5){
            middleName = name[2];
        } else {
            continue;
        }
        // @@賦值&更新{  }的key:value ，value更新規則為 計算出現次數，已出現則遞增、首次設為1
        if(middleNames[middleName]){
            middleNames[middleName]++;
        } else {
            middleNames[middleName] = 1;
        }
    }

    let uniqueMiddleNames = [ ];
    for(let middleName in middleNames){
        if(middleNames[middleName] === 1){
            uniqueMiddleNames.push(middleName);
        }
    }

    if(uniqueMiddleNames.length === 0){
        console.log("沒有");
    } else {
        for(let name of data){   //@@重新遍歷，才知獨特/出現一次的中間字 對應的完整姓名
            if((name.length === 2 || name.length === 3) && uniqueMiddleNames.includes(name[1])){
                console.log(name);
            } else if((name.length === 4 || name.length === 5) && uniqueMiddleNames.includes(name[2])){
                console.log(name);
            }
        }
    }
}
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安
    
/*Q4*/ 
function getNumber(index) {  
     /* 規律:+4+4-1 ，@@三個數字為一組(非四個，因規律指前組首數字~下組首數字)
        先找出 哪組(除以3) 的 第幾個(餘數) ，再計算數字多少 (每組首數字為7倍數，包含0也是任何它以外的倍數!)*/ 
    let group = Math.floor(index / 3); 
    
    let position = index % 3;
    let base = group * 7;
    
    let result= null;
    if (position === 0) {
        result = base;
    } else if (position === 1) {
        result = base + 4;
    } else {
        result = base + 4 + 4;
    }
    console.log(result); 
    return result;  
}
getNumber(1); // print 4
getNumber(5); // print 15
getNumber(10); // print 25
getNumber(30); // print 70