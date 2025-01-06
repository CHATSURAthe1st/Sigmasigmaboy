document.getElementById('solve').addEventListener('click', () => {
    const expression = document.getElementById('expression').value;
    fetch('/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            document.getElementById('result').innerText = `Result: ${data.result}`;
        } else {
            document.getElementById('result').innerText = `Error: ${data.error}`;
        }
    });
});
