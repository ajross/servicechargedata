# Block and Estate Lookups

These files contain the block and estate names, their synthetic IDs, and the estate associated with each block. The names cover estates, street-property groupings and address ranges from the supplied data. Some lookup entries have no corresponding annual charge row.

| File | Columns | Records |
|---|---|---:|
| `blocks.csv` | `Block_ID,Block_Name,Estate_ID` | 2,861 |
| `estates.csv` | `Estate_ID,Estate_Name` | 405 |

Block IDs begin `SB`; estate IDs begin `SE`. These synthetic IDs were created to identify blocks and estates and link them in the annual CSV. They were not supplied by Southwark Council and are not council invoice codes. Bedroom weightings are held in the annual files because they may change by year.

`SE000000,Unassigned estate` contains five blocks whose estate is not established. These blocks are absent from the annual charge file:

- Banyard Road 22A-22B(C)
- Brunel Road 20
- Colworth Street 8A-8B(C)
- Kelmore Grove 19A-19B(C)
- SYLVAN GROVE 24 (1-28(C))

The [council's block and estate list](https://www.whatdotheyknow.com/request/block_and_estate_key) is available as `Templer attachment.xlsx` in the 2022–2023 `Original Data` directory. It contains names and leasehold-property counts, not council ID codes or total-property counts for apportionment.
