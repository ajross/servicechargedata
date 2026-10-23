# Data Source

Original: [Actuals22 23.csv](<Original Data/Actuals22 23.csv>), supplied with the [30 July 2024 FOI response](https://www.whatdotheyknow.com/request/actual_service_charge).

The source is available as `2022-2023.csv` with estate and block lookup files; services are columns in the annual CSV. The original is unchanged. Record references below count the header as CSV record 1. Estate and block are output labels for source schemes and charging groups, respectively.

The data has been cleaned of text padding and pivoted into one row per estate/block combination, with services as columns. Missing service records and the ten source `NULL` costs have been set to `0.00`. The two matching WINCL duplicates have been merged into `Window_Cleaning`, retaining each amount once.

The [borough README](../README.md) describes the annual file format and calculation methodology; the [lookup README](../Lookups/README.md) explains the identifiers.

## What a row means

Each source row is a cost for one service and one charging group within a scheme. A group may describe a block, part of a block, overlapping address range, heating/lift beneficiaries or scheme-wide management/insurance properties. Scheme descriptions include neighbourhood and PFI groupings as well as named estates.

For Bayes Close (`BC`), the supplied groups include:

| Group code | Description | Property count | Example service/cost |
|---|---|---:|---|
| BAY1F | BAYES CLOSE 2 + 4 | 2 | Fire risk assessment 106.00 |
| BAYE10 | BAYES CLOSE 1 TO 4 | 4 | Repairs 0.00 |
| BAYES1 | BAYES CLOSE 1 TO 12 | 12 | Communal lighting 355.68 |
| BAYES2 | BAYES CLOSE 13 TO 24 | 12 | Communal lighting 324.48 |
| BAYES4 | BAYES CLOSE 1 TO 24 | 24 | Caretaking 2,184.59; grounds maintenance 2,708.40 |
| MGMT | ALL PROPERTIES MANAGEMENT | 24 | Management 1,800.00; insurance 973.68 |

These records cannot be collapsed into one block row without service-specific group membership. The two sweeping costs are both 573.40 for groups BAYES3 (7 properties) and BAYES4 (24 properties). Repetition alone therefore does not establish that an amount is an estate total to copy across rows.

## Duplicate descriptions and aliases

There are no competing observations for the same scheme/group/service key, so there is no basis for choosing a modal cost and discarding an outlier.

Three descriptions repeat under different group codes in the same scheme:

| Scheme | Group codes | Finding and handling |
|---|---|---|
| BY | FOX2, FOX2LI | FOXBOROUGH GARDENS 153 TO 199, both count 24. FOX2LI contains only the lift service, while FOX2 has other services. Retain both groups. |
| FH | 24BEAD, BEAD3 | BEADNELL ROAD 24 TO 34, both count 6. Services are complementary between the two groups. Retain both groups. |
| EW | DAL23, FIR26 | Both say DALMAIN ROAD 23, count 1, Repairs Level 3 cost 0.00. FIR26 may be mislabelled, but the intended property cannot be established. Retain and flag; do not infer a corrected address or merge them. |

At records **11753–11754**, WINCL repeats Window Cleaning exactly:

| Estate / block | Properties | Window Cleaning record/cost | WINCL record/cost |
|---|---:|---|---|
| LG / JOHN2 | 8 | 7365 / 30.00 | 11753 / 30.00 |
| LG / PAYN3 | 9 | 7925 / 27.00 | 11754 / 27.00 |

The two WINCL records are treated as duplicate source errors and merged into `Window_Cleaning`. Each matching amount is retained once, and the separate `Wincl` column is removed. Both source labels appear under the same annual charge column. This interpretation is supported by matching keys, descriptions, counts and costs. The **11,753 original observations become 11,751 distinct observations across 25 annual service columns**; both duplicate source records remain in the untouched original.

## Insurance and management observations

The amounts support interpreting these fields as group totals rather than already-calculated individual bills:

- Insurance is exactly `Property_Count × 40.57` in 51 of 52 records. Brockley PFI is `1605 × 83.07 = 133327.35`.
- Management is exactly `Property_Count × 75.00` in 49 of 52 records. Brockley PFI, Ewart Road Co-op and Fiveways use 86.22 per counted property.
- Brockley PFI insurance counts 1,605 properties while management counts 1,606. Preserve these separate group counts; do not substitute a scheme-wide total.

Unfortunately it's not possible to directly attribute these to a single estate wide charge since the property counts for these charges do not reliably match the counts for all the blocks/grp_ids on the estate/schid.
