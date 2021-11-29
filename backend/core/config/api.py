from rest_framework import routers

from core.apps.finances.views import (
    FinancialProfileView,
    InvestmentViewset,
    LoanViewset,
    UserFinancesViewset,
    FinancesEnumsViewset,
    PenniesRequestViewset,
    FinancialGoalViewset,
)
from core.apps.payments.views import (
    CurrentPaymentPlanViewSet,
    PaymentPlanIntentViewset,
    PromotionCodeViewset,
)
from core.apps.plan.views import UserPlanViewSet
from core.apps.users.views import AccountViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = "/?"


# Users API
api.register(r"my/account", AccountViewSet, basename="account")
api.register(r"my/finances", UserFinancesViewset, basename="user-finances")
api.register(r"my/plan/request", PenniesRequestViewset, basename="pennies-request")
api.register(r"my/finances/loans", LoanViewset)
api.register(r"my/finances/investments", InvestmentViewset)
api.register(r"my/finances/goals", FinancialGoalViewset)
api.register(r"my/finances/profile", FinancialProfileView, basename="financial-profile")
api.register(r"my/plan", UserPlanViewSet, basename="financial-plan")
api.register(r"finances/enums", FinancesEnumsViewset, basename="financial-enums")
api.register(
    r"my/payment-plan/intent", PaymentPlanIntentViewset, basename="payment-plan-intent"
)
api.register(r"my/payment-plan", CurrentPaymentPlanViewSet, basename="payment-plan")
api.register(
    r"my/payment-plan/promotion-code", PromotionCodeViewset, basename="promotion-code"
)
