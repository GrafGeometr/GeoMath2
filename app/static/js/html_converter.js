function downloadSheet() {
    source = document.getElementById('text_textarea-latex-output').childNodes[0].contentWindow.document.getElementsByTagName('body')[0];
    filename = document.getElementById('sheet_name').innerText + '.png';
    source.style.padding = "2rem";
    html2canvas(source, {
        scale: 3
    }).then(
        function (canvas) {
            source.style.padding = "0";
            link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL()
            link.click();
    });
}