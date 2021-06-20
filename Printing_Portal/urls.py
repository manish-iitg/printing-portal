# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <UrlConfSnippet>
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('printing_portal/', include('authentication.urls')),
    path('printing_portal/', include('order.urls')),
    path('printing_portal/', include('payment.urls')),
    path('printing_portal/admin/', admin.site.urls),
]
# </UrlConfSnippet>

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)