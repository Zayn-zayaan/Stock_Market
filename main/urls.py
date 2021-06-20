from django.urls import path
from main.views import MainView, handlelogin, handlelogout, handlesignup, PostJsonListView, stockdetail, search, ask_query

urlpatterns = [
    path('', MainView.as_view(), name='main-view'),
    path('stocks-json/<int:num_posts>/', PostJsonListView.as_view(), name='list-view'),
    path('<int:Sno>/', stockdetail, name='stockdetail-view'),
    path('search/', search, name='search'),
    path('query', ask_query, name='askquery'),
    path('signup', handlesignup, name='handlesignup'),
    path('login', handlelogin, name='handlelogin'),
    path('logout/', handlelogout, name='handlelogout'),
]