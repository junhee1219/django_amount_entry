from rest_framework import serializers
from .models import InvoiceMaster, InvoiceVendor

class InvoiceMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = InvoiceMaster
		fields = '__all__'

class InvoiceVendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = InvoiceVendor
		fields = '__all__'
