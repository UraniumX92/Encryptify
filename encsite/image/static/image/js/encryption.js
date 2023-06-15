const img_input = document.getElementById("imgFileInput");
const img_preview = document.getElementById("imgPreview");
const key_input = document.getElementById("key");
const img_dim = document.getElementById("img-dimensions");
const hidden_img_err_btn = document.getElementById("hidden-img-err-btn");
let img_err_count = 0;

key_input.ondblclick = show_hide;

img_input.onchange = (e) => {
    if(get_file(img_input)){
        img_preview.style.display = 'block';
        img_preview.src = get_file_preview_url(img_input);
    }
    else{
        on_img_err();
    }
}

window.onload = (e)=>{
    img_input.onchange(e);
}

img_preview.onload = function(e){
    img_dim.style.display = 'block';
    img_dim.innerText = `${img_preview.naturalWidth}x${img_preview.naturalHeight}`;
}

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