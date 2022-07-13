from rest_framework import mixins, viewsets


class ListRetrieveViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    pass


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    pass


class RetrieveListCreateUpdateDestroyViewSet(mixins.RetrieveModelMixin,
                                             mixins.ListModelMixin,
                                             mixins.CreateModelMixin,
                                             mixins.UpdateModelMixin,
                                             mixins.DestroyModelMixin,
                                             viewsets.GenericViewSet):
    pass
