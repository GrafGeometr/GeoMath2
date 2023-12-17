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
    "=": "=",
    "+": "+",
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
    var neutral = [".", "-", "(", ")", ",", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\\"];
    if (neutral.includes(symbol)) return true;

    return false;
}

function isNonMath(symbol) {
    return !isMath(symbol) && !isNeutral(symbol);
}

function toLatexWord(string) {
    // 1. Char = english letter
    // xi -> x_{i}
    // x25 or x^25 -> x^{25}
    // C60 -> C_{60}
    // 2. Char = russian letter
    // word
    // 3. Char = '.' or ','
    // 3.5 -> $3.5$
    // 4. -> $4$.
    // 5. Char in allMathSymbols (for example ∠)
    // ∠ -> "\\angle " (with space at the end!)

    var latexWord = {"word": "", "type": 1};
    const N = 5;

    if (string.length == 0) return latexWord;
    var c0 = string[0];
    if (c0.match(/[a-z]/)) {
        latexWord["type"] = 0;
        latexWord["word"] = c0;
        if (string.length == 1) return latexWord;
        var underscore = 0;
        var upperscore = 0;
        for (var i = 1; i < string.length; i++) {
            if (string[i] == '_') {
                underscore = 1;
                upperscore = 0;
                latexWord["word"] += "_{";
                continue;
            }
            if (string[i] == '^') {
                upperscore = 1;
                underscore = 0;
                latexWord["word"] += "^{";
                continue;
            }
            if (string[i].match(/[0-9]/) && (!upperscore)) {
                upperscore = 1;
                underscore = 0;
                latexWord["word"] += "^{";
            }
            if (string[i].match(/[a-z]/)) {
                if (underscore || upperscore) {
                    latexWord["word"] += "}";
                    underscore = 0;
                    upperscore = 0;
                }
                else {
                    underscore = 1;
                    upperscore = 0;
                    latexWord["word"] += "_{";
                }
            }
            
            if (upperscore && string[i].match(/[a-z]/)) {
                upperscore = 0;
                latexWord["word"] += "}";
            }
            latexWord["word"] += string[i];
        }
        if (underscore || upperscore) latexWord["word"] += "}";
        return latexWord;
    }
    if (c0.match(/[A-Z]/)) {
        latexWord["type"] = 0;
        latexWord["word"] = c0;
        if (string.length == 1) return latexWord;
        var underscore = 0;
        var upperscore = 0;
        for (var i = 1; i < string.length; i++) {
            if (string[i] == '_') {
                underscore = 1;
                upperscore = 0;
                latexWord["word"] += "_{";
                continue;
            }
            if (string[i] == '^') {
                upperscore = 1;
                underscore = 0;
                latexWord["word"] += "^{";
                continue;
            }
            if (string[i].match(/[0-9a-z]/) && (!underscore)) {
                underscore = 1;
                latexWord["word"] += "_{";
            }
            if (underscore && string[i].match(/[A-Z]/)) {
                underscore = 0;
                latexWord["word"] += "}";
            }
            if (upperscore && string[i].match(/[A-Z]/)) {
                upperscore = 0;
                latexWord["word"] += "}";
            }
            latexWord["word"] += string[i];
        }
        if (underscore || upperscore) latexWord["word"] += "}";
        return latexWord;
    }
    for (var i = 0; i < string.length; i++) {
        // The longest substr from allMathSymbols that starts in string[i]
        for (var l = N; l > 0; l--) {
            if (i + l > string.length) continue;
            char = string.slice(i, i + l);
            if (isMath(char)) {
                if (latexWord["type"] == 1) latexWord["type"] = 0;
                if (char in allMathSymbols) {
                    latexWord["word"] += allMathSymbols[char] + " ";
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

    const N = 5;
    string_new = "";
    for (var i = 0; i < string.length; i++) {
        // The longest substr from allMathSymbols that starts in string[i]
        for (var l = N; l > 0; l--) {
            if (i + l > string.length) continue;
            char = string.slice(i, i + l);
            if (char in allMathSymbols) {
                string_new += " " + char + " ";
                i += l - 1;
                break;
            }
            else if (l == 1) string_new += char;
        }
    }
    string = string_new;

    delimiters = Array(string.length).fill(0);
    for (var i = 0; i < string.length; i++) {
        if (string[i] == ' ' || string[i] == '$') {
            delimiters[i] = 1;
            continue;
        }
        if (string[i] == '.' || string[i] == ',') {
            if (i == 0 || (!string[i-1].match(/[0-9]/))) delimiters[i] = 1;
            if (i == string.length - 1 || (!string[i+1].match(/[0-9]/))) delimiters[i] = 1;
        }
    }

    words = [];
    for (var i = 0; i < string.length; i++) {
        if (string[i] == '$') {
            if (i < string.length - 1 && string[i+1] == '$') {words.push([i, i+2, 3, "$$"]); i++}
            else words.push([i, i+1, 3, "$"]);
            continue;
        }
        if ((!delimiters[i]) && (i == 0 || delimiters[i-1])) {
            words.push([i, -1, 1, ""]);
            /* [
                start_index (int)
                end_index (int)
                type (int):
                    0 - math
                    1 - neutral
                    2 - nonmath
                    3 - $
                word (string) = string[start:end)
            ]*/
        }
        if ((!delimiters[i]) && (i == string.length - 1 || delimiters[i+1])) {
            words[words.length - 1][1] = i+1;
            var word = string.slice(words[words.length - 1][0], words[words.length - 1][1]);
            var latexWord = toLatexWord(word);
            words[words.length - 1][3] = latexWord["word"];
            words[words.length - 1][2] = latexWord["type"];
        }
        if (delimiters[i]) {
            if (string[i] == " ") words.push([i, i+1, 1, ""]);
            else words.push([i, i+1, 2, ""]);
            var c = string[i] + " ";
            words[words.length - 1][3] = c;
        }
    }


    var res = "";
    var openedMath = false;
    var sz = words.length;
    var nxtByType = [[sz,sz,sz,sz]];
    for (var i = sz-1; i >=0; i--) {
        if (i == sz-1) nxtByType[sz-1-i][words[i][2]] = i;
        else {
            var last = nxtByType[nxtByType.length-1];
            nxtByType.push([last[0],last[1],last[2],last[3]]);
            nxtByType[sz-1-i][words[i][2]] = i;
            
        }
    }
    nxtByType.reverse();
    nxtByType.push([sz,sz,sz,sz]);

    var last_math_opener = "";
    console.log(words);
    for (var i = 0; i < sz; i++) {
        if (words[i][2] == 3) {
            openedMath = !openedMath;
            res += words[i][3];
            if (openedMath) last_math_opener = words[i][3];
            continue;
        }
        if (words[i][2] == 0) {
            if (!openedMath) {
                res += '$';
                last_math_opener = '$';
                openedMath = true;
            }
            res += words[i][3];
            if (openedMath && nxtByType[i+1][2] == i+1) {
                res += last_math_opener + " ";
                openedMath = false;
            }
        }
        else if (words[i][2] == 1) {
            if (!openedMath && nxtByType[i+1][0] < nxtByType[i+1][2]) {
                res += '$';
                last_math_opener = '$';
                openedMath = true;
            }
            if (words[i][3] != "  ") res += words[i][3];
            if (openedMath && nxtByType[i+1][2] == i+1) {
                res += last_math_opener + " ";
                openedMath = false;
            }
        }
        else {
            res += words[i][3];
        }
        if (i < sz-1 && (i==0 || res[res.length-1] != "$") && (words[i+1][2] != 3) && (!openedMath)) res += " ";
    }

    var res_clear = "";
    for (var i = 0; i < res.length; i++) {
        if (res[i] != " ") res_clear += res[i];
        else {
            if (i != res.length-1 && (![" ", ".", ",", ":", ";"].includes(res[i+1]))) res_clear += " ";
        }
    }
    res = res_clear;
    return res;
}