# Data Rods Explorer 1.0.0 
### Browsing NASA Data Services for Land Surface Model Maps and Time Series
**Last Updated**: November 19, 2016

The Data Rods Explorer (DRE) is a web client app that enables users to browse several NASA-hosted land surface model (LSM) outputs by LSM variable, space and time. The user can obtain a picture of the map at any valid date-time stamp; plot a time series of values available; compare two LSM variables over a mutually-available time period; and plot year-on-year changes in model outputs for a given LSM variable. Tabular and plot outputs can be downloaded, as well as graphic images of the plots. 

**NASA Land Surface Models supported**: NLDAS-Forcing, NLDAS-Noah, GLDAS-Noah, TRMM, LPRM AMSRE-D, LPRM AMSRE-A, GRACE  

**Keywords**: hydrology, hydrometeorology, atmospheric, time series, data rods, soil moisture, evapotranspiration, surface runoff, subsurface runoff, temperature, forcings, precipitation, 

**Points of Contact**:
All questions regarding this web app and documentation should be directed to the developers and project leads:

| Name  | Affiliation |
| --- | --- |
| Gonzalo Espinoza | UNESCO IHE |
| David Arctur | University of Texas at Austin |
| William Teng | ADNET, Project PI |


**Outline under construction**: *This document is an outline for the complete user guide. It is likely to be filled in with separate files for each main section. The intent is to turn this completed documentation into ReadTheDocs form. It should be maintained via github.*

## 1. Features & Tutorials

Intro text... 


### 1.1 Selecting and displaying gridded maps of model variables
### 1.2 Plotting time series of one variable
### 1.3 Comparing time series of two variables
### 1.4 Plotting year-on-year changes in a model variable
### 1.5 Using the Reset button

### 1.6 Using the map controls panel
**Layers: show/hide/transparency**

**Zoom to extent**

### 1.7 Downloading time series data and plot graphics
**Downloading Ascii tabular data with or without metadata**

**Downloading netCDF data**

**Using NASA plot service**

### 1.8 Notifications and error messages
**NASA data service URLs** 

**Error messages**


### 1.9 Testing the NASA data services 
**Quick vs Full vs WMS options**

### 1.10 Using NASA Giovanni 
### 1.11 NASA references for models and variables


## 2. Keeping Data Rods Explorer Up to Date
### 2.1 Using the NASA Data Rods Variables Info spreadsheet
### 2.2 Editing the model_config.txt file
### 2.3 Running the enddates_bounds.py script (cron job)


## 3. Developer's Corner: DRE App Process Flow
### 3.1 User navigates to the app's home page
### 3.2 User clicks on any of theTime Series plot options
### 3.3 User chooses a different model from the model dropdown
### 3.4 User chooses different variable/dates/time from a dropdown
### 3.5 User clicks on map
### 3.6 User clicks "Display Map" button
### 3.7 User clicks "Plot" button for Plot One Variable
### 3.8 User clicks "Plot" button for Compare Two Variables
### 3.9 User clicks "Plot" button for Year-on-Year Changes

## 4. Possible future enhancements

