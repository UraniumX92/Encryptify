const password_input = document.getElementById('password');
const email_input = document.getElementById('email');
const err = document.getElementById('err');

password_input.addEventListener('dblclick',show_hide);

function lgcheck(){
    return confirm("Are you sure you want to logout?");
}

// write ajax requests

function onSubmit(){
    let password = password_input.value;
    let email = email_input.value;
    let csrf_token = get_csrf_token();
    let flag = false;
    let xhr = new XMLHttpRequest();
    xhr.onload = function(){
        let rdata = JSON.parse(this.responseText);
        if(rdata['result']==='success'){
            flag = true;
        }
        else{
            err.innerHTML = rdata['message'];
            flag = false;
        }
    }
    let url = '/logincheck/';
    let body = object_to_URI_string({
        'email' : email,
        'password' : password
    });
    xhr.open('POST',url,false);
    xhr.setRequestHeader("X-CSRFToken", csrf_token); 
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(body);
    return flag;
}