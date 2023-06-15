const egg = "trippy";
let url_check_interval = null;
let trip_speed = null;
const trip_text = document.getElementById("trip-text");
const hidden_egg_btn = document.getElementById("hidden-egg-btn");
const start_trip_btn = document.getElementById("start-trip");
const egg_timeout = 1000;
let trippy_audio = null;
let anim_duration = null;
const anim_duration_ph = "$$duration_placeholder$$";
const egg_css = `*:not(html) {
    animation: trippy ${anim_duration_ph}s linear infinite;
}
`
let anim_egg_style = document.createElement('style');
let egg_style = document.createElement('style');
const head = document.head || document.getElementsByTagName('head')[0];
let egg_node = null;
let egg_intr = null;
let elist = document.querySelectorAll("*");

function current_url(){
    return window.location.href;
}

function rcolor(){
    return Math.floor(Math.random()*256);
}

function rcstr(){
    return `rgb(${rcolor()},${rcolor()},${rcolor()})`;
}

function automate_egg_css(randnum){
    egg_style = document.createElement('style');
    let temp_css = egg_css;
    temp_css = temp_css.replace(anim_duration_ph,randnum);
    egg_node = document.createTextNode(temp_css);
    head.appendChild(egg_style);
    egg_style.appendChild(egg_node)
}

function change_egg(){
    for(var i=0;i<elist.length;i++){
        let el = elist[i];
        el.style.color = rcstr();
        el.style.background = rcstr();
        el.style.transform = `scale(${(Math.random()*(1.4))+0.1})`;
        el.style.border = `5px solid ${rcstr()}`;
    }
}

function removeInlineStyles() {
    for (let i = 0; i < elist.length; i++) {
        const el = elist[i];
        el.style.removeProperty("color");
        el.style.removeProperty("background");
        el.style.removeProperty("transform");
        el.style.removeProperty("border");
        el.style.removeProperty("transition");
        el.style.removeProperty("border-radius");
    }
}

function start_egg(){
    trip_speed = ((Math.random()*(0.9))+0.1).toFixed(3);
    anim_duration = (trip_speed*5).toFixed(3);
    automate_egg_css(anim_duration);
    console.log(`trip speed : ${trip_speed}s`);
    console.log(`animation duration : ${anim_duration}s`);
    for(el of elist){
        el.style.transition = `${trip_speed}s`;
        el.style['border-radius'] = '50px';
    }
    change_egg();
    egg_intr = setInterval(change_egg,trip_speed*1000);
}

function end_egg() {
    head.removeChild(egg_style);
    clearInterval(egg_intr);
    removeInlineStyles();
}

function on_url_change(){
    let urlnow = current_url();
    let ulist = urlnow.split('#');
    let egg_condition = urlnow.includes('#') && ulist[ulist.length-1].toLowerCase()===egg;
    if(egg_condition && !head.contains(egg_style)){
        start_egg();
    }
    else if(!egg_condition && head.contains(egg_style)){
        end_egg();
    }
}

on_url_change();
url_check_interval = setInterval(on_url_change,egg_timeout);