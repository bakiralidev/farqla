# filters.py
import django_filters as df
from django.db.models import Q, F
from .models import Bank, Card, Credit, Deposit, Currency, P2POffer

class BankFilter(df.FilterSet):
    q = df.CharFilter(method='search')
    rating_min = df.NumberFilter(field_name='rating', lookup_expr='gte')
    branches_min = df.NumberFilter(field_name='number_of_branches', lookup_expr='gte')
    happy_min = df.NumberFilter(field_name='number_of_satisfied_customers', lookup_expr='gte')
    opened_from = df.DateFilter(field_name='opening_date', lookup_expr='gte')
    opened_to   = df.DateFilter(field_name='opening_date', lookup_expr='lte')

    class Meta:
        model = Bank
        fields = ['is_active']

    def search(self, qs, name, value):
        # modeltranslation: aktiv tilga mos .name/.description ishlaydi
        return qs.filter(
            Q(name__icontains=value) |
            Q(address__icontains=value) |
            Q(description__icontains=value)
        )

class CardFilter(df.FilterSet):
    system = df.CharFilter(field_name='system')
    card_type = df.CharFilter(field_name='card_type')
    currency = df.CharFilter(field_name='currency_code')
    interest_rate_min = df.NumberFilter(field_name='interest_rate', lookup_expr='gte')
    interest_rate_max = df.NumberFilter(field_name='interest_rate', lookup_expr='lte')
    period_months_min = df.NumberFilter(field_name='period_months', lookup_expr='gte')
    period_months_max = df.NumberFilter(field_name='period_months', lookup_expr='lte')
    amount_min = df.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = df.NumberFilter(field_name='amount', lookup_expr='lte')
    fast_issuance = df.BooleanFilter(field_name='fast_issuance')

    class Meta:
        model = Card
        fields = ['bank', 'is_active']

class CreditFilter(df.FilterSet):
    purpose = df.CharFilter(field_name='purpose')
    interest_rate_min = df.NumberFilter(field_name='interest_rate', lookup_expr='gte')
    interest_rate_max = df.NumberFilter(field_name='interest_rate', lookup_expr='lte')
    period_months_min = df.NumberFilter(field_name='period_months', lookup_expr='gte')
    period_months_max = df.NumberFilter(field_name='period_months', lookup_expr='lte')
    amount_min = df.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = df.NumberFilter(field_name='amount', lookup_expr='lte')
    down_payment_max = df.NumberFilter(field_name='down_payment', lookup_expr='lte')
    collateral_required = df.BooleanFilter(field_name='collateral_required')
    grace_min = df.NumberFilter(field_name='grace_period_months', lookup_expr='gte')
    grace_max = df.NumberFilter(field_name='grace_period_months', lookup_expr='lte')
    early_fee_max = df.NumberFilter(field_name='early_repayment_fee_percent', lookup_expr='lte')
    official_income_required = df.BooleanFilter(field_name='official_income_required')
    has_online_apply = df.BooleanFilter(method='online_apply')

    class Meta:
        model = Credit
        fields = ['bank', 'is_active', 'purpose']

    def online_apply(self, qs, name, value):
        return qs.exclude(online_apply_link='') if value else qs

class DepositFilter(df.FilterSet):
    currency = df.CharFilter(field_name='currency_code')
    interest_rate_min = df.NumberFilter(field_name='interest_rate', lookup_expr='gte')
    interest_rate_max = df.NumberFilter(field_name='interest_rate', lookup_expr='lte')
    period_months_min = df.NumberFilter(field_name='period_months', lookup_expr='gte')
    period_months_max = df.NumberFilter(field_name='period_months', lookup_expr='lte')
    min_amount_max = df.NumberFilter(field_name='min_amount', lookup_expr='lte')
    max_amount_min = df.NumberFilter(field_name='max_amount', lookup_expr='gte')
    payout_frequency = df.CharFilter(field_name='payout_frequency')
    capitalization = df.BooleanFilter(field_name='capitalization')
    early_withdrawal_allowed = df.BooleanFilter(field_name='early_withdrawal_allowed')
    auto_renewal = df.BooleanFilter(field_name='auto_renewal')
    has_online_open = df.BooleanFilter(method='online_open')

    class Meta:
        model = Deposit
        fields = ['bank', 'is_active']

    def online_open(self, qs, name, value):
        return qs.exclude(online_open_link='') if value else qs

class CurrencyFilter(df.FilterSet):
    code = df.CharFilter(field_name='code')
    buy_rate_max = df.NumberFilter(field_name='buy_rate', lookup_expr='lte')
    sell_rate_min = df.NumberFilter(field_name='sell_rate', lookup_expr='gte')
    change_min = df.NumberFilter(field_name='change_percent', lookup_expr='gte')
    change_max = df.NumberFilter(field_name='change_percent', lookup_expr='lte')
    updated_from = df.DateTimeFilter(field_name='updated_at_api', lookup_expr='gte')
    updated_to = df.DateTimeFilter(field_name='updated_at_api', lookup_expr='lte')

    class Meta:
        model = Currency
        fields = ['bank']

class P2PFilter(df.FilterSet):
    app_id = df.NumberFilter(field_name='app__id')
    app_slug = df.CharFilter(field_name='app__slug')
    from_scheme = df.CharFilter(field_name='from_scheme')
    to_scheme = df.CharFilter(field_name='to_scheme')
    commission_type = df.CharFilter(field_name='commission_type')
    commission_value_max = df.NumberFilter(field_name='commission_value', lookup_expr='lte')
    active_on = df.DateFilter(method='active_on_date')

    class Meta:
        model = P2POffer
        fields = ['is_active']

    def active_on_date(self, qs, name, value):
        return qs.filter(
            (Q(starts_at__isnull=True) | Q(starts_at__lte=value)),
            (Q(ends_at__isnull=True) | Q(ends_at__gte=value)),
        )
