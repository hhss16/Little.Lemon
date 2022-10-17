from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class TenCallsPerMinute(UserRateThrottle):
    scope = 'ten'


class GetAnononymousRateThrottle(AnonRateThrottle):
    scope = 'get_anon'

    def allow_request(self, request, view):
        if request.method == "POST":
            return True
        return super().allow_request(request, view)


class FivePerMinuteThrottle(AnonRateThrottle):
    # scope = 'get_five'
    def parse_rate(self, rate):
        return (5, 60)
