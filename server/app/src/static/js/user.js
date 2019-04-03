function login(){
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();
    var xhr = new XMLHttpRequest();
    var url = "/userlogin";
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4){
            var res = JSON.parse(xhr.responseText);
            if (xhr.status === 401){
                if (res.msg == "unauth"){
                    window.alert("username or password incorrect!");
                }
            }
            if (xhr.status === 200){
                window.location.href = "/";
            }
        }
    }
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    var parameters = {
        "username": username,
        "password": password,
    };
    xhr.send(JSON.stringify(parameters));
}

function signup(){
    var username = document.getElementById("signusername").value.trim();
    var password = document.getElementById("signpassword").value.trim();
    var xhr = new XMLHttpRequest();
    var url = "/usersignup";
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4){
            var res = JSON.parse(xhr.responseText);
            if (xhr.status === 401){
                if (res.msg == "occupied"){
                    window.alert("username already exists!");
                }
            }
            if (xhr.status === 200){
                window.location.href = "/";
            }
        }
    }
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    var parameters = {
        "username": username,
        "password": password,
    };
    xhr.send(JSON.stringify(parameters));
}