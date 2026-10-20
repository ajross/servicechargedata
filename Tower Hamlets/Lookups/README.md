# Block and Estate Lookups

The lookups contain the block, mapsite and estate names represented in the annual files. Each block record links to a mapsite charging area and a larger estate/group.

| File | Columns | Records |
|---|---|---:|
| `blocks.csv` | `Block_ID,Block_Name,Estate_ID,Mapsite_ID` | 1,008 |
| `mapsites.csv` | `Mapsite_ID,Mapsite_Name` | 176 |
| `estates.csv` | `Estate_ID,Estate_Name` | 91 |

Estate IDs beginning `TE` and block IDs beginning `TB` are **synthetic IDs created to identify and link records in the annual CSVs**; they were not supplied by the council. Other block and mapsite IDs are the codes/names supplied in the 2023–2024 files.

A block name can be a full address range or an abbreviated code. Some codes lack a confirmed address match, so the 1,008 lookup records are not a verified count of distinct physical buildings across both years.

`NO MAPSITE` and `NO ESTATE` are supplied group labels with recorded costs, rather than ordinary named estates. `OTHER NOT IN BLOCK` represents the unallocated 2023–2024 property group under `TE000000,Unassigned estate`.

GRVs, counts and boiler points are held in the annual files because they relate to a particular year. The larger estate name is not the GRV denominator for mapsite services.
