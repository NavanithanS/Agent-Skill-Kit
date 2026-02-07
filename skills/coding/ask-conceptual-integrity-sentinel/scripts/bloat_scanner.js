/**
 * bloat_scanner.js
 * Identifies "Slop": Files that are large but have low structural density,
 * or small files that are over-complicated (high token density).
 */
const fs = require('fs');
const path = require('path');

// Recursive function to get all files in a directory
function getAllFiles(dirPath, arrayOfFiles) {
    files = fs.readdirSync(dirPath);

    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function (file) {
        if (fs.statSync(dirPath + "/" + file).isDirectory()) {
            if (file !== 'node_modules' && file !== '.git' && file !== 'dist') {
                arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles);
            }
        } else {
            arrayOfFiles.push(path.join(dirPath, "/", file));
        }
    });

    return arrayOfFiles;
}

// Simple heuristic: "Tokens per Line" and "Brackets per Line"
function analyzeFile(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n').filter(l => l.trim().length > 0).length;

        // Count control structures (proxy for complexity)
        const complexityTokens = (content.match(/if|for|while|switch|class|function|=>/g) || []).length;

        // Heuristic: Abstraction Bloat
        // High file size + Low complexity = "Boilerplate/Slop"
        // Low file size + Extreme complexity = "Code Golf/Unreadable"
        const ratio = complexityTokens / (lines || 1);

        return {
            file: filePath,
            lines: lines,
            complexity: complexityTokens,
            ratio: ratio.toFixed(2),
            // Flag if < 0.1 (likely verbose boilerplate) or > 0.8 (too dense)
            isBloat: ratio < 0.1 && lines > 50,
            isDense: ratio > 0.8 && lines > 10
        };
    } catch (err) {
        return null;
    }
}

function main() {
    const rootDir = process.cwd();
    const files = getAllFiles(rootDir);
    const results = [];

    files.forEach(file => {
        if (file.endsWith('.js') || file.endsWith('.ts') || file.endsWith('.jsx') || file.endsWith('.tsx')) {
            const analysis = analyzeFile(file);
            if (analysis) {
                results.push(analysis);
            }
        }
    });

    console.log("--------------------------------------------------");
    console.log("BLOAT SCAN REPORT");
    console.log("--------------------------------------------------");
    console.log("File | Lines | Complexity | Ratio | Status");
    console.log("--------------------------------------------------");

    results.forEach(r => {
        let status = "OK";
        if (r.isBloat) status = "BLOAT (Low Density)";
        if (r.isDense) status = "DENSE (Too Complex)";

        if (status !== "OK") {
            console.log(`${path.relative(rootDir, r.file)} | ${r.lines} | ${r.complexity} | ${r.ratio} | ${status}`);
        }
    });
    console.log("--------------------------------------------------");
}

main();
