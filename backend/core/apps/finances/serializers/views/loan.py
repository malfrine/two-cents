from rest_framework import serializers

from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.loans import LoanInterest, MortgageDetails, Loan, LoanType


class LoanInterestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["interest_type"] == InterestTypes.FIXED:
            data.pop("prime_modifier", None)
            if not data["apr"]:
                raise serializers.ValidationError("Fixed interest loans must have an APR")
        elif data["interest_type"] == InterestTypes.VARIABLE:
            data.pop("apr", None)
            if not data["prime_modifier"]:
                raise serializers.ValidationError(
                    "Variable interest loans must have a Prime Modifier"
                )
        return data

    class Meta:
        model = LoanInterest
        fields = "__all__"


class MortgageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MortgageDetails
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    loan_interest = LoanInterestSerializer()
    mortgage_details = MortgageDetailSerializer(required=False)

    class Meta:
        model = Loan
        exclude = ("user",)

    def create(self, validated_data):
        for nested_field in ("loan_interest", "mortgage_details"):
            serializer = self.fields[nested_field]
            data = validated_data.pop(nested_field, None)
            if data is None:
                continue
            instance = serializer.create(data)
            validated_data[nested_field] = instance
        return super().create(validated_data)

    def update(self, instance: Loan, validated_data):
        for nested_field in ("loan_interest", "mortgage_details"):
            nested_instance = getattr(instance, nested_field)
            serializer = self.fields[nested_field]
            data = validated_data.pop(nested_field, None)
            if data is None:
                continue
            serializer.update(nested_instance, data)
            validated_data[nested_field] = nested_instance
        return super().update(instance, validated_data)

    def validate(self, attrs):
        # TODO: use required fields map
        loan_type = attrs["loan_type"]
        if loan_type == LoanType.MORTGAGE:
            attrs.pop("minimum_monthly_payment", None)
            attrs.pop("end_date", None)
            attrs.pop("current_balance", None)
            if not attrs["mortgage_details"]:
                raise serializers.ValidationError("Mortgage loans must have mortgage details")
        elif Loan.is_instalment_loan(loan_type):
            if not attrs["minimum_monthly_payment"]:
                raise serializers.ValidationError("Instalment loans must have a minimum monthly payment")
            if not attrs["end_date"]:
                raise serializers.ValidationError("Instalment loans must have an end date")
            if not attrs["current_balance"]:
                raise serializers.ValidationError("Instalment loans must have a current balance")
            attrs.pop("mortgage_details", None)
        else:
            # revolving loan
            attrs.pop("minimum_monthly_payment", None)
            attrs.pop("end_date", None)
            attrs.pop("mortgage_details", None)
            if not attrs["current_balance"]:
                raise serializers.ValidationError("Revolving loans must have a current balance")
        return attrs

    def get_loan_interest_serializer(self) -> LoanInterestSerializer:
        return self.fields["loan_interest"]
