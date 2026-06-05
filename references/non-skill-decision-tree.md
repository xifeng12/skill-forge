# Non-Skill Decision Tree

Not everything should be a skill. Use this to decide.

## Should This Be a Skill?

```
Is the task repeated across sessions?
├─ No → Use a prompt or instruction. Don't make a skill.
└─ Yes
   ├─ Is it a single command? → Use an alias or script.
   ├─ Is it a workflow with branching? → Use a skill.
   ├─ Is it domain knowledge? → Use a reference file.
   └─ Is it a tool wrapper? → Use a skill (Tool Wrapper archetype).
```

## Signs It Should NOT Be a Skill

- One-off task, never repeated
- Simple enough for a single instruction
- Changes every time (no reusable pattern)
- Better suited as a script or alias

## Signs It SHOULD Be a Skill

- Repeated workflow across sessions
- Benefits from structured approach
- Needs trigger phrases for discovery
- Would be useful to share with team
- Combines multiple tools/steps
