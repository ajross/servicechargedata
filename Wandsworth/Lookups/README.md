# Block and Estate Lookups

These lookups identify the estates/property groups and blocks/address groups present in the annual service-charge files.

| File | Columns | Contents |
|---|---|---|
| `estates.csv` | `Estate_ID`, `Estate_Name` | 174 estates or property groups. |
| `blocks.csv` | `Block_ID`, `Block_Name`, `Estate_ID` | 1,954 blocks or address groups, each linked to an estate/group. |

`WE` estate IDs and `WB` block IDs are **synthetic IDs created to produce and link the annual CSV**. They are not council-issued identifiers. Retain these IDs when adding future years; new groups should receive new IDs.

Block names include the supplied address range where available. Different ranges on the same street are separate groups. Nine source ranges appear as dates, and one range is absent; these limitations also apply to the lookup names.

Join annual files to these lookups using `Estate_ID` and `Block_ID`. Every lookup entry appears in the 2023–2024 annual file.
