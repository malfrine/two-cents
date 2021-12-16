from datetime import datetime

from rest_framework import serializers

from core.apps.finances.models.loans import Loan, LoanInterest
from core.config.base import ReadOnlyModelSerializer, drop_none_fields
from core.utilities import get_months_between


class LoanInterestSerializer(serializers.ModelSerializer):

    current_term_end_month = serializers.SerializerMethodField(
        source="get_current_term_end_month"
    )

    def get_current_term_end_month(self, obj: Loan):
        if obj.current_term_end_date is None:
            return None
        else:
            return get_months_between(
                datetime.today().date(), obj.current_term_end_date
            )

    def to_representation(self, instance):
        rep = super(LoanInterestSerializer, self).to_representation(instance)
        if rep["current_term_end_month"] is not None:
            # we have a mortgage loan and we need to change the rep
            d = dict()
            d["current_term_end_month"] = rep.pop("current_term_end_month")
            d["interest_rate"] = drop_none_fields(rep)
            d["interest_type"] = "Mortgage Interest Rate"
            return drop_none_fields(d)
        else:
            return drop_none_fields(rep)

    class Meta:
        model = LoanInterest
        exclude = ("id", "current_term_end_date")


class LoanSerializer(ReadOnlyModelSerializer):

    interest_rate = LoanInterestSerializer(source="loan_interest", read_only=True)
    current_balance = serializers.SerializerMethodField(source="get_current_balance")
    final_month = serializers.SerializerMethodField(source="get_final_month")
    db_id = serializers.SerializerMethodField(source="get_db_id")

    def get_current_balance(self, obj: Loan):
        return None if obj.current_balance is None else -obj.current_balance

    def get_final_month(self, obj: Loan):
        return (
            None
            if obj.end_date is None
            else get_months_between(datetime.today().date(), obj.end_date)
        )

    def get_db_id(self, obj: Loan):
        return obj.pk

    def to_representation(self, instance: Loan):
        rep = super().to_representation(instance)
        rep = drop_none_fields(rep)
        return rep

    class Meta:
        model = Loan
        exclude = (
            "id",
            "loan_interest",
            "end_date",
        )
