# Wyoming: law history in git

The statute law of Wyoming as a git repository: one file per section, committed with the official publisher named as author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the State of Wyoming | 1 | Current text (oldest version available) |
| `title-06-crimes-and-offenses/` | Wyoming Statutes Title 6: Crimes and Offenses | 1 | Current text (oldest version available) |
| `title-17-corporations/` | Wyoming Statutes Title 17: Corporations, Partnerships and Associations | 1 | Current text (oldest version available) |
| `title-34-property/` | Wyoming Statutes Title 34: Property, Conveyances and Security Transactions | 1 | Current text (oldest version available) |

Nothing else of Wyoming's law is in it yet.

## Where the text comes from

[Wyoming Statutes - Text Only](https://wyoleg.gov/StateStatutes/StatutesDownload), Wyoming Legislative Service Office: the text-only title PDFs. The LexisNexis annotated edition is not used.

## Dates

Each act has one version, dated 8 May 2026, the modification date of the Legislative Service Office's PDFs.

## What it does not show

- The Legislative Service Office publishes only the current text, so there is no history yet.
- Only the Constitution and Titles 6, 17 and 34 are included.
- Text is rebuilt from a PDF's wrapped lines, so tables and some indentation are flattened.

## How it is checked

- Every unit is read back from git on its day and compared with the corpus (`tools/check_repo.py`; results in `REPRODUCE.md`).
- Each source file is identified by its sha256, in `data/versions.json`.

## What "author" means

Each commit is authored by the publisher (Wyoming Legislative Service Office) because this first build holds one version of each act, the oldest version available. The committer is always Lexifina.
