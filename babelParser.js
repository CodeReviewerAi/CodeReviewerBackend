const babel = require('@babel/parser');

process.stdin.setEncoding('utf8');

let code = '';

process.stdin.on('readable', () => {
  let chunk;
  while ((chunk = process.stdin.read()) !== null) {
    code += chunk;
  }
});

process.stdin.on('end', () => {
  try {
    const ast = babel.parse(code, {
      sourceType: "module",
      plugins: [],
    });
    console.log(JSON.stringify(ast));
  } catch (error) {
    console.error("Parsing error:", error);
  }
});
