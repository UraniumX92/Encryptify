const MAIN_URL = 'http://localhost:80';

function lgcheck(){
    return confirm("Are you sure you want to logout?");
}

function object_to_URI_string(obj){
    let rstr = "";
    Object.keys(obj).forEach(function(key){
        rstr += `${encodeURIComponent(key)}=${encodeURIComponent(obj[key])}&`
    });
    return rstr.slice(0,rstr.length-1);
}

function get_csrf_token(){
    let csrf_inputs = document.getElementsByName("csrfmiddlewaretoken");
    return csrf_inputs[0].value;
}