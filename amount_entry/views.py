from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import InvoiceMaster, InvoiceVendor
from .serializers import InvoiceMasterSerializer, InvoiceVendorSerializer

# 인보이스 목록 조회 API
class InvoiceListView(ListAPIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = InvoiceMasterSerializer
	queryset = InvoiceMaster.objects.all()  # 필요에 따라 필터 적용 가능

# 인보이스 상세 조회 및 업데이트 API
class InvoiceDetailView(RetrieveUpdateAPIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = InvoiceMasterSerializer
	queryset = InvoiceMaster.objects.all()
	
	def update(self, request, *args, **kwargs):
		invoice = self.get_object()
		# 만약 이미 제출되어 status가 3이면 업데이트 불가
		if invoice.status and invoice.status.id == 3:
			return Response({"error": "이미 제출된 인보이스는 수정할 수 없습니다."},
			                status=status.HTTP_400_BAD_REQUEST)
		return super().update(request, *args, **kwargs)

# 인보이스 벤더 목록 조회 API
class InvoiceVendorListView(ListAPIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = InvoiceVendorSerializer
	queryset = InvoiceVendor.objects.all()
