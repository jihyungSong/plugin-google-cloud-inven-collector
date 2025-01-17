import os

from spaceone.inventory.libs.common_parser import get_data_from_yaml
from spaceone.inventory.libs.schema.cloud_service_type import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import EnumDyField, TextDyField, SizeField, SearchField, \
    DateTimeDyField
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_region_conf = os.path.join(current_dir, 'widget/count_by_region.yml')
count_by_project_conf = os.path.join(current_dir, 'widget/count_by_project.yml')

cst_insight = CloudServiceTypeResource()
cst_insight.name = 'Insight'
cst_insight.provider = 'google_cloud'
cst_insight.group = 'Recommender'
cst_insight.service_code = 'Recommender'
cst_insight.labels = ['Analytics']
cst_insight.is_primary = False
cst_insight.is_major = False
cst_insight.tags = {
    'spaceone:icon': f'{ASSET_URL}/user_preferences.svg',
}

cst_insight._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('description', 'data.description'),
        EnumDyField.data_source('State', 'data.state_info.state', default_state={
            'safe': ['ACTIVE'],
            'disable': ['ACCEPTED'],
            'alert': ['STATE_UNSPECIFIED', 'DISMISSED'],
        }),
        EnumDyField.data_source('Severity', 'data.severity', default_badge={
            'red.500': ['CRITICAL', 'HIGH', 'SEVERITY_UNSPECIFIED'], 'gray.500': ['MEDIUM', 'LOW']
        }),
        EnumDyField.data_source('Category', 'data.category', default_badge={
            'indigo.500': ['COST'],
            'peacock.500': ['SUSTAINABILITY'],
            'violet.500': ['RELIABILITY'],
            'blue.500': ['PERFORMANCE'],
            'green.500': ['MANAGEABILITY'],
            'yellow.500': ['SECURITY'],
            'coral.500': ['CATEGORY_UNSPECIFIED']
        }),
        TextDyField.data_source('Insight type name', 'data.display.insight_type_display', default_outline_badge=[
            'Cloud Asset insights', 'Dataflow insights', 'Error Reporting notification insights',
            'Firewall insights', 'GKE diagnosis insights', 'IAM policy insights',
            'IAM service account insights science', 'Idle Compute Engine resources insights',
            'Lateral movement insights', 'Managed instance group insights', 'Unattended project insights',
            'VM instance insights'
        ]),
        TextDyField.data_source('Insight type', 'data.display.insight_type'),
        DateTimeDyField.data_source('Last refresh time', 'data.last_refresh_time'),
    ],
    search=[
        SearchField.set(name='Status', key='data.state_info.state'),
        SearchField.set(name='Severity', key='data.severity'),
        SearchField.set(name='Category', key='data.category'),
        SearchField.set(name='Insight type name', key='data.display.insight_type_display'),
        SearchField.set(name='Insight type', key='data.display.insight_type'),
        SearchField.set(name='Insight subtype', key='data.insight_subtype'),
        SearchField.set(name='Etag', key='data.etag'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_region_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_project_conf))
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_insight}),
]
