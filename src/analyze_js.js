const fs = require('fs');
const babelParser = require('@babel/parser');

const code = fs.readFileSync(process.argv[2], 'utf8');
const ast = babelParser.parse(code, {sourceType: "module", plugins: ["jsx", "typescript"]});

let functions = new Set();
let classes = new Set();
let imports = new Set();

function traverse(node) {
    if (node.type === "FunctionDeclaration" && node.id) {
        functions.add(node.id.name);
    } else if (node.type === "ClassDeclaration" && node.id) {
        classes.add(node.id.name);
    } else if (node.type === "ImportDeclaration") {
        node.specifiers.forEach(spec => imports.add(spec.local.name));
    }
    for (let key in node) {
        if (node[key] && typeof node[key] === "object") {
            traverse(node[key]);
        }
    }
}

traverse(ast);

console.log(JSON.stringify({functions: Array.from(functions), classes: Array.from(classes), imports: Array.from(imports)}));
