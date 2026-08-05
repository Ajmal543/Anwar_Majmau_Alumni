from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('students/search/', views.student_search_view, name='student_search'),
    path('donate/', views.donate_view, name='donate'),
    path('donation/success/<int:donation_id>/', views.donation_success_view, name='donation_success'),
    path('donation/receipt/<int:donation_id>/', views.download_receipt_view, name='download_receipt'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('contact/', views.contact_view, name='contact'),
    
    # Staff Admin Extensions
    path('dashboard/', views.custom_admin_dashboard_view, name='admin_dashboard'),
    path('admin-export/students/', views.export_students_view, name='export_students'),
    path('admin-export/donations/', views.export_donations_view, name='export_donations'),
    path('admin-import/students/', views.import_students_view, name='import_students'),
]
