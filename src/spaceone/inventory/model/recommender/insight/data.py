from schematics import Model
from schematics.types import ModelType, ListType, StringType, DictType, UnionType, BooleanType, FloatType

from spaceone.inventory.libs.schema.cloud_service import BaseResource


class Display(Model):
    insight_type = StringType()
    insight_type_display = StringType()
    target_resources_display = ListType(DictType(StringType))


class InsightStateInfo(Model):
    state = StringType(choices=('STATE_UNSPECIFIED', 'ACTIVE', 'ACCEPTED', 'DISMISSED'))
    state_metadata = DictType(StringType())


class RecommendationReference(Model):
    recommendation = StringType()


class Insight(BaseResource):
    name = StringType()
    description = StringType()
    target_resources = ListType(StringType(), deserialize_from='targetResources')
    insight_subtype = StringType(deserialize_from='insightSubtype')
    content = DictType(UnionType(
        [StringType(), BooleanType(), ListType(StringType), DictType(StringType()), ListType(DictType(StringType()))]
    ))
    last_refresh_time = StringType(deserialize_from='lastRefreshTime')
    observation_period = StringType(deserialize_from='observationPeriod')
    state_info = ModelType(InsightStateInfo, deserialize_from='stateInfo')
    category = StringType(choices=(
        'CATEGORY_UNSPECIFIED', 'COST', 'SECURITY', 'PERFORMANCE', 'MANAGEABILITY', 'SUSTAINABILITY', 'RELIABILITY'
    ))
    severity = StringType(choices=(
        'SEVERITY_UNSPECIFIED', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    ))
    etag = StringType()
    associated_recommendations = ListType(ModelType(RecommendationReference),
                                          deserialize_from='associatedRecommendations')
    display = ModelType(Display)

    def reference(self):
        return {
            "resource_id": self.name,
            "external_link": f"https://console.cloud.google.com/home/recommendations"
        }

    class Options:
        serialize_when_none = False


class OverallStats(Model):
    reserved_count = FloatType(deserialize_from='reservedCount')
    unassigned_count = FloatType(deserialize_from='unassignedCount')
    unassigned_ratio = FloatType(deserialize_from='unassignedRatio')


class RegionStats(Model):
    region = StringType()
    stats = ModelType(OverallStats)


class IPAddressInsightContent(Model):
    project_uri = StringType(deserialize_from='projectUri')
    overall_stats = ModelType(OverallStats, deserialize_from='overallStats')
    region_stats = ListType(ModelType(RegionStats), deserialize_from='regionStats')


class IPAddressInsight(Insight):
    content = ModelType(IPAddressInsightContent)
