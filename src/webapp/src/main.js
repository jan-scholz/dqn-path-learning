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
  <button id="trainStep">Train Step</button>
  <div id="grid" class="grid-container"></div>
`

document.getElementById('submitMaze').addEventListener('click', async () => {
  const mazeText = document.getElementById('mazeInput').value;

  try {
    const response = await fetch('/create_maze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ maze: mazeText }),
    });

    await response.json();  // no output shown
  } catch (err) {
    alert(`Maze submission failed: ${err.message}`);
  }
});

document.getElementById('clearMaze').addEventListener('click', () => {
  document.getElementById('mazeInput').value = '';
});

document.getElementById('trainStep').addEventListener('click', async () => {
  try {
    const response = await fetch('/train_step', { method: 'POST' });
    const data = await response.json();
    renderQGrid(data.q_table, data.rows, data.cols);
  } catch (err) {
    alert(`Train step failed: ${err.message}`);
  }
});

function renderQGrid(qTableJSON, rows, cols) {
  const qTable = JSON.parse(qTableJSON);
  const grid = document.getElementById('grid');
  grid.innerHTML = '';  // Clear existing content
  grid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
  grid.style.display = 'grid';
  grid.style.gap = '4px';

  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const cellData = qTable.find(e => e.x === x && e.y === y);
      const q = cellData?.values ?? { up: 0, down: 0, left: 0, right: 0 };

      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.innerHTML = `
        <div class="q-grid">
          <div class="q up">↑ ${q.up.toFixed(1)}</div>
          <div class="q left">← ${q.left.toFixed(1)}</div>
          <div class="q right">→ ${q.right.toFixed(1)}</div>
          <div class="q down">↓ ${q.down.toFixed(1)}</div>
        </div>
      `;
      grid.appendChild(cell);
    }
  }
}
