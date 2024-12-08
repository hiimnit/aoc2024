if (Bun.argv.length != 3) {
  console.error("Provide file name");
  process.exit(1);
}

const file = Bun.file(Bun.argv[2]);

const text = await file.text();

const lines = text.split('\n').filter(Boolean);

const bounds = [lines.length, lines[0].length];

const antennas = new Map<String, Array<[number, number]>>();

for (const [line, row] of lines.map<[String, number]>((e, i) => [e, i])) {
  for (const [char, col] of line.split('').map<[String, number]>((e, i) => [e, i])) {
    if (char === '.') {
      continue;
    }

    const coords = antennas.get(char) ?? [];
    coords.push([row, col]);
    antennas.set(char, coords);
  }
}

const p1 = new Map<number, Set<number>>();
const p2 = new Map<number, Set<number>>();

function inBounds(row: number, col: number): boolean {
  if (row < 0 || row >= bounds[0]) {
    return false;
  }
  if (col < 0 || col >= bounds[1]) {
    return false;
  }
  return true;
}

function addP1(row: number, col: number) {
  if (!inBounds(row, col)) {
    return;
  }

  const cols = p1.get(row);
  if (cols !== undefined) {
    cols.add(col);
    return;
  }
  p1.set(row, new Set([col]));
}

function addP2(row: number, col: number, vx: number, vy: number) {
  while (inBounds(row, col)) {
    const cols = p2.get(row);
    if (cols !== undefined) {
      cols.add(col);
    } else {
      p2.set(row, new Set([col]));
    }

    row += vx;
    col += vy;
  }
}

for (const [_, coords] of antennas.entries()) {
  for (let i = 0; i < coords.length; ++i) {
    for (let j = i + 1; j < coords.length; ++j) {
      const vx = coords[j][0] - coords[i][0];
      const vy = coords[j][1] - coords[i][1];

      addP1(coords[i][0] - vx, coords[i][1] - vy);
      addP1(coords[j][0] + vx, coords[j][1] + vy);

      addP2(coords[i][0], coords[i][1], -vx, -vy);
      addP2(coords[j][0], coords[j][1], vx, vy);
    }
  }
}

console.log("p1:", p1.values().reduce((e, cols) => e + cols.size, 0));
console.log("p2:", p2.values().reduce((e, cols) => e + cols.size, 0));

