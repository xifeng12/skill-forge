#!/usr/bin/env python3
"""
Evolution loop for skill optimization.

This script orchestrates the darwin-style optimization cycle:
1. Score current SKILL.md
2. Identify lowest dimension
3. Generate improvement
4. Apply edit
5. Re-score
6. Keep or revert based on score change

Usage:
    python evolve_loop.py /path/to/skill/directory --rounds 3

This script outputs structured JSON that the calling agent can use
to coordinate the evolution process.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_CONFIG = {
    "auto_rounds": 3,
    "target_score": 80,
    "max_rounds": 10,
    "confirm_mode": "batch",
    "stagnation_limit": 2,
    "commit_prefix": "evolve:"
}


def load_config(skill_dir: Path) -> dict:
    """Load configuration from agents/interface.yaml or use defaults."""
    config_path = skill_dir / "agents" / "interface.yaml"
    if config_path.exists():
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if config and "evolution" in config:
                return {**DEFAULT_CONFIG, **config["evolution"]}
    return DEFAULT_CONFIG


def read_skill_md(skill_dir: Path) -> str:
    """Read SKILL.md content."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    return skill_md.read_text(encoding="utf-8")


def extract_archetype(skill_content: str) -> str:
    """Extract archetype from SKILL.md."""
    lines = skill_content.split("\n")
    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and "archetype:" in line.lower():
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    if "Production" in skill_content:
        return "Production"
    if "Library" in skill_content:
        return "Library"
    return "Scaffold"


def git_commit(skill_dir: Path, message: str) -> bool:
    """Create a git commit for changes in the skill directory."""
    try:
        subprocess.run(
            ["git", "add", "."],
            cwd=skill_dir,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=skill_dir,
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def git_revert(skill_dir: Path) -> bool:
    """Revert the last commit in the skill directory."""
    try:
        subprocess.run(
            ["git", "reset", "--hard", "HEAD~1"],
            cwd=skill_dir,
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def generate_improvement_prompt(skill_content: str, score_result: dict) -> str:
    """Generate prompt for improvement generation."""
    lowest_dim = score_result.get("lowest_dimension", "unknown")
    suggestion = score_result.get("improvement_suggestion", "")
    archetype = score_result.get("archetype", "Scaffold")
    
    return f"""You are a Skill Improvement Specialist. Generate ONE specific improvement for the lowest-scoring dimension.

## Current SKILL.md
```
{skill_content}
```

## Archetype
{archetype}

## Lowest Dimension
{lowest_dim}

## Suggested Improvement
{suggestion}

## Your Task

Generate ONE concrete, minimal improvement that addresses the lowest dimension.
- Focus on the specific issue, not general improvements
- Keep changes minimal and targeted
- Do not expand scope unnecessarily

## Output Format

Return valid JSON:
{{
  "dimension": "{lowest_dim}",
  "improvement_description": "<brief description of what you're changing>",
  "edit_type": "add|update|delete",
  "target_file": "SKILL.md|references/xxx.md|scripts/xxx.py",
  "old_content": "<content to find and replace, or null if adding>",
  "new_content": "<new content to add or replace with>"
}}

Generate the improvement now."""


def generate_evolution_report(history: list, skill_name: str, config: dict) -> str:
    """Generate a human-readable evolution report."""
    if not history:
        return "No rounds completed."
    
    initial = history[0]["score_before"]
    final = history[-1]["score_after"]
    
    kept_rounds = [r for r in history if r.get("kept", False)]
    reverted_rounds = [r for r in history if not r.get("kept", False)]
    
    lines = [
        f"=== Evolution Report: {skill_name} ===",
        "",
        f"Initial score: {initial}",
        f"Final score: {final}",
        f"Improvement: {'+' if final > initial else ''}{final - initial}",
        "",
        f"Rounds: {len(history)} total",
        f"  - Kept: {len(kept_rounds)}",
        f"  - Reverted: {len(reverted_rounds)}",
        "",
        "Round details:"
    ]
    
    for r in history:
        status = "✓ Kept" if r.get("kept", False) else "✗ Reverted"
        delta = r["score_after"] - r["score_before"]
        delta_str = f"+{delta}" if delta >= 0 else str(delta)
        lines.append(
            f"  Round {r['round']}: {r['score_before']} → {r['score_after']} ({delta_str}) {status}"
        )
        lines.append(f"    - Targeted: {r.get('dimension_targeted', 'unknown')}")
        lines.append(f"    - Change: {r.get('improvement', 'N/A')}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run evolution loop for skill optimization")
    parser.add_argument("skill_dir", type=str, help="Path to skill directory")
    parser.add_argument("--rounds", type=int, default=None, help="Number of rounds to run")
    parser.add_argument("--target", type=int, default=None, help="Target score percentage")
    parser.add_argument("--config", type=str, default=None, help="Path to config file")
    parser.add_argument("--output", type=str, default=None, help="Output file for evolution history")
    parser.add_argument("--dry-run", action="store_true", help="Output plan without executing")
    args = parser.parse_args()
    
    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"Error: Skill directory not found: {skill_dir}", file=sys.stderr)
        sys.exit(1)
    
    config = load_config(skill_dir)
    if args.rounds:
        config["auto_rounds"] = args.rounds
    if args.target:
        config["target_score"] = args.target
    
    skill_content = read_skill_md(skill_dir)
    archetype = extract_archetype(skill_content)
    skill_name = skill_dir.name
    
    plan = {
        "status": "ready",
        "skill_dir": str(skill_dir),
        "skill_name": skill_name,
        "archetype": archetype,
        "config": config,
        "message": "Evolution loop ready. The calling agent should:",
        "steps": [
            "1. Call Task tool with scoring prompt (blind evaluation)",
            "2. Parse score JSON from sub-agent",
            "3. If score < target, generate improvement",
            "4. Apply improvement via Edit tool",
            "5. Git commit the change",
            "6. Re-score via Task tool",
            "7. If improved: keep; else: git revert",
            "8. Repeat until target reached or max rounds"
        ],
        "scoring_prompt": {
            "note": "Use score_skill.py to generate the prompt, then call Task tool",
            "command": f"python {Path(__file__).parent / 'score_skill.py'} {skill_dir}"
        }
    }
    
    if args.dry_run:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return
    
    history_path = skill_dir / "reports" / "evolution_history.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    
    result = {
        "skill_name": skill_name,
        "archetype": archetype,
        "start_time": datetime.now().isoformat(),
        "config": config,
        "rounds": [],
        "status": "requires_agent_coordination",
        "note": "This script outputs the plan. The calling agent must coordinate scoring and edits."
    }
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Evolution plan written to: {output_path}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
