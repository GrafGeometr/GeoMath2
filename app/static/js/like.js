function likeButtons() {
    var likeDivs = document.getElementsByClassName("like");
    for (var i = 0; i < likeDivs.length; i++) {
        let likeDiv = likeDivs[i];
        let list = likeDiv.id.split("like-")[1].split("-");
        let data = {"parent_type": list[0], "parent_id": list[1]};
        likeButton(likeDiv, data);
    }
}

function likeButton(likeDiv, data) {
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

    likeDiv.appendChild(likeCnt);

    let dislikeLabel = document.createElement('label');
    likeDiv.appendChild(dislikeLabel);

    let dislikeBtn = document.createElement('input');
    dislikeBtn.type = 'checkbox';
    dislikeBtn.classList.add("hidden");
    dislikeLabel.appendChild(dislikeBtn);
   
    let dislikeIcon = document.createElement('img');
    dislikeIcon.src = '/static/images/dislike.svg';
    dislikeIcon.classList.add("w-8", "hover:cursor-pointer");
    dislikeLabel.appendChild(dislikeIcon);

    let dislikeCnt = document.createElement('span');
    dislikeCnt.classList.add("font-bold", "text-lg");

    likeDiv.appendChild(dislikeCnt);

    function refresh() {
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'json';
        xhr.open('POST', '/like', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let check = this.response["check"];
                let cnt_likes = this.response["cnt_likes"];
                let cnt_dislikes = this.response["cnt_dislikes"];

                likeIcon.src = (check == true) ? '/static/images/like_active.svg' : '/static/images/like.svg';
                likeBtn.checked = (check == true);

                dislikeIcon.src = (check == false) ? '/static/images/dislike_active.svg' : '/static/images/dislike.svg';
                dislikeBtn.checked = (check == false);

                likeCnt.innerHTML = cnt_likes;
                dislikeCnt.innerHTML = cnt_dislikes;
            }
        }
        console.log(data);
        xhr.send(JSON.stringify(data));
    }
    data['action'] = null;
    refresh();

    likeBtn.addEventListener('change', function(e) {
        if (likeBtn.checked) {
            data['action'] = 'add_like';
        }
        else {
            data['action'] = 'remove';
        }
        refresh();
    })

    dislikeBtn.addEventListener('change', function(e) {
        if (dislikeBtn.checked) {
            data['action'] = 'add_dislike';
        }
        else {
            data['action'] = 'remove';
        }
        refresh();
    })
}