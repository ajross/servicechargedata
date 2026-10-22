# Southwark Data

The Southwark files contain actual service charges for 2022–2023, block and estate bedroom weightings, and lookups linking blocks to estates.

## Sources

- [2022–2023 service-charge data](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_2), supplied as CSVs on 6 June 2024.
- [Block and estate lookup](https://www.whatdotheyknow.com/request/block_and_estate_key), supplied on 8 July 2024, reference **27546542**.
- [Services and charges](https://www.southwark.gov.uk/housing/homeowners/your-service-charges/annual-service-charge/services-we-provide).
- [How charges are apportioned](https://www.southwark.gov.uk/housing/homeowners/your-service-charges/annual-service-charge/about-paying-your-annual-service/how).

Original files are available in each year's `Original Data` directory.

## Annual service-charge files

Files are stored as `Southwark/YYYY-YYYY/YYYY-YYYY.csv`.

Each row represents one block for one service-charge year. The 2022–2023 file contains **2,800 rows and 23 columns**: eight identification/weighting fields and 15 charge fields.

Charges are in GBP, with two decimal places and no currency symbols or thousands separators. Negative amounts represent credits. Zero means no charge is recorded in the supplied data; it can also indicate that no estate charge record is available. A block absent from a file should not be interpreted as having zero charges.

### Identification and bedroom weightings

| Column | Description |
|---|---|
| `Year_Start` | Four-digit starting year of the service-charge period. |
| `Year_End` | Four-digit ending year of the service-charge period. |
| `Estate_ID` | Synthetic estate/group ID created for the annual CSV, matching the estate lookup. |
| `Estate_Name` | Estate or non-estate grouping name. |
| `Estate_Bed_Weighting` | Total estate bedroom-weighting units; 0 means unavailable. |
| `Block_ID` | Synthetic block ID created for the annual CSV, matching the block lookup. |
| `Block_Name` | Block or address-range name. |
| `Block_Bed_Weighting` | Total block bedroom-weighting units. |

These are bedroom-based units, not rateable values. The estate and block IDs are synthetic IDs created to link the records in the annual CSV. They were not supplied by Southwark Council and are not council invoice codes. The [lookups](Lookups/README.md) contain 2,861 blocks and 405 estate/group records.

The annual file includes blocks whose names match the council’s block-to-estate list after ignoring case, spacing and punctuation. The lookups also contain entries absent from the annual file. A zero estate weighting means a weighted estate-share calculation is unavailable.

### Block charge columns

These contain the amounts listed against each block:

| Column |
|---|
| `Block_Administration_Charge` |
| `Block_TV_Aerial` |
| `Block_Repairs_and_Maintenance` |
| `Block_Lighting` |
| `Block_Security_Services` |
| `Block_Lift` |
| `Block_Heating_and_Hot_Water` |
| `Block_Ground_Rent` |
| `Block_Building_Insurance` |
| `Block_Door_Entry` |
| `Block_Care_and_Upkeep` |

### Estate charge columns

These contain the amounts listed against the estate, repeated for each associated block:

| Column |
|---|
| `Estate_Care_and_Upkeep` |
| `Estate_Grounds_Maintenance` |
| `Estate_Lighting` |
| `Estate_Repairs_and_Maintenance` |

**Do not sum repeated estate charges or estate weightings across block rows.** For estate-level comparisons, use one record per estate and year.

## Calculation Methodology

Southwark's property-size weighting is **four units plus the number of bedrooms**. A one-bedroom flat has five units; a three-bedroom flat has seven.

For services apportioned by bedroom weighting:

```text
Property units = 4 + Bedrooms
Block share = Block charge / Block_Bed_Weighting × Property units
Estate share = Estate charge / Estate_Bed_Weighting × Property units
```

Use only services applicable to the property. A weighting of 0 means the required denominator is unavailable. Heating, insurance, ground rent and administration have their own charging rules; the bedroom-weighting formula should not automatically be applied to every column.

## Additional Charges

The annual file already includes the following amounts against each block:

| Charge | Basis |
|---|---|
| Administration | Council guidance describes a 10% fee; TMO arrangements can differ. |
| Building insurance | Depends on the insured property and policy, including bedroom count. |
| Ground rent | Set by the lease. |
| Heating and hot water | Depends on the heat network and the property's heating provision. |

These amounts should not be added again as separate estimated charges. The files do not provide all property-specific inputs needed to reproduce an individual invoice.
