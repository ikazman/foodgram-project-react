from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import FollowViewSet, UserViewSet
from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='User')
router.register('ingredients', IngredientViewSet, basename='Ingredient')
router.register('recipes', RecipeViewSet, basename='Recipe')
router.register('tags', TagViewSet, basename='Tag')


urlpatterns = [
    path('users/subscriptions/',
         FollowViewSet.as_view(({'get': 'list'})), name='Subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
