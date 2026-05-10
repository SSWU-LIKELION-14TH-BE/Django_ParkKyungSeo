from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # 1. 기본 유저 정보 저장 
        user = super().save_user(request, sociallogin, form)
        
        # 2. 네이버에서 넘겨준 상세 데이터(extra_data) 가져오기
        extra_data = sociallogin.account.extra_data
        
        if sociallogin.account.provider == 'naver':
            # 네이버 API 응답 구조에 맞춰 매핑
            user.real_name = extra_data.get('name')          # 회원이름
            user.nickname = extra_data.get('nickname')       # 별명
            user.email = extra_data.get('email')             # 이메일 주소
            user.phone_number = extra_data.get('mobile')     # 휴대전화번호
            user.birthday = extra_data.get('birthday')       # 생일
            user.birthyear = extra_data.get('birthyear')     # 출생연도
            
            user.save()
        return user