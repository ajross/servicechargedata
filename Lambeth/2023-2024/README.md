# Data Source

The data was originally supplied in PDF format in response to a FOI request.
Unfortunately due to the lack of response to the FOI request made on [WhatDoTheyKnow.com](https://www.whatdotheyknow.com/request/actual_service_charge_costs_for_5) the issue was escalated to the ICO.  The data was eventually supplied via email.

The data was provided in 2 csv files as seen in the Original Data directory, although the following data issues were identified:
 - BD003808 still has Unknown estate code and name.
 - BD003806 still has Block RV = 1, which looks like another uncorrected placeholder.
 - EA019SV vs EA019 means 13 Caldwell Gardens blocks cannot join to their estate charges.
 - EA056SV vs EA056 means 5 Holland Town blocks cannot join.
 - 892 block rows in total reference estate codes absent from the estate file; most are non-estate groupings, but Lambeth needs to explain the intended relationship between the two datasets.
 - The estate file inconsistently includes two non-estate codes (ENBR2, ENNL7) but omits many other non-estate codes.
 - ENNL7 is named NL7 in the block file but NI7 in the estate file.
 - Four charge-bearing estates have no corresponding block/estate assignment in the block file.

Lambeth was alerted to these issues but did not respond and provided no further versions of the data.
As such, we must assume that Lambeth is happy that the data is suitable for use.

The data from the original files has been reformatted and joined.