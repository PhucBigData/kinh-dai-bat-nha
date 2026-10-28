
import { parseMarkdown } from './reader/js/parser.js';
import fs from 'fs';
const md = fs.readFileSync('Tap_01/Tap_01_Quyen_05.md', 'utf8');
const html = parseMarkdown(md);
const lines = html.split('
');
console.log('--- FIRST 25 LINES OF RENDERED HTML ---');
console.log(lines.slice(0, 25).join('
'));
