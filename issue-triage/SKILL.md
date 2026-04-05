---
name: issue-triage
description: Skill for triaging, responding to, and closing GitHub issues on open-source projects. Covers drafting responses, batch posting, managing a tracking file, and applying the AI disclosure policy.
---

# Issue Triage

This skill defines the workflow for reviewing, responding to, and closing open GitHub issues on @bramp's open-source projects. It is designed for batch processing with human review at each step.

## Prerequisites

- GitHub CLI (`gh`) authenticated as the repository owner.
- Set `export GH_PAGER=cat` to prevent interactive paging.
- The `gh-cli` skill should be available for reference.

## Core Principles

1. **Human Review**: Never post a comment without explicit user approval. Draft all responses first, present them for review, then post only after approval.
2. **AI Disclosure**: Every posted comment must end with the disclosure line:
   ```
   *Note: This response was written by an AI agent (GitHub Copilot) on behalf of @bramp.*
   ```
3. **Batch Efficiency**: Process issues in batches — draft many, review together, post approved ones.
4. **Be Helpful**: Provide working code examples, link to related issues, and suggest workarounds where possible.
5. **Close Decisively**: Don't leave issues open without a reason. Close with the appropriate reason.

## Tracking File (ISSUE_RESPONSES.md)

Maintain a tracking file in the project root to manage progress. Structure:

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
- {bullet points summarizing the issue and any existing comments}

### Proposed Response
> {draft response in blockquote format}
```

### Tracking File Rules

- Remove sections from the file once they have been posted (keep the header lists updated).
- Keep the completed/posted lists in the header current.
- The file should only contain issues that still need action.

## Workflow

### Phase 1: Research

1. List all open issues:
   ```bash
   gh issue list --repo {owner}/{repo} --state open --limit 100 --json number,title,labels,createdAt,author
   ```

2. For each issue, fetch full details:
   ```bash
   gh issue view {number} --repo {owner}/{repo} --json title,body,comments,labels,author,createdAt
   ```

3. Create `ISSUE_RESPONSES.md` with draft responses for all issues.

### Phase 2: Categorization

Categorize each issue and determine the appropriate action:

| Category | Action | Close Reason |
|----------|--------|-------------|
| **Question (answered)** | Summarize the answer, link to docs/examples | `completed` |
| **Question (stale, no follow-up)** | Answer if possible, note staleness | `not planned` |
| **Bug (fixed)** | Confirm the fix, reference the PR/commit | `completed` |
| **Bug (not a library issue)** | Explain why, suggest debugging steps | `not planned` |
| **Bug (legitimate, unfixed)** | Acknowledge, suggest workaround, leave open | — |
| **Enhancement (accepted)** | Agree, outline approach, welcome PR | Leave open |
| **Enhancement (out of scope)** | Explain why it's out of scope | `not planned` |
| **Duplicate** | Link to the canonical issue | `not planned` |
| **Stale (no response >1 year)** | Close with invitation to reopen | `not planned` |

### Phase 3: Review & Approval

Present drafts to the user. Wait for explicit approval before posting. The user may:
- Approve as-is
- Request edits
- Skip (defer for later)
- Reject (don't post)

### Phase 4: Posting

Use the file-based approach to avoid shell escaping issues:

```bash
# 1. Write comment body to a temp file
# 2. Post and close
gh issue comment {number} --repo {owner}/{repo} --body-file tmp/comment_{number}.md
gh issue close {number} --repo {owner}/{repo} --reason "{reason}"
rm tmp/comment_{number}.md
```

**Never use heredoc (`<<EOF`)** — it causes terminal garbling with complex markdown.

After posting, update `ISSUE_RESPONSES.md`:
- Move issue number to the appropriate header list (completed or posted).
- Remove the section from the file body.

## Response Guidelines

### Tone
- Professional but approachable.
- Concise — don't over-explain.
- Thank contributors when appropriate.
- Acknowledge good ideas even when closing.

### Structure
A good response typically includes:
1. **Acknowledgment** — validate the issue or question.
2. **Answer/explanation** — the actual response.
3. **Code example** — when applicable (working Java/shell snippets).
4. **Links** — to related issues, PRs, or documentation.
5. **Action** — what happens next (closing, welcoming PR, etc.).
6. **AI disclosure** — always last.

### What to Avoid
- Don't apologize for delayed responses on old issues.
- Don't promise timelines.
- Don't speculate about things you haven't verified in the codebase.
- Don't post duplicate comments if one was already posted.

## Closing Issues

When closing:
- **`completed`**: The issue was answered, fixed, or resolved.
- **`not planned`**: Out of scope, stale, duplicate, or not a library issue.

Some issues should be left open after commenting:
- Legitimate unfixed bugs.
- Accepted enhancements welcoming PRs.
- Issues awaiting contributor response on active discussions.

## Filing New Issues

When triage reveals gaps (missing tests, needed refactoring, etc.), file new tracking issues:

```bash
gh issue create --repo {owner}/{repo} --title "{title}" --body-file tmp/new_issue.md --label "enhancement"
```

Reference these in `ISSUE_RESPONSES.md` under "Self-filed tracking issues."

## Verifying Before Responding

Before claiming something is fixed or works a certain way:
- **Read the actual source code** to confirm behavior.
- **Run the tests** if you've made code changes.
- **Check PR/commit history** when referencing fixes.
- **Verify issue state** with `gh issue view` before posting (avoid double-posting).
