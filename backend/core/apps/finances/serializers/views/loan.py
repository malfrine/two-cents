from rest_framework import serializers

from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.loans import LoanInterest, Loan, LoanType


class LoanInterestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["interest_type"] == InterestTypes.FIXED:
            data.pop("prime_modifier", None)
            if data.get("apr") is None:
                raise serializers.ValidationError(
                    "Fixed interest loans must have an APR"
                )
        elif data["interest_type"] == InterestTypes.VARIABLE:
            data.pop("apr", None)
            if data.get("prime_modifier") is None:
                raise serializers.ValidationError(
                    "Variable interest loans must have a Prime Modifier"
                )
        return data

    class Meta:
        model = LoanInterest
        fields = "__all__"


# class MortgageDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = MortgageDetails
#         fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    loan_interest = LoanInterestSerializer()
    # mortgage_details = MortgageDetailSerializer(required=False)

    class Meta:
        model = Loan
        exclude = ("financial_data",)

    def create(self, validated_data):
        for nested_field in ("loan_interest",):
            serializer = self.fields[nested_field]
            data = validated_data.pop(nested_field, None)
            if data is None:
                continue
            instance = serializer.create(data)
            validated_data[nested_field] = instance
        return super().create(validated_data)

    def update(self, instance: Loan, validated_data):
        for nested_field in ("loan_interest",):
            nested_instance = getattr(instance, nested_field)
            serializer = self.fields[nested_field]
            data = validated_data.pop(nested_field, None)
            if data is None:
                continue
            serializer.update(nested_instance, data)
            validated_data[nested_field] = nested_instance
        return super().update(instance, validated_data)

    def validate(self, attrs):
        mandatory_fields = tuple()
        pop_fields = tuple()
        loan_type = attrs["loan_type"]

        # define fields to pop and validate
        if loan_type == LoanType.MORTGAGE:
            mandatory_fields = (
                "minimum_monthly_payment",
                "end_date",
                "current_balance",
            )
        elif Loan.is_instalment_loan(loan_type):
            mandatory_fields = (
                "minimum_monthly_payment",
                "end_date",
                "current_balance",
            )
            pop_fields = ("mortgage_details",)
        else:
            mandatory_fields = ("current_balance",)
            pop_fields = ("minimum_monthly_payment", "end_date", "mortgage_details")

        for field in pop_fields:
            if field in attrs:
                attrs.pop(field)
        for field in mandatory_fields:
            if attrs.get(field) is None:
                raise serializers.ValidationError(
                    f"{loan_type} loan must have '{field}' in input"
                )
        return attrs

    def get_loan_interest_serializer(self) -> LoanInterestSerializer:
        return self.fields["loan_interest"]
