from django.apps import AppConfig


class BooksApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books_api'

    def ready(self):
        import books_api.signals