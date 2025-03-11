from django.shortcuts import redirect
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# 기본 User 모델 가져오기
User = get_user_model()
# 서명 객체 (이메일 인증용)
signer = TimestampSigner()


def email_authenticate(request, email, password):
	"""
	email을 기준으로 User 객체를 찾은 후 비밀번호 확인
	"""
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return None
	if user.check_password(password):
		return user
	return None


class LoginView(APIView):
	# 로그인은 인증 없이 접근 가능
	authentication_classes = []
	permission_classes = []
	
	def post(self, request, format=None):
		email = request.data.get('email')
		password = request.data.get('password')
		if not email or not password:
			return Response({'error': '모든 필드를 입력하세요.'},
							status=status.HTTP_400_BAD_REQUEST)
		user = email_authenticate(request, email=email, password=password)
		if user is not None:
			# 로그인 성공 시 토큰 발급 및 세션 로그인 처리(필요 시)
			token, created = Token.objects.get_or_create(user=user)
			role = 'admin' if user.is_staff else 'worker'
			login(request, user)
			return Response({
				'success': True,
				'role': role,
				'token': token.key,
			}, status=status.HTTP_200_OK)
		else:
			return Response({'error': '잘못된 이메일 또는 비밀번호'},
							status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
	# 인증 없이 접근 가능
	authentication_classes = []
	permission_classes = []
	
	def post(self, request, format=None):
		email = request.data.get('email')
		nickname = request.data.get('nickname')
		password = request.data.get('password')
		password2 = request.data.get('password2')
		
		# 필수 입력값 검증
		if not email or not nickname or not password or not password2:
			return Response({'error': '모든 필드를 입력하세요.'},
			                status=status.HTTP_400_BAD_REQUEST)
		if password != password2:
			return Response({'error': '비밀번호가 일치하지 않습니다.'},
			                status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(email=email).exists():
			return Response({'error': '이미 사용 중인 이메일입니다.'},
			                status=status.HTTP_400_BAD_REQUEST)
		
		# 신규 사용자 생성
		# username 필드에는 email 값을 저장하고, nickname은 first_name 필드에 저장 (단, 실제 프로젝트에서는 커스텀 유저모델 권장)
		user = User.objects.create_user(username=email, email=email, password=password)
		user.first_name = nickname  # 화면에 표시할 닉네임
		user.is_active = False  # 이메일 인증 전에는 활성화하지 않음
		user.save()
		
		# 이메일 인증 토큰 생성 (유효기간 24시간)
		token = signer.sign(user.pk)
		verification_url = request.build_absolute_uri(reverse('email-verify')) + f'?token={token}'
		
		subject = '이메일 인증'
		message = f'가입을 완료하려면 다음 링크를 클릭하세요:\n{verification_url}'
		from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
		send_mail(subject, message, from_email, [email])
		
		return Response({
			'success': True,
			'message': '회원가입 성공! 이메일로 전송된 인증 링크를 확인해주세요.'
		}, status=status.HTTP_201_CREATED)


class EmailVerifyView(APIView):
	authentication_classes = []
	permission_classes = []
	
	def get(self, request, format=None):
		token = request.GET.get('token')
		if not token:
			return redirect('http://localhost:3000/?error=token_missing')
		try:
			user_pk = signer.unsign(token, max_age=60*60*24)  # 24시간 유효
			user = User.objects.get(pk=user_pk)
			user.is_active = True
			user.save()
			# 인증 성공 시 React 메인페이지로 리다이렉트 (예: http://localhost:3000)
			return redirect('http://localhost:3000/')
		except SignatureExpired:
			return redirect('http://localhost:3000/?error=token_expired')
		except BadSignature:
			return redirect('http://localhost:3000/?error=bad_token')
		except User.DoesNotExist:
			return redirect('http://localhost:3000/?error=user_not_found')