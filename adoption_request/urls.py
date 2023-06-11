from rest_framework.routers import SimpleRouter
from .views import AdoptionRequestListView, AdoptionRequestApproveView


urlpatterns = []


router = SimpleRouter()
router.register("", AdoptionRequestListView)
router.register("approve", AdoptionRequestApproveView)

urlpatterns += router.urls
