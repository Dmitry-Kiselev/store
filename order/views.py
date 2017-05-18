from django.views.generic.edit import FormView
from .models import Order, Payment
from .forms import PaymentForm


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
        payment = Payment.objects.create(order=order)
        payment.charge(number, exp_month, exp_year, cvc)
        return result

