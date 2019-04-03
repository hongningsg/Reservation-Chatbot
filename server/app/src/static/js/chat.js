function sendToFlask(msg){
    var xhr = new XMLHttpRequest();
    var url = "/userquery";
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                var res = JSON.parse(xhr.responseText);
                if (res.cmd == "message"){
                    botSay(res.msg);
                }
                else if (res.cmd == "book"){
                    var r = confirm("Are you sure you want to reserve " + res.msg);
                    if (r == true){
                        var parameters = {
                            "cmd": "book",
                            "userquery": msg,
                        };
                        xhr.open("POST", url, true);
                        xhr.send(JSON.stringify(parameters));
                    }else{
                        botSay("OK, you are fickle :)")
                    }
                }else if (res.cmd == "cancel"){
                    var r = confirm("Are you sure you want to cancel reservation of " + res.msg);
                    if (r == true){
                        var parameters = {
                            "cmd": "cancel",
                            "userquery": msg,
                        };
                        xhr.open("POST", url, true);
                        xhr.send(JSON.stringify(parameters));
                    }else{
                        botSay("OK, no cancel.")
                    }
                }else if (res.cmd == "cancelID"){
                    var r = confirm("Are you sure you want to cancel reservation of " + res.msg);
                    if (r == true){
                        var parameters = {
                            "cmd": "cancelID",
                            "userquery": msg,
                        };
                        xhr.open("POST", url, true);
                        xhr.send(JSON.stringify(parameters));
                    }else{
                        botSay("OK, no cancel.")
                    }
                }
            }else{
                botSay("Oops...I cannot understand that, can you please say it with more details?");
            }
        }
    }
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    var parameters = {
        "cmd": "query",
        "userquery": msg,
    };
    xhr.send(JSON.stringify(parameters));
}

function logout(){
    var xhr = new XMLHttpRequest();
    var url = "/logout";
     xhr.onreadystatechange = function () {
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                window.location.href = "/login";
            }
        }
    }
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    var parameters = {
        "logout": false,
    };
    xhr.send(JSON.stringify(parameters));
}

function sendMsg(){
    var text = document.getElementById("text").value.trim();
    document.getElementById("text").value = "";
    if (text != ""){
        sendToFlask(text);
        var div = document.createElement('div');
        div.className = "user_chat self"
        div.innerHTML =
            '<div class="user_img"><img src="../static/image/user.jpg"></div>\
             <p class="user_msg">' + String(text) +  '</p>';
        var Chatlogs = document.getElementById('Chatlogs');
        Chatlogs.appendChild(div);
        var xH = Chatlogs.scrollHeight;
        Chatlogs.scrollTo(0, xH);
    }
}

function botSay(msg){
    var div = document.createElement('div');
    div.className = "user_chat bot"
    div.innerHTML =
        '<div class="user_img"><img src="../static/image/bot.jpg"></div>\
         <p class="user_msg">' + String(msg) +  '</p>';
    var Chatlogs = document.getElementById('Chatlogs');
    Chatlogs.appendChild(div);
    var xH = Chatlogs.scrollHeight;
    Chatlogs.scrollTo(0, xH);
}

window.onload = function(){
    var input = document.getElementById("text");
    input.addEventListener("keydown", function(event) {
      if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("send").click();
      }
    });
}

