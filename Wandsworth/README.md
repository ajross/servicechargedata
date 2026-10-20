# Wandsworth Data

Actual service-charge costs for 2023–2024, supplied by Wandsworth Council. The annual file contains block and estate costs, together with property counts where supplied. It does not contain individual leaseholders' bills, rateable values or apportionment percentages.

## Sources

- [2023–2024 FOI request and source CSV files](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_6).
- [Council service-charge guidance](https://www.wandsworth.gov.uk/housing/council-tenants-and-leaseholders/council-leaseholders/service-charges-for-council-leaseholders/).
- [Your service charges explained](https://www.wandsworth.gov.uk/media/t02orttd/your_service_charges_explained.pdf). The available guide is the 2026 edition; its tariffs should not be applied retrospectively to this dataset.
- [Additional apportionment explanation](Notes/README.md).

Original CSVs are retained in the year's `Original Data` directory.

## Annual service-charge files

Files are stored as `Wandsworth/YYYY-YYYY/YYYY-YYYY.csv`.

Each row represents one block or address group for a service-charge year. The 2023–2024 file contains **1,954 rows and 23 columns**: ten identification/count fields and thirteen charge fields. Address groups on the same street can have different charges.

Charges are numeric GBP amounts, with two decimal places and no currency symbols or thousands separators. Negative amounts are credits. All fields are populated. A zero can mean either a supplied zero or an unavailable value; see the year README for coverage limitations.

### Identification and property counts

| Column | Description |
|---|---|
| `Year_Start` | Starting year of the service-charge period. |
| `Year_End` | Ending year of the service-charge period. |
| `Estate_ID` | Synthetic estate/group ID, matching the estate lookup. |
| `Estate_Name` | Estate or council property-group name. |
| `Estate_Flat_Count` | Supplied estate total of flats and maisonettes. Houses and bungalows are excluded. |
| `Estate_House_Count` | Supplied estate house count. |
| `Block_ID` | Synthetic block/address-group ID, matching the block lookup. |
| `Block_Name` | Supplied block/street name followed by its address range, where available. |
| `Block_Property_Count` | Supplied number of properties in that block/address group. |
| `Block_Property_Type` | `Flats` or `Houses`, corresponding to the source's `Y`/`H` flags; `Unknown` where no flag was supplied. |

The IDs were created to produce and link these files; they are **not council-issued IDs**. Some estate names describe acquisitions or infill groups rather than a physical estate. Property counts do not always reconcile between the block and estate files, and zero counts cannot be used as calculation denominators.

### Block charge columns

These contain the total cost for the block/address group.

| Column | Service |
|---|---|
| `Block_Grounds_Maintenance` | Gardening. |
| `Block_Tree_Maintenance` | Trees. |
| `Block_Communal_Electricity` | Block electricity. |
| `Block_Lift_Electricity` | Lift electricity. |
| `Block_Repairs_and_Maintenance` | Block repairs. |
| `Block_Lift_Repairs` | Lift repairs. |
| `Block_Cleaning` | Cleaning. |
| `Block_Paladins` | Paladin communal refuse bins. |

### Estate charge columns

These contain the whole-estate cost, repeated on every associated block row.

| Column | Service |
|---|---|
| `Estate_Grounds_Maintenance` | Garden maintenance. |
| `Estate_Tree_Maintenance` | Trees. |
| `Estate_Communal_Electricity` | Estate electricity. |
| `Estate_Repairs_and_Maintenance` | Estate repairs. |
| `Estate_Cleaning` | Cleaning. |

**Select one record per estate and year before summing estate charges or counts.**

## Calculation Methodology

Use the flat-to-block and flat-to-estate percentages shown on the lease or service-charge bill:

```text
Flat block service charge = Block service cost × Flat block percentage / 100
Flat estate service charge = Estate service cost × Flat estate percentage / 100
```

The block percentage is the property's gross rateable value divided by the total gross rateable value of its block, multiplied by 100. These rateable values are not supplied in this dataset.

The additional explanation describes the estate percentage as the block percentage multiplied by the block's share of the estate's flats and maisonettes:

```text
Flat estate percentage = Flat block percentage × Block flat count / Estate flat count
```

Houses and bungalows are excluded from this estate denominator. `Block_Property_Count` provides the block flat count only for a group identified as `Flats`. Use the lease/bill percentage where counts are unavailable, inconsistent or the property falls outside that description. Do not assume that every flat on an estate pays an equal share.

## Additional Charges

The supplied files do not provide separate amounts for emergency response, buildings insurance, contribution fund payments or management fees. A resident's bill may therefore include additional items. The council guide explains these charges and the applicable lease terms. Minor works commissioning fees may already be included in repair costs; they should not be added twice.
