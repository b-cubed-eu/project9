1. # to check query from the sample json file (created for the AD4GD project purposes), type in command line:
curl --include --header "Content-Type: application/json" --data @query_datacube.json https://api.gbif.org/v1/occurrence/download/request/validate

2. # to replace username and password
curl --include --user username:password --header "Content-Type: application/json" --data @query_datacube.json https://api.gbif.org/v1/occurrence/download/request

# returns download code on the last line

3. # to paste download code into curl request
curl -Ss https://api.gbif.org/v1/occurrence/download/{download-code}
# for example:
curl -Ss https://api.gbif.org/v1/occurrence/download/0019637-240626123714530

4. # run 2_gridding.py and analyse output in band 2 in the /output directory. Reprojected occurrence data are recorded into the same grid as band 1.
