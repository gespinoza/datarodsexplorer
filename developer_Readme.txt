This is the documentation intended for future developers of the data rod explorer app.

This was written by Hart Henrichsen, who converted the app from Tethys 2 to 3. I also converted the app from Python 2 to 3.

To keep the app updated the enddate_bounds.py needs to be run daily. This script update the spatial and temporal bounds of the datasets. This change is stored in the public/data/dates_and_spatial_range.txt. The links to update these bounds is stored in public/data/model_config.txt. If any of the links need updating including versions, this file needs to be updated.
If there is an issue with the endate_bounds.py connecting with a dataset, it will skip the dataset and it will be unavailable.

When opening up the app, the display button is deactivated. This was a quick fix to prevent any of the NLDAS datasets from being plotted, as those services are not available.

The cronjob to run enddate_bounds.py needs to be updated everytime the version of the app changes. This is due to how the Tethys warehouse stores apps. The current ~/../var/tethys/miniconda3/envs/tethys/bin/python command is: ~/../var/tethys/miniconda3/envs/tethys/lib/python3.7/site-packages/tethysapp_data_rods_explorer-0.0.2-py3.7.egg/tethysapp/data_rods_explorer/enddate_bounds.py. The path to python ensures that python 3 is being ran. The '0.0.2' is the version that is to be updated on a version change. Admin permissions are needed to access this python command.

