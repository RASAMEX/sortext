from django.apps import AppConfig

class RafflesConfig(AppConfig):
    """
    RafflesConfig

    This class represents the configuration of the Raffles application in Django.

    Attributes:
        default_auto_field (str): The default auto field for models in the application.
        name (str): The name of the application.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'raffles'
