const babel = require('@babel/parser');
const fs = require('fs');

const code = fs.readFileSync(process.argv[2], 'utf8');

try {
  const ast = babel.parse(code, {
    sourceType: "module",
    plugins: [],
  });
  console.log(JSON.stringify(ast));
} catch (error) {
  console.error("Parsing error:", error);
}
