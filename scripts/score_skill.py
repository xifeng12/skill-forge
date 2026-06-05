#!/usr/bin/env python3
"""
Score a skill using sub-agent blind evaluation.

This script:
1. Reads the SKILL.md content
2. Reads the scoring rubric
3. Determines archetype from SKILL.md frontmatter
4. Calls Task tool to spawn a sub-agent for blind scoring
5. Returns the score JSON

Usage:
    python score_skill.py /path/to/skill/directory
"""

import argparse
import json
import sys
from pathlib import Path


def read_skill_md(skill_dir: Path) -> str:
    """Read SKILL.md content."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    return skill_md.read_text(encoding="utf-8")


def extract_archetype(skill_content: str) -> str:
    """Extract archetype from SKILL.md frontmatter or infer from metadata."""
    lines = skill_content.split("\n")

    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and line.startswith("metadata:"):
            continue
        if in_frontmatter and "archetype:" in line.lower():
            return line.split(":", 1)[1].strip().strip('"').strip("'")

    if "Production" in skill_content or "team" in skill_content.lower():
        return "Production"
    if "Library" in skill_content or "infrastructure" in skill_content.lower():
        return "Library"
    return "Scaffold"


def extract_design_mode(skill_content: str) -> str:
    """Extract design mode from SKILL.md frontmatter."""
    lines = skill_content.split("\n")

    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and line.startswith("mode:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")

    return "unknown"


def read_scoring_rubric(skill_forge_dir: Path) -> str:
    """Read the scoring rubric."""
    rubric_path = skill_forge_dir / "references" / "scoring-rubric.md"
    if not rubric_path.exists():
        raise FileNotFoundError(f"Scoring rubric not found at {rubric_path}")
    return rubric_path.read_text(encoding="utf-8")


def generate_scoring_prompt(
    skill_content: str, rubric: str, archetype: str, design_mode: str = "unknown",
    synthesis: dict = None,
) -> str:
    synthesis_note = ""
    if synthesis and archetype != "Scaffold":
        status = "PASS" if synthesis.get('synthesis_pass', True) else ("WARN" if synthesis.get('is_warning') else "FAIL")
        synthesis_note = f"""

## Synthesis Coverage

- SOURCES.md: {"present" if synthesis.get('has_sources_md') else "missing"}
- Sources: {synthesis.get('source_count', 0)}
- {"⚠️ " if synthesis.get('is_warning') else ""}{status}

When scoring documentation:
- SOURCES.md present with sources → consider raising documentation by 1 (max 10)
- SOURCES.md missing for Library → lower documentation by 1
- SOURCES.md missing for Production → note as minor gap, no penalty"""

    return f"""You are an independent Skill Evaluator. Your job is to score the following SKILL.md objectively.

IMPORTANT: You must NOT consider any context about "what was changed" or "this is round N". Evaluate only what you see.

## Archetype
{archetype}

## Design Mode
{design_mode}

## Scoring Rubric
{rubric}

{synthesis_note}

## SKILL.md to Evaluate
```
{skill_content}
```

## Your Task

1. Score each dimension according to the rubric for the given archetype.
2. Calculate the total score.
3. Identify the lowest-scoring dimension.
4. Provide ONE specific, actionable improvement suggestion for the lowest dimension.

## Output Format

Return ONLY valid JSON (no markdown, no explanation before/after):

{{
  "archetype": "{archetype}",
  "design_mode": "{design_mode}",
  "scores": {{
    "trigger_accuracy": <0-15>,
    "execution_reliability": <0-20>,
    "boundary_clarity": <0-10>,
    "context_efficiency": <0-10>,
    "documentation": <0-10 or null if Scaffold>,
    "error_handling": <0-10 or null if Scaffold>,
    "portability": <0-10 or null if not Library>,
    "governance_maturity": <0-15 or null if not Library>
  }},
  "total": <sum of non-null scores>,
  "max_possible": <max for this archetype>,
  "percentage": <total/max_possible * 100, rounded>,
  "lowest_dimension": "<dimension name>",
  "improvement_suggestion": "<one specific, actionable suggestion>"
}}

Score now."""


def check_synthesis_coverage(skill_dir: Path, archetype: str) -> dict:
    """Check synthesis coverage. Only Library level fails on missing SOURCES.md."""
    result = {
        "has_sources_md": False,
        "source_count": 0,
        "has_coverage_matrix": False,
        "coverage_gaps": 0,
        "synthesis_pass": True,
        "is_warning": False,
        "details": [],
    }

    if archetype == "Scaffold":
        result["details"].append("Scaffold: synthesis optional")
        return result

    sources_md = skill_dir / "SOURCES.md"
    if not sources_md.exists():
        if archetype == "Library":
            result["synthesis_pass"] = False
            result["details"].append(f"{archetype}: SOURCES.md missing (required for Library)")
        else:
            result["is_warning"] = True
            result["details"].append(f"{archetype}: SOURCES.md missing (recommended but optional)")
        return result

    result["has_sources_md"] = True
    content = sources_md.read_text(encoding="utf-8")

    table_rows = [l for l in content.split("\n") if l.strip().startswith("|") and "Source" not in l and "---" not in l]
    result["source_count"] = len([r for r in table_rows if r.count("|") >= 4])

    if "Coverage Area" in content or "coverage" in content.lower():
        result["has_coverage_matrix"] = True
        gap_lines = [l for l in content.split("\n") if "❌" in l]
        result["coverage_gaps"] = len(gap_lines)
        if gap_lines and archetype == "Library":
            result["synthesis_pass"] = False
            result["details"].append(f"{archetype}: {len(gap_lines)} critical coverage gap(s)")
        elif gap_lines:
            result["is_warning"] = True
            result["details"].append(f"{archetype}: {len(gap_lines)} coverage gap(s) noted")

    if result["source_count"] < 3:
        if archetype == "Library":
            result["synthesis_pass"] = False
            result["details"].append(f"{archetype}: only {result['source_count']} sources (minimum 3)")
        else:
            result["is_warning"] = True
            result["details"].append(f"{archetype}: {result['source_count']} sources (3+ recommended)")

    if not result["details"]:
        result["details"].append(f"{archetype}: synthesis coverage adequate")

    return result


def call_subagent_score(prompt: str) -> dict:
    """
    This function is a placeholder for the actual sub-agent call.

    In practice, this will be called by the evolve_loop.py which has
    access to the Task tool. The Task tool will spawn a sub-agent
    with the scoring prompt.

    Returns the score JSON from the sub-agent.
    """
    return {
        "note": "This function should be called via Task tool in evolve_loop.py",
        "prompt": prompt,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Score a skill using sub-agent blind evaluation"
    )
    parser.add_argument("skill_dir", type=str, help="Path to skill directory")
    parser.add_argument(
        "--skill-forge-dir",
        type=str,
        default=None,
        help="Path to skill-forge directory",
    )
    parser.add_argument(
        "--output", type=str, default=None, help="Output file for score JSON"
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"Error: Skill directory not found: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    skill_forge_dir = (
        Path(args.skill_forge_dir)
        if args.skill_forge_dir
        else Path(__file__).parent.parent
    )
    if not skill_forge_dir.exists():
        print(
            f"Error: skill-forge directory not found: {skill_forge_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        skill_content = read_skill_md(skill_dir)
        archetype = extract_archetype(skill_content)
        design_mode = extract_design_mode(skill_content)
        rubric = read_scoring_rubric(skill_forge_dir)
        synthesis = check_synthesis_coverage(skill_dir, archetype)
        prompt = generate_scoring_prompt(skill_content, rubric, archetype, design_mode, synthesis)

        result = {
            "skill_dir": str(skill_dir),
            "archetype": archetype,
            "design_mode": design_mode,
            "synthesis": synthesis,
            "prompt": prompt,
            "status": "ready_for_subagent",
        }

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(
                json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            print(f"Prompt written to: {output_path}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
