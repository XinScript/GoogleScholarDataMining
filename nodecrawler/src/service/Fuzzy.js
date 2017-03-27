const fuzzy = require('fast-levenshtein');

const score = fuzzy.get('back','back',{useCollator:true});
console.log(score)
