function changeColor() {
    // make a random color in the format #RRGGBB
    const randomColor = '#' + Math.floor(Math.random()*16777215).toString(16);
    
    // change the background color to random color
    document.body.style.backgroundColor = randomColor;
}
