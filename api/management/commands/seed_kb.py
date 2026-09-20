from django.core.management.base import BaseCommand
from api.models import KBEntry


class Command(BaseCommand):
    help = 'Seed the database with initial Knowledge Base (KB) entries'

    def handle(self, *args, **options):
        entries = [
            {
                "question": "What is select_related in Django ORM?",
                "answer": "select_related performs a SQL JOIN and fetches related single-valued relationships (ForeignKey, OneToOneField) in a single query.",
                "category": KBEntry.Category.DATABASE,
            },
            {
                "question": "How to use select_related for query optimization?",
                "answer": "You can use select_related when accessing foreign keys or one-to-one models to avoid N+1 query problems by joining tables.",
                "category": KBEntry.Category.DATABASE,
            },
            {
                "question": "How does transaction.atomic() work in Django?",
                "answer": "transaction.atomic() creates a database transaction block ensuring that all database operations inside succeed together or rollback completely.",
                "category": KBEntry.Category.DATABASE,
            },
            {
                "question": "What is a JWT token and how is it used in REST APIs?",
                "answer": "JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties in API authentication.",
                "category": KBEntry.Category.API,
            },
            {
                "question": "How to implement JWT authentication in Django REST Framework?",
                "answer": "You can use djangorestframework-simplejwt package and configure DEFAULT_AUTHENTICATION_CLASSES in settings.py.",
                "category": KBEntry.Category.API,
            },
            {
                "question": "When should I use Q objects in Django queries?",
                "answer": "Q objects allow complex database queries using OR (|), AND (&), and NOT (~) operators across multiple fields.",
                "category": KBEntry.Category.DATABASE,
            },
            {
                "question": "How do signals work in Django?",
                "answer": "Django signals allow decoupled applications to get notified when actions occur elsewhere in the framework, such as post_save on models.",
                "category": KBEntry.Category.FRAMEWORK,
            },
            {
                "question": "What is cloud deployment strategy for Django applications?",
                "answer": "Deploying Django on cloud infrastructure involves containerization with Docker, managed PostgreSQL databases, and reverse proxies like Nginx.",
                "category": KBEntry.Category.CLOUD,
            },
            {
                "question": "How to manage environment variables securely?",
                "answer": "Store sensitive credentials in a .env file and read them using python-dotenv or decouple, never hardcoding them in settings.py.",
                "category": KBEntry.Category.GENERAL,
            },
            {
                "question": "What are Django REST Framework permissions and authentication?",
                "answer": "Permissions determine whether a request should be granted or denied based on user roles and authentication state.",
                "category": KBEntry.Category.FRAMEWORK,
            },

            {
                "question": "How to use prefetch_related vs select_related?",
                "answer": "select_related is used for single-valued relationships via JOINs, whereas prefetch_related is used for multi-valued relationships (ManyToManyField, reverse ForeignKey) using separate queries.",
                "category": KBEntry.Category.DATABASE,
            },
            {
                "question": "What is Docker containerization for Python web apps?",
                "answer": "Docker package applications and dependencies into standardized containers for development, staging, and cloud infrastructure.",
                "category": KBEntry.Category.CLOUD,
            }
        ]

        created_count = 0
        for entry in entries:
            obj, created = KBEntry.objects.get_or_create(
                question=entry["question"],
                defaults={
                    "answer": entry["answer"],
                    "category": entry["category"]
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {created_count} new KB entries (Total in DB: {KBEntry.objects.count()}).')
        )
