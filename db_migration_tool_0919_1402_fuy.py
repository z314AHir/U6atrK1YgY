# 代码生成时间: 2025-09-19 14:02:25
import os
from django.core.management import call_command
from django.core.management.base import BaseCommand

"""
A Django management command for performing database migrations.
This tool wraps Django's built-in `migrate` command,
providing a simple interface for executing migrations in a Django project.
"""

class Command(BaseCommand):
    help = "Perform database migrations"
    
    def add_arguments(self, parser):
        parser.add_argument("--migrate", action="store_true", help="Perform migration")
        parser.add_argument("--rollback", action="store_true", help="Rollback last migration")
        parser.add_argument("--fake", action="store_true", help="Fake migration")
        parser.add_argument("--name", type=str, help="Specify the name of the migration to apply or rollback")
    
    def handle(self, *args, **options):
        # Check if we are in a Django project
        if not os.path.exists("manage.py"):
            self.stderr.write("Error: This script must be run from the root of a Django project")
            return

        # Perform migration
        if options["--migrate"]:
            try:
                if options["--name"]:
                    # Apply a specific migration
                    call_command("migrate", options["--name"], migration_name=options["--name"])
                else:
                    # Apply all pending migrations
                    call_command("migrate")
            except Exception as e:
                self.stderr.write(f"Error: {e}")

        # Rollback last migration
        elif options["--rollback"]:
            try:
                self.stdout.write("Rolling back last migration...")
                call_command("migrate", "zero")
            except Exception as e:
                self.stderr.write(f"Error: {e}")

        # Fake migration
        elif options["--fake"]:
            try:
                if options["--name"]:
                    # Fake a specific migration
                    call_command("migrate", options["--name"], fake=True)
                else:
                    # Fake all pending migrations
                    call_command("migrate", fake=True)
            except Exception as e:
                self.stderr.write(f"Error: {e}")

        else:
            # Show help message if no options are provided
            self.stdout.write("Usage: python manage.py db_migration_tool --migrate|--rollback|--fake|--name")
