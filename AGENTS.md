# Repository maintenance

- Keep the existing search, filters, pagination and Excel download behavior.
- `catalog.json` is the catalog source. Source `index.html` contains an identical JSON snapshot from the existing external updater.
- Run `python scripts/build_agent_site.py` to create `_site`. Never edit generated output or commit it.
- Inject agent discovery into the build artifact, so external HTML regeneration cannot remove it from a successful deployment.
- Run `python -m unittest discover -s tests -v` and the build before submitting changes.
- Preserve category IDs, repository IDs, confidence and README blob SHAs. Do not invent compatibility, install commands, network requirements or test results.
- Collection timestamps are not per-feature verification timestamps. Unknown fields stay null; detailed new claims require explicit evidence and a separate reviewed data model.
- Keep all Pages links under `/star/`; check generated internal links and reject stale or duplicate entries.
- Keep the Skill as a distributable repository file. Do not claim it has been registered in other agents.
- The external updater is not included here. Do not replace or disable it. Document publishing integration and token-trigger limitations in README.
