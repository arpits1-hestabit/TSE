# Week-1 Retrospectives (Summary of learnings and what broke)

Overview :-
- Worked through terminal tooling, Node basics, streams vs buffers, simple CLIs, worker threads and a tiny HTTP server.
- Collected screenshots and perf. logs.

What I learned -
- Day-1: System inspection commands (cat /etc/os-release, lsb_release, hostnamectl, echo $SHELL, which, npm root -g, PATH inspection). Created introspect.js and captured outputs/screenshots.
- Day-1 (streams vs buffer): Created a large test file (bigfile.txt, 100 MB) and measured readFile vs createReadStream. Captured execution/memory snapshots in logs-perf.js and day1-perf.json.
- Day-2: Built a word-stat CLI (wordstat.js). Explored synchronous and yargs approaches.
- Day-3: Used git troubleshooting artifacts (bisect-session.txt, stash-session.txt, MERGE-POSTMORTEM.md) — practice with debugging and bisect.
- Day-4: Implemented a small HTTP server (server.js) with /echo, /slow and /cache endpoints and conditional caching.
- Day-5: Learned about Husky hooks and a tiny PrettyPrint build pipeline (scripts, pre-commit hooks).

What broke / issues encountered
- wordstat.js (Day-2) with worker_threads:
  - Script can hang/keep running. 
    Causes found: shebang not at file start, partial/unfinished worker code, and missing worker termination/resolve logic.
- CLI invocation confusion:
  - Running as ./wordstat.js without proper shebang placement or executable bit caused unexpected behavior. Use `node wordstat.js ...` or move shebang to line 1 and chmod +x.
- Husky / hooks:
  - Pre-commit scripts may block commits if lint/build steps fail. Also when I installed husky in the existing git repository, the modules(husky) were not getting installed; after reading docs., I reinitialized the git in the folder and then proceeded with the next steps.

  