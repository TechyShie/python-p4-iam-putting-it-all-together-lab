from app import app
from models import db, User, Recipe


def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create users with ALL required fields
        users = [
            User(
                username='chef_john',
                image_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
                bio='Professional chef with 10 years of experience in French and Italian cuisine.'
            ),
            User(
                username='baking_betty',
                image_url='https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150',
                bio='Home baker and dessert enthusiast specializing in cakes and pastries.'
            ),
            User(
                username='healthy_harry',
                image_url='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150',
                bio='Certified nutritionist and healthy cooking advocate focused on plant-based recipes.'
            )
        ]

        # Set passwords for all users
        for user in users:
            user.password_hash = 'password123'

        db.session.add_all(users)
        db.session.commit()

        # Create recipes with proper data
        recipes = [
            Recipe(
                title='Classic Chocolate Chip Cookies',
                instructions='''Preheat oven to 375°F (190°C). In a medium bowl, whisk together 2 1/4 cups flour, 1 tsp baking soda, and 1 tsp salt.
                In a large bowl, beat 1 cup softened butter, 3/4 cup granulated sugar, 3/4 cup brown sugar, and 1 tsp vanilla until creamy.
                Add 2 large eggs one at a time, beating well after each addition. Gradually beat in flour mixture. Stir in 2 cups chocolate chips.
                Drop by rounded tablespoon onto ungreased baking sheets. Bake for 9 to 11 minutes or until golden brown.
                Cool on baking sheets for 2 minutes; remove to wire racks to cool completely.''',
                minutes_to_complete=30,
                user_id=users[1].id),
            Recipe(
                title='Vegetable Stir Fry',
                instructions='''Heat 2 tbsp oil in a large wok or skillet over high heat. Add 2 cloves minced garlic and 1 tbsp grated ginger, stir for 30 seconds.
                Add 2 cups broccoli florets, 1 sliced bell pepper, and 1 cup sliced carrots, stir-fry for 4-5 minutes until vegetables are tender-crisp.
                Add 3 tbsp soy sauce, 1 tbsp sesame oil, and 1 tsp sugar. Stir well to combine. Add 1 cup snow peas and cook for another 2 minutes.
                Serve immediately over rice or noodles. Garnish with sesame seeds and sliced green onions.''',
                minutes_to_complete=20,
                user_id=users[2].id),
            Recipe(
                title='Homemade Pizza Dough',
                instructions='''In a large bowl, combine 1 1/2 cups warm water, 2 1/4 tsp active dry yeast, and 1 tsp sugar. Let sit for 5 minutes until foamy.
                Add 4 cups all-purpose flour, 1 1/2 tsp salt, and 2 tbsp olive oil. Mix until a dough forms.
                Knead on a floured surface for 8-10 minutes until smooth and elastic. Place in a greased bowl, cover, and let rise in a warm place for 1-2 hours until doubled in size.
                Punch down dough and roll out to desired thickness. Add your favorite toppings and bake at 475°F (245°C) for 12-15 minutes until crust is golden.''',
                minutes_to_complete=90,
                user_id=users[0].id),
            Recipe(
                title='Creamy Tomato Soup',
                instructions='''Heat 2 tbsp olive oil in a large pot over medium heat. Add 1 chopped onion and 2 minced garlic cloves, cook until soft.
                Add 2 cans (28 oz each) crushed tomatoes, 4 cups vegetable broth, 1/2 cup heavy cream, and 1 tbsp sugar.
                Bring to a boil, then reduce heat and simmer for 20 minutes. Use an immersion blender to puree until smooth.
                Season with salt and pepper to taste. Serve hot with grilled cheese sandwiches for dipping.''',
                minutes_to_complete=35,
                user_id=users[0].id),
            Recipe(
                title='Banana Bread',
                instructions='''Preheat oven to 350°F (175°C). Grease a 9x5 inch loaf pan. In a large bowl, mash 3 ripe bananas.
                Mix in 1/3 cup melted butter, 3/4 cup sugar, 1 beaten egg, and 1 tsp vanilla. In another bowl, whisk together 1 1/2 cups flour,
                1 tsp baking soda, and 1/4 tsp salt. Stir flour mixture into banana mixture until just combined.
                Pour batter into prepared loaf pan. Bake for 60-65 minutes until a toothpick inserted comes out clean.
                Cool in pan for 10 minutes, then remove to wire rack to cool completely.''',
                minutes_to_complete=75,
                user_id=users[1].id)]

        db.session.add_all(recipes)
        db.session.commit()

        print("✅ Database seeded successfully!")
        print(f"   Created {len(users)} users")
        print(f"   Created {len(recipes)} recipes")

        # Verify data
        user_count = User.query.count()
        recipe_count = Recipe.query.count()
        print(
            f"   Verification: {user_count} users, {recipe_count} recipes in database")


if __name__ == '__main__':
    seed_data()
