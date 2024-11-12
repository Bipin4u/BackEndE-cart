from django.core.management.base import BaseCommand
from .e_cart.models import Item
import random

class Command(BaseCommand):
    help = 'Populate the Item model with 20 sample items for each type'

    def handle(self, *args, **kwargs):
        # Define item types and sample descriptions
        TYPE_CHOICES = [
            'sofa', 'recliner', 'dining', 'bed', 
            'office_study_table', 'chair', 'center_table'
        ]

        descriptions = {
            'sofa': 'A comfortable and stylish sofa',
            'recliner': 'A relaxing recliner for comfort',
            'dining': 'A classic dining set',
            'bed': 'A cozy and spacious bed',
            'office_study_table': 'Perfect table for study or office work',
            'chair': 'An ergonomic chair',
            'center_table': 'A beautiful center table',
        }

        materials = ['Leather', 'Wood', 'Fabric', 'Metal', 'Plastic']

        # Generating 20 items for each type
        for item_type in TYPE_CHOICES:
            for i in range(1, 21):
                Item.objects.create(
                    name=f"{item_type}_{i}",
                    type=item_type,
                    price=random.randint(5000, 50000),
                    description=descriptions[item_type],
                    features=[f"{item_type}_feature_{j}" for j in range(1, 4)],
                    rating=round(random.uniform(1.0, 5.0), 1),
                    reviews_count=random.randint(0, 100),
                    discount=round(random.uniform(0.0, 10.0), 2),
                    dimensions=f"{random.randint(2, 7)}x{random.randint(2, 7)} ft",
                    warranty=f"{random.randint(1, 10)} years",
                    package_details=f"{random.randint(1, 3)} package(s)",
                    material=random.choice(materials)
                )

        self.stdout.write(self.style.SUCCESS("20 items for each type have been successfully created!"))
