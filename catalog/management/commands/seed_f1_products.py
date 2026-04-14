from decimal import Decimal
from urllib.parse import quote

from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Seed 45 F1 categories and products with images"

    def handle(self, *args, **kwargs):
        categories = self.create_categories()
        products = self.create_products(categories)
        self.stdout.write(self.style.SUCCESS(f"F1 categories and {len(products)} products seeded successfully."))

    def upsert_category(self, name, slug, parent=None):
        category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "parent": parent})
        category.name = name
        category.parent = parent
        category.save()
        return category

    def make_product_image(self, text, bg="7f1d1d", fg="ffffff"):
      return f"https://placehold.co/1200x900/{bg}/{fg}?text={quote(text)}"

    def build_product(
        self,
        category,
        name,
        slug,
        description,
        brand,
        color,
        size,
        price,
        stock,
        is_premium_only,
        image_bg="7f1d1d"
    ):
        return {
            "category": category,
            "name": name,
            "slug": slug,
            "description": description,
            "brand": brand,
            "color": color,
            "size": size,
            "price": Decimal(price),
            "stock": stock,
            "is_premium_only": is_premium_only,
            "external_image_url": self.make_product_image(name, image_bg),
        }

    def create_categories(self):
        clothing = self.upsert_category("Clothing", "clothing")
        accessories = self.upsert_category("Accessories", "accessories")
        collectibles = self.upsert_category("Collectibles", "collectibles")
        experiences = self.upsert_category("Experiences", "experiences")

        caps = self.upsert_category("Caps", "caps", accessories)
        mugs = self.upsert_category("Mugs", "mugs", accessories)
        flags = self.upsert_category("Flags", "flags", accessories)
        backpacks = self.upsert_category("Backpacks", "backpacks", accessories)

        jerseys = self.upsert_category("Jerseys", "jerseys", clothing)
        hoodies = self.upsert_category("Hoodies", "hoodies", clothing)
        jackets = self.upsert_category("Jackets", "jackets", clothing)

        model_cars = self.upsert_category("Model Cars", "model-cars", collectibles)
        posters = self.upsert_category("Posters", "posters", collectibles)
        helmets = self.upsert_category("Helmet Replicas", "helmet-replicas", collectibles)

        tickets = self.upsert_category("Tickets", "tickets", experiences)
        regular_tickets = self.upsert_category("Regular Tickets", "regular-tickets", tickets)
        premium_tickets = self.upsert_category("Premium Tickets", "premium-tickets", tickets)
        exclusive_tickets = self.upsert_category("Exclusive Tickets", "exclusive-tickets", tickets)

        return {
            "accessories": accessories,
            "caps": caps,
            "mugs": mugs,
            "flags": flags,
            "backpacks": backpacks,
            "clothing": clothing,
            "jerseys": jerseys,
            "hoodies": hoodies,
            "jackets": jackets,
            "collectibles": collectibles,
            "model_cars": model_cars,
            "posters": posters,
            "helmets": helmets,
            "experiences": experiences,
            "tickets": tickets,
            "regular_tickets": regular_tickets,
            "premium_tickets": premium_tickets,
            "exclusive_tickets": exclusive_tickets,
        }

    def create_products(self, c):
        p = self.build_product

        products = [
            # Caps (5)
            p(c["caps"], "Ferrari Team Cap", "ferrari-team-cap",
              "Classic Ferrari Formula 1 fan cap with embroidered logo.",
              "Ferrari", "Red", "One Size", "34.99", 25, False, "b91c1c"),

            p(c["caps"], "Mercedes AMG Team Cap", "mercedes-amg-team-cap",
              "Mercedes AMG Petronas cap for race weekend styling.",
              "Mercedes", "Black", "One Size", "36.99", 20, False, "111827"),

            p(c["caps"], "Red Bull Racing Cap", "red-bull-racing-cap",
              "Official-style Red Bull Racing fan cap.",
              "Red Bull", "Navy", "One Size", "35.50", 22, False, "1e3a8a"),

            p(c["caps"], "Lewis Hamilton Collector Cap", "lewis-hamilton-collector-cap",
              "Collector cap inspired by championship-winning race style.",
              "Mercedes", "Black", "One Size", "39.99", 12, False, "0f172a"),

            p(c["caps"], "Max Verstappen Fan Cap", "max-verstappen-fan-cap",
              "Fan cap inspired by Red Bull title-winning weekends.",
              "Red Bull", "Navy", "One Size", "38.99", 15, False, "1d4ed8"),

            # Jerseys (4)
            p(c["jerseys"], "McLaren Team Jersey", "mclaren-team-jersey",
              "Lightweight McLaren team jersey for everyday fan wear.",
              "McLaren", "Orange", "M", "79.99", 15, False, "ea580c"),

            p(c["jerseys"], "Ferrari Fan Jersey", "ferrari-fan-jersey",
              "Ferrari supporter jersey inspired by the paddock look.",
              "Ferrari", "Red", "L", "82.99", 18, False, "dc2626"),

            p(c["jerseys"], "Mercedes Team Jersey", "mercedes-team-jersey",
              "Mercedes fan jersey for race weekends and events.",
              "Mercedes", "Black", "M", "81.99", 16, False, "1f2937"),

            p(c["jerseys"], "Red Bull Driver Jersey", "red-bull-driver-jersey",
              "Red Bull Racing jersey inspired by current driver kits.",
              "Red Bull", "Navy", "L", "83.99", 14, False, "1e40af"),

            # Hoodies (4)
            p(c["hoodies"], "Mercedes Performance Hoodie", "mercedes-performance-hoodie",
              "Warm Mercedes hoodie with motorsport-inspired design.",
              "Mercedes", "Black", "L", "94.99", 12, False, "111827"),

            p(c["hoodies"], "Red Bull Pit Lane Hoodie", "red-bull-pit-lane-hoodie",
              "Pit-lane inspired hoodie for Red Bull Racing fans.",
              "Red Bull", "Navy", "M", "96.50", 10, True, "1d4ed8"),

            p(c["hoodies"], "Lando Norris Fan Hoodie", "lando-norris-fan-hoodie",
              "McLaren-inspired hoodie for fans of modern race weekends.",
              "McLaren", "Orange", "M", "89.99", 11, False, "f97316"),

            p(c["hoodies"], "Ferrari Scuderia Hoodie", "ferrari-scuderia-hoodie",
              "Ferrari hoodie for cold race nights and casual wear.",
              "Ferrari", "Red", "L", "92.99", 13, False, "b91c1c"),

            # Jackets (4)
            p(c["jackets"], "Red Bull Racing Jacket", "red-bull-racing-jacket",
              "Race-inspired Red Bull jacket for cooler track weekends.",
              "Red Bull", "Navy", "L", "119.99", 10, True, "2563eb"),

            p(c["jackets"], "Ferrari Trackside Jacket", "ferrari-trackside-jacket",
              "Trackside-style Ferrari jacket for premium fan wear.",
              "Ferrari", "Red", "L", "124.99", 9, True, "dc2626"),

            p(c["jackets"], "Mercedes Paddock Jacket", "mercedes-paddock-jacket",
              "Mercedes paddock-inspired jacket with premium styling.",
              "Mercedes", "Black", "M", "126.99", 8, True, "111827"),

            p(c["jackets"], "McLaren Rain Jacket", "mclaren-rain-jacket",
              "McLaren weather-ready race weekend jacket.",
              "McLaren", "Orange", "M", "114.99", 10, False, "ea580c"),

            # Mugs (4)
            p(c["mugs"], "Ferrari Ceramic Mug", "ferrari-ceramic-mug",
              "Ferrari mug for coffee before every race session.",
              "Ferrari", "Red", "Standard", "18.99", 30, False, "ef4444"),

            p(c["mugs"], "McLaren Racing Mug", "mclaren-racing-mug",
              "McLaren branded mug for F1 fans.",
              "McLaren", "Orange", "Standard", "17.99", 26, False, "fb923c"),

            p(c["mugs"], "Mercedes Garage Mug", "mercedes-garage-mug",
              "Mercedes mug inspired by the team garage.",
              "Mercedes", "Black", "Standard", "18.49", 24, False, "1f2937"),

            p(c["mugs"], "Red Bull Energy Mug", "red-bull-energy-mug",
              "Bold Red Bull mug for morning race briefings.",
              "Red Bull", "Navy", "Standard", "18.79", 22, False, "1d4ed8"),

            # Flags (3)
            p(c["flags"], "Ferrari Supporter Flag", "ferrari-supporter-flag",
              "Large Ferrari supporter flag for race weekends and room decoration.",
              "Ferrari", "Red", "Large", "22.99", 25, False, "dc2626"),

            p(c["flags"], "Mercedes Fan Flag", "mercedes-fan-flag",
              "Mercedes team supporter flag for home or race-day display.",
              "Mercedes", "Black", "Large", "23.99", 20, False, "111827"),

            p(c["flags"], "Red Bull Champion Flag", "red-bull-champion-flag",
              "Red Bull supporter flag for title celebrations and events.",
              "Red Bull", "Navy", "Large", "24.99", 18, False, "1e40af"),

            # Backpacks (3)
            p(c["backpacks"], "Mercedes Team Backpack", "mercedes-team-backpack",
              "Mercedes backpack for travel, university, or race days.",
              "Mercedes", "Black", "Standard", "72.99", 14, False, "111827"),

            p(c["backpacks"], "McLaren Team Backpack", "mclaren-team-backpack",
              "McLaren-themed backpack for school, work, or race-day travel.",
              "McLaren", "Orange", "Standard", "69.99", 14, False, "f97316"),

            p(c["backpacks"], "Ferrari Travel Backpack", "ferrari-travel-backpack",
              "Ferrari backpack for fans who travel light to race weekends.",
              "Ferrari", "Red", "Standard", "74.99", 12, True, "dc2626"),

            # Posters (4)
            p(c["posters"], "Ferrari Driver Poster", "ferrari-driver-poster",
              "Ferrari-themed wall poster for Formula 1 fans.",
              "Ferrari", "Red", "A2", "21.99", 18, False, "b91c1c"),

            p(c["posters"], "Mercedes Garage Poster", "mercedes-garage-poster",
              "Mercedes-themed Formula 1 garage poster for wall display.",
              "Mercedes", "Black", "A2", "19.99", 18, False, "1f2937"),

            p(c["posters"], "Monaco Grand Prix Poster", "monaco-grand-prix-poster",
              "Decorative Monaco Grand Prix wall poster for motorsport fans.",
              "F1", "Blue", "A2", "21.99", 20, False, "2563eb"),

            p(c["posters"], "McLaren Victory Poster", "mclaren-victory-poster",
              "McLaren racing poster inspired by podium moments.",
              "McLaren", "Orange", "A2", "20.99", 19, False, "ea580c"),

            # Model cars (4)
            p(c["model_cars"], "1:43 Ferrari SF Model Car", "1-43-ferrari-sf-model-car",
              "Detailed Ferrari Formula 1 scale model collectible.",
              "Ferrari", "Red", "1:43", "64.99", 8, False, "dc2626"),

            p(c["model_cars"], "1:43 Mercedes W Model Car", "1-43-mercedes-w-model-car",
              "Detailed Mercedes Formula 1 scale model collectible.",
              "Mercedes", "Silver", "1:43", "66.99", 9, False, "475569"),

            p(c["model_cars"], "1:43 Red Bull RB Model Car", "1-43-red-bull-rb-model-car",
              "Collectible Red Bull Racing scale model car.",
              "Red Bull", "Navy", "1:43", "68.99", 7, True, "1d4ed8"),

            p(c["model_cars"], "1:43 McLaren MCL Model Car", "1-43-mclaren-mcl-model-car",
              "McLaren scale model collectible for display shelves.",
              "McLaren", "Orange", "1:43", "67.99", 8, False, "f97316"),

            # Helmet replicas (3)
            p(c["helmets"], "Charles Leclerc Helmet Replica", "charles-leclerc-helmet-replica",
              "Collectible helmet replica inspired by Ferrari driver styling.",
              "Ferrari", "Red", "Collectible", "149.99", 6, True, "dc2626"),

            p(c["helmets"], "Lewis Hamilton Helmet Replica", "lewis-hamilton-helmet-replica",
              "Collectible helmet replica inspired by Mercedes champion styling.",
              "Mercedes", "Black", "Collectible", "152.99", 5, True, "111827"),

            p(c["helmets"], "Max Verstappen Helmet Replica", "max-verstappen-helmet-replica",
              "Collectible helmet replica inspired by Red Bull title-winning style.",
              "Red Bull", "Navy", "Collectible", "151.99", 5, True, "1e40af"),

            # Accessories root (2)
            p(c["accessories"], "Ferrari Lanyard", "ferrari-lanyard",
              "Ferrari branded lanyard for keys or passes.",
              "Ferrari", "Red", "One Size", "12.99", 40, False, "dc2626"),

            p(c["accessories"], "McLaren Keyring", "mclaren-keyring",
              "Compact McLaren keyring with racing style.",
              "McLaren", "Orange", "One Size", "9.99", 50, False, "f97316"),

            # Regular tickets (2)
            p(c["regular_tickets"], "Silverstone Regular Weekend Pass", "silverstone-regular-weekend-pass",
              "Regular grandstand access for the Silverstone Formula 1 weekend.",
              "F1 Experiences", "Blue", "Weekend", "189.99", 10, False, "2563eb"),

            p(c["regular_tickets"], "Italian Grand Prix Grandstand Ticket", "italian-grand-prix-grandstand-ticket",
              "Regular Monza grandstand ticket package for Formula 1 fans.",
              "F1 Experiences", "Green", "Weekend", "199.99", 10, False, "15803d"),

            # Premium tickets (2)
            p(c["premium_tickets"], "Monaco Premium Hospitality Pass", "monaco-premium-hospitality-pass",
              "Premium Monaco race-weekend ticket with hospitality access.",
              "F1 Experiences", "Gold", "Package", "349.99", 6, True, "a16207"),

            p(c["premium_tickets"], "Abu Dhabi Premium Lounge Pass", "abu-dhabi-premium-lounge-pass",
              "Premium lounge ticket package for the Abu Dhabi finale.",
              "F1 Experiences", "Gold", "Package", "359.99", 6, True, "92400e"),

            # Exclusive tickets (1)
            p(c["exclusive_tickets"], "Monaco Paddock Club Exclusive", "monaco-paddock-club-exclusive",
              "Exclusive paddock club experience with premium race access.",
              "F1 Experiences", "Black", "Exclusive", "899.99", 3, True, "111111"),
        ]

        for item in products:
            Product.objects.update_or_create(
                slug=item["slug"],
                defaults=item
            )

        return products