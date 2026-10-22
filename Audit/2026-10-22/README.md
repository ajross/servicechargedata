# Source-to-CSV audit — 22 October 2026

Baseline: `servicechargedata` commit `1087f97` (includes the two previously approved Lambeth 2022–2023 corrections). The generated findings, coverage, ledger and hashes record the original read-only audit snapshot. Subsequent authorised corrections are recorded below; those snapshot artifacts have not been regenerated.

**L01 resolved after review:** the user authorised restoring 2023–2024 estate RVs to 53176 for ENBR2 (43 rows) and 107430 for ENNL7 (107 rows). Exactly 150 Estate_RV cells changed; all other fields, original files, other annual files, lookups, BOM and line endings were preserved. The 2022–2023 and 2024–2025 sources do not supply estate records for these groups, so their zeros were left in place. See [L02 details](L02-details.md) for the subsequent explanation and supplementary identity evidence for those three blocks.

**L02 follow-up:** with user approval, BD001961 Barcombe Avenue 239–241, BD000440 Chardin House 1–15 and BD003244 Mead Row 1–16 Cons were removed from 2022–2023 only (1900 → 1897 rows), because none has a named record in the retained block PDF. Their later-year rows and lookups remain because council sources support those. Git history now traces Chardin and Mead Row to individual January 2024 additions in the old website, with all 27 charges and both RVs unchanged since those additions. Their underlying invoice/attachment is not recorded. See [L02 details](L02-details.md) and [removal record](L02-resolution.json). The counts/findings below remain the original audit snapshot.

**L03 resolved after review:** with user approval, the 2022–2023 BD001520 row carrying the PDF’s “Dunbar Street 51” figures (RV 326) under “Dunbar Street 45–63” was removed (1897 → 1896 rows). The later original block files contain only the 45–63 group (RV 2510), not a separate number 51 row. The user considers it likely that the individual property was later included in the group; this remains an inference. Source-backed later-year rows and the lookup remain. See [removal record](L03-resolution.json).

**L04/L05 review decisions:** the user accepts the six estate-only source records in L04 without a data change, and accepts retaining lookup entries with no annual charge rows in L05 (631 blocks and seven estates, still the current counts after the approved removals). These are coverage observations, not requests for repair. L05 also records a separate limitation in the retained ID-source evidence; accepting unused lookup rows does not establish the provenance of every ID. No lookup or charge values were changed for these decisions.

**L06 resolved by source clarification:** the user confirms that the 2015–2016 through 2021–2022 data was user supplied. The absence of council attachments for those seven years is therefore expected and accepted. The historical comparison remains corroboration against the legacy website export, not independent validation of the original submissions or historical RVs. No data values were changed.

**S01 resolved after review:** the user requested removal of every Southwark block without an exact source lookup name match. All 61 flagged rows (56 assigned and five unassigned) were removed from 2022–2023 (2861 → 2800 rows). An independent check of the original workbook confirms that all remaining block names and their estate assignments agree under the documented case/spacing/punctuation normalisation. No remaining charge or weighting values changed; lookups and original source files remain intact. Public README counts and coverage descriptions were updated. See [removal record](S01-resolution.json). The generated findings and comparison counts below remain the original audit snapshot.

**T01/T02/W01 accepted as documented limitations:** the user accepts the uncertainty in Tower Hamlets name/code and estate/mapsite links, and the source-side inconsistency or absence of Wandsworth property counts. These are not demonstrated transformation bugs. For T01, 2022–2023 supplies full block names and relationships but no block codes; 2023–2024 supplies abbreviated codes and costs but no estate/mapsite links. The 743 cross-year code/address associations were inferred from names, not joined on a council code present in both sources. A further 134 later-year rows lack confirmed earlier full-address matches. No Tower Hamlets or Wandsworth data values or links were changed; the limitations remain relevant to calculations.

**D01 resolved:** references to a nonexistent Lewisham service lookup were removed from the borough, year and lookup READMEs. They now describe the services as columns in the annual CSV and the aliases as retained in the original source attachment. No new lookup or data changes were required.

## Findings and review decisions

The original audit found **150 Lambeth 2023–2024 estate RVs stored as zero despite a populated source value**; L01 has since been corrected with user approval. No unexplained charge-amount difference was detected in the source-linked comparisons completed below. That does **not** certify records without adequate source evidence or prove the councils' underlying bills correct.

| ID | Finding | Classification | Review decision |
| --- | --- | --- | --- |
| L01 | ENBR2: 43 annual rows have estate RV 0; original estate CSV record 206 supplies **53176**. ENNL7: 107 rows have 0; record 207 supplies **107430**. The supplied estate service costs are all zero for these groups. | Confirmed annual/source discrepancy; denominator omission, not altered charge amount | Resolved with user approval: all 150 RVs restored to the supplied values. Original snapshot findings retained for traceability. |
| L02 | Four 2022–2023 block labels lack an exact PDF name match. Three—**BD001961 Barcombe Avenue 239–241**, **BD000440 Chardin House 1–15**, **BD003244 Mead Row 1–16 Cons**—have no corresponding named block in the retained block PDF. Cowley and Wellington Mills estate totals also have no named row in the estate PDF. | Source/provenance gap; their presence in a legacy export is insufficient independent evidence | Resolved with user approval: remove all three unsupported 2022–2023 rows. Source-backed later-year rows and lookups retained. See L02-details.md. |
| L03 | The fourth label is **BD001520 DUNBAR STREET 45–63**. The PDF says **Dunbar Street 51**, with the same RV 326 and all 21 block amounts. PDF page 7 has no estate label for that row. The output's broader address range and EA040 mapping are later assignments. | Financial match; identity/address-coverage assumption requiring review | Resolved with user approval: remove the 2022–2023 row because the single-property figures cannot be established as covering the later 45–63 group. Later-year rows and lookup retained. |
| L04 | Six estate PDF records have no estate represented in the 2022–2023 annual file: Maytree Walk, Limetree Close, Guernsey Grove, Joseph Powell, Knights Walk and Greenham Close. | Coverage gap in a block-row format; not proof that a supplied block was dropped | Accepted by user: leave the files as they are; no auxiliary file or invented block rows required. |
| L05 | **631 block lookup rows and seven estate lookup rows** have no annual use. **640 block IDs** are absent from the retained 2023/2024 ID-bearing source CSVs; nine of those are used in annual files. They may originate in supplemental lists, which are not retained here. | Lookup scope/provenance gap, not automatically invalid codes | Unused lookup entries accepted by user and retained. The separate ID-source evidence limitation remains documented; detailed keys are in findings.csv. |
| L06 | 2015–2016 through 2021–2022 have **30 annual rows** but no original council attachments in this repo. Their 810 charge cells match the legacy website export. RVs match the documented oldest-known annual-value carry-back. | Cannot independently verify historical transformations or actual historical RVs | Accepted: user confirms these years were user supplied. Missing council attachments are expected; no data change required. |
| S01 | **61 Southwark block-to-estate mappings** cannot be matched by normalized full block name to the supplied lookup workbook; this includes the five explicitly unassigned blocks. The remaining **2800** exact matches agree with their assigned estates. | Mapping evidence gap; not 61 confirmed wrong estates | Resolved with user approval: all 61 rows removed from the annual CSV; 2800 source-matched rows remain. Original candidate suggestions retained only as audit evidence. |
| T01 | The 2023–2024 Tower Hamlets block CSV has **no estate or mapsite relationship columns**. Its 877 parent assignments therefore lack direct same-year source evidence. Of the 1008 block lookup records, **134** have no unique full-address match in the 2022 workbook; 874 have an exact historical match and those relationships agree. | Cross-year/inferred identity and membership limitation | Accepted by user as a documented mapping risk, not a confirmed bug. Retain the data; confirmation would require additional council information. |
| T02 | Two mapsite lookup names lack a 2022 workbook full-name match; **TE000090 Watts Grove** has no exact estate-name counterpart in that workbook. The later files supply codes, not a full-name/estate hierarchy. | Later-code/name provenance gap | Accepted by user as a documented source-evidence limitation. Retain the data and synthetic-ID labels. |
| W01 | Wandsworth count reconciliation differs for **57 estates with supplied estate counts**, plus **20 groups whose estate counts are unavailable**. All retained counts match their source values. | Source-side inconsistency/coverage, not transformation corruption | Accepted by user as a documented source-data limitation. Retain supplied values; do not treat unreconciled counts as verified denominators. See wandsworth-count-reconciliation.csv. |
| D01 | Documentation in the Lewisham borough/year/lookups READMEs mentions a service lookup file, but no such file exists in the repository. The charge pivot itself matches the source, including the agreed WINCL merge. | Documentation/deliverable discrepancy | Resolved: inaccurate service-lookup references removed from the Lewisham READMEs. Services are annual CSV columns. |

## Lookup audit first

All block, estate and mapsite lookup files were checked for duplicate identities, referenced-parent existence and annual use. Annual names were checked against lookups. Names are compared after case/spacing/punctuation normalization; this is not a fuzzy street-address correction. Synthetic IDs cannot be validated as council-issued IDs: only their uniqueness and the source-backed entity/relationship can be checked.

- **Lambeth:** 3100 blocks / 210 estates. ID-bearing 2023/2024 originals support 2460 lookup block codes; 640 lack that retained evidence. The seven unused estate rows and 631 unused block rows are listed, not deleted. EX01 and reassignment of source non-estate codes are recorded as mapping overrides, not silently called corruption. The PDF supplies names and financial values, not council IDs.
- **Lewisham:** 2652 scheme/group pairs / 54 schemes. All lookup codes and names match the trimmed original `sc_schid`, `sc_grpid`, `sc_schname` and `sc_grpdesc`. Bare group codes legitimately repeat across schemes. All lookup rows have annual use.
- **Southwark:** 2861 blocks / 405 estate/group IDs. All block labels have a source charge row, and all ordinary estate labels appear in the source workbook/estate charges. Parent links have 2800 exact corroborations and 61 unresolved full-name cases. IDs are synthetic. Unassigned estate is an intentional synthetic grouping, not a council estate.
- **Tower Hamlets:** 1008 blocks / 91 estates / 176 mapsites. All annual lookup references are valid. The 874 exact 2022 full-address records agree with the original workbook's estate and mapsite relationships. Later abbreviated-code links have the limitations in T01/T02. No amount discrepancy establishes or cures those links.
- **Wandsworth:** 1954 blocks / 174 estates/groups, all used. Block names/ranges, parent groups, counts and type flags match source records after two transparent spelling normalizations: `PUTNEY INFILS` → `PUTNEY INFILLS`, and `SOUTHFIELD INFLLS` → `SOUTHFIELD INFILLS`. IDs are synthetic. Twenty groups have no estate-cost source record.

## Annual-file verification

**489,070 comparisons** were performed. This includes repeated metadata checks, structural checks, historical corroboration and repeated estate values; it is not a count of independently verified original council cells. Each attempted successful/different field comparison has a source reference in the compressed cell ledger. Join failures are explicit in findings.csv and are not counted as verified.

| File | Rows | Comparisons | Equal under declared rules | Open findings / qualifications |
| --- | ---: | ---: | ---: | --- |
| `Lambeth/2015-2016/2015-2016.csv` | 3 | 99 | 99 | Historical legacy comparison only |
| `Lambeth/2016-2017/2016-2017.csv` | 2 | 66 | 66 | Historical legacy comparison only |
| `Lambeth/2017-2018/2017-2018.csv` | 3 | 99 | 99 | Historical legacy comparison only |
| `Lambeth/2018-2019/2018-2019.csv` | 3 | 99 | 99 | Historical legacy comparison only |
| `Lambeth/2019-2020/2019-2020.csv` | 5 | 165 | 165 | Historical legacy comparison only |
| `Lambeth/2020-2021/2020-2021.csv` | 6 | 198 | 198 | Historical legacy comparison only |
| `Lambeth/2021-2022/2021-2022.csv` | 8 | 264 | 264 | Historical legacy comparison only |
| `Lambeth/2022-2023/2022-2023.csv` | 1900 | 56529 | 56529 | 141 review records; see classifications |
| `Lambeth/2023-2024/2023-2024.csv` | 2438 | 80454 | 80304 | 1042 review records; see classifications |
| `Lambeth/2024-2025/2024-2025.csv` | 2107 | 69531 | 69531 | 764 review records; see classifications |
| `Lewisham/2022-2023/2022-2023.csv` | 2652 | 112167 | 112167 | 0 review records; see classifications |
| `Southwark/2022-2023/2022-2023.csv` | 2861 | 60081 | 60081 | 61 review records; see classifications |
| `Tower Hamlets/2022-2023/2022-2023.csv` | 874 | 33212 | 33212 | 0 review records; see classifications |
| `Tower Hamlets/2022-2023/mapsites.csv` | 174 | 1740 | 1740 | 0 review records; see classifications |
| `Tower Hamlets/2023-2024/2023-2024.csv` | 877 | 31572 | 31572 | 0 review records; see classifications |
| `Tower Hamlets/2023-2024/mapsites.csv` | 176 | 1760 | 1760 | 0 review records; see classifications |
| `Wandsworth/2023-2024/2023-2024.csv` | 1954 | 41034 | 41034 | 2 review records; see classifications |

### Lambeth

Every matched block RV and all 21 block service columns were compared separately, as were every matched estate RV and all six estate service columns. For 2023/2024, council column-code mappings were explicit. For 2022, the PDFs were independently extracted with `pdftotext -layout`, taking RV plus 21 or six amounts from the right of each row to prevent column shifts. The block PDF yielded 1897 rows; the estate PDF yielded 193. The Dunbar page was also visually inspected. Text-line references count Python `splitlines()` of that extraction; they are not PDF row numbers.

The previously corrected Dunbar and Barcombe estate amounts agree with the retained estate PDF where those estate rows exist. This audit cannot verify Barcombe's block charge vector from the block PDF, which does not contain it.

The **230 fractional-penny cells in 2024–2025** reproduce the originals: 174 distinct block charges and four estate charges repeated 56 times. All values, including fourteen occurrences of 385.6454795, are source-origin, not introduced by the annual reformatting. They are catalogued in source-precision.csv. This says nothing about whether Lambeth's original calculation was correct.

There are 1656 annual/source estate-code overrides across 2023/2024. These include the user-approved non-estate regrouping and stable-estate mappings. They remain visible as `mapping_override` review rows because original labels and output identity are different; they are not numerical charge errors. The 2022 PDF has no named estate records for BR2/NL7 or the two estates in L02: those values remain unverified rather than being certified by their repetition in the annual file.

### Lewisham

The raw 11753 service observations were independently pivoted by scheme/group/service. All 25 output services, all group property counts and source names match. Absent services and ten `NULL` costs become zero by agreement. The two WINCL observations duplicate Window Cleaning for LG/JOHN2 and LG/PAYN3 and are retained once as explicitly agreed. Complementary groups sharing descriptions remain separate. The -554.41 lighting credit remains attached to its source group. No unexplained numeric discrepancy found.

### Southwark

All 2861 block source rows' weighting and eleven charge amounts match. All matched estate weightings and four estate service amounts match and repeat consistently. Fisher's missing estate weighting, missing estate source records, and the five unassigned groups use the agreed zero treatment. These zeros do not validate the missing denominator. The unresolved 61 parent mappings prevent a full correctness assertion for their selected estate charges, even though the chosen estate's amounts themselves match the estate source. The source estate file's `Total` row is a summary, not a missing estate record.

### Tower Hamlets

All 874 workbook block rows and 877 later CSV block rows match their represented costs, GRVs and supplied population counts. All 174/176 mapsite records match the represented mapsite values, including the 8/9 mapsites without blocks. The main files' mapsite values are separately compared to the original mapsite source, rather than merely compared to the derived mapsites.csv. Boiler names/system points/block points match available 2022 boiler-sheet records; unavailable year-specific fields are zero/`Not supplied` as documented.

Workbook cached numeric values contain floating-point tails such as 193735.80000000005. Differences below 0.000001 are classified as Excel representation noise, not changed currency costs; this tolerance is explicit, confined to workbook comparisons, and logged. The later CSVs are compared exactly. Source `#N/A` GRVs for the unallocated 2023 group become zero. Total-property and leasehold-property counts remain separate. The management flat rate and group total remain in separate columns.

The original workbook's estate aggregate tab and block-service aggregate columns on other tabs are not all represented in the usable annual table. This audit verifies the chosen block/mapsite grains and does not certify the council's aggregate calculations, cost basis, or that every original workbook column is a distinct additional bill item.

### Wandsworth

All 1954 source block/address records match their eight charges, supplied property counts and Y/H type flags. Estate counts and five estate charges match wherever supplied. The 20 unmatched estate/property groups retain zero placeholders. The -1691 electricity credit is preserved. Nine source address ranges already resemble dates; this is a source-quality issue rather than a conversion performed here. The 77 reconciliation rows separate supplied count discrepancies from missing estate-count records.

## Reproduce and inspect

Run from any directory with Python 3 and Poppler's `pdftotext` available:

```sh
python3 /home/ai-ajross/projects/servicechargedata/Audit/2026-10-22/audit.py
```

The historical corroboration additionally reads `/home/ai-ajross/projects/ServiceChargerator/public/charges.csv` and `blocks.csv`. That is a disclosed dependency on a prior transformed export, not primary source evidence. No network download, database import, rounding of annual files or data repair is performed.

- [findings.csv](findings.csv): every discrepancy, mapping override, source join gap and unused lookup key, with source references. `difference` is the numerical mismatch category; other categories have the different meanings described above. The numerous overrides/gaps must not be counted as thousands of corrupted charge cells.
- [southwark-mapping-review.csv](southwark-mapping-review.csv): all 61 unresolved mappings with three possible source-book candidates each. Similarity is not proof. Some candidates intentionally demonstrate why fuzzy matching would be unsafe.
- [wandsworth-count-reconciliation.csv](wandsworth-count-reconciliation.csv): source-count discrepancies and unavailable-count groups.
- [source-precision.csv](source-precision.csv): all 230 fractional-penny annual cells.
- [coverage.json](coverage.json): per-file comparison counts; `excel_noise` and `blank_to_zero` are explicitly permitted normalizations.
- [cell-ledger.csv.gz](cell-ledger.csv.gz): successful and differing field comparisons, compressed to avoid a roughly 57 MB text file. Keys and source references enable tracing. Unmatched joins appear in findings rather than a fictitious verified ledger entry.
- [input-sha256.json](input-sha256.json): hashes of every repository CSV/PDF/XLSX input at audit time.
- [supplemental-sha256.json](supplemental-sha256.json): hashes of the historical legacy exports used for corroboration.
- [audit.py](audit.py): independent read-only audit, including injected in-memory penny/sign mistakes to confirm that the checker flags numerical changes.

No fixes have been applied. Review the identity/provenance gaps separately from the confirmed RV discrepancy before deciding what to change. Missing primary evidence cannot be repaired by choosing the most similar name or the most common value.
