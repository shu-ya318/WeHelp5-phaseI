window.onload = function() {
    document.getElementById("signinForm").onsubmit = async function(event) {
        event.preventDefault();  

        if (!document.getElementById("checkbox").checked) {   
            alert("Please check the checkbox first");
            return false;  //(o)阻函式繼續執行  (x)返回一個錯誤
        }

        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        try {
            let response = await fetch("http://127.0.0.1:8000/signin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body:`username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            });
            //先處理 接收失敗( HTTP 狀態碼 200~299以外)時，throw error 給catch捕獲
            if (!response.ok) {
                throw new Error("網路請求失敗");
            }
            //接收成功，導向新的子頁面
            let result = await response.json();
            window.location.href = result.url;
        } catch (error) {
            console.error("執行的 fetch 操作有誤", error);
        }
        return false;
    }
}