#!/usr/bin/env python3
"""
Ratchet mechanism for skill evolution.

Implements the "only keep improvements" principle:
- Score can only go up
- Each round either improves the skill or cleanly reverts
- No accumulation of partial regressions

Usage:
    python ratchet.py keep --skill-dir /path/to/skill --score 75
    python ratchet.py revert --skill-dir /path/to/skill
    python ratchet.py status --skill-dir /path/to/skill
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_git_head(skill_dir: Path) -> str:
    """Get current git HEAD commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=skill_dir,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def git_commit(skill_dir: Path, message: str) -> bool:
    """Create a git commit."""
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
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e.stderr.decode() if e.stderr else 'unknown error'}", file=sys.stderr)
        return False


def git_revert(skill_dir: Path) -> bool:
    """Revert the last commit (soft reset to HEAD~1)."""
    try:
        subprocess.run(
            ["git", "reset", "--hard", "HEAD~1"],
            cwd=skill_dir,
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git revert failed: {e.stderr.decode() if e.stderr else 'unknown error'}", file=sys.stderr)
        return False


def load_ratchet_state(skill_dir: Path) -> dict:
    """Load ratchet state from file."""
    state_file = skill_dir / "reports" / ".ratchet_state.json"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "best_score": 0,
        "best_commit": "",
        "rounds": []
    }


def save_ratchet_state(skill_dir: Path, state: dict) -> None:
    """Save ratchet state to file."""
    state_file = skill_dir / "reports" / ".ratchet_state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def cmd_keep(args):
    """Keep an improvement if score is better than baseline."""
    skill_dir = Path(args.skill_dir).resolve()
    new_score = args.score
    
    state = load_ratchet_state(skill_dir)
    best_score = state["best_score"]
    
    if new_score > best_score:
        commit = get_git_head(skill_dir)
        state["best_score"] = new_score
        state["best_commit"] = commit
        state["rounds"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "keep",
            "score_before": best_score,
            "score_after": new_score,
            "commit": commit
        })
        save_ratchet_state(skill_dir, state)
        
        print(json.dumps({
            "action": "kept",
            "reason": f"Score improved: {best_score} → {new_score}",
            "new_best_score": new_score,
            "commit": commit
        }, indent=2))
        return 0
    else:
        print(json.dumps({
            "action": "reject",
            "reason": f"Score did not improve: {new_score} <= {best_score}",
            "current_best": best_score,
            "suggested_action": "revert"
        }, indent=2))
        return 1


def cmd_revert(args):
    """Revert the last commit."""
    skill_dir = Path(args.skill_dir).resolve()
    
    state = load_ratchet_state(skill_dir)
    
    if git_revert(skill_dir):
        state["rounds"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "revert",
            "score_after": state["best_score"],
            "commit": state["best_commit"]
        })
        save_ratchet_state(skill_dir, state)
        
        print(json.dumps({
            "action": "reverted",
            "current_best_score": state["best_score"],
            "current_best_commit": state["best_commit"]
        }, indent=2))
        return 0
    else:
        print(json.dumps({
            "action": "failed",
            "reason": "Git revert failed"
        }, indent=2))
        return 1


def cmd_status(args):
    """Show current ratchet state."""
    skill_dir = Path(args.skill_dir).resolve()
    state = load_ratchet_state(skill_dir)
    
    print(json.dumps({
        "skill_dir": str(skill_dir),
        "best_score": state["best_score"],
        "best_commit": state["best_commit"],
        "total_rounds": len(state["rounds"]),
        "rounds_summary": [
            {
                "timestamp": r["timestamp"],
                "action": r["action"],
                "score": r.get("score_after", "N/A")
            }
            for r in state["rounds"][-5:]
        ]
    }, indent=2))
    return 0


def cmd_reset(args):
    """Reset ratchet state (use with caution)."""
    skill_dir = Path(args.skill_dir).resolve()
    
    if args.score is None:
        print("Error: --score required for reset", file=sys.stderr)
        return 1
    
    commit = get_git_head(skill_dir)
    state = {
        "best_score": args.score,
        "best_commit": commit,
        "rounds": [{
            "timestamp": datetime.now().isoformat(),
            "action": "reset",
            "score_after": args.score,
            "commit": commit
        }]
    }
    save_ratchet_state(skill_dir, state)
    
    print(json.dumps({
        "action": "reset",
        "new_baseline": args.score,
        "commit": commit
    }, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Ratchet mechanism for skill evolution")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    keep_parser = subparsers.add_parser("keep", help="Keep improvement if score improved")
    keep_parser.add_argument("--skill-dir", required=True, help="Path to skill directory")
    keep_parser.add_argument("--score", type=int, required=True, help="New score")
    
    revert_parser = subparsers.add_parser("revert", help="Revert last commit")
    revert_parser.add_argument("--skill-dir", required=True, help="Path to skill directory")
    
    status_parser = subparsers.add_parser("status", help="Show ratchet state")
    status_parser.add_argument("--skill-dir", required=True, help="Path to skill directory")
    
    reset_parser = subparsers.add_parser("reset", help="Reset ratchet baseline")
    reset_parser.add_argument("--skill-dir", required=True, help="Path to skill directory")
    reset_parser.add_argument("--score", type=int, help="New baseline score")
    
    args = parser.parse_args()
    
    if args.command == "keep":
        return cmd_keep(args)
    elif args.command == "revert":
        return cmd_revert(args)
    elif args.command == "status":
        return cmd_status(args)
    elif args.command == "reset":
        return cmd_reset(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
