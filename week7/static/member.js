//共通輔助函式-判斷欄位是否空字串
function validateInput(input) {
    if (input.trim() === '') {
        alert('請輸入內容');
        return false;
    }
    return true;
}


//更新姓名輔助函式-連帶更新介面1.動態訊息+2.留言板姓名(因使用不同提交方式)
function updateNameInUI(name) {
    document.getElementById("welcome_message").textContent = `${name}，歡迎登入系統`;
    let messageNameElements = document.querySelectorAll('.current_member');
    messageNameElements.forEach(function(element) {
        element.textContent = name;
    });
}

//主要函式-處理 查詢姓名顯示
document.getElementById("query_button").addEventListener("click", function(event) {
    event.preventDefault();
    let username = document.getElementById("query_username").value.trim(); //先過濾空白 再提交
    if (!validateInput(username)) {
        return;
    }
    fetch("/api/member?username=" + encodeURIComponent(username))  //url參數為字串: 用內建函式encodeURIComponent來編碼
        .then(response => response.json())
        .then(data => {
            let resultDiv = document.getElementById("query_result");
            resultDiv.style.textAlign = "center";
            if (data.data !== null) {
                resultDiv.textContent = `${data.data.name}(${data.data.username})`;
            } else {
                resultDiv.textContent = "無此會員";
            }
        });
});


//主要函式-處理 更新姓名顯示
document.getElementById("update_name_button").addEventListener("click", function(event) {
    event.preventDefault();
    let newName = document.getElementById("new_name").value.trim();
    if (!validateInput(newName)) {
        return;
    }
    fetch("/api/member", {
        method: "PATCH",     //須全部大寫
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({name: newName})
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("update_name_result");
        resultDiv.style.textAlign = "center";
        if (data.ok) {
            resultDiv.textContent = "更新成功";
            updateNameInUI(newName);
        } else {
            resultDiv.textContent = "更新失敗";
        }
    });
});


//重載頁面時，介面均顯示 更新後姓名
window.addEventListener('load', (event) => {
    fetch("/api/member")
    .then(response => response.json())
    .then(data => {
        if (data.ok && data.data !== null) {
            updateNameInUI(data.data.name);
        }
    });
});