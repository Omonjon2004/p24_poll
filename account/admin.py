from django.contrib import admin

from account.models import Account, Interest

admin.site.register([Interest, Account])
