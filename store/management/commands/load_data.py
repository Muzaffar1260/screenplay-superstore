import csv
import os
from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Load movie data into Product model'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(base_dir))
        csv_path = os.path.join(project_root, 'movies_2009_2024_clean.csv')
        print(f"Looking for CSV at: {csv_path}")

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Skip rows where Gross is empty
                if not row['Gross'] or row['Gross'].strip() == '':
                    print(f"Skipping row with empty Gross: {row['Title']}")
                    continue

                # Normalize Year: Convert to integer to remove ".0"
                year = str(int(float(row['Year'])))  # e.g., "2009.0" -> "2009"
                category, _ = Category.objects.get_or_create(name=year)

                gross = float(row['Gross'])
                price = round(gross / 1_000_000, 2)
                description = f"Experience the magic of {row['Title']}!"

                # Optional: Check for existing Product to avoid duplicates
                if not Product.objects.filter(name=row['Title'], category=category).exists():
                    Product.objects.create(
                        name=row['Title'],
                        description=description,
                        price=price,
                        category=category,
                        location="Hollywood"
                    )
                else:
                    print(f"Skipping duplicate product: {row['Title']} ({year})")

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))