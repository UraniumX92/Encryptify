const job_image = document.getElementById("job_image");
const info_text = document.getElementById("info_text");
const data_element = document.getElementById("job_data");
const spinner = document.getElementById("spinner");
const job_id = data_element.getAttribute("data-job-id");
const download_btn = document.getElementById("download-btn");
const modal = document.getElementById("info-modal");
const modal_heading = document.getElementById("info-modal-h");
const modal_body = document.getElementById("info-modal-content");
const img_dim = document.getElementById("img-dimensions");
const url = `/image/encryption/info/${job_id}`;
const iurl = `/image/encryption/job/${job_id}`;
const interval = 1000;
let image_poll_interval = null;
let info_poll_interval = null;

function on_img_err(){
    job_image.style.display = 'none';
}

job_image.onload = function(e){
    spinner.innerHTML = '';
    img_dim.innerHTML = `${job_image.naturalWidth}x${job_image.naturalHeight}`;
}

on_img_err();

function poll_for_job_info(){
    let xhr = new XMLHttpRequest();
    xhr.onload = function(){
        let xresp = '';
        try{
            xresp = JSON.parse(this.responseText);
        }
        catch(err){
            clearInterval(info_poll_interval);
        }
        let status = xresp['status'];
        if(status === 200){
            if(xresp['message']==="Finished"){
                clearInterval(info_poll_interval);
                job_image.style.display = 'block';
                job_image.src = iurl;
                download_btn.href = iurl;
                info_text.innerHTML = "Image successfully loaded";
                let job_info = xresp['job_info'];
                let st = new Date(job_info['started_at']*1000);
                let fn = new Date(job_info['finished_at']*1000);
                let exp = new Date(job_info['expires_at']*1000);
                let innerHTML = '<p>';
                innerHTML += `<span class="fw-bold">Task ID :</span> ${job_info['id']}<br><br>`;
                innerHTML += `<span class="fw-bold">Task name :</span> Image Encryption<br><br>`;
                innerHTML += `<span class="fw-bold">Operation :</span> ${job_info['operation']}<br><br>`;
                if(job_info['user_name']){
                    innerHTML += `<span class="fw-bold">Requested by :</span> ${job_info['user_name']}<br><br>`;
                }
                innerHTML += `<span class="fw-bold">Started at :</span> ${getDateTimeStr(st)}<br><br>`;
                innerHTML += `<span class="fw-bold">Finished at :</span> ${getDateTimeStr(fn)}<br><br>`;
                innerHTML += `<span class="fw-bold">Expires at :</span> ${getDateTimeStr(exp)}<br><br>`;
                innerHTML += `<span class="fw-bold">Time taken to perform operation :</span> ${job_info['time_taken']}.<br></p>`;
                modal_body.innerHTML = innerHTML;
                modal_heading.innerHTML = `Image Encryption Task Details:`;
            }
        }
        else if(status===102){
            modal_body.innerHTML = xresp['message'];
            info_text.innerHTML = "Processing...";

        }
        else{
            clearInterval(info_poll_interval);
        }
    }
    xhr.open('GET',url,true);
    xhr.send()
}

info_poll_interval = setInterval(poll_for_job_info,interval);