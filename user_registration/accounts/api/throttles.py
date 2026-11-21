from rest_framework.throttling import AnonRateThrottle


class SignupRateThrottle(AnonRateThrottle):
    scope = "signup"
