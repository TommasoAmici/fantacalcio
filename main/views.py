# Create your views here.
from django.conf import settings
from rest_framework import permissions, serializers, viewsets
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .models import League, Role, Player, Season, Performance
from .serializers import (
    LeagueSerializer,
    UserSerializer,
    RoleSerializer,
    PlayerSerializer,
    SeasonSerializer,
    PerformanceSerializer,
)
from .custom_permissions import IsOwnerOrReadOnly


User = get_user_model()


class LeagueViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    lookup_field = "slug"
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = (permissions.IsAuthenticated,)
