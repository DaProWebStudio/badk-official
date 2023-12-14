from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title='BADK server',
      default_version='v1',
      description="Бишкекский автомобильно-дорожный колледж - имени Кусаина Кольбаева",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="help@el-kitep.kg"),
      license=openapi.License(name="MIT License"),
   ),
   public=False,
   permission_classes=[permissions.AllowAny],
)