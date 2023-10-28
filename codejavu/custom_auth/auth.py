from rest_framework_simplejwt.tokens import RefreshToken


def generate_access_token(user):
    refresh = generate_refresh_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_refresh_token(user):
    refresh_token = RefreshToken.for_user(user)
    return refresh_token
