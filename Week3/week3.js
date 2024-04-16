document.addEventListener("DOMContentLoaded", function() {
/*
處理 無使用資料的純頁面效果
*/ 
let menuHamburger = document.getElementById("menu-hamburger");
let menuClose = document.getElementById("menu-close");
let popupMenu = document.getElementById("popup-menu-mobile");

menuHamburger.onclick = function(event) {
    menuHamburger.style.display = "none"; 
    menuClose.style.display = "flex";
    popupMenu.style.display = "flex";
} 
menuClose.onclick = function(event) {
    menuClose.style.display = "none";
    menuHamburger.style.display = "flex"; 
    popupMenu.style.display = "none";
}
/*
處理 用到json資料的內容
*/
let touristSpots ={ };   // 全域變數 ，預備給不同函式均可使用
/*函式主體為非同步 ，但內部運作卻是同步執行
  async function: 定義非同步函式。
  利用await讓 async非同步函式內部有"同步效果"             - 因awiat會暫停async函式執行，後行所有code要等待前行的promise回傳完成 才繼續執行
          但  async非同步函式以外的函式們 保持"非同步效果" -毋庸等待async執行完成
  寫法:
  成功狀態 : try內部 用await來等待 Promise (非同步操作)完成  *多個promise就多個awiat
                    promise均完成，才往下執行後續code。 如: 賦值給變數、宣告多個變數、定義&呼叫多個函式*/
async function fetchData() {  
    try {  
          /* 1-1. fetch :發送一個 HTTP 請求到指定 URL，返回一個 Response 物件(data、status、header等屬性)
             1-2. 從 Response 物件中，只取得data實際資料 ( .json 取得JSON檔 .text()純字檔 .blob()圖或PDF檔)
          */                     
        const response = await fetch("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1");
        const data = await response.json();
        touristSpots = data;
        /*取得指定資料*/
        /*連接頁面:DOM，內部動態增加多元素   @@ 依html序來增加 、css樣式效果 :待元素出現,自動套用設定*/
        const SmallBoxes = document.querySelectorAll(".m-wrapper-smallbox");
        const BigBoxes = document.querySelector(".m-grid-bigboxes");
        const loadMoreBtn = document.getElementById("load-more");

        /*放首行，1.所有操作只用到 單抓出 物件的一個整體的子陣列*/
        let spotsResults = touristSpots.data.results;

        /*過濾  元素ㄟ圖片的值 (限定某張)  */
        /*＠＠取出filelis的值(限定某張圖)?2.array方法取出子物件元素ㄟ屬性值 (+放內部的操作敘述  搭配其它方法 ++該方法善後加工 成想要的值)                                     
                                    (2-1)取出值為一堆字串: 用字串的split方法----特性:分割後裝一個整體陣列  
                                    (2-2-a對特性善後) 因指定'https://' 隔開，若開頭就有 首元素被切成空值 →移除首元素 
                                    (2-2-b對特性善後) @@因指定'https://' 隔開，手動加回被省略的分割單位  →對[特定索引]值  操作 用+運算合併字串
                                    ps若要回傳  一個元素中該值 內部再分開所有URL ，則用flatMap( )
        */
        //所有元素 
        let firstUrls = spotsResults.map(item => {                   
        let filelistSplit = item.filelist.split('https://');
        if (filelistSplit[0] === '') {
            filelistSplit.shift();
        }
        return 'https://' + filelistSplit[0];
        });
        //部分元素 (小 + 大的立即10個 + 大的觸發事件剩下個) //slice省第2參數=取到尾個
        let SmallBoxesUrls = firstUrls.slice(0, 3);                
        let BigBoxesUrls = firstUrls.slice(3);

        /*過濾  元素ㄟ標題的值   2.array方法取出子物件元素ㄟ屬性＂值＂*/
            //所有元素
        let spotsTitles = spotsResults.map(item => item.stitle);
            //[當沒先取得所有元素值] 只處理部分元素 ，2-2.+ CHAIN其它array方法   (序: 先濾出 部分指定位置元素 再操作取值)
        let SmallBoxesSpotTitles = spotsResults.slice(0, 3).map(item => item.stitle);
        let BigBoxesSpotTitles = spotsResults.slice(3).map(item => item.stitle);

        /*取得資料後，渲染到頁面*/
        //指定不可以寫item.innerHTML = SmallBoxesSpotTitles[index] ;
        /*@@ DOM節點 動態增加 ----想樹狀圖 
            @@變數存DOM父節點.appendChild(變數儲新建元素) 把  參數指定的 子節點，附加到 父容器節點的末端   @@一層層加，確保套用到css樣式
            序: 處理完一個元素全部設定 ，再處理下個元素
            (一)圖片  1.新增<img>元素 - 2.動態設定所有屬性 -3.附加進父元素
            (二)字1-1.增加 新元素<p></p>       (@@刪既有<p class="m-text-smallbox">元素，避免p元素內又包p元素)---
                1-2.增加 新文字節點        :文字為"[索引]地點" 
                2.文字節點 附加進<p>
                3.<p>元素有文字內容後，再動態設定屬性
                3.最後才附加 完整子元素  進大的父元素*/
        function renderSmallBoxesTitles(){
        SmallBoxes.forEach((item, index) => {  
            //圖
            let imgElement = document.createElement("img");
            imgElement.setAttribute("src",SmallBoxesUrls[index]);    
            imgElement.setAttribute("class","m-image-smallbox-small");
            imgElement.setAttribute("alt","spotImg");
            imgElement.setAttribute("width","80px");
            item.appendChild(imgElement);
            //字
            let pElement = document.createElement("p");
            let textNode = document.createTextNode(SmallBoxesSpotTitles[index]);
            pElement.appendChild(textNode);
            pElement.setAttribute("class","m-text-smallbox");
            item.appendChild(pElement);
        });
        }
        renderSmallBoxesTitles();
    /* @A@函式執行原理同，僅取得個數資料異 =  通用寫法(如 更改迴圈的i) ，呼叫時傳入 可變動的指定參數
                                           留意 +變數的停止條件，否則無限增生*/ 
        function renderBigBoxes(startIndex){
        for (let i = startIndex; i < startIndex + 10; i++){  
             //@@ 防止big box 生出無法取得會變動資料的元素 (否則無限滾動，多出的在頁面顯示undefined)
            if (i >= BigBoxesUrls.length || i >= BigBoxesSpotTitles.length) {
                break;  //比用return全部中斷好
              }
            //先動態生出 大的  每個Big Box <div>元素,含屬性&值  (@@勿逕附加最大祖父元素,否則<div>元素無法再調整，致內部無法再加子元素)
            let BigBoxDiv = document.createElement("div");
            BigBoxDiv.setAttribute("class","m-wrapper-bigbox");
            BigBoxDiv.style.backgroundImage = `url("${BigBoxesUrls[i]}")`;  
            /* @@特別改變 每第9、10個的big box 在RWD的CSS樣式改變 (利用條件式 動態增加不同裝置的class名)
              為它者兩倍大 (因為只在中等裝置套用，多增加專屬class) */
            if ((i - startIndex) % 10 === 8 || (i - startIndex) % 10 === 9) {
                BigBoxDiv.classList.add("m-flatColumn-bigbox");
                BigBoxDiv.classList.add("m-mobileColumn-bigbox");
              }
            //再生出<div>的子元素icon <外載> ，不再調整 就附加
            let BigBoxIcon = document.createElement("i");
            BigBoxIcon.setAttribute("class", "m-image-bigbox fa-solid fa-star");
            BigBoxIcon.style.color = "rgb(12, 226, 246)";
            BigBoxDiv.appendChild(BigBoxIcon);
            //再生出<div>的子元素字 <p>，不再調整 就附加
            let BigBoxTitle = document.createElement("p");
            BigBoxTitle.setAttribute("class", "m-text-bigbox");
            BigBoxTitle.textContent = `${BigBoxesSpotTitles[i]}`;
            BigBoxDiv.appendChild(BigBoxTitle);
            //全部完整，才附加
            BigBoxes.appendChild(BigBoxDiv);
        }                
        }
        // 頁載完時,沒觸發事件 就跑 原始陣列第4~尾個元素(新陣列第1~尾個元素)
        renderBigBoxes(0);  
        // 觸發點擊事件，改變顯示的資料索引值
            //BigBoxes Urls跟SpotTitles[i]要排除已顯示[0~9]的十個
        let currentIndex = 10;     
            //函式外部設完初始值 ，再開始每次的執行操作 
        loadMoreBtn.addEventListener("click", function() {
            renderBigBoxes(currentIndex);
            currentIndex += 10;
                //特別處理 資料庫到底時，不再顯示按鈕 + 不再生成big box (否則無限滾動)
            if(currentIndex >= BigBoxesUrls.length || currentIndex >= BigBoxesSpotTitles.length){
                loadMoreBtn.style.display = "none"; 
                return currentIndex;       //中斷
            }
        });
        } catch (error) {
            console.error('錯誤:', error);
        }

}
fetchData();
}); //監聽頁面載完