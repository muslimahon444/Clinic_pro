from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from doctors_app.urls import router as doctors_router
from user_app.urls import router as user_router


router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(doctors_router.registry)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include(router.urls))

]
