#!/usr/bin/env python3
"""Echo PR Reviewer - modeled on CodeRabbit pattern"""
import os, json, urllib.request, urllib.error

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
PR_NUMBER = os.environ['PR_NUMBER']
REPO = os.environ['REPO']

def gh(path, method='GET', payload=None):
    url = f'https://api.github.com{path}'
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    if payload: req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f'GH error {e.code}: {e.read().decode()[:80]}')
        return None

# Fetch PR
pr = gh(f'/repos/{REPO}/pulls/{PR_NUMBER}')
if not pr:
    print('Could not fetch PR — exiting')
    exit(0)

title = pr.get('title', '')
body = pr.get('body', '') or ''
n_files = pr.get('changed_files', 0)
adds = pr.get('additions', 0)
dels = pr.get('deletions', 0)

# Fetch files
files = gh(f'/repos/{REPO}/pulls/{PR_NUMBER}/files?per_page=20') or []
file_lines = []
for f in files[:12]:
    fname = f.get('filename', '')
    status = f.get('status', '')
    fa = f.get('additions', 0)
    fd = f.get('deletions', 0)
    patch = (f.get('patch', '') or '')[:300]
    file_lines.append(f'- `{fname}` ({status} +{fa}/-{fd})\n  {patch[:200]}')
files_text = '\n'.join(file_lines) or 'No file details'

# Build review
if ANTHROPIC_API_KEY:
    prompt = (
        f'You are Echo PR Reviewer for the Echo Universe project.\n'
        f'Review this PR concisely and directly.\n\n'
        f'Title: {title}\n'
        f'Description: {body[:400]}\n'
        f'Changed: {n_files} files (+{adds}/-{dels} lines)\n\n'
        f'Files:\n{files_text}\n\n'
        f'Provide:\n'
        f'1. **Summary** (2 sentences)\n'
        f'2. **Key changes** (bullets)\n'
        f'3. **Issues found** (bugs/security/missing tests — or say none)\n'
        f'4. **Verdict**: APPROVE / REQUEST_CHANGES / COMMENT\n\n'
        f'Max 300 words. No fluff.'
    )
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=json.dumps({
            'model': 'claude-haiku-4-5-20251001',
            'max_tokens': 400,
            'messages': [{'role': 'user', 'content': prompt}]
        }).encode(),
        method='POST'
    )
    req.add_header('x-api-key', ANTHROPIC_API_KEY)
    req.add_header('anthropic-version', '2023-06-01')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            review_text = data['content'][0]['text']
    except Exception as e:
        review_text = f'Echo PR Reviewer: API error ({e}). Manual review needed.'
else:
    issues = []
    if n_files > 20: issues.append('- Large PR: consider splitting')
    if adds > 500: issues.append('- High line count: ensure test coverage')
    if not body.strip(): issues.append('- No PR description provided')
    issues_text = '\n'.join(issues) if issues else '- No automated concerns'
    review_text = (
        f'## Echo PR Review\n\n'
        f'**{n_files} files** changed (+{adds}/-{dels} lines)\n\n'
        f'**Files**:\n'
        + '\n'.join([f'- `{f.get("filename","")}` ({f.get("status","")})' for f in files[:10]])
        + f'\n\n**Checks**:\n{issues_text}\n\n'
        f'*Add ANTHROPIC_API_KEY secret for AI-powered review.*'
    )

comment = review_text + '\n\n---\n*Echo PR Reviewer - Echo Universe*'

# Update existing comment or post new one
comments = gh(f'/repos/{REPO}/issues/{PR_NUMBER}/comments?per_page=50') or []
existing = [c for c in comments if 'Echo PR Reviewer' in c.get('body', '')]
if existing:
    gh(f'/repos/{REPO}/issues/comments/{existing[0]["id"]}',
       method='PATCH', payload={'body': comment})
    print(f'Updated review on PR #{PR_NUMBER}')
else:
    gh(f'/repos/{REPO}/issues/{PR_NUMBER}/comments',
       method='POST', payload={'body': comment})
    print(f'Posted review on PR #{PR_NUMBER}')
