window.onload = function() {
    document.getElementById("signinForm").onsubmit =  function(event) {
        if (!document.getElementById("checkbox").checked) {   
            alert("Please check the checkbox first");
            return false;  //(o)阻函式繼續執行  (x)返回一個錯誤
        }
    }
}
