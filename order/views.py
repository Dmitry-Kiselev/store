import logging
import traceback

from django.contrib import messages
from django.contrib.messages.api import MessageFailure
from django.db import IntegrityError, DatabaseError
from django.utils import timezone
from django.views.generic.edit import FormView
from stripe.error import InvalidRequestError

from payment.forms import PaymentForm
from payment.models import Payment
from payment.providers import PaymentProviders
from .models import Order

logger = logging.getLogger('django')


class OrderCreate(FormView):
    form_class = PaymentForm
    template_name = 'order/checkout.html'
    success_url = '/'
    payment_provider_class = PaymentProviders.get_default_provider()

    def __init__(self):
        super(OrderCreate, self).__init__()
        self.form_class = PaymentForm

    def form_valid(self, form):
        result = super(OrderCreate, self).form_valid(form)
        basket = self.request.user.basket
        discount = self.request.user.get_discount()
        order = Order.objects.create(basket=basket, discount=discount)
        basket.submit()
        basket.save()

        number = form.cleaned_data["number"]
        exp_month = form.cleaned_data["expiration_month"]
        exp_year = form.cleaned_data["expiration_year"]
        cvc = form.cleaned_data["cvc"]
        provider = self.payment_provider_class()
        try:
            charge_id = provider.charge(number, exp_month, exp_year, cvc,
                                        order.total_price)
        except InvalidRequestError as e:
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
            charge_id = None
            try:
                messages.error(self.request,
                               'Some error happened during checkout process. Please, try later ')
            except MessageFailure:  # happens during test, so we do not need to add this to log
                pass
        try:
            Payment.objects.create(charge_id=charge_id, order=order)
        except (DatabaseError, IntegrityError) as e:
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
        try:
            messages.success(self.request, 'Success!')
        except MessageFailure:  # happens during test, so we do not need to add this to log
            pass
        return result
