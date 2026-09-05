import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_sys.settings')
django.setup()

from api.models import Restaurant, Category, MenuItem
from django.contrib.auth.models import User

def seed_db():
    print("Seeding database...")
    
    # Categories
    categories = ['Pizza', 'Burgers', 'Sushi', 'Desserts', 'Salads', 'Indian', 'Healthy', 'Beverages']
    category_objs = []
    for cat_name in categories:
        cat, _ = Category.objects.get_or_create(name=cat_name)
        category_objs.append(cat)
    
    # Restaurants & Home Chefs
    restaurants = [
        ("Pizza Palace", "Bistupur, Jamshedpur", 4.5, False),
        ("Burger King", "Sakchi, Jamshedpur", 4.2, False),
        ("Sushi Express", "Adityapur", 4.8, False),
        ("Auntie's Kitchen", "Bistupur", 4.9, True),
        ("Home Delights", "Sonari", 4.7, True),
        ("Healthy Bites", "Kadma", 4.3, False),
    ]
    
    restaurant_objs = []
    for name, loc, rat, is_home in restaurants:
        res, _ = Restaurant.objects.get_or_create(
            name=name, 
            location=loc, 
            defaults={'rating': rat, 'is_home_chef': is_home}
        )
        restaurant_objs.append(res)
        
    # Menu Items
    menu_items = [
        ("Margherita Pizza", "Classic tomato and mozzarella", 299, "Pizza", "Pizza Palace"),
        ("Pepperoni Feast", "Lots of pepperoni and cheese", 399, "Pizza", "Pizza Palace"),
        ("Veggie Supreme", "Fresh vegetables and olives", 349, "Pizza", "Pizza Palace"),
        ("Whopper Burger", "Flame-grilled beef patty", 199, "Burgers", "Burger King"),
        ("Chicken Zinger", "Crispy chicken fillet", 149, "Burgers", "Burger King"),
        ("California Roll", "Crab, avocado, and cucumber", 450, "Sushi", "Sushi Express"),
        ("Salmon Nigiri", "Fresh salmon over rice", 550, "Sushi", "Sushi Express"),
        ("Homemade Lasagna", "Traditional beef lasagna", 350, "Indian", "Auntie's Kitchen"),
        ("Quinoa Salad", "Healthy quinoa with vegetables", 250, "Healthy", "Healthy Bites"),
        ("Keto Chicken Bowl", "Low carb chicken and greens", 320, "Healthy", "Healthy Bites"),
        ("Vegan Buddha Bowl", "Chickpeas, kale, and tahini", 280, "Healthy", "Healthy Bites"),
        ("Grandma's Pickles", "Traditional homemade mango pickle", 120, "Indian", "Home Delights"),
    ]
    
    for name, desc, price, cat_name, res_name in menu_items:
        cat = Category.objects.get(name=cat_name)
        res = Restaurant.objects.get(name=res_name)
        
        item, created = MenuItem.objects.get_or_create(
            name=name,
            restaurant=res,
            defaults={
                'description': desc,
                'price': Decimal(price),
                'category': cat,
                'stock': random.randint(5, 50),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'calories': random.randint(200, 800),
                'protein': random.randint(10, 40),
                'carbs': random.randint(20, 100),
                'fat': random.randint(5, 30),
                'is_vegan': 'Vegan' in name or 'Veggie' in name,
                'is_keto': 'Keto' in name,
                'is_near_expiry': random.random() < 0.2
            }
        )
        if created:
            print(f"Created item: {name}")

    # Update Grandma's Pickles to match exact specifications
    print("Updating Grandma's Pickles...")
    try:
        pickles = MenuItem.objects.get(name="Grandma's Pickles")
        pickles.price = Decimal("120.00")
        pickles.stock = 33
        pickles.calories = 670
        pickles.protein = 31.0
        pickles.carbs = 95.0
        pickles.fat = 21.0
        pickles.image_url = 'images/pickle.png'
        pickles.save()
        print("Updated Grandma's Pickles")
    except MenuItem.DoesNotExist:
        pass

    # Create a test user
    if not User.objects.filter(username='pavan').exists():
        User.objects.create_user('pavan', 'pavan@example.com', 'pavan123')
        print("Created test user: pavan")

    print("Success!")

if __name__ == "__main__":
    seed_db()
