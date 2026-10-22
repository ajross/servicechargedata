# L02: the three 2022–2023 blocks without retained PDF records

L02 identifies missing supporting source records, not conflicting charge amounts. The annual file contains these three blocks, but the retained 2022–2023 block PDF contains no corresponding named rows. The user has since authorised removal of all three rows from the 2022–2023 annual CSV (1900 → 1897 rows). Their source-backed later-year rows and block lookup records remain. The user considers the January 2024 additions likely to have been user-submitted; that origin is plausible but not independently documented. The tables below preserve the pre-removal audit values.

## Identifiers and rateable values

| Field | BD001961 | BD000440 | BD003244 |
| --- | --- | --- | --- |
| Block name | Barcombe Avenue 239-241 | Chardin House 1-15 | Mead Row 1-16 Cons |
| Block RV | 434 | 3971 | 4173 |
| Estate ID | EA069 | EA036 | EA122 |
| Estate name | Leigham Court Estate | Cowley Estate | Wellington Mills Estate |
| Estate RV | 175220 | 139809 | 37163 |

These values are from the audited 2022–2023 annual CSV before the approved removals. All three IDs, block names and block RVs are also present in the older `ServiceChargerator/data/Block Description list.csv`; `Estate_Block_Codes.csv` supports all three estate links. The original 2023–2024 boroughwide block CSV independently supplies the same block IDs, names, block RVs and estate links. This corroborates identity; it does not establish the 2022–2023 charges.

## Every charge value in the annual file

These are the pre-removal total block/estate amounts in pounds, not per-flat charges. Estate totals repeat on each applicable block row. Zero values are shown explicitly.

| Annual CSV field | BD001961 | BD000440 | BD003244 |
| --- | ---: | ---: | ---: |
| Block_Boiler_Repairs_and_Maintenance | 0.00 | 6635.26 | 5986.74 |
| Block_Cleaning | 0.00 | 2252.85 | 2065.51 |
| Block_Communal_Electricity | 0.00 | 6503.97 | 0.00 |
| Block_Communal_Electrical_Maintenance | 0.00 | 513.31 | 100.05 |
| Block_Communal_Ventilation_Maintenance | 0.00 | 0.00 | 13162.93 |
| Block_Communal_Water_Quality | 0.00 | 206.86 | 0.00 |
| Block_Communal_Window_Cleaning | 0.00 | 117.28 | 0.00 |
| Block_Concierge | 0.00 | 0.00 | 0.00 |
| Block_CCTV | 0.00 | 0.00 | 0.00 |
| Block_Disinfestation | 0.00 | 221.02 | 0.00 |
| Block_Door_Entry_System | 0.00 | 0.00 | 0.00 |
| Block_Dry_Riser | 0.00 | 0.00 | 0.00 |
| Block_Lightning_Protection | 0.00 | 0.00 | 0.00 |
| Block_Lift_Services_and_Repairs | 0.00 | 1257.02 | 0.00 |
| Block_Fire_Ventilation_Maintenance | 0.00 | 0.00 | 0.00 |
| Block_Repairs_and_Maintenance | 0.00 | 38.17 | 0.00 |
| Block_TV_Aerial | 0.00 | 0.00 | 124.53 |
| Block_Ext_Cleaning | 0.00 | 0.00 | 0.00 |
| Block_Ext_External_Tree_Maintenance | 0.00 | 0.00 | 0.00 |
| Block_Ext_Grounds_Maintenance | 0.00 | 0.00 | 0.00 |
| Block_Ext_Repairs_and_Maintenance | 0.00 | 0.00 | 0.00 |
| Estate_Cleaning | 18522.72 | 30134.80 | 14886.60 |
| Estate_CCTV | 0.00 | 57787.72 | 0.00 |
| Estate_Communal_Electricity | 2602.43 | 0.00 | 29028.00 |
| Estate_Grounds_Maintenance | 338.21 | 26845.50 | 12186.50 |
| Estate_Repairs_and_Maintenance | 0.00 | 16468.20 | 8589.02 |
| Estate_Tree_Maintenance | 336.41 | 30655.02 | 0.00 |

## Traced origin in the original website history

The two populated charge records were individual additions to `ServiceChargerator` before the April 2024 boroughwide FOI import:

| Current block | First addition | Commit message | Original block / estate IDs |
| --- | --- | --- | --- |
| BD000440 — Chardin House 1–15 | 27 January 2024, `c497ca041c409aeb572d130c2e5b65635570a08a` | Add Chardin House, Cowley Estate data | 13 / 10 |
| BD003244 — Mead Row 1–16 Cons | 24 January 2024, `eef134db51d66ef017f064d0e3e618d13e71a616` | Add data for Wellington Mills Estate | 10 / 8 |

Each commit directly adds the block, estate and charge rows to `public/blocks.csv`, `public/estates.csv` and `public/charges.csv`. Every one of the 27 annual charge values, the block RV and the estate RV matches the corresponding initial January addition exactly. These commits contain no invoice or original attachment and do not explain how the figures were obtained. Their underlying documentary source therefore remains unknown; it would be speculation to call them council-FOI figures or resident-invoice figures.

`cee7cd1` (22 April 2024, “Update estate and block codes to Lambeth values”) replaces the old numeric IDs with the current council codes. `4a7589e` (29 April 2024, “Update with latest FOI data”) imports the later bulk dataset. The January records predate that import and survived into the legacy website export used for the new annual files. This establishes that their figures were not invented by the recent annual CSV transformation.

Barcombe also originated in an individual addition: `9cb9e1306f6142d863f1e0d1ed34f10d8569576e`, 27 January 2024, “Add data for Barcombe Avenue, Leigham Court Estate”. Its original block charges were all zero. Its 2022–2023 row has now been removed as instructed.

These histories can be inspected with `git -C /home/ai-ajross/projects/ServiceChargerator show <commit>`.

## What could and could not be matched

- **BD001961, Barcombe Avenue 239–241:** the block PDF contains numerous other Barcombe Avenue addresses, but none for 239–241. Its RV of 434 and all 21 zero block charges appear in the old website exports. Other Barcombe addresses have their own rows; their presence does not establish the missing address's figures. Leigham Court Estate *is* in the estate PDF: RV 175220, cleaning 18522.72, CCTV 0, communal electricity 2602.43, grounds 338.21, repairs 0, trees 336.41. These match the current annual row. Four estate amounts differ from the old website export (cleaning 18522.21, electricity 2599.10, grounds 335.84, trees 335.84); those were already corrected against the PDF before this audit. L02 leaves only the missing primary evidence for the block RV/charges, not the current Leigham estate amounts.
- **BD000440, Chardin House 1–15:** no Chardin row appears in the block PDF, and Cowley Estate has no row in the estate PDF. The RV and all 27 charges in the annual file are consistent with the old website exports. That is evidence they predate the recent reformatting, but the old export is itself transformed data and cannot independently verify those 2022–2023 figures.
- **BD003244, Mead Row 1–16 Cons:** no Mead Row row appears in the block PDF, and Wellington Mills Estate has no row in the estate PDF. The RV and all 27 charges agree with the old website exports. As with Chardin, the retained council PDFs cannot independently verify them. The text “Longmead House” occurs in the PDF; it is a different block on Woodvale Estate and is not a candidate match.

The `Block.pdf` and `Estate.pdf` files in the older `ServiceChargerator/data` directory are byte-identical to those retained in `servicechargedata`, so they do not supply an alternative version containing these missing rows. No source-specific charge disagreement has been established for the missing block records; the reason they could not be matched is their absence from the retained primary attachments.

## Other available RV evidence

The undated supplementary `ServiceChargerator/data/Estate_List.csv` gives Leigham Court RV **174768**, Cowley RV **140430**, and Wellington Mills RV **37163**. The current 2022–2023 annual file uses **175220**, **139809**, and **37163** respectively. Leigham's annual value is supported by the 2022 PDF; Cowley's 139809 also appears in the original 2023–2024 estate CSV. The supplementary list has no established charging year here, so its differing RVs are not grounds to overwrite the annual data.

The 2023–2024 originals supply all three block identities with the same block RVs (434, 3971 and 4173); their different service amounts apply to a different year. The 2024–2025 block original includes Barcombe 239–241 (RV 434), but no corresponding Chardin or Mead Row row. None of this supplies the missing 2022–2023 primary charge records.

## Source locations

- Pre-removal snapshot values (all three rows are now removed): [2022–2023 annual CSV](../../Lambeth/2022-2023/2022-2023.csv), audit snapshot records 537 (Barcombe), 282 (Chardin), 1847 (Mead), counting the header as record 1. All three rows are now removed; their values remain recorded in this audit document and L02-resolution.json.
- Primary attachments: [block PDF](../../Lambeth/2022-2023/Original%20Data/Block.pdf), [estate PDF](../../Lambeth/2022-2023/Original%20Data/Estate.pdf).
- Later council evidence: [2023–2024 original block CSV](../../Lambeth/2023-2024/Original%20Data/23-24%20Boroughwide%20Block%20Costs%20v2.csv), records 1334 (Barcombe), 341 (Chardin), 2121 (Mead); [original estate CSV](../../Lambeth/2023-2024/Original%20Data/23-24%20Boroughwide%20Estate%20Costs%20v2.csv).
- Additional available lists: `/home/ai-ajross/projects/ServiceChargerator/data/Block Description list.csv` (records 1807, 431, 2789), `Estate_Block_Codes.csv`, and `Estate_List.csv` (records 65, 35, 114). These files are outside the data repository and their dates are not established by this review.
- Historical corroboration: `/home/ai-ajross/projects/ServiceChargerator/public/blocks.csv`, `estates.csv` and `charges.csv`. These are prior transformed website exports, not original charge attachments.
