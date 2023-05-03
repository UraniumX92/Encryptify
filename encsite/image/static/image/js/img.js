function get_file(file_input){
    [ifile] = file_input.files;
    return ifile;
}

function get_file_type(file){
    return file.type || 'unknown';
}

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
    while(arr.length<size){
        rnum = Math.floor(Math.random()*256);
        if(arr.indexOf(rnum) ===-1){
            arr.push(rnum);
        }
    }
    return arr;
}
