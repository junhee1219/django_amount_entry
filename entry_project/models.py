# models.py
from django.db import models
from django.conf import settings

# 공통 필드를 위한 추상 모델
class BaseModel(models.Model):
	use_yn = models.BooleanField(default=True, verbose_name="사용여부")
	reg_user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="%(class)s_reg",
		on_delete=models.PROTECT,
		verbose_name="등록유저",
		null=True, blank=True
	)
	reg_dtm = models.DateTimeField(auto_now_add=True, verbose_name="등록일시", null=True)
	modi_user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name="%(class)s_modi",
		on_delete=models.PROTECT,
		null=True, blank=True,
		verbose_name="수정유저",
	)
	modi_dtm = models.DateTimeField(auto_now=True, verbose_name="수정일시", null=True)
	
	class Meta:
		abstract = True