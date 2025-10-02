from django.urls import path
from .views import (
    BinomialFormulaView, 
    NormalFormulaView, 
    BernoulliFormulaView, 
    MultinomialFormulaView, 
    GibbsFormulaView,
    ExponencialFormulaView,
    BivariateNormalView
)

urlpatterns = [
    path('binomial/', BinomialFormulaView.as_view(), name='binomial-formula'),
    # Esta es la única URL que necesitas para la Normal General
    path('normal-standard/', NormalFormulaView.as_view(), name='normal-standard-formula'),
    path('bernoulli/', BernoulliFormulaView.as_view(), name='bernoulli_formula'),
    path('multinomial/', MultinomialFormulaView.as_view(), name='multinomial-formula'),
    path('gibbs/', GibbsFormulaView.as_view(), name='gibbs-formula'),
    path('exponencial/', ExponencialFormulaView.as_view(), name='exponencial-formula'),
    path('bivariate-normal/', BivariateNormalView.as_view(), name='bivariate-normal-formula'),

]
