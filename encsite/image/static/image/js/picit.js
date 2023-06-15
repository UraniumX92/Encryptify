const img_input = document.getElementById("imgFileInput");
const img_preview = document.getElementById("imgPreview");
const img_label = document.getElementById("imgLabel");
const file_inp = document.getElementById("txtFileInput");
const inp_area = document.getElementById("txtArea");
const key_input = document.getElementById("key");
const op_radios = document.getElementsByName("operation");
const enc_els = document.getElementsByClassName("op-encrypt");
const dec_els = document.getElementsByClassName("op-decrypt");
const txt_inp_btn = document.getElementById("txt-inp-btn");
const hidden_ftype_btn = document.getElementById("hidden-ftype-btn");
const hidden_alert_btn = document.getElementById("hidden-alert-btn");
const force_import_btn = document.getElementById("force-import-btn");
const hidden_img_err_btn = document.getElementById("hidden-img-err-btn");
const img_dim = document.getElementById("img-dimensions");
const txt_size = document.getElementById("txt-size");
const MAX_TXT_LENGTH = 16000000;
let img_err_count = 0;
let txt_file = null;

enableDropFiles(txt_inp_btn,file_inp);
enableDropFiles(inp_area,file_inp);
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
    file_inp.click();
}

force_import_btn.onclick = async function(e){
    if(txt_file){
        let text = await txt_file.text();
        inp_area.value = text;
        txt_change();
        txt_file = null;
    }
    else{
        hidden_alert_btn.click();
    }
}

file_inp.onchange = async function(e){
    let file = get_file(file_inp);
    if(file){
        txt_file = file;
        if(get_file_type(file).startsWith("text/")){
            let text = await file.text();
            inp_area.value = text;
            file_inp.value = '';
            txt_change();
        }
        else{
            file_inp.value = '';
            hidden_ftype_btn.click();
        }
    }
    else{
        file_inp.value = '';
    } 
}

img_input.onchange = function(e){
    if(get_file(img_input)){
        img_preview.style.display = 'block';
        img_preview.src = get_file_preview_url(img_input);
    }
    else{
        img_dim.innerHTML = '';
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
        img_label.innerHTML = "Select an Image file to convert it to text";
        for(enc of enc_els){
            enc.style.display = 'none';
        }
        for(dec of dec_els){
            dec.style.display = 'block';
        }
        img_input.onchange();
    }
    else{
        img_input.value = '';
        img_input.onchange();
        for(enc of enc_els){
            enc.style.display = 'block';
        }
        for(dec of dec_els){
            dec.style.display = 'none';
        }
    }
}

inp_area.onkeyup = txt_change;
function txt_change(){
    let lnow = inp_area.value.length;
    if(lnow > MAX_TXT_LENGTH){
        txt_size.classList.remove("text-info");
        txt_size.classList.remove("text-warning");
        txt_size.classList.add("text-danger");
    }
    else if(lnow === MAX_TXT_LENGTH){
        txt_size.classList.remove("text-info");
        txt_size.classList.remove("text-danger");
        txt_size.classList.add("text-warning");
    }
    else{
        txt_size.classList.remove("text-warning");
        txt_size.classList.remove("text-danger");
        txt_size.classList.add("text-info");
    }
    let tratio = (lnow/MAX_TXT_LENGTH)*100;
    txt_size.innerHTML = `${lnow}/${MAX_TXT_LENGTH} - ${tratio.toFixed(3)}%`
}

img_preview.onload = function(e){
    img_dim.style.display = 'block';
    img_dim.innerHTML = `${img_preview.naturalWidth}x${img_preview.naturalHeight}`;
}

window.onload = (e)=>{
    rchange_display(e);
    txt_change();
    img_input.onchange(e);
    for(rad of op_radios){
        rad.onchange = rchange_display;
    }
}
