
Current goal:

Get record parts and merge them into a single large record.

1. Each r.json() is stored as a list of dictionaries in python. We can use
this formatting to our advantage by using list.extend(nextlist) to aggregate
the complete dataset in one json file locally.
2. The function currently written handles individual requests.  Another wrapping
functionality needs to exist which reviews the current entry, extends the aggregate
list, logs failures for retry, records any metadata available, and detects the end 
of the list document successfully (in our case, detecting the end is easy because
the wrapping list returns empty as the default sfgov socrata behavior (this is true
at least for our test dataset).
