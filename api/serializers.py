from rest_framework import serializers
from .models import KBEntry, Company, QueryLog


class KBEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = KBEntry
        fields = ['id', 'question', 'answer', 'category']


class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, help_text="Unique company username")
    password = serializers.CharField(write_only=True, help_text="Account password")
    company_name = serializers.CharField(max_length=255, help_text="Name of the company")
    email = serializers.EmailField(required=False, allow_blank=True, help_text="Company contact email")


class RegisterResponseSerializer(serializers.Serializer):
    username = serializers.CharField()
    company_name = serializers.CharField()
    api_key = serializers.CharField()
    access = serializers.CharField(help_text="JWT access token")


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="JWT access token")
    company_name = serializers.CharField()
    api_key = serializers.CharField()


class QueryKBRequestSerializer(serializers.Serializer):
    search = serializers.CharField(help_text="Keyword to search in question or answer")


class QueryKBResponseSerializer(serializers.Serializer):
    search = serializers.CharField()
    count = serializers.IntegerField()
    results = KBEntrySerializer(many=True)


class UsageSummaryTopSearchTermSerializer(serializers.Serializer):
    search_term = serializers.CharField()
    count = serializers.IntegerField()


class UsageSummaryResponseSerializer(serializers.Serializer):
    total_queries = serializers.IntegerField()
    active_companies = serializers.IntegerField()
    top_search_terms = UsageSummaryTopSearchTermSerializer(many=True)

