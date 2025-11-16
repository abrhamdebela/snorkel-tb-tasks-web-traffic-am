function getRandomColor() {
    const random = Math.floor(Math.random() * 16777215);
    return '#' + random.toString(16).padStart(6, '0');
}

document.getElementById('colorButton').addEventListener('click', function () {
    const newColor = getRandomColor();
    document.body.style.backgroundColor = newColor;

    // Calculate brightness
    const r = parseInt(newColor.slice(1, 3), 16);
    const g = parseInt(newColor.slice(3, 5), 16);
    const b = parseInt(newColor.slice(5, 7), 16);
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;

    document.body.style.color = brightness > 128 ? 'black' : 'white';

    const codeDisplay = document.getElementById('colorCode');
    codeDisplay.textContent = `Current color: ${newColor}`;
});
