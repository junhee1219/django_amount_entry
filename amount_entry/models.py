from django.db import models
from django.conf import settings
from entry_project.models import BaseModel

# FK 대상 모델들 (예시 스텁, 실제 모델 구조에 맞게 수정)
class WorkSchedule(BaseModel):
	from_work_date = models.DateField(null=True)
	to_work_date = models.DateField(null=True)
	work_user_id = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		verbose_name="작업자",
		null=True
	),
	weight = models.DecimalField(max_digits=4, decimal_places=3, default=0)
	
	def __str__(self):
		return self.work_user_id


class InvoiceVendor(BaseModel):
	title = models.CharField(max_length=100, verbose_name="벤더명")
	
	def __str__(self):
		return self.title


class Store(BaseModel):
	code = models.CharField(max_length=10, verbose_name="매장코드")
	name = models.CharField(max_length=100, verbose_name="매장명")
	sort_number = models.IntegerField(verbose_name="정렬순서", null=True)
	
	def __str__(self):
		return self.name


class Department(BaseModel):
	name = models.CharField(max_length=100, verbose_name="부서명")
	sort_number = models.IntegerField(verbose_name="정렬순서", null=True)
	
	def __str__(self):
		return self.name


class Status(BaseModel):
	status = models.CharField(max_length=50, verbose_name="상태")
	
	def __str__(self):
		return self.status


# 작업 인보이스 마스터 모델
class InvoiceMaster(BaseModel):
	invoice_name = models.CharField(max_length=255, verbose_name="인보이스명")
	invoice_number = models.CharField(max_length=100, unique=True, verbose_name="인보이스번호")
	invoice_issue_date = models.DateField(verbose_name="인보이스날짜")
	invoice_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="총금액")
	invoice_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="인보이스 파일 URL")
	invoice_thumb_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="인보이스 썸네일 경로")
	sort_number = models.IntegerField(verbose_name="정렬순서", null=True)
	
	# FK들
	work_schd = models.ForeignKey(WorkSchedule, on_delete=models.PROTECT, verbose_name="스케줄 ID")
	invoice_vendor = models.ForeignKey(InvoiceVendor, on_delete=models.PROTECT, verbose_name="인보이스 벤더 ID")
	store = models.ForeignKey(Store, on_delete=models.PROTECT, verbose_name="매장 ID")
	department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="부서 ID")
	status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="상태 ID")
	
	def __str__(self):
		return f"{self.invoice_number} - {self.invoice_name}"
