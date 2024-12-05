if (Bun.argv.length != 3) {
  console.error("Provide file name");
  process.exit(1);
}

const file = Bun.file(Bun.argv[2]);

const text = await file.text();

const [block1, block2] = text.split("\n\n");

const rules = [];

for (const line of block1.split('\n')) {
  rules.push(line.split('|').map((e) => parseInt(e)));
}

const books = [];

for (const line of block2.split('\n').filter(Boolean)) {
  const pages = line.split(',').map((e) => parseInt(e));
  const middlePage = pages[(pages.length - 1) / 2];

  const map = new Map(pages.map((e, i) => [e, i]));
  books.push({
    pages,
    middlePage,
    map,
  });
}

let p1 = 0;

const invalidBooks = [];

for (const book of books) {
  const { map, middlePage } = book;

  let valid = true;
  for (const [x, y] of rules) {
    const first = map.get(x);
    if (first === undefined) {
      continue;
    }
    const second = map.get(y);
    if (second === undefined) {
      continue;
    }

    if (first > second) {
      valid = false;
      break;
    }
  }

  if (valid) {
    p1 += middlePage;
  } else {
    invalidBooks.push(book);
  }
}

console.log("p1:", p1);

let p2 = 0;

for (const { map, pages } of invalidBooks) {
  let valid = false;

  while (!valid) {
    valid = true;

    for (const [x, y] of rules) {
      const first = map.get(x);
      if (first === undefined) {
        continue;
      }
      const second = map.get(y);
      if (second === undefined) {
        continue;
      }

      if (first > second) {
        map.set(x, second);
        map.set(y, first);
        valid = false;
        break;
      }
    }
  }

  const middleIndex = (pages.length - 1) / 2;
  p2 += [...map.entries()].filter(([_, value]) => value === middleIndex)[0][0];
}

console.log("p2:", p2);

