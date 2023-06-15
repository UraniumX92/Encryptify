function get_file_preview_url(file_input){
    var ifile = get_file(file_input);
    if (ifile){
        var ifile_url = URL.createObjectURL(ifile);
        return ifile_url;
    }
    else{
        return '';
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
}