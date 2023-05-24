from django.urls import path
from . import views


urlpatterns = [
    path("",views.admins_log),
    path('admins_login', views.admin_login, name='admins_login'),
    path('admins_home',views.admin_home),
    # path('admins_delete/<int:id>',views.admins_delete,name='admins_delete'),

    path('product_details', views.product_details, name='product_details'),
    path('category', views.category_details, name='category'),
    path('order', views.order_details, name='order'),
    path('add_product', views.add_products, name='add_product'),
    path('product_delete/<int:id>',views.product_delete,name='product_delete'),

    path('add_category', views.add_category, name='add_category'),
    path('cat_delete/<int:id>',views.category_delete,name='category_delete'),
    path('new_product/',views.new_products),
    path('edit_products/<int:id>',views.edit_products,name='edit_products'),
    path('product_update/<int:id>',views.product_update,name='product_update'),
    path('prod_upd/<int:id>',views.pro_update),
    path('cat_update/<int:id>',views.category_update,name='cat_update'),
    path('cat_upd/<int:id>',views.cat_update),
    path('new_category',views.new_category),
    path('delete_product',views.product_delete),
    path('user_block/<int:id>',views.user_block,name='user_block'),
    path('user_unblock/<int:id>',views.user_unblock,name='user_unblock'),
    path('order_delete/<int:id>',views.order_delete,name = 'order_delete'),
    path('order_update/<int:id>',views.order_update,name='order_update'),
    path('ord_upd/<int:id>',views.order_upd),
    path('dashboard/',views.Dashboard),
    path('logout/',views.Logout)
    
    
   
]