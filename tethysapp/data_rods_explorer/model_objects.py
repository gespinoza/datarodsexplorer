WORKSPACE = 'data_rods_explorer'
GEOSERVER_URL = 'http://appsdev.hydroshare.org:8181/geoserver/wms'
### Uncomment the following line for local development
# GEOSERVER_URL =  'http://127.0.0.1:8181/geoserver/wms'
MODEL_OPTIONS = [('TESTING -- NLDAS-Noah (LSM)', 'nldas'),
				 ('GLDAS-Noah (LSM)', 'gldas'),
				 ('TRMM (retrieval)', 'trmm'),
				 ('GRACE soil moisture', 'grace')]

STARTDATE_OPTIONS = [('NLDAS-Noah (LSM)', '1/2/1979'),
				 ('GLDAS-Noah (LSM)', '3/1/2000'),
				 ('TRMM (retrieval)', '12/31/1997'),
				 ('GRACE soil moisture', '1/6/2003')]
				 
ENDDATE_OPTIONS = [('NLDAS-Noah (LSM)', '4/7/2016'),
				 ('GLDAS-Noah (LSM)', '3/31/2016'),
				 ('TRMM (retrieval)', '1/31/2016'),
				 ('GRACE soil moisture', '5/3/2015')]

DATARODS_TSB = {}
DATARODS_TSB.update({'nldas': {'noah': ('http://hydro1.sci.gsfc.nasa.gov/daac-bin/access/timeseries.cgi?'
							   			'variable=NLDAS:NLDAS_NOAH0125_H.002:{0}&'  # SSRUNsfc
							            'type=asc2&location=GEOM:POINT({1})&'
							            'startDate={2}&endDate={3}'),
							   'forcing': ('http://hydro1.sci.gsfc.nasa.gov/daac-bin/access/timeseries.cgi?'
							   			   'variable=NLDAS:NLDAS_FORA0125_H.002:{0}&'  # SSRUNsfc
							               'type=asc2&location=GEOM:POINT({1})&'
							               'startDate={2}&endDate={3}')
							  }})
DATARODS_TSB.update({'gldas': ('http://hydro1.sci.gsfc.nasa.gov/daac-bin/access/timeseries.cgi?'
							   'variable=GLDAS:GLDAS_NOAH025_3H.001:{0}&'  # precip
							   'type=asc2&location=GEOM:POINT({1})&'
							   'startDate={2}&endDate={3}')
					})
DATARODS_TSB.update({'trmm': ('http://hydro1.sci.gsfc.nasa.gov/daac-bin/access/timeseries.cgi?'
							  'variable=TRMM:TRMM_3B42.007:{0}itation&'
							  'type=asc2&location=GEOM:POINT({1})&'
							  'startDate={2}&endDate={3}')
					})
DATARODS_TSB.update({'grace': ('http://hydro1.sci.gsfc.nasa.gov/daac-bin/access/timeseries.cgi?'
							   'variable=GRACE:GRACEDADM_CLSM025NA_7D.1:{0}_inst&'
							   'type=asc2&location=GEOM:POINT({1})&'
							   'startDate={2}&endDate={3}')
					})

DATARODS_PNG = ('http://giovanni.gsfc.nasa.gov/giovanni/daac-bin/wms_ag4?VERSION=1.1.1'
				'&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=512&HEIGHT=256'
				'&LAYERS=Time-Averaged.{5}'  # NLDAS_NOAH0125_M_002_soilm0_100cm
				'&STYLES=default&TRANSPARENT=TRUE&FORMAT=image/tiff'
				'&time={4}'  # 2008-01-01T00:00:00Z/2008-01-01T00:00:00Z
				'&bbox={0},{1},{2},{3}')  # -119,30,-107,36

WMS_VARS = {"nldas": {}, "gldas": {}, "trmm": {}, "grace": {}}
WMS_VARS['nldas'].update({"APCPsfc": ["NLDAS_FORA0125_H_002_apcpsfc", "Precipitation hourly total", "kg/m^2"],
						  "DLWRFsfc": ["NLDAS_FORA0125_H_002_dlwrfsfc", "Surface DW longwave radiation flux", "W/m^2"],
						  "DSWRFsfc": ["NLDAS_FORA0125_H_002_dswrfsfc", "Surface DW shortwave radiation flux", "W/m^2"],
						  "PEVAPsfc": ["NLDAS_FORA0125_H_002_pevapsfc", "Potential evaporation", "kg/m^2"],
						  "SPFH2m": ["NLDAS_FORA0125_H_002_spfh2m", "2-m above ground specific humidity", "kg/kg"],
						  "TMP2m": ["NLDAS_FORA0125_H_002_tmp2m", "2-m above ground temperature", "K"],
						  "UGRD10m": ["NLDAS_FORA0125_H_002_ugrd10m", "10-m above ground zonal wind", "m/s"],
						  "VGRD10m": ["NLDAS_FORA0125_H_002_vgrd10m", "10-m above ground meridional wind", "m/s"],
						  "EVPsfc": ["NLDAS_NOAH0125_H_002_evpsfc", "Total evapotranspiration", "kg/m^2"],
						  "GFLUXsfc": ["NLDAS_NOAH0125_H_002_gfluxsfc", "Ground heat flux", "w/m^2"],
						  "LHTFLsfc": ["NLDAS_NOAH0125_H_002_lhtflsfc", "Latent heat flux", "w/m^2"],
						  "SHTFLsfc": ["NLDAS_NOAH0125_H_002_shtflsfc", "Sensible heat flux", "(w/m^2)"],
						  "SSRUNsfc": ["NLDAS_NOAH0125_H_002_ssrunsfc", "Surface runoff (non-infiltrating)", "kg/m^2"],
						  "BGRIUNdfc": ["NLDAS_NOAH0125_H_002_bgriundfc", "Subsurface runoff (baseflow)", "kg/m^2"],
						  "SOILM0-10cm": ["NLDAS_NOAH0125_H_002_soilm0_10cm", "0-10 cm soil moisture content", "kg/m^2"],
						  "SOILM0-100cm": ["NLDAS_NOAH0125_H_002_soilm0_100cm", "0-100 cm soil moisture content", "kg/m^2"],
						  "SOILM0-200cm": ["NLDAS_NOAH0125_H_002_soilm0_200cm", "0-200 cm soil moisture content", "kg/m^2"],
						  "SOILM10-40cm": ["NLDAS_NOAH0125_H_002_soilm10_40cm", "0-40 cm soil moisture content", "kg/m^2"],
						  "SOILM40-100cm": ["NLDAS_NOAH0125_H_002_soilm40_100cm", "40-100 cm soil moisture content", "kg/m^2"],
						  "SOILM100-200cm": ["NLDAS_NOAH0125_H_002_soilm100_200cm", "100-200 cm soil moisture content", "kg/m^2"],
						  "TSOIL0-10cm": ["NLDAS_NOAH0125_H_002_tsoil0_10cm", "0-10 cm soil temperature", "K"]
						})
WMS_VARS['gldas'].update({"Evap": ["", "Total Evapotranspiration", "kg/m^2/s"],
						  "precip": ["", "Precipitation rate", "kg/m^2/hr"],
						  "Rainf": ["", "Rain rate", "kg/m^2/s"],
						  "Snowf": ["", "Snow rate", "kg/m^2/s"],
						  "Qs": ["", "Surface Runoff", "kg/m^2/s"],
						  "Qsb": ["", "Subsurface Runoff", "kg/m^2/s"],
						  "SOILM0-100cm": ["", "0-100 cm top 1 meter soil moisture content", "kg/m^2"],
						  "SOILM0-10cm": ["", "0-10 cm layer 1 soil moisture content", "kg/m^2"],
						  "SOILM10-40cm": ["", "10-40 cm layer 2 soil moisture content", "kg/m^2"],
						  "SOILM40-100cm": ["", "40-100 cm layer 3 soil moisture content", "kg/m^2"],
						  "Tair": ["", "Near surface air temperature", "K"],
						  "TSOIL0-10cm": ["", "Average layer 1 soil temperature", "K"],
						  "Wind": ["", "Near surface wind magnitude", "m/s"]
						})
WMS_VARS['trmm'].update({"precip": ["TRMM_3B42_daily_precipitation_V7", "Precipitation", "mm/hr"]
					    })
WMS_VARS['grace'].update({"sfsm": ["GRACEDADM_CLSM025NA_7D_1_0_sfsm_inst", "Surface Soil Moisture", "percentile"],
						  "rtzsm": ["GRACEDADM_CLSM025NA_7D_1_0_rtzsm_inst", "Root Zone Soil Moisture", "percentile"],
						  "gws": ["GRACEDADM_CLSM025NA_7D_1_0_gws_inst", "Ground Water", "percentile"]
						})
