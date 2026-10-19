# Lambeth Data

The service charge data for Lambeth has been sourced from a mix of resident supplied data and Freedom of Information requests.
All data from 2021-2022 onwards was supplied by Lambeth Council via FOI requests.

For each FOI request the data has been received in slightly different formats and there have been frequent data quality issues such as blocks that could not be mapped to estates.

There are some anomalies with the charge values such as negative values, however since the council has supplied this data themselves we must trust that these were the values used for calculating charges.  Perhaps they represent a refund.

## Sources

- Resident-supplied records, documented in the individual year READMEs.
- [2022–2023 FOI request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for).
- [2023–2024 FOI request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_5). The year README records that the data was ultimately supplied by email following escalation to the ICO.
- [2024–2025 FOI request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_10).
- [2025–2026 FOI request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_12).

The year-specific READMEs describe the source and processing for each period. Original files, where retained, are stored under each year's `Original Data` directory.

## Annual service-charge files

Files are stored as `Lambeth/YYYY-YYYY/YYYY-YYYY.csv`.

Each row represents one block or street-property charge group for one service-charge year. Each file contains **35 columns**: eight identification/rateable-value fields and 27 charge fields.

All charge columns contain numeric values in GBP, without currency symbols or thousands separators.

Coverage varies by year.  A block absent from a file should not be interpreted as having zero charges; it was likely just not supplied.
 
### Identification and rateable values

| Column | Description |
|---|---|
| `Year_Start` | Four-digit starting year of the service-charge period. |
| `Year_End` | Four-digit ending year of the service-charge period. |
| `Estate_ID` | Estate or non-estate grouping identifier, matching the estate lookup. |
| `Estate_Name` | Estate or grouping name, matching the estate lookup. |
| `Estate_RV` | Estate rateable value used for that year, where available. |
| `Block_ID` | Council service-charge block identifier, matching the block lookup. |
| `Block_Name` | Block/property-group name, matching the block lookup. |
| `Block_RV` | Block rateable value used for that year. |

Names are standardised using the lookups and may differ from historical source names.

`ENBR2` and `ENNL7` identify council-labelled non-estate groups. `EX01`, named `Street Property`, is an artificial grouping with estate RV `0`.

For records before 2022–23, the oldest known block and estate RVs are used as fallback values. These are not independently verified historical RVs.

### Block charge columns

These contain the whole-block cost of each service:

| Column |
|---|
| `Block_Boiler_Repairs_and_Maintenance` |
| `Block_Cleaning` |
| `Block_Communal_Electricity` |
| `Block_Communal_Electrical_Maintenance` |
| `Block_Communal_Ventilation_Maintenance` |
| `Block_Communal_Water_Quality` |
| `Block_Communal_Window_Cleaning` |
| `Block_Concierge` |
| `Block_CCTV` |
| `Block_Disinfestation` |
| `Block_Door_Entry_System` |
| `Block_Dry_Riser` |
| `Block_Lightning_Protection` |
| `Block_Lift_Services_and_Repairs` |
| `Block_Fire_Ventilation_Maintenance` |
| `Block_Repairs_and_Maintenance` |
| `Block_TV_Aerial` |
| `Block_Ext_Cleaning` |
| `Block_Ext_External_Tree_Maintenance` |
| `Block_Ext_Grounds_Maintenance` |
| `Block_Ext_Repairs_and_Maintenance` |

### Estate charge columns

These contain the whole-estate cost, repeated for every associated block:

| Column |
|---|
| `Estate_Cleaning` |
| `Estate_CCTV` |
| `Estate_Communal_Electricity` |
| `Estate_Grounds_Maintenance` |
| `Estate_Repairs_and_Maintenance` |
| `Estate_Tree_Maintenance` |

**Do not sum estate charges or estate RVs across block rows.** For estate-level analysis, select one record per estate and year, checking any source conflicts recorded in the audit.

## Calculation Methodology

For calculating service charges per flat, Lambeth uses the rateable value of a flat/property to work out what proportion of a charge should be paid.

These are calculated as:

`Block Service = Total_Block_Charge / Block_Rateable_Value * Property_Rateable Value`
`Estate Service = Total_Estate_Charge / Block_Rateable_Value * Property_Rateable Value`

## Additional Charges

Leaseholder service charge invoices also include additional items not included in these datasets.

| Charge | Note |
| Hot Water | Only included for properties with a communal boiler.  The existence of a communal boiler can be inferred by the existence of a `Block_Boiler_Repairs_and_Maintenance` charge. |
| Heating | Only included for properties with a communal boiler.  The existence of a communal boiler can be inferred by the existence of a `Block_Boiler_Repairs_and_Maintenance` charge. |
| Building Insurance | Lambeth calculates this based on the number of bedrooms in a property. |
| Management Charge | This is generally either 10% or 16.5% of the total bill but the percentage is dependent on the teams of each lease. |
| Ground Rent | Generally £10 per year |
