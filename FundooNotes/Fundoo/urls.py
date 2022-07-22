from django.contrib import admin
from django.urls import path, include
from .routers import router

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Fundoo Notes')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fundoonotes/', schema_view),
    path('user/', include('users.urls')),
    path('notes/', include('Fundoonotes.urls')),
    path('labels/', include('labels.urls')),
    # path('api/notes/', include(router.urls)),
]
