function findTagsElement() {
    return document.getElementById("tags");
}

var tagList;
function selectTag(tagEl) {
    topicColor = tagEl.parentElement.parentElement.getAttribute("color");
    tagEl.classList.add("selected");
    tagEl.style.borderColor = topicColor;
    tagEl.style.backgroundColor = topicColor;
    tagEl.style.color = "white";
    var inputEl = document.createElement("input");
    inputEl.value = tagEl.innerHTML;
    inputEl.name = "tag " + tagEl.innerHTML;
    tagList.appendChild(inputEl);
}

function removeTag(tagEl) {
    tagEl.classList.remove("selected");
    tagEl.style.borderColor = null;
    tagEl.style.backgroundColor = null;
    tagEl.style.color = null;
    for (i = 0; i < tagList.children.length; i++) {
        if (tagList.children[i].value == tagEl.innerHTML) {
            tagList.children[i].remove();
        }
    }
}

function bindClick(tagEl) {
    tagEl.onclick = function() {
        if (tagEl.classList.contains("selected")) {
            removeTag(tagEl);
        }
        else {
            selectTag(tagEl);
        }
    }
}

function buildTagsMenu(root, structure, tags) {
    root.classList.add("flex", "flex-col", "gap-y-4");
    
    tagList = document.createElement("div");
    root.appendChild(tagList);
    tagList.classList.add("hidden");

    for (topic_id in structure) {
        topic = structure[topic_id];
        var topicEl = document.createElement("div");
        root.appendChild(topicEl);
        topicEl.setAttribute("color", topic.color);
        var topicHeader = document.createElement("div");
        topicEl.appendChild(topicHeader);
        topicHeader.classList.add("text-2xl");
        if (topic.color) {
            topicHeader.style.color = topic.color;
        }
        else {
            topicHeader.style.color = "black";
        }
        topicHeader.innerHTML = topic.name;
        var topicBody = document.createElement("div");
        topicEl.appendChild(topicBody);
        topicBody.classList.add("flex-wrap", "flex", "gap-x-2", "gap-y-2");
        for (tag_id in topic["tags"]) {
            tag = topic["tags"][tag_id];
            var tagEl = document.createElement("div");
            tagEl.classList.add("text-base", "rounded-full", "border", "border-neutral-500", "p-2", "flex", "justify-center", "hover:cursor-pointer", "select-none", "transition-colors");
            tagEl.classList.add("tagEl");
            tagEl.classList.add("text-neutral-500", "hover:text-neutral-800");
            tagEl.classList.add("hover:bg-slate-100");
            tagEl.innerHTML = tag;
            topicBody.appendChild(tagEl);
            bindClick(tagEl);
            if (tags.includes(tag)) {
                selectTag(tagEl);
            }
        }
    }
}

function parseData() {
    var root = findTagsElement();
    var structure;
    var tags;
    
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';

    var data = {};
    xhr.open('POST', '/get_tags_structure', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            structure = xhr.response;
            var objectType = root.getAttribute("object-type");
            var objectId = root.getAttribute("object-id");
            var link;
            if (objectType == "problem") {
                link = "/get_tags_by_problem";
            }
            else if (objectType == "sheet") {
                link = "/get_tags_by_sheet";
            }
            else if (objectType == "contest") {
                link = "/get_tags_by_contest";
            }
            
            var xhr2 = new XMLHttpRequest();
            xhr2.responseType = 'json';
            data = {"id": objectId};
            xhr2.open('POST', link, true);
            xhr2.setRequestHeader('Content-Type', 'application/json');
            xhr2.onreadystatechange = function() {
                if (xhr2.readyState === 4 && xhr2.status === 200) {
                    tags = xhr2.response;
                    buildTagsMenu(root, structure, tags);
                }
            }
            xhr2.send(JSON.stringify(data));
        }
    }
}

parseData();