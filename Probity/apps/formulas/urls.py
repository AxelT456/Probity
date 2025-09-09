from django.urls import path
from .views import BinomialFormulaView, NormalFormulaView, BernoulliFormulaView, MultinomialFormulaView, GibbsFormulaView, NormalCumulativeView, ExponencialFormulaView

urlpatterns = [
    path('binomial/', BinomialFormulaView.as_view(), name='binomial-formula'),
    path('normal-standard/', NormalFormulaView.as_view(), name='normal-standard-formula'),
    path('bernoulli/', BernoulliFormulaView.as_view(), name='bernoulli_formula'),
    path('multinomial/', MultinomialFormulaView.as_view(), name='multinomial-formula'),
    path('gibbs/',GibbsFormulaView.as_view(),name='gibbs-formula'),
    path('normal-cumulative/', NormalCumulativeView.as_view(), name='normal-cumulative-formula'),
    path('exponencial/',ExponencialFormulaView.as_view(),name='exponencial-formula')
]