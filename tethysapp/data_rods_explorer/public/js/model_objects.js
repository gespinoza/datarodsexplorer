var MODEL_FENCES = {};
var MODEL1_LAYER = null;
var MODEL2_LAYER = null;
var VAR_DICT = {};
VAR_DICT["nldas"] = [{
    "text": "Precipitation hourly total (kg/m^2)",
    "value": "APCPsfc",
    "layerName": "PrecipHrlyTotal"
}, {
    "text": "Surface DW longwave radiation flux (W/m^2)",
    "value": "DLWRFsfc",
    "layerName": "SurfDwLongWaveRadFlux"
}, {
    "text": "Surface DW shortwave radiation flux (W/m^2)",
    "value": "DSWRFsfc",
    "layerName": "SurfDwShrtWaveRadFlux"
},
    //{"text": "Potential evaporation (kg/m^2)",
    //"value": "PEVAPsfc"},
    {
        "text": "2-m above ground specific humidity (kg/kg)",
        "value": "SPFH2m",
        "layerName": "2mAbvGrndSpecifHumid"
    }, {
        "text": "2-m above ground temperature (K)",
        "value": "TMP2m",
        "layerName": "2mAbvGrndTemp"
    },
    //{"text": "10-m above ground zonal wind (m/s)",
    //"value": "UGRD10m"},
    //{"text": "10-m above ground meridional wind (m/s)",
    //"value": "VGRD10m"},
    {
        "text": "Total evapotranspiration (kg/m^2)",
        "value": "EVPsfc",
        "layerName": "TotEvapotrans"
    }, {
        "text": "Ground heat flux (w/m^2)",
        "value": "GFLUXsfc",
        "layerName": "GrndHeatFlux"
    }, {
        "text": "Latent heat flux (w/m^2)",
        "value": "LHTFLsfc",
        "layerName": "LatentHeatFlux"
    }, {
        "text": "Sensible heat flux (w/m^2)",
        "value": "SHTFLsfc",
        "layerName": "SensHeatFlux"
    }, {
        "text": "Surface runoff (non-infiltrating) (kg/m^2)",
        "value": "SSRUNsfc",
        "layerName": "SurfRunoff(NonInfilt)"
    },
    //{"text": "Subsurface runoff (baseflow) (kg/m^2)",
    //"value": "BGRIUNdfc"},
    {
        "text": "0-10 cm soil moisture content (kg/m^2)",
        "value": "SOILM0-10cm",
        "layerName": "0-10cmSoilMoistCont"
    }, {
        "text": "0-100 cm soil moisture content (kg/m^2)",
        "value": "SOILM0-100cm",
        "layerName": "0-100cmSoilMoistCont"
    }, {
        "text": "0-200 cm soil moisture content (kg/m^2)",
        "value": "SOILM0-200cm",
        "layerName": "0-200cmSoilMoistCont"
    }, {
        "text": "10-40 cm soil moisture content (kg/m^2)",
        "value": "SOILM10-40cm",
        "layerName": "10-40cmSoilMoistCont"
    }, {
        "text": "40-100 cm soil moisture content (kg/m^2)",
        "value": "SOILM40-100cm",
        "layerName": "40-100cmSoilMoistCont"
    }, {
        "text": "100-200 cm soil moisture content (kg/m^2)",
        "value": "SOILM100-200cm",
        "layerName": "100-200cmSoilMoistCont"
    }, {
        "text": "0-10 cm soil temperature (K)",
        "value": "TSOIL0-10cm",
        "layerName": "0-10cmSoilTemp"
    }
];
VAR_DICT["gldas"] = [
    {
        "text": "Total Evapotranspiration (kg/m^2/s)",
        "value": "Evap",
        "layerName": "TotalEvapotrans"
    },
    {
        "text": "Precipitation rate (kg/m^2/hr)",
        "value": "precip",
        "layerName": "PrecipRate"
    },
    {
        "text": "Rain rate (kg/m^2/s)",
        "value": "Rainf",
        "layerName": "RainRate"
    },
    {
        "text": "Snow rate (kg/m^2/s)",
        "value": "Snowf",
        "layerName": "SnowRate"
    },
    {
        "text": "Surface Runoff (kg/m^2/s)",
        "value": "Qs",
        "layerName": "SurfRunoff"
    },
    {
        "text": "Subsurface Runoff (kg/m^2/s)",
        "value": "Qsb",
        "layerName": "SubsurfRunoff"
    },
    {
        "text": "0-100 cm top 1 meter soil moisture content (kg/m^2)",
        "value": "SOILM0-100cm",
        "layerName": "0-100cmTop1MetSoilMoistCont"
    },
    {
        "text": "0-10 cm layer 1 soil moisture content (kg/m^2)",
        "value": "SOILM0-10cm",
        "layerName": "0-10cmLay1SoilMoistCont"
    },
    {
        "text": "10-40 cm layer 2 soil moisture content (kg/m^2)",
        "value": "SOILM10-40cm",
        "layerName": "10-40cmLay2SoilMoistCont"
    },
    {
        "text": "40-100 cm layer 3 soil moisture content (kg/m^2)",
        "value": "SOILM40-100cm",
        "layerName": "40-100cmLay3SoilMoistCont"
    },
    {
        "text": "Near surface air temperature (K)",
        "value": "Tair",
        "layerName": "NearSurfAirTemp"
    },
    {
        "text": "Average layer 1 soil temperature (K)",
        "value": "TSOIL0-10cm",
        "layerName": "AvgLay1SoilTemp"
    },
    {
        "text": "Near surface wind magnitude (m/s)",
        "value": "Wind",
        "layerName": "NearSurfWindMag"
    }
];
VAR_DICT["gldas2"] = [
    {
        "text": "10-40 cm layer 2 soil moisture content (kg/m^2)",
        "value": "SOILM10_40cm",
        "layerName": "10-40cmLay2SoilMoistCont"
    },
    {
        "text": "40-100 cm layer 3 soil moisture content (kg/m^2)",
        "value": "SOILM40_100cm",
        "layerName": "40-100cmLay3SoilMoistCont"
    },
    {
        "text": "100-200 cm layer 4 soil moisture content (kg/m^2)",
        "value": "SOILM100_200cm",
        "layerName": "100-200cmLay4SoilMoistCont"
    }

];
VAR_DICT["trmm"] = [
    {
        "text": "Precipitation (mm/hr)",
        "value": "precip",
        "layerName": "Precipitation"
    }
];

VAR_DICT["grace"] = [
    {
        "text": "Surface Soil Moisture Percentile",
        "value": "sfsm",
        "layerName": "SurfSoilMoistPercent"
    },
    {
        "text": "Root Zone Soil Moisture Percentile",
        "value": "rtzsm",
        "layerName": "RootZoneSoilMoistPercent"
    },
    {
        "text": "Ground Water Percentile",
        "value": "gws",
        "layerName": "GrndWatPercent"
    }
];
