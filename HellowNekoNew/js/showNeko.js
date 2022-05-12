console.log('neko');

let neko_path = "https://ln.topdf.de/img/images/0865.png";
let cycle_speed = 0;
let cycle = false;
let last_tag = "cute";

const backgroundElem = document.getElementsByClassName("parallax-window")[0];
const imgElem = document.getElementById("neko-img");
const headerElem = document.getElementById("headline");

let id = "0000"

let history = [];



let tagsList;
let tag_map = {};

const request = new XMLHttpRequest();
const url = 'https://ln.topdf.de/HellowNekoNew/api/all_tag.php';
request.open("GET", url);
request.send();

request.onload = (e) => {
    tagsList = JSON.parse(request.response);
}


window.addEventListener('load', function () {
    let buttons = document.getElementsByClassName('next');
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].style.display = "inline";
    }

    let htmlStr = "";
    for(let i = 0; i < tagsList.length; i++) {
        tag_map[tagsList[i]['name']] = tagsList[i];
        htmlStr += `<option value="${tagsList[i]['name']}">`;
    }

    document.getElementById('tags').innerHTML = htmlStr;
});

document.addEventListener('keyup', onKeyPress)
function onKeyPress(e) {
    if(e.keyCode === 39 || e.keyCode === 68 || e.keyCode === 32){
        search();
        return;
    }
    if(e.keyCode === 37 || e.keyCode === 65){
        previous();
        return;
    }
}

function previous() {
    history.pop();

    neko_path = history[history.length-1][0];
    id = history[history.length-1][1];
    prevUpdate();
}

function pad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length-size);
}

function cycle_neko() {
    console.log("new cycle");
    newNekoTag(last_tag);
}

const searchElem = document.getElementById('search-input');
function search(event) {
    if (!(event === undefined)) {
        if(!(event.keyCode === 13)) {
            return;
        }
        searchElem.blur();
    }
    const val = searchElem.value;

    if(val === "") {
        newNekoTag('cute');
        return;
    }

    if(val.substring(0, 7) === "cycle: ") {
	console.log(val.substring(7, val.length));
        cycle_speed = parseFloat(val.substring(7, val.length));
	console.log(cycle_speed);
	if (cycle_speed == 0 && cycle_speed != NaN) {
	    if (cycle_speed < 1) {
	    	return;
	    }
	    clearInterval(cycle)
	    console.log("stop cycle");
	}else {
	    clearInterval(cycle)
	    cycle = setInterval(cycle_neko, cycle_speed*1000);
	}
        return;
    }

    if(!isNaN(val)) {
        id = pad(parseInt(val), 4);
        console.log(id)
        neko_path = `https://ln.topdf.de/img/images/${id}.png`;
        update();
        return;
    }

    newNekoTag(val);
}



function newNekoTag(tag) {
    if(!tag_map.hasOwnProperty(tag)) {return}

    var sfw = ""
    if(tag === "cute") {sfw = "&sfw=1"}

    var tag_id = tag_map[tag]['id']

    $.getJSON(`https://ln.topdf.de/HellowNekoNew/api/image?tag_id=${tag_id}${sfw}`, function(data) {
        id = data['id'];
	    tags = data['tags'];
        neko_path = data['url'];

        console.log(data);
        update();
    });
}

function loaded() {
    backgroundElem.style.backgroundImage = `url(${neko_path})`;
    headerElem.innerText = id;
}

function prevUpdate() {
    imgElem.src = neko_path;
    imgElem.addEventListener('load', loaded);
}

function update() {
    history.push([neko_path, id]);
    if(255 < history.length) {
        console.log(history.length);
        history.shift();
    }
    imgElem.src = neko_path;
    imgElem.title = id + "\n" + tags.join("\n");

    imgElem.addEventListener('load', loaded);
}
