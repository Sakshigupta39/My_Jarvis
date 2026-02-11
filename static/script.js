async function sendCommand() {
    const command = document.getElementById('command').value;
    const response = await fetch('/speak', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: command })
    });
  
    const data = await response.json();
    document.getElementById('response').innerText = "JARVIS: " + data.response;
  }
  