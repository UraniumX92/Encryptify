const job_image = document.getElementById("job_image");
const info_text = document.getElementById("info_text");
const error_text = document.getElementById("err");
const data_element = document.getElementById("job_data");
const job_id = data_element.getAttribute("data-job-id");
const spinner = document.getElementById("spinner");
const buffer_text = document.getElementById("buffertext");
const show_info_btn = document.getElementById("show-info-btn");
const img_download_btn = document.getElementById("img-download-btn");
const secondary_img_download_btn = document.getElementById("secondary-img-download");
const enter_key_btn = document.getElementById("enter-key-btn");
const txt_download_btn = document.getElementById("txt-download-btn");
const try_again_modal_btn = document.getElementById("try-again-modal-btn");
const modal = document.getElementById("info-modal");
const modal_heading = document.getElementById("info-modal-h");
const modal_body = document.getElementById("info-modal-content");
const ask_key_modal_btn = document.getElementById("ask-key-modal-btn");
const err_modal_btn = document.getElementById("err-modal-btn");
const key_submit_btn = document.getElementById("key-submit");
const textarea_container = document.getElementById("pct-textarea");
const imgarea_container = document.getElementById("pct-imgarea");
const textarea = document.getElementById("txtArea");
const err_content = document.getElementById("err-modal-text");
const pct_key_inp = document.getElementById("pct-key");
const modal_ask_key = document.getElementById("ask-key-modal");
const key_form = document.getElementById("key-form");
const img_dim = document.getElementById("img-dimensions");
const info_url = `/image/picit/info/${job_id}/`;
const job_url = `/image/picit/job/${job_id}/`;
const interval = 1000;
let extract_text_success = false;
let image_poll_interval = null;
let info_poll_interval = null;
let txt_filename = null;
const picit_ops = {
    'encrypt' : "Text to Image",
    'decrypt' : "Image to Text"
}

function on_img_err(){
    job_image.style.display = 'none';
}

on_img_err();

function poll_for_job_info(){
    let xhr = new XMLHttpRequest();
    xhr.onload = function(e){
        let xresp = '';
        try{
            xresp = JSON.parse(this.responseText);
        }
        catch(err){
            clearInterval(info_poll_interval);
        }
        let {status,message} = xresp;
        if(status === 200){
            if(message==="Finished"){
                clearInterval(info_poll_interval);
                let {job_info} = xresp;
                if(job_info['operation']==="encrypt"){
                    imgarea_container.style.display = 'block';
                    job_image.src = job_url;
                    job_image.style.display = 'block';
                    img_download_btn.href = job_url;
                    info_text.innerHTML = "Image successfully loaded";
                    show_info_btn.style.display = 'block';
                    enter_key_btn.style.display = 'none';
                }
                else{
                    if(job_info['protected']){
                        enter_key_btn.style.display = 'block';
                        info_text.innerHTML = "PicIt Image requires password";
                        buffer_text.innerHTML = "Enter the Password/Encryption key to proceed..."
                        ask_key_modal_btn.click();
                    }
                    else{
                        info_text.innerHTML = "Extracting text..."
                        get_pct_text();
                    }
                }
                let st = new Date(job_info['started_at']*1000);
                let fn = new Date(job_info['finished_at']*1000);
                let exp = new Date(job_info['expires_at']*1000);
                let innerHTML = '<p>';
                innerHTML += `<span class="fw-bold">Task ID :</span> ${job_info['id']}<br><br>`;
                innerHTML += `<span class="fw-bold">Task name :</span> PicIt<br><br>`;
                innerHTML += `<span class="fw-bold">Operation :</span> ${picit_ops[job_info['operation']]}<br><br>`;
                if(job_info['user_name']){
                    innerHTML += `<span class="fw-bold">Requested by :</span> ${job_info['user_name']}<br><br>`;
                }
                if(job_info['operation']==='encrypt'){
                    innerHTML += `<span class="fw-bold">Started at :</span> ${getDateTimeStr(st)}<br><br>`;
                    innerHTML += `<span class="fw-bold">Finished at :</span> ${getDateTimeStr(fn)}<br><br>`;
                    innerHTML += `<span class="fw-bold">Expires at :</span> ${getDateTimeStr(exp)}<br><br>`;
                    innerHTML += `<span class="fw-bold">Time taken to perform operation :</span> ${job_info['time_taken']}.<br></p>`;
                    modal_body.innerHTML = innerHTML;
                }
                modal_heading.innerHTML = `PicIt Task Details:`
            }
        }
        else if(status===102){
            modal_body.innerHTML = message;
            info_text.innerHTML = "Processing...";
        }
        else if(status===415){
            clearInterval(info_poll_interval)
            try_again_modal_btn.style.display = 'none';
            let errs = xresp['errs'];
            let err_txt = Object.values(errs)[0];
            info_text.innerHTML = "Error";
            err_content.innerHTML = err_txt;
            spinner.innerHTML = '';
            err_modal_btn.click();
            error_text.innerHTML = err_txt;
        }
        else{
            clearInterval(info_poll_interval);
        }
    }
    xhr.open('GET',info_url,true);
    xhr.send()
}

function get_pct_text(key=null){
    let t_url = job_url;
    if(key){
        t_url += `?key=${encodeURIComponent(key)}`;
    }
    let xhr = new XMLHttpRequest();
    xhr.onload = function(e){
        let resp = JSON.parse(this.responseText);
        let {status} = resp;
        if(status===200){
            info_text.innerHTML = "Extracted Text"
            extract_text_success = true;
            txt_filename = resp['filename'];
            textarea_container.style.display = 'block';
            textarea.value = resp['text'];
            show_info_btn.style.display = 'block';
            enter_key_btn.style.display = 'none';
            spinner.innerHTML = '';
            let {job_info} = resp;
            let st = new Date(job_info['started_at']*1000);
            let fn = new Date(job_info['finished_at']*1000);
            let exp = new Date(job_info['expires_at']*1000);
            let innerHTML = '<p>';
            innerHTML += `<span class="fw-bold">Task ID :</span> ${job_info['id']}<br><br>`;
            innerHTML += `<span class="fw-bold">Task name :</span> PicIt<br><br>`;
            innerHTML += `<span class="fw-bold">Operation :</span> ${picit_ops[job_info['operation']]}<br><br>`;
            if(job_info['user_name']){
                innerHTML += `<span class="fw-bold">Requested by :</span> ${job_info['user_name']}<br><br>`;
            }
            innerHTML += `<span class="fw-bold">Started at :</span> ${getDateTimeStr(st)}<br><br>`;
            innerHTML += `<span class="fw-bold">Finished at :</span> ${getDateTimeStr(fn)}<br><br>`;
            innerHTML += `<span class="fw-bold">Expires at :</span> ${getDateTimeStr(exp)}<br><br>`;
            innerHTML += `<span class="fw-bold">Time taken to perform operation :</span> ${job_info['time_taken']}.<br></p>`;
            modal_body.innerHTML = innerHTML;
        }
        else{
            err_content.innerHTML = resp['err'];
            spinner.innerHTML = '';
            err_modal_btn.click();
        }
    }
    xhr.open("GET",t_url,true);
    xhr.send();
}

pct_key_inp.ondblclick = show_hide;

job_image.onload = function(e){
    spinner.innerHTML = '';
    img_dim.innerHTML = `${job_image.naturalWidth}x${job_image.naturalHeight}`;
}

txt_download_btn.onclick = function(e){
    download_text_file(textarea.value,txt_filename);
}

secondary_img_download_btn.onclick = function(e){
    img_download_btn.click();
}

function key_submit(){
    let key = pct_key_inp.value;
    if(key){
        get_pct_text(key);
        pct_key_inp.value = '';
    }
    else{
        err_content.innerHTML = "Please enter the password/encryption key";
        err_modal_btn.click();
    }
    return false;
}

modal_ask_key.addEventListener('shown.bs.modal',function(e){
    pct_key_inp.focus();
});

window.onload = function(e){
    enter_key_btn.style.display = 'none';
}

info_poll_interval = setInterval(poll_for_job_info,interval);