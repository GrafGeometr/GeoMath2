function likeButtons(withCounter=false) {
    var likeDivs = document.getElementsByClassName("like");
    for (var i = 0; i < likeDivs.length; i++) {
        let likeDiv = likeDivs[i];
        let list = likeDiv.id.split("like-")[1].split("-");
        let data = {"parent_type": list[0], "parent_id": list[1]};
        likeButton(likeDiv, withCounter, data);
    }
}

function likeButton(likeDiv, withCounter=false, data) {
    likeDiv.classList.add("flex", "items-center", "gap-x-2");

    let likeLabel = document.createElement('label');
    likeDiv.appendChild(likeLabel);

    let likeBtn = document.createElement('input');
    likeBtn.type = 'checkbox';
    likeBtn.classList.add("hidden");
    likeLabel.appendChild(likeBtn);
   
    let likeIcon = document.createElement('img');
    likeIcon.src = '/static/images/like.svg';
    likeIcon.classList.add("w-8", "hover:cursor-pointer");
    likeLabel.appendChild(likeIcon);

    let likeCnt = document.createElement('span');
    likeCnt.classList.add("font-bold", "text-lg");

    if (withCounter) {
        likeDiv.appendChild(likeCnt);
    }

    function refresh() {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'json';
        xhr.open('POST', '/like', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let check = this.response["check"];
                let cnt = this.response["cnt"];
                likeIcon.src = check ? '/static/images/like_active.svg' : '/static/images/like.svg';
                likeBtn.checked = check;
                console.log('refreshed', check, cnt);
                if (withCounter) {
                    likeCnt.innerHTML = cnt;
                }
            }
        }
        console.log(data);
        xhr.send(JSON.stringify(data));
    }
    data['action'] = null;
    refresh();

    likeBtn.addEventListener('change', function(e) {
        console.log(likeBtn.checked);
        if (likeBtn.checked) {
            data['action'] = 'add';
        }
        else {
            data['action'] = 'remove';
        }
        refresh();
    })

    
}