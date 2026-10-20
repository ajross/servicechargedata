# Council Service Charge Data

Service-charge data for council-owned residential blocks and estates in London. The repository brings together council data supplied through Freedom of Information requests and resident-supplied records, with annual CSV files and lookup tables for exploring the charges.

The files describe costs for blocks, estates and other charging groups. They are not individual leaseholders' bills, and coverage varies by borough and year.

This repository has been created to bring together available service charge data from across London in order to help leaseholders understand their charges, analyse the data to ensure they are being charged correctly, and to compare charges across boroughs.

For each borough/year I have attempted to restructure the data into a more consistent format, however since each borough uses a slightly different calculation methology and the data is not always complete, this is not a simple task.  As more data is acquired, I will endeavour to update the datasets, add missing IDs, and improve data quality.

## Available data

| Borough | Years with annual CSV data | Coverage |
|---|---|---|
| [Lambeth](Lambeth/README.md) | 2015–2016 to 2024–2025 | Limited historical records through 2021–2022; much broader coverage from 2022–2023. Includes block and estate charges and rateable values. |
| [Lewisham](Lewisham/README.md) | 2022–2023 | Service costs and property counts for charging groups, including groups that overlap or cover an entire estate. |
| [Southwark](Southwark/README.md) | 2022–2023 | Block and estate charges, with bedroom-based weightings. |
| [Tower Hamlets](Tower%20Hamlets/README.md) | 2022–2023 and 2023–2024 | Block and mapsite charges, gross rateable values and other apportionment information where supplied. Mapsites are communal charging areas used for estate services. |
| [Wandsworth](Wandsworth/README.md) | 2023–2024 | Block and estate charges, with property counts where supplied. |

Some directories are reserved for future years and do not yet contain annual data. Borough and year READMEs describe the available sources and limitations.

## Directory structure

```text
Borough/
├── README.md
├── Lookups/
│   ├── README.md
│   ├── blocks.csv
│   └── estates.csv
└── YYYY-YYYY/
    ├── README.md
    ├── YYYY-YYYY.csv
    └── Original Data/
```

- **Borough README:** file definitions, source links and charging methodology.
- **Lookups:** block and estate names, identifiers and relationships. Some boroughs have additional lookup tables.
- **Annual CSV:** charges and year-specific apportionment information, suitable for opening in Excel or importing into analysis tools.
- **Year README:** source details and limitations specific to that year's data.
- **Original Data:** council-supplied files, where retained, in their original format.

Tower Hamlets also has a `mapsites.csv` in each year directory containing the complete supplied mapsite-level data.

## Using the data

Annual files identify the service-charge period, estate and block or charging group, followed by service costs and any available rateable values, property counts or weightings. Charge columns contain numeric GBP amounts without currency symbols or thousands separators. Negative amounts are retained.

The column sets and calculation rules differ between boroughs. A block can represent an address range or service-specific group rather than a single building. Identifiers may be council-issued or synthetic; the borough documentation explains their meaning and the keys needed to join records.

Where estate or mapsite costs repeat across block rows, count each estate or mapsite only once when calculating totals. Lewisham's overlapping charging groups also require care when selecting the services applicable to a property.

**Zero does not always mean a confirmed zero cost.** It can represent an unavailable or unreported value. An absent block is not a zero-charge record. Consult the relevant README and original files before drawing conclusions about missing services or changes between years.

Calculating an individual property's share may require information from its lease or bill, such as its rateable value, bedroom count or apportionment percentages. The datasets do not necessarily include every invoice item or all inputs needed to reproduce a bill. Cross-borough comparisons should account for differences in service definitions, coverage and charging methods.
