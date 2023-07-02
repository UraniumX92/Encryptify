const file_name = "encryptify_binary_$ts.txt";
const convert_btn = document.getElementById("c-btn");

convert_btn.onclick = req_handler;
txt_download_btn.onclick = download_text_handler;

function get_op(){
    let rads = document.getElementsByName("operation");
    for(el of rads){
        if(el.checked){
            return el.value;
        }
    }
}

async function req_handler() {
    let op = get_op();
    let text = inp_area.value;
    if(!text){
        this.classList.remove("btn-primary");
        this.classList.add("btn-warning");
        this.innerHTML = "Field Empty";
        let btn = this;
        setTimeout(function() {
            btn.classList.remove("btn-warning");
            btn.classList.add("btn-primary");
            btn.innerHTML = "Convert";
        }, 1000);
        return;
    }
    let xhr = new XMLHttpRequest();
    xhr.onload = function(){
        let result = this.responseText;
        let rjson = null;
        try {
            rjson = JSON.parse(result);
        } catch (error) {
            console.error("error parsing text into json",result);            
        }
        let {status} = rjson;
        if(status===200){
            out_area.value = rjson['text'];
            rtl_update();
        }
        else{
            err_text.innerHTML = rjson['err'];
            err_modal_btn.click();
        }
    }
    let url = '/text/binx/';
    let body = object_to_URI_string({
        text,
        op,
    });
    xhr.open('POST',url,true);
    xhr.setRequestHeader("X-CSRFToken", csrf_token); 
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(body);
}
