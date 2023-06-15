const img_input = document.getElementById("imgFileInput");
const img_preview = document.getElementById("imgPreview");
const img_label = document.getElementById("imgLabel");
const txt_input = document.getElementById("txtFileInput");
const txt_area = document.getElementById("txtArea");
const key_input = document.getElementById("key");
const op_radios = document.getElementsByName("operation");
const pass_check = document.getElementById("pass-check");
const enc_els = document.getElementsByClassName("op-encrypt");
const txt_inp_btn = document.getElementById("txt-inp-btn");
const hidden_ftype_btn = document.getElementById("hidden-ftype-btn");
const hidden_alert_btn = document.getElementById("hidden-alert-btn");
const force_import_btn = document.getElementById("force-import-btn");
const hidden_img_err_btn = document.getElementById("hidden-img-err-btn");
const img_dim = document.getElementById("img-dimensions");
let img_err_count = 0;
let txt_file = null;

enableDropFiles(txt_inp_btn,txt_input);
enableDropFiles(txt_area,txt_input);
key_input.ondblclick = show_hide;

function on_img_err(){
    if(img_err_count>0){
        if (img_input.value){
            hidden_img_err_btn.click();
        }
        img_input.value = '';
    }
    else{
        img_err_count += 1;
    }
    img_preview.style.display = 'none';
    img_dim.style.display = 'none';
}

txt_inp_btn.onclick = function (e){
    txt_input.click();
}

force_import_btn.onclick = async function(e){
    if(txt_file){
        let text = await txt_file.text();
        txt_area.value = text;
        txt_file = null;
    }
    else{
        hidden_alert_btn.click();
    }
}

txt_input.onchange = async function(e){
    let file = get_file(txt_input);
    if(file){
        txt_file = file;
        if(get_file_type(file).startsWith("text/")){
            let text = await file.text();
            txt_area.value = text;
            txt_input.value = '';
        }
        else{
            txt_input.value = '';
            hidden_ftype_btn.click();
        }
    }
    else{
        txt_input.value = '';
    } 
}

img_input.onchange = (e) => {
    if(get_file(img_input)){
        img_preview.style.display = 'block';
        img_preview.src = get_file_preview_url(img_input);
    }
    else{
        on_img_err();
    }
}

function get_op(){
    for(var i = 0; i<op_radios.length;i++){
        var elm = op_radios[i];
        if(elm.checked){
            return elm.value;
        }   
    }
}

function rchange_display(e){
    let op = get_op();
    if(op==="decrypt"){
        img_label.innerHTML = "Select an Image file to extract text from it";
        pass_check.checked = false;
        for(enc of enc_els){
            enc.style.display = 'none';
        }
    }
    else{
        img_label.innerHTML = "Select an Image file to hide text in it";
        for(enc of enc_els){
            enc.style.display = 'block';
        }
    }
}

img_preview.onload = function(e){
    img_dim.style.display = 'block';
    img_dim.innerText = `${img_preview.naturalWidth}x${img_preview.naturalHeight}`;
}

window.onload = (e)=>{
    rchange_display(e);
    img_input.onchange(e);
    for(rad of op_radios){
        rad.onchange = rchange_display;
    }
}
