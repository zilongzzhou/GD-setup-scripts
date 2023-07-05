## Cohort Generation
- Run `python3 cohort-generator.py <cohort_size>`
- `cohort_size` = no of cohorts needed (must be a multiple of 20 for now as initial file contains 20 cohorts)
- new csv `cohorts_final.csv` will be generated

## Child Layer URL Generation
* Run `python3 scrypt.py <match_id> <bearer>` 
* `match_id` = match Id in CMS
* `bearer` = CMS auth token
* It will generate a csv `master.csv` with all `fhd` and `ssai` tagged master URLs
* Then it will create a csv 	`child_layers.csv` with all child urls from the above master URLs
* Then it will replicate the child URLs according to the distribution below
- The first 12 layers are replicated as follows
    | Layer | Count | Layer | Count |
    |--|--|--|--|
    | Hindi/Mobile/H265 | 3840 | English/Mobile/H265 | 960  |
    | Hindi/Mobile/H264 | 2320 | English/Mobile/H264 | 580 |
    | Hindi/TV/H265 | 640 | English/TV/H265 | 160 |
    | Hindi/TV/H264 | 240 | English/TV/H264 | 60 |
    | Hindi/1080/H265 | 80 | English/1080/H265 | 20 |
    | Hindi/1080/H264 | 80 | English/1080/H264 | 20 |

- From half (Hindi) of the remaining layers a value is picked 800 times (each time a random value) and from other half (English) a value is picked 200 times (each time a random value).
- Total 10000 layers are generated.

## Mock Server Child Layer URL Generation
* Run `python3 mock-server-gen.py`
* new `layers-mock.csv` will be generated
