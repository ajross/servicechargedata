# Tower Hamlets Data

The files contain reported block and mapsite service charges for 2022–2023 and 2023–2024, gross rateable values (GRVs), property counts and lookup names.

A **mapsite** is the communal charging area used for estate services. Larger named estates can contain several mapsites. Use the mapsite, rather than the larger estate name, for estate-service apportionment.

## Sources

- [2022–2023 FOI request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_4); the workbook includes the council's definitions and calculation rules.
- [2023–2024 FOI request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_8); block and mapsite CSVs supplied on 14 April 2025.
- [Council charging-methodology guide](https://www.towerhamlets.gov.uk/Documents/Housing/Housing-management/Overview-of-how-your-charges-are-calculated.pdf).

## Annual service-charge files

Main files are stored as `Tower Hamlets/YYYY-YYYY/YYYY-YYYY.csv`. Each row represents a supplied block or property group, with associated mapsite charges repeated alongside its block charges. Both years have **39 columns**: 17 identification/apportionment fields and 22 amount/rate fields.

| Year | Block records | Mapsite records |
|---|---:|---:|
| 2022–2023 | 874 | 174 |
| 2023–2024 | 877 | 176 |

Each year also has `mapsites.csv`, containing the complete mapsite-level costs and GRVs. This includes mapsites with no associated block in the supplied block data: eight in 2022–2023 and nine in 2023–2024.

Amounts are in GBP with two decimal places. Negative amounts are credits. Zero can mean no supplied value; it does not prove that a service was free. A block absent from a year is not a zero-charge observation.

### Identification and gross rateable values

| Columns | Description |
|---|---|
| `Year_Start`, `Year_End` | Service-charge year. |
| `Estate_ID`, `Estate_Name` | Larger estate or non-estate grouping. |
| `Mapsite_ID`, `Mapsite_Name` | Communal charging area. |
| `Mapsite_GRV`, `Block_GRV` | Year-specific gross rateable values; 0 means unavailable. |
| `Block_ID`, `Block_Name` | Block/group identifier and supplied address or code. |
| `Mapsite_Property_Count`, `Block_Property_Count` | Total property counts supplied for 2022–2023. |
| `Mapsite_Leasehold_Property_Count`, `Block_Leasehold_Property_Count` | Leasehold counts supplied for 2023–2024. |
| `Boiler_Name` | Communal boiler identifier where supplied. |
| `Boiler_Total_Points`, `Block_Boiler_Points` | Boiler-system and block boiler points, available for 2022–2023. |

An unavailable count or points value is 0; an unavailable boiler name is `Not supplied`. The two count types are distinct and should not be compared as the same population. GRVs also vary by year.

Some 2023–2024 block names are abbreviated source codes without a confirmed address range. Such records do not establish a unique cross-year address match. The [lookups](Lookups/README.md) describe identifiers and source groupings.

### Block charge columns

These contain the reported amounts associated with each block:

| Column |
|---|
| `Block_Repairs` |
| `Boiler_Repairs` |
| `Block_Lift_Repairs` |
| `Block_Door_Entry_System_Repairs` |
| `Block_TV_Aerial_Repairs` |
| `Block_Caretaking` |
| `Block_Bin_Hire` |
| `Boiler_Fuel` |
| `Block_Communal_Electricity` |
| `Block_Concierge_Service` |
| `Block_Pest_Control_Service` |
| `Block_Resident_Engagement_Service` |
| `Block_Customer_Access` |
| `Block_Antisocial_Behaviour_Service` |
| `Block_TMO_Housing_Management_Service` |
| `Block_Building_Insurance_Total` |

### Estate charge columns

Estate services are charged by mapsite:

| Column |
|---|
| `Mapsite_Repairs` |
| `Mapsite_Caretaking` |
| `Mapsite_Grounds_Maintenance` |
| `Mapsite_Bulk_Waste` |

These amounts repeat across associated block rows. **Do not sum them across blocks**; use each year's `mapsites.csv` for mapsite totals.

## Calculation Methodology

For services apportioned by GRV, the council's calculation is:

```text
Block share = Full block service cost × Property GRV / Block GRV
Mapsite share = Full mapsite service cost × Property GRV / Mapsite GRV
```

Boiler repairs use the boiler unit's GRV, which is not supplied as a separate denominator. Fuel uses property boiler points divided by total boiler points. Insurance depends on bedrooms; leasehold management is a flat-rate service.

The workbook contains unusually large aggregated figures, and the years are not verified as like-for-like full service costs. The supplied amounts should not be treated as confirmed numerators for an individual bill without clarification of their cost basis. Missing denominators and 2023–2024 boiler points also limit bill calculations. The linked methodology guide illustrates historical tariffs; the annual files supply the amounts for their respective years.

## Additional Charges

Insurance and boiler fuel are already included in the amount columns. Leasehold management has two separate fields:

| Column | Meaning |
|---|---|
| `Leasehold_Management_Per_Property` | Supplied 2022–2023 flat rate: £169.08 where recorded. |
| `Leasehold_Management_Total` | Supplied 2023–2024 block/group management amount. |

A zero in the other management field means that basis was not supplied. A per-property rate must not be added as though it were a block total. Property-specific charges and adjustments may also appear on an individual invoice.
