# designextractor

Claude Code skills that turn seven reference design boards into report designs.

| Skill | What it does |
|---|---|
| [`design-picker`](.claude/skills/design-picker/SKILL.md) | Decides **which design to use** for a document. You get a primary and an alternate family with reasons, plus the palette with contrast checks, fonts, motif, layout recipes, a page-by-page plan and a rhythm check. |
| [`report-design`](.claude/skills/report-design/SKILL.md) | Builds a DOCX report from a content file in the "Slab & Rule" style; renders it and checks every page. |

The seven families are extracted from the boards in `.claude/skills/report-design/references/images/` (copies of the WhatsApp images in the repo root):

| | Family | Board | Best for |
|---|---|---|---|
| A | Navy Annual | Rapport annuel 2025 | annual, ESG, public-sector and board reports |
| B | Forest Breakslide | Breakslide | dark-mode portfolios and profiles (screen) |
| C | Leaf & Black | Business Plan | business plans, pitch documents |
| D | Prism Rounded | Prism | marketing, company profiles |
| E | Clinicare Aqua | Clinicare | clinical, patient and public-health reports |
| F | Docoro Royal Block | Docoro | healthcare services brochures |
| G | Market Frame | Market | consulting, white papers, proposals |

Design system for building documents like the boards: [`DESIGN.md`](DESIGN.md).

Quick start:

```bash
python3 .claude/skills/design-picker/scripts/pick_design.py --list
python3 .claude/skills/design-picker/scripts/pick_design.py .claude/skills/design-picker/examples/brief-hospital.json
```
