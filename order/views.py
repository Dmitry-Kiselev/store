import logging
import traceback

from django.contrib import messages
from django.db import IntegrityError, DatabaseError
from django.utils import timezone
from django.views.generic.edit import FormView
from stripe.error import InvalidRequestError

from payment.models import Payment
from .forms import PaymentForm
from .models import Order


class OrderCreate(FormView):
    form_class = PaymentForm
    template_name = 'order/checkout.html'
    success_url = '/'

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
        payment_service = Payment.get_payment_service()
        payment = payment_service(order=order)
        try:
            payment.charge(number, exp_month, exp_year, cvc)
        except InvalidRequestError as e:
            logger = logging.getLogger(__name__)
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
            messages.error(self.request,
                           'Some error happened during checkout process. Please, try later ')
        try:
            payment.save()
        except (DatabaseError, IntegrityError) as e:
            logger = logging.getLogger(__name__)
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
        messages.success(self.request, 'Success!')
        return result
