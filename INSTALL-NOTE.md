# Paste-ready install note (Teams / email)

Copy the block below to the team once the repo is pushed to `github.com/candyco-plugins/claude-plugins`.

---

**Subject: One-time setup — the CandyCo design system in Claude Code**

Team — we've packaged our design system so Claude builds everything (reports, decks, dashboards, docs) in CandyCo's look automatically. Two commands, one time, in Claude Code:

```
/plugin marketplace add candyco-plugins/claude-plugins
/plugin install candyco-design-system@candyco
```

After that, anything visual you ask Claude to build comes out on-brand — right colors, type, logos, and the standard paged report layout — without you doing anything else.

If you hit an auth error on the first command, run `gh auth login` (or make sure your GitHub account has access to the CandyCo org) and try again.

Questions → Scott.

---
