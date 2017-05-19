from django.views.generic.edit import FormView
from .models import Order
from .forms import PaymentForm
from payment.models import Payment
from django.contrib import messages
from stripe.error import InvalidRequestError


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
            payment.save()
            messages.success(self.request, 'Success!')
        except InvalidRequestError as e:
            messages.error(self.request, str(e))
        return result
