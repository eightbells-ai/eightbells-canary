# eightbells-canary

A deliberately minimal repository used as a delivery canary for Eightbells
agent runs. Its only purpose is to prove that the end-to-end delivery path — a
run reaching the `ready` stage and opening a pull request — works.

There is intentionally **no** real build, dependency install, or test suite
here. Verification must be trivially green in a fresh, network-less sandbox, so
the repo carries at most one dependency-free check (see
`.github/workflows/ci.yml`). Please keep it that way: do not add dependencies,
integration tests, or anything that needs network access or secrets.
<!-- eightbells canary: automated delivery check -->