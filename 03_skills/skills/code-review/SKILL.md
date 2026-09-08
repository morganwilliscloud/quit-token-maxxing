---
name: code-review
description: Review code for security vulnerabilities, logic errors, and best practices
allowed-tools: file_read shell
---

# Code Review

## Process
1. Read the code carefully, focusing on logic errors first
2. Check for security vulnerabilities (SQL injection, XSS, etc.)
3. Evaluate error handling completeness
4. Assess test coverage gaps
5. Note style issues last (lowest priority)

## Output Format
Structure your review as:
- **Critical**: Must fix before merge
- **Warning**: Should fix, but not blocking
- **Suggestion**: Nice to have improvements

## Rules
- Be specific: point to exact lines
- Suggest fixes, don't just point out problems
- Acknowledge good patterns you see
