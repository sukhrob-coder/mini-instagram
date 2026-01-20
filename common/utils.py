from rest_framework_simplejwt.tokens import AccessToken


def get_verification_token(user):
    token = AccessToken.for_user(user)
    token["type"] = "email_verification"
    return str(token)
