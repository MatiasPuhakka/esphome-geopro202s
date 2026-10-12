## How this repo works

`components/geopro_202s` is an ESPHome external component that reads an Ouman Geopro 202S Controller over a 4800 baud bus. `node.yaml` holds the settings of the Node that runs it. `geopro.yaml` builds the Node with the Component from the checkout, and `addon/geopro-202s.yaml`, which the owner pastes into the Home Assistant add-on, builds it with the Component from `main`.

- **Settled facts** live in `CONTEXT.md` (terms, the wire protocol), `docs/adr/` (decisions and their reasons) and `docs/agents/` (procedures). What the manuals say lives in their transcriptions, `manuals/kasikirja.md` and `manuals/asennusohje.md`. A fact that an issue comment or a handoff settled belongs in one of these, so move it there; in a transcription it goes in a **Repo note** (ADR 0006).
- **Checks** are the `Makefile` targets that `.github/workflows/ci.yml` runs. The `esphome` on PATH may be older than 2026.9; pass `ESPHOME=/path/to/esphome` to make.
- **Secrets**: `secrets.yaml` (next to `geopro.yaml`) and `.env` are gitignored. Keep their values out of output, docs and commits.
- **Changes that alter what the Node runs** (the Component, `node.yaml`, the ESPHome version), and any raw bus trace capture, follow `docs/agents/verification.md`.
- **Manuals**: cite a manual page by linking its anchor in the transcription, such as `manuals/kasikirja.md#s21` for the Käsikirja's p. 21; `make check-manual-links` checks the links. The PDFs next to the transcriptions are the archive a transcription is checked against. To read a PDF page, crop a figure or transcribe a page, follow `docs/agents/manual-transcription.md`.
- **Handoffs**: write a session's handoff doc to `.scratch/` (gitignored).

## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues and are managed with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels, each named after its role. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
