if (Bun.argv.length != 3) {
  console.error("Provide file name");
  process.exit(1);
}

const file = Bun.file(Bun.argv[2]);

const text = await file.text();

const map = text.split('\n').filter(Boolean).map((e) => e.split('').map(e => parseInt(e)));
const bounds = [map.length, map[0].length];

function findTrail(row: number, col: number, find: number, mem: Set<string>): number {
  if (row < 0 || row >= bounds[0] || col < 0 || col >= bounds[1]) {
    return 0;
  }
  if (map[row][col] !== find) {
    return 0;
  }
  if (find == 9) {
    mem.add(`${row} ${col}`);
    return 1;
  }

  return findTrail(row, col + 1, find + 1, mem)
    + findTrail(row + 1, col, find + 1, mem)
    + findTrail(row, col - 1, find + 1, mem)
    + findTrail(row - 1, col, find + 1, mem);
}

let p1 = 0;
let p2 = 0;

for (let row = 0; row < map.length; ++row) {
  for (let col = 0; col < map[row].length; ++col) {
    if (map[row][col] !== 0) {
      continue;
    }

    const mem = new Set<string>();
    p2 += findTrail(row, col, 0, mem);

    p1 += mem.size;
  }
}

console.log("p1:", p1);
console.log("p2:", p2);
