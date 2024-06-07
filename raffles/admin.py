from django.contrib import admin
from .models import *

admin.site.register(Raffle)
admin.site.register(Participant)

"""
Admin Registration

This module registers models in the Django admin panel.

- Raffle: Represents a raffle model.
- Participant: Represents a participant model.

Registering models in the admin panel allows administrators to manage them through the Django admin interface, facilitating tasks such as adding, editing, and deleting records.

For more information, see the Django documentation: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
"""