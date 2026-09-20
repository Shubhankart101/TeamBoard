from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .models import Company, KBEntry, QueryLog
from .permissions import IsAdminUser
from .serializers import (
    KBEntrySerializer,
    RegisterRequestSerializer,
    RegisterResponseSerializer,
    LoginRequestSerializer,
    LoginResponseSerializer,
    QueryKBRequestSerializer,
    QueryKBResponseSerializer,
    UsageSummaryResponseSerializer,
)


@extend_schema(
    summary="Register a new company",
    description="Public endpoint to register a company details. Returns auto-generated API key and JWT access token.",
    request=RegisterRequestSerializer,
    responses={201: RegisterResponseSerializer, 400: "Bad Request"}
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_view(request):
    """
    POST /api/auth/register/
    Public endpoint to register a new company.
    """
    data = request.data
    username = data.get('username')
    password = data.get('password')
    company_name = data.get('company_name')
    email = data.get('email', '')

    if not username or not password or not company_name:
        return Response(
            {'error': 'username, password, and company_name are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create user; post_save signal auto-creates Company & generates api_key
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    company = user.company
    company.company_name = company_name
    # Ensure role remains CLIENT regardless of any input
    company.role = Company.Role.CLIENT
    company.save()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response(
        {
            'username': user.username,
            'company_name': company.company_name,
            'api_key': company.api_key,
            'access': access_token,
        },
        status=status.HTTP_201_CREATED
    )


@extend_schema(
    summary="Company login",
    description="Public endpoint to authenticate company user credentials and receive a fresh JWT access token.",
    request=LoginRequestSerializer,
    responses={200: LoginResponseSerializer, 401: "Unauthorized"}
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    """
    POST /api/auth/login/
    Public endpoint to log in with username & password.
    """
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response(
            {'error': 'username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    company = getattr(user, 'company', None)
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response(
        {
            'access': access_token,
            'company_name': company.company_name if company else '',
            'api_key': company.api_key if company else '',
        },
        status=status.HTTP_200_OK
    )


@extend_schema(
    summary="Query Knowledge Base",
    description="Protected endpoint for companies to search KB entries by keyword. Usage is atomically logged.",
    request=QueryKBRequestSerializer,
    responses={200: QueryKBResponseSerializer, 400: "Bad Request", 401: "Unauthorized"}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def query_kb_view(request):
    """
    POST /api/kb/query/
    Protected endpoint to search Knowledge Base.
    """
    search_term = request.data.get('search')
    if search_term is None or str(search_term).strip() == '':
        return Response(
            {'error': 'Search field is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not hasattr(request.user, 'company'):
        return Response(
            {'error': 'User is not associated with any company.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    company = request.user.company

    with transaction.atomic():
        matching_entries = KBEntry.objects.filter(
            Q(question__icontains=search_term) | Q(answer__icontains=search_term)
        )
        count = matching_entries.count()
        results = KBEntrySerializer(matching_entries, many=True).data

        QueryLog.objects.create(
            company=company,
            search_term=search_term,
            results_count=count
        )

    return Response(
        {
            'search': search_term,
            'count': count,
            'results': results,
        },
        status=status.HTTP_200_OK
    )


@extend_schema(
    summary="Admin usage summary dashboard",
    description="Admin-only endpoint providing platform-wide usage metrics (total queries, active companies, top 5 search terms).",
    responses={200: UsageSummaryResponseSerializer, 403: "Forbidden"}
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def usage_summary_view(request):
    """
    GET /api/admin/usage-summary/
    Admin-only endpoint for platform-wide usage statistics.
    """
    total_queries_res = QueryLog.objects.aggregate(total=Count('id'))
    total_queries = total_queries_res['total'] or 0

    active_companies = QueryLog.objects.values('company').distinct().count()

    top_search_terms_qs = QueryLog.objects.values('search_term').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    top_search_terms = list(top_search_terms_qs)

    return Response(
        {
            'total_queries': total_queries,
            'active_companies': active_companies,
            'top_search_terms': top_search_terms,
        },
        status=status.HTTP_200_OK
    )
