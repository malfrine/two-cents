from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from core.apps.finances.models.loans import Loan, LoanType, LoanInterest, MortgageDetails
from core.config.base import ReadOnlyModelSerializer, drop_none_fields
from core.utilities import get_months_between


class LoanInterestSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super(LoanInterestSerializer, self).to_representation(instance)
        return drop_none_fields(rep)

    class Meta:
        model = LoanInterest
        exclude = ("id",)


class MortgageDetailSerializer(serializers.ModelSerializer):

    current_term_start_month = serializers.SerializerMethodField(source="get_current_term_start_month")
    current_term_final_month = serializers.SerializerMethodField(source="get_current_term_final_month")
    start_month = serializers.SerializerMethodField(source="get_start_month")
    final_month = serializers.SerializerMethodField(source="get_final_month")

    def get_current_term_start_month(self, obj: MortgageDetails):
        return get_months_between(datetime.today().date(), obj.current_term_start_date)

    def get_current_term_final_month(self, obj: MortgageDetails):
        current_term_end_date = obj.current_term_start_date + relativedelta(years=obj.current_term_years)
        return get_months_between(datetime.today().date(), current_term_end_date)

    def get_start_month(self, obj: MortgageDetails):
        return get_months_between(datetime.today().date(), obj.purchase_date)

    def get_final_month(self, obj: MortgageDetails):
        final_date = obj.purchase_date + relativedelta(years=obj.amortization_years)
        return get_months_between(datetime.today().date(), final_date)

    class Meta:
        model = MortgageDetails
        exclude = ("id", "current_term_start_date", "current_term_years", "purchase_date", "amortization_years")


class LoanSerializer(ReadOnlyModelSerializer):

    interest_rate = LoanInterestSerializer(source="loan_interest", read_only=True)
    mortgage_details = MortgageDetailSerializer(read_only=True)
    current_balance = serializers.SerializerMethodField(source="get_current_balance")
    final_month = serializers.SerializerMethodField(source="get_final_month")

    def get_current_balance(self, obj: Loan):
        return None if obj.current_balance is None else -obj.current_balance

    def get_final_month(self, obj: Loan):
        return None if obj.end_date is None else get_months_between(datetime.today().date(), obj.end_date)

    def to_representation(self, instance: Loan):
        rep = super().to_representation(instance)
        rep = drop_none_fields(rep)
        if rep["loan_type"] == LoanType.MORTGAGE.value:
            mortgage_details = rep.pop("mortgage_details", dict())
            interest_rate = dict(interest_type='Interest Rate Terms')
            terms = [
                dict(
                    interest_rate=rep.pop("interest_rate"),
                    start_month=mortgage_details.pop("current_term_start_month"),
                    final_month=mortgage_details.pop("current_term_final_month"),
                )
            ]
            interest_rate["terms"] = terms
            rep["interest_rate"] = interest_rate
            return dict(**rep, **mortgage_details)
        else:
            return rep

    class Meta:
        model = Loan
        exclude = ("user", "id", "loan_interest", "end_date")
