const fs = require('fs');
const file = fs.readFileSync('frontend/src/components/SkillDetail.jsx', 'utf-8');
const lines = file.split('\n');

// Block 1 (Graphs): lines 156 to 258 (indices 155 to 257)
const block1 = lines.slice(155, 258);

// Block 2 (Recommendations, Weak Topics, Upload Assessment): lines 259 to 343 (indices 258 to 342)
const block2 = lines.slice(258, 343);

const newLines = [
    ...lines.slice(0, 155),
    ...block2,
    ...block1,
    ...lines.slice(343)
];

fs.writeFileSync('frontend/src/components/SkillDetail.jsx', newLines.join('\n'));
console.log('Successfully reordered components!');
