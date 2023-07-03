// LaTeX highlighting

function fitContent(input, border=2) {
    input.style.height = "3rem";
    let scHeight = input.scrollHeight;
    input.style.height = `${scHeight+border*2}px`;
}

function update(elementId, text) {
    let result_element = document.getElementById(elementId);
    // Handle final newlines (see article)
    text += "\n\n";
    if (text[text.length - 1] == "\n") {
        text += " ";
    }
    // Update code
    result_element.innerHTML = text.replace(new RegExp("&", "g"), "&amp;").replace(new RegExp("<", "g"), "&lt;"); /* Global RegExp */
    // Syntax Highlight
    Prism.highlightElement(result_element);
}

function sync_scroll(element, resultElementId) {
    /* Scroll result to scroll coords of event - sync with textarea */
    let result_element = document.getElementById(resultElementId);
    // Get and set x and y
    result_element.scrollTop = element.scrollTop;
    result_element.scrollLeft = element.scrollLeft;
}

function check_tab(element, event) {
    let code = element.value;
    if (event.key == "Tab") {
        /* Tab key pressed */
        event.preventDefault(); // stop normal
        let before_tab = code.slice(0, element.selectionStart); // text before tab
        let after_tab = code.slice(element.selectionEnd, element.value.length); // text after tab
        let cursor_pos = element.selectionStart + 1; // where cursor moves after tab - moving forward by 1 char to after tab
        element.value = before_tab + "\t" + after_tab; // add tab char
        // move cursor
        element.selectionStart = cursor_pos;
        element.selectionEnd = cursor_pos;
        update(element.value); // Update text to include indent
    }
}

function makeLaTeXArea(elementId, editorType="problem") {
    console.log(editorType);
    const element = document.getElementById(elementId);

    // highlighting

    element.style.fontFamily = "Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace";

    element.spellcheck = false;
    element.style.zIndex = 1;

    element.style.color = "transparent";

    element.classList.add("bg-transparent");
    element.style.caretColor = "black";
    element.style.overflow = "hidden";
    element.style.whiteSpace = "pre-wrap";
    element.style.overflowWrap = "break-word";


    const highlightArea = document.createElement("pre");
    highlightArea.id = `${elementId}-highlighting`;
    highlightArea.ariaHidden = "true";

    highlightArea.classList.add("p-4", "border-slate-200", "border-2", "rounded-lg", "h-full", "bg-white");

    if (element.classList.contains("hidden")) {
        highlightArea.classList.add("hidden");
    }

    const codeArea = document.createElement("span");
    codeArea.id = `${elementId}-highlighting-content`;
    codeArea.classList.add("language-latex");
    highlightArea.appendChild(codeArea);
    element.parentElement.appendChild(highlightArea);


    highlightArea.style.position = "absolute";
    highlightArea.style.top = element.offsetTop;
    highlightArea.style.left = element.offsetLeft;
    highlightArea.style.width = `${element.offsetWidth}px`;
    highlightArea.style.height = `${element.offsetHeight}px`;

    highlightArea.style.zIndex = 0;
    codeArea.style.zIndex = 0;


    let timeout;

    // create output div
    const latexOutput = document.createElement("div");
    latexOutput.id = `${elementId}-latex-output`;
    latexOutput.classList.add("text-lg", "p-4", "bg-white", "border-2", "border-solid", "border-slate-200", "rounded-lg", "w-1/2");

    element.parentElement.appendChild(latexOutput);
    element.parentElement.classList.add("gap-x-4");


    const render = () => {
        manageAttachments();

        var input = document.getElementById(elementId).value;

        var outputElement = document.getElementById(`${elementId}-latex-output`);

        outputElement.innerHTML = "";

        outputElement.appendChild(getRenderedIframe(input, elementId, editorType));
    }

    renderAreas[elementId] = render;


    element.addEventListener("input", event => {
        if (event.data && event.data.length === 1) {
            const brackets = [["(", ")"], ["[", "]"], ["{", "}"], ["$", "$"]];
            for (let i = 0; i < brackets.length; i++) {
                let openBracket = brackets[i][0];
                closeBracket = brackets[i][1];
                if (event.data == closeBracket && element.value.length != element.selectionStart && element.value[element.selectionStart] == closeBracket) {
                    const start = element.selectionStart;
                    const end = element.selectionEnd;
                    element.value = element.value.slice(0, start - 1) + element.value.slice(start, element.value.length);
                    element.selectionStart = start;
                    element.selectionEnd = end;
                } else
                    if (event.data == openBracket) {
                        const start = element.selectionStart;
                        const end = element.selectionEnd;
                        element.value = element.value.slice(0, start) + closeBracket + element.value.slice(start, element.value.length);
                        element.selectionStart = start;
                        element.selectionEnd = end;
                    }
            }
        }
        let text = event.target.value;

        update(`${elementId}-highlighting-content`, text);
        sync_scroll(element, `${elementId}-highlighting`);

        clearTimeout(timeout);
        timeout = setTimeout(render, 500);

        fitContent(element, 2);
    })

    element.addEventListener("scroll", event => {
        sync_scroll(element, `${elementId}-highlighting`);
    })

    element.addEventListener("keydown", event => {
        check_tab(element, event);
    })

    const observer = new ResizeObserver(entries => {
        highlightArea.style.width = `${element.offsetWidth}px`;
        highlightArea.style.height = `${element.offsetHeight}px`;
    });

    observer.observe(element);

    update(`${elementId}-highlighting-content`, element.value);
    sync_scroll(element, `${elementId}-highlighting`);

    setTimeout(render, 500);

    fitContent(element, 2);
}

// LaTeX rendering


const getGenerator = (inputElementId = null, editorType = 'problem') => {
    const generator = new latexjs.HtmlGenerator({
        CustomMacros: (function () {
            var args = CustomMacros.args = {},
                prototype = CustomMacros.prototype;

            function CustomMacros(generator) {
                this.g = generator;
            }

            args['bf'] = ['V', 'u']
            prototype['bf'] = function (arg) {
                var res = getRenderedIframe("Some \\LaTeX text and formules $\\frac{a}{b}$ ");
                // const res = 
                return [res]
            };

            args['img'] = ['V', 'o?', 'k'];
            prototype['img'] = function (caption, name) {
                // make request to current/url/get_image/name

                const result = document.createElement('div');


                result.style = "text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 1rem; row-gap: 0.5rem";


                const imgFilename = attachmentDbFilenameByName(name);

                const cachedImage = localStorage.getItem(imgFilename);

                if (cachedImage) {
                    const img = document.createElement('img');
                    img.src = cachedImage;
                    img.style.width = "70%";
                    img.style.margin = "0.5rem 0";
                    result.appendChild(img);
                } else {
                    const img = document.createElement('span');
                    img.innerHTML = "Ошибка при загрузке картинки, проверьте название";
                    img.style.color = "red";
                    result.appendChild(img);

                    const href = `${window.location.origin}/get_image/${imgFilename}`;
                    requestsSet.add(href);

                    fetch(href).then(response => {
                        if (response.status == 200) return response.blob();
                        else throw new Error("Failed to fetch image");
                    }).then(blob => {
                        const reader = new FileReader();
                        reader.onloadend = () => {
                            const imgData = reader.result;
                            localStorage.setItem(imgFilename, imgData);
                            if (requestsSet.has(href)) {
                                requestsSet.delete(href);
                                if (requestsSet.size == 0) {
                                    console.log(inputElementId);
                                    toReRenderList.push(inputElementId);
                                }
                            }
                        }
                        reader.readAsDataURL(blob);
                    })
                }

                if (caption) result.appendChild(caption);

                return [result];
            }
            
            args['includeproblem'] = ['V', 'k?', 'k', 'k?'];
            prototype['includeproblem'] = function (parts, problem_hashed_id, comment) {
                if (editorType == 'sheet') {
                    if (!parts) parts = "";
                    parts = parts.split(/\s+/);
                    parts = parts.map(p => p.trim()).filter(p => p.length > 0);
                    console.log("problem_hashed_id: ", problem_hashed_id);
                    console.log("parts: ", parts);

                    if (!(problem_hashed_id in problemList)){
                        const href = `${window.location.origin}/get_problem_content/${problem_hashed_id}`;
                        requestsSet.add(href);
                        fetch(`${href}`).then(response => {
                            if (response.status == 200) return response.json();
                            else throw new Error("Failed to fetch problem");
                        }).then(json => {
                            problemList[problem_hashed_id] = json;
                            if (requestsSet.has(href)) {
                                requestsSet.delete(href);
                                if (requestsSet.size == 0) {
                                    console.log(inputElementId);
                                    toReRenderList.push(inputElementId);
                                }
                            }
                        });

                        return [document.createElement('p', "Loading problem...")];
                    }
                    return [renderProblem(comment, problemList[problem_hashed_id], parts, "inplace", inputElementId)];
                }
                else {
                    const element = document.createElement('p');
                    element.innerHTML = "Упс! Задачу можно прикреплять только к подборке";
                    element.style.color = "red";
                    return [element];
                }
            }

            return CustomMacros;
        }())
    });


    generator.KaTeX.__defineMacro('\\neq', '\\mathrel{\\char`≠}');
    generator.KaTeX.__defineMacro('\\ne', '\\mathrel{\\char`≠}');

    return generator;
}

function getRenderedIframe(text, inputElementId = null, editorType = 'problem') {
    var generator = getGenerator(inputElementId, editorType);

    generator = latexjs.parse(text, { generator: generator });

    const result = generator.htmlDocument(baseURL = "https://cdn.jsdelivr.net/npm/latex.js/dist/");

    const iframe = document.createElement('iframe');

    iframe.classList.add("latex-iframe");
    iframe.style = "width: 100%; justify-content: flex-start; display: flex; align-items: flex-start;";
    

    iframe.style.border = "0";
    iframe.scrolling = "no";


    result.documentElement.style = "";
    result.documentElement.style.marginRight = '5%';
    result.documentElement.style.marginLeft = '5%';
    result.documentElement.style.fontSize = '1.25rem';
    result.documentElement.style.margin = '0';
    result.documentElement.style.padding = '0';

    result.documentElement.children[1].children[0].classList.remove('body');

    iframe.srcdoc = result.documentElement.outerHTML;

    const fixSize = ((iframe) => {
        iframe.height = `${(iframe.contentWindow.document.body).scrollHeight}px`;
    })

    const work = iframe => {
        try {
            for (newIframe of iframe.contentWindow.document.body.children[0].querySelectorAll('iframe')) {
                if (newIframe.classList.contains('latex-iframe')) {
                    work(newIframe);
                }
            }
            fixSize(iframe);
        } catch (e) {
            iframe.addEventListener('load', () => {
                for (newIframe of iframe.contentWindow.document.body.children[0].querySelectorAll('iframe')) {
                    if (newIframe.classList.contains('latex-iframe')) {
                        work(newIframe);
                    }
                }
                fixSize(iframe);
            })
        }
    }

    work(iframe);

    return iframe;
}

var renderAreas = {}; // input_area_id -> render_function
var toReRenderList = [];
var requestsSet = new Set();

function checkReRender() {
    while (toReRenderList.length > 0) {
        const id = toReRenderList.pop();
        console.log(id);
        renderAreas[id]();
    }
}

setInterval(checkReRender, 500);

// images management -- db_filename -> preview_name (preview_name -> first db_filename)

var imageNameList = [];

function manageAttachments() {
    imageNameList = [];

    const attNameFields = document.querySelectorAll('.input-attachment-name');
    for (let i = 0; i < attNameFields.length; i++) {
        manageAttachment(attNameFields[i]);
    }
}

function manageAttachment(element) {
    const attachmentDbFilename = element.id.split("attachment-name-")[1];
    attachmentName = element.value;

    imageNameList.push([attachmentDbFilename, attachmentName]);

    element.addEventListener("input", event => {
        const attachmentDbFilename = element.id.split("attachment-name-")[1];
        attachmentName = element.value;

        for (let i = 0; i < imageNameList.length; i++) {
            if (imageNameList[i][0] == attachmentDbFilename) {
                imageNameList[i][1] = attachmentName;
            }
        }
    })
}


function attachmentDbFilenameByName(name) {
    for (let i = 0; i < imageNameList.length; i++) {
        if (imageNameList[i][1] == name) {
            return imageNameList[i][0];
        }
    }
    return null;
}


var problemList = {};

// problem_hashed_id -> {'name': ..., 'statement': ..., 'solution': ..., 'files': [['file_short_name', 'file_db_filename']], 'tags': [...]}


function renderProblem(additional, json, args, mode = "inplace", inputElementId = null) {
    if (mode == "inplace") {
        if (args.length == 0) args = ['statement'];
        var toRender = '';
        if (additional) toRender += `\\textbf{ ${additional}. } `;
        if (args.includes('name')) toRender += `\\textbf{ ${json['name']} } `;
        if (args.includes('statement')) toRender += json['statement'];
        if (args.includes('solution')) toRender += `\n\n${json['solution']}`;
        if (args.includes('tags')) toRender += `\n\n${json['tags'].map(t => `\\footnotesize{\\textit{ \\# ${t} }}`).join('\n')}`;
        toRender = toRender.replace('#', '\\#');
        console.log(toRender);

        var oldImageNameList = imageNameList;
        imageNameList = [];
        for (let i = 0; i < json['files'].length; i++) {
            imageNameList.push([json['files'][i][1], json['files'][i][0]]);
        }
        const result = getRenderedIframe(toRender, inputElementId, 'problem');
        imageNameList = oldImageNameList;
        return result;
    }
}

