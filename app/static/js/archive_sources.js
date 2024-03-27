function reload(root, data) {
    let possib = new Set();
    for (let el of data) {
        possib.add(el);
    }
    let values = ["olimpiad", "year", "grade", "variant"];
    for (let iter = 0; iter<4; iter++) {
        let cnt_nonhid = 0;
        for (let li of root.children[iter].children) {
            li.classList.remove("hidden");
            let chb = li.children[0];
            if (chb.value == "all") continue;
            found = false;
            for (let el of possib) {
                console.log(iter, values[iter], el[values[iter]], chb.value);
                if (chb.value == el[values[iter]]) {
                    found = true;
                    cnt_nonhid++;
                    break;
                }
            }
            console.log(found, chb);
            if (!found) {
                chb.checked = false;
                chb.parentNode.classList.add("hidden");
            }
            if (!chb.checked) {
                console.log(chb);
                for (let el of possib) {
                    if (chb.value == el[values[iter]]) {
                        possib.delete(el);
                    }
                }
            }
        }
        if (cnt_nonhid == 0) {
            root.children[iter].children[0].classList.add("hidden");
            root.children[iter].children[0].children[0].checked = false;
        }
    }
}

function fill_archive_sources_search() {
    let root = document.getElementById("archive_sources_search");
    root.classList.add("flex", "flex-row", "w-full");
    let olimpiads_ul = document.createElement("ul");
    let years_ul = document.createElement("ul");
    let grades_ul = document.createElement("ul");
    let variants_ul = document.createElement("ul");
    let olimpiads_set = new Set();
    let years_set = new Set();
    let grades_set = new Set();
    let variants_set = new Set();
    root.appendChild(olimpiads_ul);
    root.appendChild(years_ul);
    root.appendChild(grades_ul);
    root.appendChild(variants_ul);

    // get olimpiads list from url params
    let urlParams = new URLSearchParams(window.location.search);
    let olimpiads_in_url = (urlParams.get('olimpiads') || '').split(';');
    let years_in_url = (urlParams.get('years') || '').split(';');
    let grades_in_url = (urlParams.get('grades') || '').split(';');
    let variants_in_url = (urlParams.get('variants') || '').split(';');
    console.log(olimpiads_in_url);
    
    let data;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            data = JSON.parse(xhr.responseText);

            for (let el of data) {
                olimpiads_set.add(el["olimpiad"]);
                years_set.add(el["year"]);
                grades_set.add(el["grade"]);
                variants_set.add(el["variant"]);
            }

            var li = document.createElement("li");
            var chb = document.createElement("input");
            chb.type = "checkbox";
            chb.name = "olimpiads";
            chb.value = "all";
            chb.checked = (olimpiads_in_url.indexOf(chb.value) != -1);
            chb.style.width = "1.25rem";
            chb.style.height = "1.25rem";
            chb.addEventListener("click", function(e) {
                if (e.target.checked) {
                    for (let el of olimpiads_ul.children) {
                        el.children[0].checked = true;
                    }
                }
                else {
                    for (let el of olimpiads_ul.children) {
                        el.children[0].checked = false;
                    }
                }
                reload(root, data);
            })
            li.appendChild(chb);
            li.appendChild(document.createTextNode("Все"));
            olimpiads_ul.appendChild(li);
            for (let el of olimpiads_set) {
                let li = document.createElement("li");
                let chb = document.createElement("input");
                chb.type = "checkbox";
                chb.name = "olimpiads";
                chb.value = el;
                chb.checked = (olimpiads_in_url.indexOf(chb.value) != -1);
                chb.style.width = "1.25rem";
                chb.style.height = "1.25rem";
                chb.addEventListener("click", function(e) {
                    if (e.target.checked) {}
                    else olimpiads_ul.children[0].children[0].checked = false;
                    reload(root, data);
                })
                li.appendChild(chb);
                li.appendChild(document.createTextNode(el));
                olimpiads_ul.appendChild(li);
            }

            li = document.createElement("li");
            chb = document.createElement("input");
            chb.type = "checkbox";
            chb.name = "years";
            chb.value = "all";
            chb.checked = (years_in_url.indexOf(chb.value) != -1);
            chb.style.width = "1.25rem";
            chb.style.height = "1.25rem";
            chb.addEventListener("click", function(e) {
                if (e.target.checked) {
                    for (let el of years_ul.children) {
                        el.children[0].checked = true;
                    }
                }
                else {
                    for (let el of years_ul.children) {
                        el.children[0].checked = false;
                    }
                }
                reload(root, data);
            })
            li.appendChild(chb);
            li.appendChild(document.createTextNode("Все"));
            years_ul.appendChild(li);
            for (let el of years_set) {
                let li = document.createElement("li");
                let chb = document.createElement("input");
                chb.type = "checkbox";
                chb.name = "years";
                chb.value = el;
                chb.checked = (years_in_url.indexOf(chb.value) != -1);
                chb.style.width = "1.25rem";
                chb.style.height = "1.25rem";
                chb.addEventListener("click", function(e) {
                    if (e.target.checked) {}
                    else years_ul.children[0].children[0].checked = false;
                    reload(root, data);
                })
                li.appendChild(chb);
                li.appendChild(document.createTextNode(el));
                years_ul.appendChild(li);
            }

            li = document.createElement("li");
            chb = document.createElement("input");
            chb.type = "checkbox";
            chb.name = "grades";
            chb.value = "all";
            chb.checked = (grades_in_url.indexOf(chb.value) != -1);
            chb.style.width = "1.25rem";
            chb.style.height = "1.25rem";
            chb.addEventListener("click", function(e) {
                if (e.target.checked) {
                    for (let el of grades_ul.children) {
                        el.children[0].checked = true;
                    }
                }
                else {
                    for (let el of grades_ul.children) {
                        el.children[0].checked = false;
                    }
                }
                reload(root, data);
            })
            li.appendChild(chb);
            li.appendChild(document.createTextNode("Все"));
            grades_ul.appendChild(li);
            for (let el of grades_set) {
                let li = document.createElement("li");
                let chb = document.createElement("input");
                chb.type = "checkbox";
                chb.name = "grades";
                chb.value = el;
                chb.checked = (grades_in_url.indexOf(chb.value) != -1);
                chb.style.width = "1.25rem";
                chb.style.height = "1.25rem";
                chb.addEventListener("click", function(e) {
                    if (e.target.checked) {}
                    else grades_ul.children[0].children[0].checked = false;
                    reload(root, data);
                })
                li.appendChild(chb);
                li.appendChild(document.createTextNode(el));
                grades_ul.appendChild(li);
            }

            li = document.createElement("li");
            chb = document.createElement("input");
            chb.type = "checkbox";
            chb.name = "variants";
            chb.value = "all";
            chb.checked = (variants_in_url.indexOf(chb.value) != -1);
            chb.style.width = "1.25rem";
            chb.style.height = "1.25rem";
            chb.addEventListener("click", function(e) {
                if (e.target.checked) {
                    for (let el of variants_ul.children) {
                        el.children[0].checked = true;
                    }
                }
                else {
                    for (let el of variants_ul.children) {
                        el.children[0].checked = false;
                    }
                }
                reload(root, data);
            })
            li.appendChild(chb);
            li.appendChild(document.createTextNode("Все"));
            variants_ul.appendChild(li);
            for (let el of variants_set) {
                let li = document.createElement("li");
                let chb = document.createElement("input");
                chb.type = "checkbox";
                chb.name = "variants";
                chb.value = el;
                chb.checked = (variants_in_url.indexOf(chb.value) != -1);
                chb.style.width = "1.25rem";
                chb.style.height = "1.25rem";
                chb.addEventListener("click", function(e) {
                    if (e.target.checked) {}
                    else variants_ul.children[0].children[0].checked = false;
                    reload(root, data);
                })
                li.appendChild(chb);
                li.appendChild(document.createTextNode(el));
                variants_ul.appendChild(li);
            }

            reload(root, data);
        }
    }
    xhr.open('POST', '/autocomplete', true);
    let to_send = {"obj": "olimpiad_variants"}
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(to_send));
}