from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceVendorListView

urlpatterns = [
	path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
	path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
	path('invoicevendors/', InvoiceVendorListView.as_view(), name='invoice-vendor-list'),
]
