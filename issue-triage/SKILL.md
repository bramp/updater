---
name: issue-triage
description: Batch triage, verify, respond to, and close open GitHub issues with human review gates and mandatory AI disclosure. Use this skill when reviewing a repository's open issues, drafting responses, filing follow-up tracking issues, or cleaning up stale bug trackers.
license: BSD-3-Clause
---

# Issue Triage

This skill defines the workflow for reviewing, verifying, responding to, and closing open GitHub issues on @bramp's open-source projects using batch review and explicit human approval gates.

## Prerequisites

- GitHub CLI (`gh`) authenticated as the repository owner.
- Disable interactive pagers (`export GH_PAGER=cat` or `gh --no-pager`).

## Core Principles

1. **Human Review Required**: Never post a comment, close an issue, or open a new issue without explicit user approval. Draft responses first, review in batches, then post only approved items.
2. **Accurate AI Disclosure**: Every posted comment must end with an honest disclosure identifying the active AI agent (e.g., `GitHub Copilot`, `Gemini CLI`, `Claude Code`):
   ```markdown
   *Note: This response was written by an AI agent ({AGENT_NAME}) on behalf of @bramp.*
   ```
3. **Keep Target Git Working Trees Clean**: Never commit triage scratch files into the target repository. Store `ISSUE_RESPONSES.md` and temporary comment files in an untracked scratch directory (e.g., `$(mktemp -d)` or the session workspace, or add `ISSUE_RESPONSES.md` to `.git/info/exclude`).
4. **Verify Before Claiming**: Always inspect the actual source code, tests, and commit/PR history before stating how the library behaves or whether a bug is fixed.
5. **Close Decisively**: Close resolved, out-of-scope, duplicate, or stale issues with the appropriate `--reason` (`completed` vs `not planned`).

## Tracking File (`ISSUE_RESPONSES.md`)

Keep a live tracking document in your scratch/session workspace (excluded from git commits):

```markdown
# GitHub Issue Responses

Draft responses for remaining open issues on {owner}/{repo}.
Generated {date}. Updated {date}.

Completed (posted + closed): #NNN, #NNN, ...
Posted (left open): #NNN, #NNN, ...
Self-filed tracking issues (no response needed): #NNN, ...

---

## Issue #NNN — {title}
**Labels:** {labels}
**Opened:** {date} by @{user}
**URL:** {url}

### Summary of Discussion
- {concise bullets summarizing the report, reproduction status, and existing comments}

### Proposed Response
> {draft response in blockquote format, ending with the AI disclosure line}
```

Remove issue sections from the body once posted, moving their issue numbers into the header summary lists so only pending work remains in the file.

## Workflow

### Phase 1: Research & Codebase Verification

1. List open issues:
   ```bash
   GH_PAGER=cat gh issue list --repo "{owner}/{repo}" --state open --limit 100 --json number,title,labels,createdAt,author
   ```
2. Fetch full discussion for each issue:
   ```bash
   GH_PAGER=cat gh issue view "{number}" --repo "{owner}/{repo}" --json title,body,comments,labels,author,createdAt
   ```
3. Verify behavior against current source code, tests, and git log, then draft responses in `ISSUE_RESPONSES.md`.

### Phase 2: Categorization

| Category | Action | Close Reason |
| :--- | :--- | :--- |
| **Question (answered)** | Summarize the verified answer and link to docs/examples | `completed` |
| **Question (stale, no follow-up)** | Provide best answer if possible, note staleness | `not planned` |
| **Bug (fixed)** | Confirm fix and link the resolving PR/commit/release | `completed` |
| **Bug (not a library issue)** | Explain root cause and suggest debugging steps | `not planned` |
| **Bug (legitimate, unfixed)** | Acknowledge, share workaround if any, leave open | — |
| **Enhancement (accepted)** | Confirm alignment, outline design direction, welcome PR | — |
| **Enhancement (out of scope)** | Explain why it falls outside project scope | `not planned` |
| **Duplicate** | Link the canonical issue | `not planned` |
| **Stale (>1 year awaiting info)** | Close politely with invitation to reopen with details | `not planned` |

### Phase 3: Batch Review & Approval

Present drafts to the user and wait for explicit disposition (`approve`, `edit`, `skip`, or `reject`) on each issue before posting.

### Phase 4: Posting Safely

Write comment bodies to temporary files (never inline shell strings or `<<EOF` heredocs that can garble backticks/markdown), re-verify issue state to prevent double-posting, post, and clean up:

```bash
TMP_DIR="$(mktemp -d)"
# Write approved markdown body to "${TMP_DIR}/comment_${NUMBER}.md", then:
GH_PAGER=cat gh issue view "${NUMBER}" --repo "{owner}/{repo}" --json state,comments
gh issue comment "${NUMBER}" --repo "{owner}/{repo}" --body-file "${TMP_DIR}/comment_${NUMBER}.md"
gh issue close "${NUMBER}" --repo "{owner}/{repo}" --reason "${REASON}" # omit if leaving open
rm -rf "${TMP_DIR}"
```

## Response Tone & Structure

- **Concise, warm, and direct**: Acknowledge the report, give the verified technical answer + working snippet/links, state the disposition (closing vs leaving open), and append the AI disclosure last.
- **Avoid**: Apologizing for response latency on old issues, promising delivery timelines, or speculating without checking code.

## Filing Follow-up Tracking Issues

When triage uncovers genuine technical debt or missing test coverage (and the user approves filing an issue):

```bash
gh issue create --repo "{owner}/{repo}" --title "{title}" --body-file "${TMP_DIR}/new_issue.md" --label "enhancement"
```

Record newly filed issue numbers under `Self-filed tracking issues` in `ISSUE_RESPONSES.md`.
