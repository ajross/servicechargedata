# Data Source

The actual 2022–2023 charges were supplied in separate block and estate CSV files in response to a [Freedom of Information request](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_2). The block-to-estate list was supplied through a [separate request](https://www.whatdotheyknow.com/request/block_and_estate_key). Original files are in `Original Data`.

The annual file contains **2,800 blocks**, bedroom weightings and 15 charge columns. Its block and estate IDs are synthetic IDs created to link the records in this CSV; they were not supplied by Southwark Council. Estate amounts repeat for associated blocks. File definitions and calculation guidance are in the [borough README](../README.md).

Some source grand totals differ from the sums of their individual rows, including ground rent and the estate charge categories. The five negative block-lighting amounts are credits.
