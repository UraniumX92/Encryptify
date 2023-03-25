let p1 = document.getElementById('password1');
let p2 = document.getElementById('password2');
let err = document.getElementById('err');
let email = document.getElementById('email');
let uname = document.getElementById('name');

p1.addEventListener('dblclick',show_hide);
p2.addEventListener('dblclick',show_hide);

function show_hide(){
    if (this.type=='text'){
        this.type = 'password';
    }
    else{
        this.type = 'text';
    }
}

function onSubmit(){
    let pv1 = p1.value;
    let pv2 = p2.value;
    let email_val = email.value;
    let name_val = uname.value;

    if(name_val.length>100){
        err.innerHTML = "Name cannot contain more than 100 characters";
        return false;
    }
    if(email_val.length>150){
        err.innerHTML = "Email cannot contain more than 150 characters";
        return false;
    }
    if((pv1.length>=8) && (pv2.length>=8)){
        if(pv1===pv2){
            let flag = false;
            let xhr = new XMLHttpRequest();
            let csrf_token = get_csrf_token();
            xhr.onload = function(){
                let rdata = JSON.parse(this.responseText)
                if (rdata['result'] === 'success'){
                    flag = true;
                }
                else{
                    err.innerHTML = rdata['message'];
                    flag = false;
                }
            };
            let url = `${MAIN_URL}/signupcheck`;
            let data = {
                'name' : name_val,
                'email' : email_val,
                'password' : pv1,
                'password2' : pv2,
            }
            xhr.open('POST',url,false);
            xhr.setRequestHeader("X-CSRFToken", csrf_token); 
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            let body = object_to_URI_string(data);
            xhr.send(body);
            return flag;
        }
        err.innerHTML = "Passwords do not match";
        return false;
    }
    else{
        err.innerHTML = "Password must contain atleast 8 characters";
        return false;
    }
}
