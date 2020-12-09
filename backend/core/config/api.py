from rest_framework import routers
from core.apps.finances.views import FinancialProfileView, InvestmentViewset, LoanViewset
from core.apps.users.views import UserViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = "/?"

# Users API
api.register(r"users", UserViewSet)
api.register(r"my/finances/loans", LoanViewset)
api.register(r"my/finances/investments", InvestmentViewset)
api.register(r"my/finances/profile", FinancialProfileView, basename="profile")