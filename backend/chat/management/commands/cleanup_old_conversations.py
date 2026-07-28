from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from chat.models import Conversation


class Command(BaseCommand):
    help = "Permanently delete conversations that were soft-deleted before the retention cutoff."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Retention period in days for soft-deleted conversations (default: 30).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report how many conversations would be deleted without deleting them.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        if days < 0:
            raise CommandError("--days must be zero or greater.")

        cutoff = timezone.now() - timedelta(days=days)
        queryset = Conversation.objects.filter(deleted_at__isnull=False, deleted_at__lt=cutoff)
        count = queryset.count()

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(f"{count} conversation(s) would be permanently deleted."))
            return

        queryset.delete()
        self.stdout.write(self.style.SUCCESS(f"Permanently deleted {count} conversation(s)."))


def run_cleanup():
    """Entry point used by django-crontab for the daily retention job."""
    Command().handle(days=30, dry_run=False)
