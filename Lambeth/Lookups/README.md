# Block and Estate Lookups

These files contain the estate and block IDs and names and the relation between blocks and estates.
The data has been compiled from the data sourced via FOI requests for each year as well as other lists of ID and names that could be found.

Across the data that Lambeth has provided, the estate/block name field is often inconsistent (capitalisation, abbreviations, etc).
The `estates.csv` file contains an extra row `EX01,Street Property` which has been matched to all entries in `blocks.csv` where Lambeth had not provided an estate code.
This has been done in order to ensure that the data files for each year could be fully populated.
