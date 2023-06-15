const file_name = "encryptify_xor_$ts.txt";
const encrypt_btn = document.getElementById("e-btn");
const decrypt_btn = document.getElementById("d-btn");

decrypt_btn.style.display = 'none';
encrypt_btn.innerHTML = "XOR";
encrypt_btn.onclick = req_handler;

function req_handler() {
    let text = inp_area.value;
    let key = key_input.value;
    if(!text || !key){
        this.classList.remove("btn-primary");
        this.classList.add("btn-warning");
        this.innerHTML = "Fields Empty";
        let btn = this;
        setTimeout(function() {
            btn.classList.remove("btn-warning");
            btn.classList.add("btn-primary");
            btn.innerHTML = "XOR";
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
    let url = '/text/xorx/';
    let body = object_to_URI_string({
        text,
        key,
    });
    xhr.open('POST',url,false);
    xhr.setRequestHeader("X-CSRFToken", csrf_token); 
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send(body);
}
