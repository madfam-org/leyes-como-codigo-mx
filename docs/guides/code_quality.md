# Code Quality Standards

## File Size Limits

To maintain code quality and readability, we enforce the following file size limits:

- **ERROR** (blocks commit): Files over **800 lines**
- **WARNING** (shown but allows commit): Files over **600 lines**

### Enforcement

A pre-commit hook automatically checks all staged Python files before each commit:

```bash
# The hook is already installed at:
.git/hooks/pre-commit → ../../scripts/utils/pre-commit-file-size.py
```

### Manual Audits

Run these scripts anytime to check the codebase:

```bash
# Quick file size check
python scripts/utils/audit_file_sizes.py

# Comprehensive complexity analysis
python scripts/utils/refactoring_analysis.py
```

### Bypassing the Hook (Emergency Only)

If you absolutely must commit a file that violates the limits:

```bash
git commit --no-verify -m "your message"
```

**Note**: This should be rare and discussed with the team first.

### Current Status

As of 2026-02-04:
- ✅ All files under 600 lines
- ✅ Only 1 file over 400 lines (`akn_generator_v2.py` at 433 lines)
- ✅ Average file size: 88 lines

See [`walkthrough.md`](file:///Users/aldoruizluna/.gemini/antigravity/brain/ea38a790-49e7-4368-8647-77b881c90633/walkthrough.md) for full audit details.
