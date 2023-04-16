const img_input = document.getElementById("imgFileInput");
const img_preview = document.getElementById("imgPreview");
const key_input = document.getElementById("key");
let img_err_count = 0;

img_input.onchange = (e) => {
    if(get_file(img_input)){
        img_preview.style.display = 'block';
        img_preview.src = get_file_preview_url(img_input);
    }
    else{
        on_img_err();
    }
}

function set_random_key(){
    key_input.value = JSON.stringify(get_random_key(30)).replace(" ","");
}

function clear_key(){
    key_input.value = '';
    key_input.focus();
}

function on_img_err(){
    if(img_err_count>0){
        if (img_input.value){
            alert("You are supposed to select an image file.")
        }
        img_input.value = '';
    }
    else{
        img_err_count += 1;
    }
    img_preview.style.display = 'none';
}