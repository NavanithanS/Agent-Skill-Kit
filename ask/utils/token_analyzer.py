"""Token analysis utilities for skill optimization."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Try to import tiktoken, fallback to estimation if not available
try:
    import tiktoken
    _encoder = tiktoken.get_encoding("cl100k_base")
    HAS_TIKTOKEN = True
except ImportError:
    _encoder = None
    HAS_TIKTOKEN = False


def count_tokens(text: str) -> int:
    """
    Count tokens in text using tiktoken (cl100k_base encoding).
    
    Falls back to word-based estimation if tiktoken is not installed.
    """
    if HAS_TIKTOKEN and _encoder:
        return len(_encoder.encode(text))
    # Fallback: rough estimation (1 token ≈ 4 chars for English)
    return len(text) // 4


def analyze_skill(skill_path: Path) -> Dict:
    """
    Analyze a SKILL.md file for token count and schema compliance.
    
    Returns dict with:
        - name: skill name
        - path: file path
        - tokens: token count
        - bytes: file size
        - status: 'ok', 'warning', or 'error'
        - issues: list of schema violations
    """
    if not skill_path.exists():
        return {"error": f"File not found: {skill_path}"}
    
    content = skill_path.read_text(encoding="utf-8")
    tokens = count_tokens(content)
    
    # Determine status based on token count
    if tokens <= 500:
        status = "ok"
    elif tokens <= 700:
        status = "warning"
    else:
        status = "error"
    
    # Check for schema compliance
    issues = _check_schema_compliance(content)
    
    return {
        "name": skill_path.parent.name,
        "path": str(skill_path),
        "tokens": tokens,
        "bytes": len(content.encode("utf-8")),
        "status": status,
        "issues": issues,
    }


def _check_schema_compliance(content: str) -> List[Tuple[str, str]]:
    """
    Check SKILL.md content for schema violations.
    
    Returns list of (severity, message) tuples.
    Severity: 'critical' (blocks strict mode), 'warning' (informational)
    """
    issues = []
    
    # Check for required <critical_constraints> block (critical)
    if "<critical_constraints>" not in content:
        issues.append(("critical", "Missing <critical_constraints> block"))
    
    # Check for polite/verbose language patterns (critical)
    verbose_patterns = [
        (r"\bplease\b", "Contains 'please' - remove polite language"),
        (r"\bit is important to\b", "Contains 'it is important to' - simplify"),
        (r"\bwe recommend\b", "Contains 'we recommend' - use ✅ MUST instead"),
        (r"\byou should\b", "Contains 'you should' - use ✅ MUST instead"),
        (r"\bconsider using\b", "Contains 'consider using' - be directive"),
    ]
    
    for pattern, message in verbose_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(("critical", message))
    
    # Check for long paragraphs (informational only, does not block)
    paragraphs = content.split("\n\n")
    for para in paragraphs:
        sentences = len(re.findall(r"[.!?]+", para))
        if sentences > 3 and not para.strip().startswith("```"):
            issues.append(("warning", "Contains paragraph with >3 sentences - consider breaking up"))
            break
    
    return issues


def generate_report(skills_dir: Path) -> Tuple[str, Dict]:
    """
    Generate a token analysis report for all skills.
    
    Returns:
        - Formatted report string
        - Summary dict with totals
    """
    results = []
    
    for skill_md in skills_dir.rglob("SKILL.md"):
        analysis = analyze_skill(skill_md)
        if "error" not in analysis:
            category = skill_md.parent.parent.name
            analysis["category"] = category
            results.append(analysis)
    
    # Sort by tokens descending
    results.sort(key=lambda x: -x["tokens"])
    
    # Build report
    lines = []
    lines.append("Category   | Skill Name                     | Tokens | Status")
    lines.append("-----------|--------------------------------|--------|-------")
    
    total_tokens = 0
    ok_count = 0
    warning_count = 0
    error_count = 0
    
    for r in results:
        total_tokens += r["tokens"]
        status_icon = {"ok": "✅", "warning": "⚠️", "error": "🔴"}[r["status"]]
        
        if r["status"] == "ok":
            ok_count += 1
        elif r["status"] == "warning":
            warning_count += 1
        else:
            error_count += 1
        
        lines.append(
            f"{r['category']:10} | {r['name']:30} | {r['tokens']:6} | {status_icon}"
        )
    
    lines.append("-----------|--------------------------------|--------|-------")
    lines.append(f"Total: {len(results)} skills | {total_tokens} tokens | Avg: {total_tokens // max(len(results), 1)}")
    lines.append(f"✅ OK: {ok_count} | ⚠️ Warning: {warning_count} | 🔴 Error: {error_count}")
    
    summary = {
        "total_skills": len(results),
        "total_tokens": total_tokens,
        "average_tokens": total_tokens // max(len(results), 1),
        "ok_count": ok_count,
        "warning_count": warning_count,
        "error_count": error_count,
        "results": results,
    }
    
    return "\n".join(lines), summary


def lint_skill(skill_path: Path, strict: bool = False) -> Tuple[bool, List[str]]:
    """
    Lint a single skill file.
    
    Args:
        skill_path: Path to SKILL.md
        strict: If True, critical issues and token warnings are treated as errors
        
    Returns:
        - passed: bool
        - messages: list of issues
    """
    analysis = analyze_skill(skill_path)
    
    if "error" in analysis:
        return False, [analysis["error"]]
    
    messages = []
    passed = True
    
    # Token count check
    if analysis["status"] == "error":
        messages.append(f"❌ Token count {analysis['tokens']} exceeds limit (700)")
        passed = False
    elif analysis["status"] == "warning":
        msg = f"⚠️ Token count {analysis['tokens']} exceeds recommended (500)"
        messages.append(msg)
        if strict:
            passed = False
    
    # Schema issues - handle (severity, message) tuples
    for issue in analysis["issues"]:
        if isinstance(issue, tuple):
            severity, msg = issue
            if severity == "critical":
                messages.append(f"❌ {msg}")
                if strict:
                    passed = False
            else:
                # Informational warnings don't block
                messages.append(f"ℹ️ {msg}")
        else:
            # Legacy format (string only)
            messages.append(f"⚠️ {issue}")
            if strict:
                passed = False
    
    if not messages:
        messages.append(f"✅ {analysis['name']}: {analysis['tokens']} tokens")
    
    return passed, messages
