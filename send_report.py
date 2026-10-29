import json
import os
from datetime import datetime, timezone

import requests

with open("report.json") as f:
    r = json.load(f)

tests = []
for t in r.get("tests", []):
    msg = None
    if t["outcome"] != "passed":
        msg = (t.get("call", {}).get("longrepr") or "failed")[:500]
    tests.append({
        "name": t["nodeid"],
        "result": t["outcome"],
        "failure_message": msg,
    })

s = r["summary"]
payload = {
    "repository": os.environ.get("GITHUB_REPOSITORY"),
    "branch": os.environ.get("GITHUB_REF_NAME"),
    "commit_sha": os.environ.get("GITHUB_SHA"),
    "run_id": os.environ.get("GITHUB_RUN_ID"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "total": s.get("total", 0),
    "passed": s.get("passed", 0),
    "failed": s.get("failed", 0),
    "overall_status": "PASSED" if s.get("failed", 0) == 0 else "FAILED",
    "tests": tests,
}

# Email body for the CI email step
lines = [
    "Repository: " + str(payload["repository"]),
    "Branch: " + str(payload["branch"]),
    "Commit: " + str(payload["commit_sha"]),
    "Run ID: " + str(payload["run_id"]),
    "Overall result: " + payload["overall_status"],
    "Total: " + str(payload["total"])
    + "  Passed: " + str(payload["passed"])
    + "  Failed: " + str(payload["failed"]),
    "",
    "Individual results:",
]
for t in tests:
    lines.append("- " + t["name"] + ": " + t["result"])
with open("email_body.txt", "w") as f:
    f.write("\n".join(lines))

# Send the report to the local receiver
url = os.environ["RECEIVER_URL"].rstrip("/") + "/report"
resp = requests.post(url, json=payload, headers={"bypass-tunnel-reminder": "1"}, timeout=30)
print(resp.status_code, resp.text)