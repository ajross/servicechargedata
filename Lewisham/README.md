# Lewisham Data

The service charge data for Lewisham was supplied by Lewisham Council in response to a Freedom of Information request. The 2022–23 data has been cleaned and pivoted into an annual CSV, with estate, block and service lookup files. The original attachment is unchanged.

The source scheme is represented as an estate and the source charging group as a block. Groups may cover a building, an address range, service-specific properties or an entire scheme.

Due to the way Lewisham have formatted the data, charges applied to a property may span multiple rows.
For example, `2 Bayes Close` appears to be covered by multiple `sc_grpid` (i.e. what we're treating as a block ID) entries.

| Estate | Block code | Properties covered | Service |
|---|---|---|---|
| BC | BAY1F | 2 + 4 | Fire risk assessment |
| BC | BAYES1 | 1–12 | Communal lighting |
| BC | BAYES4 | 1–24 | Caretaking |

Some groups overlap, so a resident may need several groups to identify all applicable services.

## Sources

- [FOI request and response](https://www.whatdotheyknow.com/request/actual_service_charge): request 3 July 2024, response 30 July 2024, reference **25223277**.
- [Council service descriptions and calculation guidance](https://lewisham.gov.uk/myservices/housing/leaseholders/your-property/services-we-provide-to-leaseholders).

The FOI describes allocation among benefiting properties, with some rateable-value exceptions. Its 4 August 2024 follow-up asks about the field definitions, calculations, repair levels and WINCL; no reply appears on the request page reviewed on 19 October 2026.

Original files and processing details are recorded in the [2022–23 README](2022-2023/README.md).

## Annual service-charge files

Files are stored as `Lewisham/YYYY-YYYY/YYYY-YYYY.csv`.

Each row represents one estate/block charging-group combination for one service-charge year. The 2022–23 file contains **2,652 rows and 32 columns**: seven identification/property-count fields and 25 charge fields.

Numeric charge values are in GBP, without currency symbols or thousands separators, and have two decimal places. CSV files use UTF-8 with BOM for Excel.

Where a group has no source record for a service, the charge is set to `0.00`. The ten source `NULL` costs are also set to `0.00` as a processing assumption. All annual charge cells are numeric; consult the original file to distinguish these substitutions from reported zeros. A group absent from the file should not be interpreted as having zero charges.

### Identification and property counts

| Column | Description |
|---|---|
| `Year_Start` | Four-digit starting year of the service-charge period. |
| `Year_End` | Four-digit ending year of the service-charge period. |
| `Estate_ID` | Original council scheme code (`sc_schid`), matching the estate lookup. |
| `Estate_Name` | Cleaned source scheme name (`sc_schname`). |
| `Block_ID` | Original council group code (`sc_grpid`), matching the block lookup together with `Estate_ID`. |
| `Block_Name` | Cleaned source group description (`sc_grpdesc`), including address ranges or service restrictions. |
| `Property_Count` | Source `propcnt`, used as the working count of benefiting properties for that group and year. |

**Use both `Estate_ID` and `Block_ID` to identify or join a block record.** Block codes can repeat across estates: for example, Bayes Close (`BC`) and Brasted Close (`BD`) both use `MGMT`. Annual rows are unique by `(Year_Start, Year_End, Estate_ID, Block_ID)`.

Names and codes have been cleaned of text padding. Counts remain in the annual file because they may change between years. No rateable values were supplied. See the [lookup README](Lookups/README.md) for the 54 estates, 2,652 blocks/groups and source-service mappings.

### Block charge columns

These contain the cost of each service for the supplied block or charging group. Group membership determines which properties share the cost; these are not necessarily whole-building costs, and the repair level numbers do not establish an estate/block hierarchy.

| Column |
|---|
| `Asbestos_Survey` |
| `Bulk_Waste_Service` |
| `Caretaking` |
| `Caretaking_Level_2` |
| `Central_Heating` |
| `Communal_Lighting` |
| `Entryphone` |
| `Fire_Risk_Assessment` |
| `Ground_Rent_Special` |
| `Grounds_Maintenance` |
| `Lift` |
| `Pest_Control` |
| `Repairs` |
| `Repairs_Level_2` |
| `Repairs_Level_3` |
| `Repairs_Special` |
| `Sweeping` |
| `Technical_Repairs_Central_Heating_Only` |
| `Technical_Repairs` |
| `Technical_Repairs_Level_2` |
| `Technical_Repairs_Level_3` |
| `Technical_Repairs_Level_4` |
| `Window_Cleaning` |

`WINCL` has been merged into `Window_Cleaning`. Its two source observations exactly duplicate existing Window Cleaning amounts: estate `LG`, block `JOHN2` (30.00) and block `PAYN3` (27.00). Each amount is retained once. The service lookup maps 26 source labels to the 25 annual charge columns.

Reported zeros and the -554.41 Communal Lighting credit are preserved. All source service observations are retained except for consolidating the two matching WINCL duplicates. Detailed mappings and validation results are in the year README.

### Estate charge columns

Estate/scheme-wide insurance and management costs are also included:

| Column |
|---|
| `Insurance` |
| `Management` |

These appear on the council's supplied management/insurance groups, such as `MGMT` and `INS`, with their own `Property_Count`. They are not copied across every block row. Other services can also cover broader groups where specified by the source description.

**Do not sum property counts across overlapping groups or add estate-wide costs more than once for a property.** Counts can differ by service: Brockley PFI has 1,605 properties in its insurance group and 1,606 in its management group.

## Calculation Methodology

The working assumption is that `Property_Count` identifies the properties benefiting from the group's service. For services apportioned equally:

`Per-property service charge = Group_Service_Cost / Property_Count`

For example, Bayes Close 1–24 caretaking is `2184.59 / 24`, approximately **£91.02** before invoice-specific rounding. Users do not need to supply the property count because it is already in the data.

The council guidance describes equal shares for caretaking, sweeping, ordinary repairs, entryphones, window cleaning and communal lighting. Technical repairs can apply to a subgroup, and lifts exclude ground-floor properties. The guidance page is marked published 9 December 2025, so it does not independently establish every 2022–23 rule.

The FOI mentions rateable-value exceptions but supplies neither the RVs nor a mapping of the services concerned. Identify the groups applicable to a property and confirm eligibility, exceptions and rounding before treating the calculation as a complete invoice reconstruction. Source `NULL` costs have been replaced with zero in the annual CSV by agreement; those zeros are processing assumptions rather than confirmed council costs.

## Additional Charges

The dataset already includes insurance, management, central heating and special ground rent where supplied. These should not be added again as separate estimated charges.

It does not establish a complete list of every item on an individual leaseholder's invoice. Any additional charge, tariff or lease-specific adjustment needs separate evidence; no Lambeth management percentage, insurance tariff or ground-rent amount is applied to Lewisham.
