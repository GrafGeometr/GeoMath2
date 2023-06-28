// LaTeX highlighting

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

function makeLaTeXArea(elementId) {
    const element = document.getElementById(elementId);

    // highlighting

    element.style.fontFamily = "Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace";

    element.spellcheck = false;
    element.style.zIndex = 1;

    element.style.color = "transparent";
    element.classList.add("bg-transparent");
    element.style.caretColor = "black";


    const highlightArea = document.createElement("pre");
    highlightArea.id = `${elementId}-highlighting`;
    highlightArea.ariaHidden = "true";

    highlightArea.classList.add("p-4", "border-slate-200", "border-2", "rounded-lg", "h-full");

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
    latexOutput.classList.add("text-lg", "ml-4", "p-4", "bg-white", "border-2", "border-solid", "border-sky-400", "rounded-lg", "w-1/2");

    element.parentElement.appendChild(latexOutput);

    // place to store images and iframes
    const imgContainer = document.createElement("div");
    imgContainer.id = `${elementId}-img-container`;



    const render = () => {
        var input = document.getElementById(elementId).value;

            var outputElement = document.getElementById(`${elementId}-latex-output`);

            outputElement.innerHTML = "";

            outputElement.appendChild(getRenderedIframe(input));
    }


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

    render();
}

// LaTeX rendering

const getGenerator = (editorType = 'problem') => {
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
                console.log("name: ", name);

                const result = document.createElement('div');


                result.style = "text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;"
                
                /*console.log("Loading image: ", name);
                const img = document.createElement('img');
                img.src = `${window.location.href}/get_image/${name}`;
                img.width = "70%";
                result.appendChild(img);*/

                const cachedImage = localStorage.getItem(name);

                if (cachedImage) {
                    const img = document.createElement('img');
                    img.src = cachedImage;
                    img.style.width = "70%";
                    result.appendChild(img);
                } else {
                    const img = document.createElement('img');
                    img.src = `${window.location.href}/get_image/${name}`;
                    img.style.width = "70%";
                    result.appendChild(img);

                    fetch(`${window.location.href}/get_image/${name}`).then(response => {
                        if (response.status == 200) return response.blob();
                        else throw new Error("Failed to fetch image");
                    }).then(blob => {
                        const reader = new FileReader();
                        reader.onloadend = () => {
                            const imgData = reader.result;
                            localStorage.setItem(name, imgData);
                        }
                        reader.readAsDataURL(blob);
                    })
                }
                
                if (caption) result.appendChild(caption);

                return [result];
            }

            return CustomMacros;
        }())
    });


    generator.KaTeX.__defineMacro('\\neq', '\\mathrel{\\char`≠}');
    generator.KaTeX.__defineMacro('\\ne', '\\mathrel{\\char`≠}');

    return generator;
}

function getRenderedIframe(text) {
    var generator = getGenerator();

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

