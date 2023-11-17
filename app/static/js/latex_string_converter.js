var allMathSymbols = {};
var greekLetters = {
    "α": "\\alpha",
    "β": "\\beta",
    "γ": "\\gamma", "Γ": "\\Gamma",
    "δ": "\\delta", "Δ": "\\Delta",
    "ϵ": "\\epsilon", "ε": "\\varepsilon",
    "ζ": "\\zeta",
    "η": "\\eta",
    "θ": "\\theta", "𝜗": "\\vartheta", "Θ": "\\Theta",
    "ι": "\\iota",
    "κ": "\\kappa",
    "λ": "\\lambda", "Λ": "\\Lambda",
    "μ": "\\mu",
    "ν": "\\nu",
    "ξ": "\\xi", "Ξ": "\\Xi",

    "π": "\\pi", "Π": "\\Pi",
    "ρ": "\\rho", "ϱ": "\\varrho",
    "σ": "\\sigma", "Σ": "\\Sigma",
    "τ": "\\tau",
    "υ": "\\upsilon", "Υ": "\\Upsilon",
    "ϕ": "\\phi", "φ": "\\varphi", "Φ": "\\Phi",
    "χ": "\\chi",
    "ψ": "\\psi", "Ψ": "\\Psi",
    "ω": "\\omega", "Ω": "\\Omega"
}
var arrows = {
    "←": "\\leftarrow",
    "↑": "\\uparrow",
    "→": "\\rightarrow",
    "↓": "\\downarrow",
    "↔": "\\leftrightarrow",
    "↕": "\\updownarrow",
    "⇐": "\\Leftarrow",
    "⇑": "\\Uparrow",
    "⇒": "\\Rightarrow",
    "⇓": "\\Downarrow",
    "⇔": "\\Leftrightarrow",
    "⇕": "\\Updownarrow",
    "↦": "\\mapsto"
}
var binaryOperators = {
    "+": "+",
    "=": "=",
    "/": "/",
    "×": "\\times",
    "÷": "\\div",
    "±": "\\pm",
    "∓": "\\mp",
    "·": "\\cdot",
    "⋅": "\\cdot",
    "∘": "^\\circ",
    "°": "^\\circ",
    "∪": "\\cup",
    "∩": "\\cap",
    "⊂": "\\subset",
    "⊃": "\\supset",
    "⊆": "\\subseteq",
    "⊇": "\\supseteq",
    "⊕": "\\oplus",
    "⊗": "\\otimes",
    "≤": "\\leq",
    "≥": "\\geq",
    "≡": "\\equiv",
    "||": "\\parallel",
    "⊥": "\\bot",
    "≈": "\\approx"
}
var unaryOperators = {
    "√": "\\sqrt",
    "∠": "\\angle",
    "∞": "\\infty",
    "∫": "\\int",
    "∫∫": "\\iint",
    "∫∫∫": "\\iiint",
    "∮": "\\oint",
    "∮∮": "\\oiiint",
    "∮∮∮": "\\oiint",
    "$": "\\$",
    "{": "\\{",
    "}": "\\}",
    "\\": "\\"
}

for (symbol in greekLetters) allMathSymbols[symbol] = greekLetters[symbol];
for (symbol in arrows) allMathSymbols[symbol] = arrows[symbol];
for (symbol in binaryOperators) allMathSymbols[symbol] = binaryOperators[symbol];
for (symbol in unaryOperators) allMathSymbols[symbol] = unaryOperators[symbol];



function isLetterEn(symbol) {
    return symbol.length == 1 && symbol.match(/[a-zA-Z]/);
}
function isLetterRu(symbol) {
    return symbol.length == 1 && symbol.match(/[а-яА-Я]/);
}


function isMath(symbol) {
    if (symbol in allMathSymbols) return true;
    if (isLetterEn(symbol)) return true;
    
    return false;
}
function isNeutral(symbol) {
    var neutral = [".", "-", "(", ")", ",", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
    if (symbol in neutral) return true;

    return false;
}

function isNonMath(symbol) {
    return !isMath(symbol) && !isNeutral(symbol);
}

function toLatexWord(string) {
    var latexWord = {"word": "", "type": 1};
    const N = 5;
    for (var i = 0; i < string.length; i++) {
        // The longest substr from allMathSymbols that starts in string[i]
        for (var l = N; l > 0; l--) {
            if (i + l > string.length) continue;
            char = string.slice(i, i + l);
            if (isMath(char)) {
                if (latexWord["type"] == 1) latexWord["type"] = 0;
                if (char in allMathSymbols) {
                    latexWord["word"] += allMathSymbols[char];
                }
                else if (isLetterEn(char)) {
                    latexWord["word"] += char;
                }
                i += l - 1;
                break;
            }
            else if (isNeutral(char)) {
                latexWord["word"] += char;
                i += l - 1;
                break;
            }
            else if (l == 1) {
                if (latexWord["type"] == 1) latexWord["type"] = 2;
                latexWord["word"] += char;
                i += l - 1;
                break;
            }
        }
    }
    return latexWord;
}

function toLatex(string) {
    string = string.replace(/(\r\n|\n|\r)/gm, " ");
    words = [];
    for (var i = 0; i < string.length; i++) {
        if (string[i] == ' ') {
            res += ' ';
            continue;
        }
        if (string[i] != ' ' && (i == 0 || string[i - 1] == ' ')) {
            words.push([i, -1, 1, ""]);
            /* [
                start_index (int)
                end_index (int)
                type (int):
                    0 - math
                    1 - neutral
                    2 - nonmath
                word (string)
            ]*/
        }
        if (string[i] != ' ' && (i == string.length - 1 || string[i + 1] == ' ')) {
            words[words.length - 1][1] = i+1;
            var word = string.slice(words[words.length - 1][0], words[words.length - 1][1]);
            var latexWord = toLatexWord(word);
            words[words.length - 1][3] = latexWord["word"];
            words[words.length - 1][2] = latexWord["type"];
        }
    }
    var res = "";
    var openedMath = false;
    var sz = words.length;
    var nxtByType = [[sz,sz,sz]];
    for (var i = sz-1; i >=0; i--) {
        if (i == sz-1) nxtByType[sz-1-i][words[i][2]] = i;
        else {
            var last = nxtByType[nxtByType.length-1];
            nxtByType.push([last[0],last[1],last[2]]);
            nxtByType[sz-1-i][words[i][2]] = i;
            
        }
    }
    nxtByType.reverse();
    nxtByType.push([sz,sz,sz]);
    for (var i = 0; i < sz; i++) {
        if (words[i][2] == 0) {
            if (!openedMath) {
                res += '$';
                openedMath = true;
            }
            res += words[i][3];
            if (openedMath && nxtByType[i+1][2] == i+1) {
                res += '$';
                openedMath = false;
            }
        }
        else if (words[i][2] == 1) {
            if (!openedMath && nxtByType[i+1][0] <= nxtByType[i+1][2]) {
                res += '$';
                openedMath = true;
            }
            res += words[i][3];
            if (openedMath && nxtByType[i+1][2] == i+1) {
                res += '$';
                openedMath = false;
            }
        }
        else {
            res += words[i][3];
        }
        if (i < sz-1) res += ' ';
    }
    return res;
}