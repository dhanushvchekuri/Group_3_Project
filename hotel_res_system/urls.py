
from django.contrib import admin
from django.urls import path

from app.hotel_booking_logic import hotel_home,admin_signup_logic,customer_dashboard,feedback_view

from app.hotel_booking_logic import profile_view,edit_profile_view,my_bookings_view,customer_signup_logic

from app.hotel_booking_logic import payment_details_view,admin_dashboard,view_customers

from app.hotel_booking_logic import add_room,delete_room,add_service,delete_service,service_list

from app.hotel_booking_logic import room_list,book_room,select_additional_room_services,payment_view

from app.hotel_booking_logic import booking_list,customer_logic_logic,admin_login_logic

from app.hotel_booking_logic import see_feedback_list

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',hotel_home,name='hotel_home'),

    path('customer_signup/', customer_signup_logic, name='customer_signup'),

    path('admin_signup/', admin_signup_logic, name='admin_signup'),

    path('customer_login/', customer_logic_logic, name='customer_login'),

    path('admin_login/', admin_login_logic, name='admin_user_login'),

    path('customer/dashboard',customer_dashboard,name='customer_dashboard'),

    path('feedback/', feedback_view, name='feedback'),

    path('customer_profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),

    path('my-bookings/', booking_list, name='my_bookings'),

    path('payment-details/', payment_details_view, name='payment_details'),

    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),

    path('customer_profile_with_bookings/', view_customers, name='view_customers'),

    path('admin_rooms/add/', add_room, name='add_room'),
    path('admin_rooms/delete/<int:room_id>/', delete_room, name='delete_room'),


    path('admin_services/add/', add_service, name='add_service'),
    path('admin_services/delete/<int:service_id>/', delete_service, name='delete_service'),
    path('admin_services/', service_list, name='service_list'),

    path('rooms/', room_list, name='room_list'),

    path('book_room/<int:room_id>/', book_room, name='book_room'),

    path('select_services/<int:booking_id>/', select_additional_room_services, name='select_services'),

    path('payment/<int:booking_id>/', payment_view, name='make_payment'),

    path('bookings/',booking_list,name='booking_list'),

    path('feedbacks/list/',see_feedback_list,name='feedback_list'),

]
