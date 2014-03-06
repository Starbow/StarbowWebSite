from django.conf import settings


def starbowmodweb(request):
    return dict(
        ABOUT_PAGES=settings.ABOUT_PAGES
    )
