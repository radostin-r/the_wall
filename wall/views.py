from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import WallProfile, DailyIceUsage


class WallProfileViewSet(viewsets.ViewSet):
    class IceAmountOutputSerializer(serializers.Serializer):
        day = serializers.CharField()
        ice_amount = serializers.CharField()

    class CostOutputSerializer(serializers.Serializer):
        day = serializers.CharField(allow_null=True, required=False)
        cost = serializers.CharField()

    @action(detail=True, url_path='days/(?P<day>\d+)')
    def daily_usage(self, request, pk=None, day=None):
        """
        Handles the daily ice usage for a specific profile.
        """
        ice_used = DailyIceUsage.objects.filter(profile_id=pk, day=day)
        if not ice_used:
            return Response({'error': 'No daily costs calculated.'}, status=404)

        output_serializer = self.IceAmountOutputSerializer({'day': ice_used[0].day, 'ice_amount': ice_used[0].ice_used})
        return Response(output_serializer.data)

    @action(detail=True, url_path='overview/(?P<day>\d+)?')
    def profile_overview(self, request, pk=None, day=None):
        """
        Returns the cost overview for a specific profile on a specific day.
        """
        ice_used = DailyIceUsage.objects.filter(profile_id=pk, day=day)
        if not ice_used:
            return Response({'error': 'No daily costs calculated.'}, status=404)
        daily_costs = [usage.cost for usage in ice_used]

        output_serializer = self.CostOutputSerializer({'day': ice_used[0].day, 'cost': sum(daily_costs)})
        return Response(output_serializer.data)

    @action(detail=False, url_path='overview/(?P<day>\d+)?')
    def daily_overview(self, request, day=None):
        """
        Returns the cost overview for all profiles on a specific day.
        """
        ice_used = DailyIceUsage.objects.filter(day=day)
        if not ice_used:
            return Response({'error': 'No daily costs calculated.'}, status=404)
        daily_costs = [usage.cost for usage in ice_used]

        output_serializer = self.CostOutputSerializer({'day': ice_used[0].day, 'cost': sum(daily_costs)})
        return Response(output_serializer.data)

    @action(detail=False, url_path='overview')
    def total_overview(self, request):
        """
        Returns the total cost of all profiles.
        """
        total_cost = sum([profile.calculate_total_cost() for profile in WallProfile.objects.all()])
        output_serializer = self.CostOutputSerializer({'day': None, 'cost': total_cost})
        return Response(output_serializer.data)
