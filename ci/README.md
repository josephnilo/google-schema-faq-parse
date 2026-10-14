# Local CI

Python 3.11. Prepare `python3 -m pip install --require-hashes -r ci/requirements.lock`.
Tests use synthetic HTML and mock HTTP responses, including HTTP failure, empty FAQs
and quoted text. JSON-LD is serialized before wrapping it in an HTML script element.

Run `./ci/run.sh` in a disposable source checkout. Dependency preparation is a
separate trusted step; the check command never installs packages or calls live
services. Linux validation targets Ubuntu Air ARM64.

No Actions runner is added or admitted by this change. Automatic Actions checks
remain unavailable under the current selected private runner policy. This entrypoint
is ready for review and manual local execution; it is not a branch protection check.
No hosted runner, deployment, upload, merge or paid API is involved.

The CI lock resolves the production requirements unchanged except for removing
the redundant `bs4` alias: BeautifulSoup is already supplied by `beautifulsoup4`.
This permits wheel-only preparation without executing the legacy alias sdist.
