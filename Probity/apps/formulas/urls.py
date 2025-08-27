from django.urls import path
from .views import BinomialFormulaView
from .views import BernoulliFormulaView

urlpatterns = [
    path('binomial/', BinomialFormulaView.as_view(), name='binomial-formula'),
    path('bernoulli/', BernoulliFormulaView , name='bernoulli-formula' )
]