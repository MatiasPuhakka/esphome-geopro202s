## How this repo works

`components/geopro_202s` is an ESPHome external component that reads an Ouman Geopro 202S Controller over a 4800 baud bus. `example/geopro202s.yaml` shows how to use it. The owner's own Node, its config and the tools around their heat pump live in a private repo that builds the Node from this repo's `main`, so a merge here reaches their Node at its next install.

- **Settled facts** live in `CONTEXT.md` (terms, the wire protocol), `docs/adr/` (decisions and their reasons) and `docs/agents/` (procedures). What the manuals say lives in their transcriptions, `manuals/kasikirja.md` and `manuals/asennusohje.md`. A fact that an issue comment or a handoff settled belongs in one of these, so move it there; in a transcription it goes in a **Repo note** (ADR 0006).
- **Checks** are the `Makefile` targets that `.github/workflows/ci.yml` runs. The `esphome` on PATH may be older than 2026.9; pass `ESPHOME=/path/to/esphome` to make.
- **Secrets**: `secrets.yaml` and `.env` are gitignored. Keep their values out of output, docs and commits.
- **Changes to the Component or the ESPHome version** get verified on the owner's Node before they merge, following the verification procedure in their private repo. Ask the owner.
- **Manuals**: cite a manual page by linking its anchor in the transcription, such as `manuals/kasikirja.md#s21` for the Käsikirja's p. 21; `make check-manual-links` checks the links. The PDFs next to the transcriptions are the archive a transcription is checked against. To read a PDF page, crop a figure or transcribe a page, follow `docs/agents/manual-transcription.md`.
- **Handoffs**: write a session's handoff doc to `.scratch/` (gitignored).

## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues and are managed with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels, each named after its role. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
