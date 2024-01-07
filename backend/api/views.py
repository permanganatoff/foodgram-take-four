from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.paginations import CustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (
    FavoriteCreateDeleteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    ShoppingCartCreateDeleteSerializer,
    SubscribeCreateSerializer,
    SubscribeSerializer,
    TagSerializer,
)
from api.services import generate_shopping_cart_text
from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from users.models import User


class BaseRelationsViewSet:
    def relation_create(self, request, serializer_class, data):
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def relation_delete(self, request, serializer_class,
                        user_id, target_id, target_type):
        serializer = serializer_class()
        if target_type == 'author':
            serializer.validate_for_delete(
                user_id=user_id, author_id=target_id)
            serializer.Meta.model.objects.filter(
                user_id=user_id, author_id=target_id).delete()
        elif target_type == 'recipe':
            serializer.validate_for_delete(
                user_id=user_id, recipe_id=target_id)
            serializer.Meta.model.objects.filter(
                user_id=user_id, recipe_id=target_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(BaseRelationsViewSet, viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags', 'ingredients')
    permission_classes = [AuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        data = {'user': request.user.id, 'recipe': pk}
        return self.relation_create(
            request,
            FavoriteCreateDeleteSerializer,
            data
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.relation_delete(
            request,
            FavoriteCreateDeleteSerializer,
            user_id=request.user.id,
            target_id=pk,
            target_type='recipe'
        )

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        data = {'user': request.user.id, 'recipe': pk}
        return self.relation_create(
            request,
            ShoppingCartCreateDeleteSerializer,
            data
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.relation_delete(
            request,
            ShoppingCartCreateDeleteSerializer,
            user_id=request.user.id,
            target_id=pk,
            target_type='recipe'
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart_text = generate_shopping_cart_text(request)
        response = HttpResponse(
            shopping_cart_text,
            content_type='text/plain')
        response['Content-Disposition'] = (
            "attachment;filename='shopping_cart.txt'")
        return response


class UserViewSet(BaseRelationsViewSet, BaseUserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        data = {'user': request.user.id, 'author': id}
        return self.relation_create(request, SubscribeCreateSerializer, data)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        return self.relation_delete(
            request,
            SubscribeCreateSerializer,
            user_id=request.user.id,
            target_id=id,
            target_type='author'
        )

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            author__user=request.user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
