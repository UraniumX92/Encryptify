const inp_area = document.getElementById("txtArea");
const out_area = document.getElementById("rtxtArea");
const file_inp = document.getElementById("txtFileInput");
const key_input = document.getElementById("key");
const txlen = document.getElementById("txlen");
const rtxlen = document.getElementById("rtxlen");
const err_text = document.getElementById("err-modal-text");
const imp_txt_btn = document.getElementById("import-txt-btn");
const err_modal_btn = document.getElementById("err-modal-btn");
const hidden_ftype_btn = document.getElementById("hidden-ftype-btn");
const force_import_btn = document.getElementById("force-import-btn");
const txt_download_btn = document.getElementById("txt-download-btn");
const csrf_token = get_csrf_token();
const ops = {
    "e-btn" : "encrypt",
    "d-btn" : "decrypt"
}
let txt_file = null;

try {
    key_input.ondblclick = show_hide;
} catch (error) {
    console.log("ignoring key input double click event modifier error.");
}
inp_area.onkeyup = tl_update;
inp_area.onkeydown = tl_update;
imp_txt_btn.onclick = imp_txt;
txt_download_btn.onclick = download_text_handler;
enableDropFiles(inp_area,file_inp);

function getFileName(){
    let ts = Date.now().toString();
    return file_name.replace("$ts",ts);
}

async function imp_txt(){
    let data = out_area.value;
    if(data.length){
        inp_area.value = data;
        tl_update();
    }
    else{
        this.classList.remove("btn-success");
        this.classList.add("btn-warning");
        this.innerHTML = "Text area is empty";
        let dbtn = this;
        setTimeout(function(){
            dbtn.classList.remove("btn-warning");
            dbtn.classList.add("btn-success");
            dbtn.innerHTML = "Import below text";
        },1000);
    }
}

function download_text_handler() {
    let data = out_area.value;
    if(data.length){
        download_text_file(data,file_name);
    }
    else{
        this.classList.remove("btn-success");
        this.classList.add("btn-warning");
        this.innerHTML = "Text area is empty";
        let dbtn = this;
        setTimeout(function(){
            dbtn.classList.remove("btn-warning");
            dbtn.classList.add("btn-success");
            dbtn.innerHTML = "Download text as a file";
        },1000);
    }
}

function get_random_key(size=30){
    arr = [];
    let max = 125;
    let min = 33;
    while(arr.length<size){
        rnum = Math.floor(Math.random()*(max-min)+min);
        if(arr.indexOf(rnum) ===-1){
            arr.push(rnum);
        }
    }
    return arr;
}

function tl_update() {
    txlen.innerHTML = `Text length : ${inp_area.value.length}`;
}

function rtl_update(){
    rtxlen.innerHTML = `Text length : ${out_area.value.length}`;
}

function set_random_key(){
    let rkey = get_random_key();
    let key = '';
    for(i of rkey){
        key += String.fromCodePoint(i);
    }
    key_input.value = key;
}

function clear_key(){
    key_input.value = '';
}

file_inp.onchange = async function(e){
    let file = get_file(file_inp);
    if(file){
        txt_file = file;
        if(get_file_type(file).startsWith("text/")){
            let text = await file.text();
            inp_area.value = text;
            file_inp.value = '';
            txt_file = null;
            tl_update();
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

force_import_btn.onclick = async function(e){
    if(txt_file){
        let text = await txt_file.text();
        inp_area.value = text;
        tl_update();
        txt_file = null;
    }
    else{
        hidden_alert_btn.click();
    }
}

tl_update();