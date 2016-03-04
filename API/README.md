# API
Core api functions.

## Files
- closestbus.py
  - Script for getting the closest bus to a given stop.
- histdata.py
  - Manage accessing the log files and formats of these files when referencing
    historical data. This will be subbed out for an actual database eventually
    and is not meant to be permenant. This will be here only for the duration of
    testing and development.


## File Hierarchy
/path/to/working_dir/
- buses/
  - route_number/
    - yyyymmdd_hhmmss.json
- stops/
  - route_number/
    - yyyymmdd_hhmmss.json
- vector_plots/
  - route_number/
    - direction.json

