"""Compatibility alias for the maintained professional template catalogue."""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load the maintained 21-template professional portfolio catalogue"

    def handle(self, *args, **options):
        self.stdout.write("Loading the maintained professional template catalogue…")
        call_command("load_templates", stdout=self.stdout, stderr=self.stderr)
