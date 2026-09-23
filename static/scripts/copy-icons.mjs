// Копирует нужные иконки из lucide-static и simple-icons в templates/icons/.
// Список — в static/icons.txt. Запуск: npm run icons
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, '..', 'templates', 'icons');
mkdirSync(out, {recursive: true});

const names = readFileSync(join(root, 'icons.txt'), 'utf8')
    .split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#'));

for (const name of names) {
    const brand = name.startsWith('brand:');
    const id = brand ? name.slice(6) : name;
    const src = brand
        ? join(root, 'node_modules', 'simple-icons', 'icons', `${id}.svg`)
        : join(root, 'node_modules', 'lucide-static', 'icons', `${id}.svg`);
    const svg = readFileSync(src, 'utf8');
    // Сохраняем только внутренности <svg>, обёртку рисует тег {% icon %}
    const inner = svg.replace(/<!--[\s\S]*?-->/g, '').replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '')
        .replace(/<title>[\s\S]*?<\/title>/, '').replace(/\n\s*/g, '').trim();
    writeFileSync(join(out, `${brand ? 'brand-' : ''}${id}.svg`), inner + '\n');
}
console.log(`icons: ${names.length}`);
