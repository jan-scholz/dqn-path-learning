import './style.css'

const exampleMaze = `S . . X G
. X . X .
. . . . .
X X . X .
. . . . .`;

document.querySelector('#app').innerHTML = `
  <h2>Enter Maze</h2>
  <textarea id="mazeInput" rows="10" cols="40">${exampleMaze}</textarea>
  <br/>
  <button id="submitMaze">Submit Maze</button>
  <button id="clearMaze">Clear</button>
  <div id="response"></div>
`

document.getElementById('submitMaze').addEventListener('click', async () => {
  const mazeText = document.getElementById('mazeInput').value;

  try {
    const response = await fetch('/create_maze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ maze: mazeText }),
    });

    const result = await response.json();
    document.getElementById('response').textContent = `Response: ${JSON.stringify(result, null, 2)}`;
  } catch (err) {
    document.getElementById('response').textContent = `Error: ${err.message}`;
  }
});

document.getElementById('clearMaze').addEventListener('click', () => {
  document.getElementById('mazeInput').value = '';
  document.getElementById('response').textContent = '';
});
