# Lewisham lookups

The lookups preserve the council's original scheme and group codes in separate columns. The pair `(Estate_ID, Block_ID)` uniquely identifies each block record. Estate/block terminology follows the annual-file convention: the source entities are schemes and charging groups, some of which overlap or are service-specific.

| File | Columns | Rows |
|---|---|---:|
| `estates.csv` | `Estate_ID,Estate_Name` | 54 |
| `blocks.csv` | `Block_ID,Block_Name,Estate_ID` | 2,652 |

## Source mapping

- `Estate_ID` = trimmed `sc_schid`; `Estate_Name` = cleaned `sc_schname`.
- `Block_ID` = trimmed original `sc_grpid`; `Block_Name` = cleaned `sc_grpdesc`.
- Join annual records to the block lookup using both `Estate_ID` and `Block_ID`. For example, estate `BC` and block `BAYES1` identify one record.
- Services are represented by charge columns in the annual CSV. `WINCL` and `WINDOW CLEANING` both appear under `Window_Cleaning`, with the two matching duplicate observations retained only once.

There are 2,546 distinct bare group codes but 2,652 estate/group pairs. `MGMT`, for example, is used under 51 schemes. Block_ID alone is not globally unique: use `(Estate_ID, Block_ID)` as the lookup key. Each lookup record references one estate; all lookup entries have annual data.

Names are display fields rather than identity keys. Within each estate/group pair, the description and property count are consistent across all source service records. Counts stay in the annual CSV because they can vary by year. No RVs were supplied.

When adding future years, reuse these source-code pairs where supported by the incoming records. Review changed codes or descriptions rather than silently merging by name. Preserve the original codes if additional council identifiers become available.

## Service-specific groups and aliases

For example, Bayes Close 1–12, 1–24 and 2 + 4 are separate supplied groups carrying different services. Keep each group under its own ID. The three duplicate-description cases are documented in the year README; complementary services are retained separately and the potentially mislabelled EW / FIR26 record is flagged without guessing a corrected address.

`WINCL` and `WINDOW CLEANING` are merged into the single `Window_Cleaning` annual column. Their two matching observations are treated as duplicate source errors; each amount is retained once. Both original labels remain in the source attachment. See the borough and year READMEs for the evidence.
