function object_to_URI_string(obj){
    let rstr = "";
    Object.keys(obj).forEach(function(key){
        rstr += `${encodeURIComponent(key)}=${encodeURIComponent(obj[key])}&`
    });
    return rstr.slice(0,rstr.length-1);
}

function download_text_file(data,filename) {
    const txtfile_blob = new Blob([data], { type: 'text/plain' });
    const txtfile_elem = window.document.createElement('a');
    txtfile_elem.href = window.URL.createObjectURL(txtfile_blob);
    txtfile_elem.target = '_blank';
    txtfile_elem.download = filename;
    txtfile_elem.click();
}

function get_csrf_token(){
    let csrf_inputs = document.getElementsByName("csrfmiddlewaretoken");
    return csrf_inputs[0].value;
}

function preventDefault(e){
    e.preventDefault();
}

function enableDropFiles(element,fileInput){
    element.ondragover = preventDefault;
    element.ondragenter = preventDefault;
    element.ondrop = function(e){
        fileInput.files = e.dataTransfer.files;
        fileInput.onchange();
        e.preventDefault();
    }
}

function getDateTimeStr(dt){
    let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    let seconds = dt.getUTCSeconds();
    let minutes = dt.getUTCMinutes();
    let hours = dt.getUTCHours();
    let day = dt.getUTCDate();
    let month = dt.getUTCMonth();
    let year = dt.getUTCFullYear();
    let ampm = "AM";
    if (hours > 12) {
        hours -= 12;
        ampm = "PM";
    }
    let tcomponents = [day,hours,minutes,seconds];
    for(let i = 0;i<tcomponents.length;i++){
        if(tcomponents[i]<10){
            tcomponents[i] = `0${tcomponents[i]}`;
        }
    }
    [day,hours,minutes,seconds] = tcomponents;
    return `${day}/${months[month]}/${year} - ${hours}:${minutes}:${seconds} ${ampm} [UTC]`;
}