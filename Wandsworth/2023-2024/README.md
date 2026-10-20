# Data Source

Actual costs for 2023–2024, supplied by Wandsworth Council on 3 April 2025 in response to a [Freedom of Information request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_6). The original estate and block CSVs are in `Original Data`.

`2023-2024.csv` contains 1,954 block/address groups. Block costs appear once per group; estate costs and counts repeat across its associated groups. The [borough README](../README.md) describes the columns and calculation methodology, and the [lookups](../Lookups/README.md) provide the synthetic IDs and names.

Estate costs are supplied for 154 estates. A further 20 estate/property groups, covering 632 rows, have no matching estate-cost record: their estate costs and counts are shown as `0`, meaning unavailable rather than confirmed zero. Groups labelled as acquisitions or infills are included.

Three block property counts are absent and two are supplied as zero; all five appear as `0`. Two property types are `Unknown`. Counts do not always reconcile between the estate and block sources, so use the property's lease/bill percentages for apportionment where necessary.

Nine address ranges appear as date-like labels in the source, such as `Jan-22` and `01-Oct`; these labels remain in the block names. One block has no supplied address range. The negative block electricity amount of £1,691 for Cornford Grove, 46–60 even, on Ryde Vale is retained as a credit.
