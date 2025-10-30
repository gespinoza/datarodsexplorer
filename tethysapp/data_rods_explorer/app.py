from tethys_apps.base import TethysAppBase
from tethys_sdk.app_settings import SpatialDatasetServiceSetting, CustomSetting, SecretCustomSetting


class DataRodsExplorer(TethysAppBase):
    """
    Tethys app class for Data Rods Explorer.
    """

    name = 'Data Rods Explorer'
    index = 'home'
    icon = 'data_rods_explorer/images/DataRodsExplorer_icon.png'
    package = 'data_rods_explorer'
    root_url = 'data-rods-explorer'
    color = '#5971A8'

    def spatial_dataset_service_settings(self):
        """
        Example spatial_dataset_service_settings method.
        """
        sds_settings = (
            SpatialDatasetServiceSetting(
                name='default',
                description='spatial dataset service for app to use',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )

        return sds_settings
    
    def custom_settings(self):
        custom_settings = (
            CustomSetting(
                name='earth_data_username',
                description='Earthdata Login Username',
                required=True,
            ),
            CustomSetting(
                name='earth_data_password',
                description='Earthdata Login Password',
                required=True,
            ),
        )

        return custom_settings