import './style.css'

const exampleMaze = `S . . X G
. X . X .
. . . . .
X X . X .
. . . . .`;

let mazeData = null;

document.querySelector('#app').innerHTML = `
  <h2>Enter Maze</h2>
  <textarea id="mazeInput" rows="6" cols="40">${exampleMaze}</textarea>
  <br/>
  <button id="submitMaze">Submit Maze</button>
  <button id="clearMaze">Clear</button>
  <button id="trainStep">Train Step</button>
  <button id="train10Steps">Train 10 Steps</button>
  <div id="goalMessage" style="display: none; color: green; margin-top: 1rem;">Goal Reached!</div>
  <div id="grid" class="grid-container"></div>
`

document.getElementById('submitMaze').addEventListener('click', async () => {
  const mazeText = document.getElementById('mazeInput').value;
  mazeData = mazeText.split('\n').map(row => row.split(' ').filter(c => c));

  document.getElementById('trainStep').disabled = false;
  document.getElementById('train10Steps').disabled = false;
  document.getElementById('goalMessage').style.display = 'none';

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
  mazeData = null;
  document.getElementById('grid').innerHTML = '';
  document.getElementById('trainStep').disabled = false;
  document.getElementById('train10Steps').disabled = false;
  document.getElementById('goalMessage').style.display = 'none';
});

document.getElementById('trainStep').addEventListener('click', async () => {
  try {
    const response = await fetch('/train_step', { method: 'POST' });
    const data = await response.json();
    renderQGrid(data.q_table, data.rows, data.cols);
    if (data.goal_reached) {
      document.getElementById('goalMessage').innerText = `Goal Reached in ${data.step} steps!`;
      document.getElementById('goalMessage').style.display = 'block';
      document.getElementById('trainStep').disabled = true;
      document.getElementById('train10Steps').disabled = true;
    }
  } catch (err) {
    alert(`Train step failed: ${err.message}`);
  }
});

document.getElementById('train10Steps').addEventListener('click', async () => {
  try {
    let data;
    for (let i = 0; i < 10; i++) {
      const response = await fetch('/train_step', { method: 'POST' });
      data = await response.json();
      if (data.goal_reached) break;
    }
    renderQGrid(data.q_table, data.rows, data.cols);
    if (data.goal_reached) {
      document.getElementById('goalMessage').innerText = `Goal Reached in ${data.step} steps!`;
      document.getElementById('goalMessage').style.display = 'block';
      document.getElementById('trainStep').disabled = true;
      document.getElementById('train10Steps').disabled = true;
    }
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
      const cellType = mazeData && mazeData[y] && mazeData[y][x] ? mazeData[y][x] : '.';

      const cell = document.createElement('div');
      cell.className = 'cell';

      if (cellType === 'S') {
        cell.classList.add('start-cell');
      } else if (cellType === 'G') {
        cell.classList.add('goal-cell');
      } else if (cellType === 'X') {
        cell.classList.add('wall-cell');
      }

      const maxQ = Math.max(q.up, q.down, q.left, q.right);
      let arrow = '';
      if (q.up === maxQ) arrow = '↑';
      else if (q.down === maxQ) arrow = '↓';
      else if (q.left === maxQ) arrow = '←';
      else if (q.right === maxQ) arrow = '→';

      let centerContent = arrow;
      if (cellType === 'S') centerContent = `S ${arrow}`;
      if (cellType === 'G') centerContent = `G ${arrow}`;


      cell.innerHTML = `
        <div class="q-grid">
          <div class="q-subcell"></div>
          <div class="q-subcell q-up">${q.up.toFixed(1)}</div>
          <div class="q-subcell"></div>
          <div class="q-subcell q-left">${q.left.toFixed(1)}</div>
          <div class="q-subcell">${centerContent}</div>
          <div class="q-subcell q-right">${q.right.toFixed(1)}</div>
          <div class="q-subcell"></div>
          <div class="q-subcell q-down">${q.down.toFixed(1)}</div>
          <div class="q-subcell"></div>
        </div>
      `;
      grid.appendChild(cell);
    }
  }
}
