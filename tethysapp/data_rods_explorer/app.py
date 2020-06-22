from tethys_apps.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import SpatialDatasetServiceSetting


class DataRodsExplorer(TethysAppBase):
    """
    Tethys app class for Data Rods Explorer.
    """

    name = 'Data Rods Explorer'
    index = 'data_rods_explorer:home'
    icon = 'data_rods_explorer/images/DataRodsExplorer_icon.png'
    package = 'data_rods_explorer'
    root_url = 'data-rods-explorer'
    color = '#5971A8'

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='data-rods-explorer',
                           controller='data_rods_explorer.controllers.home'),
                    UrlMap(name='plot',
                           url='data-rods-explorer/plot',
                           controller='data_rods_explorer.controllers.plot'),
                    UrlMap(name='plot2',
                           url='data-rods-explorer/plot2',
                           controller='data_rods_explorer.controllers.plot2'),
                    UrlMap(name='years',
                           url='data-rods-explorer/years',
                           controller='data_rods_explorer.controllers.years'),
                    UrlMap(name='map',
                           url='data-rods-explorer/request-map-layer',
                           controller='data_rods_explorer.controllers.request_map_layer'),
                    UrlMap(name='run_tests',
                           url='data-rods-explorer/run-tests',
                           controller='data_rods_explorer.tests.unit_tests.test_nasa_endpoints'),
                    #UrlMap(name='ajax_upload_to_hs',
                    #       url='data-rods-explorer/upload-to-hs',
                    #       controller='data_rods_explorer.controllers.upload_to_hs'),
                    )

        return url_maps

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
