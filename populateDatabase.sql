-- Copy and paste this into same directory as createDatabase.sql, connect to mysql, run commands below in order to populate the database with the data
-- FOLLOW createDatabase.sql COMMANDS FIRST
-- USE healthApp; (if youre not already using the db)
--  source ./populateData.sql

-- Sample Employee Table
INSERT INTO Employee (Employee_ID, EName)
VALUES 
  (1, 'John Doe'),
  (2, 'Jane Smith'),
  (3, 'Michael Brown'),
  (4, 'Emily Davis'),
  (5, 'William Johnson'),
  (6, 'Olivia Miller'),
  (7, 'James Wilson'),
  (8, 'Sophia Taylor'),
  (9, 'Benjamin Anderson'),
  (10, 'Ava Thomas'),
  (11, 'Lucas Jackson'),
  (12, 'Mia White'),
  (13, 'Henry Harris'),
  (14, 'Charlotte Martin'),
  (15, 'Alexander Thompson'),
  (16, 'Amelia Garcia'),
  (17, 'Daniel Martinez'),
  (18, 'Harper Robinson'),
  (19, 'Matthew Clark'),
  (20, 'Evelyn Rodriguez');

-- Sample Customers Table
INSERT INTO Customers (Customer_ID, CName, Dietary_Preference, Contact_Info, Payment_Info, Expenses, Nutritional_Info)
VALUES 
  (1, 'Alice Smith', 'Vegan', 'alice@example.com', 'Visa 1234', 100.00, 'Low Calorie'),
  (2, 'Bob Johnson', 'Gluten-Free', 'bob@example.com', 'Mastercard 5678', 50.00, 'High Fiber'),
  (3, 'Charlie Brown', 'Vegetarian', 'charlie@example.com', 'Amex 9012', 75.00, 'Low Fat'),
  (4, 'Diana Prince', 'None', 'diana@example.com', 'Discover 3456', 60.00, 'High Protein'),
  (5, 'Ethan Hunt', 'Keto', 'ethan@example.com', 'Visa 7890', 120.00, 'Low Carb'),
  (6, 'Fiona Gallagher', 'Vegan', 'fiona@example.com', 'Mastercard 1122', 80.00, 'High Fiber'),
  (7, 'George Michael', 'Vegetarian', 'george@example.com', 'Amex 3344', 90.00, 'Low Sugar'),
  (8, 'Hannah Baker', 'Gluten-Free', 'hannah@example.com', 'Discover 5566', 65.00, 'Rich in Vitamins'),
  (9, 'Ian Somerhalder', 'None', 'ian@example.com', 'Visa 7788', 110.00, 'Balanced'),
  (10, 'Julia Roberts', 'Keto', 'julia@example.com', 'Mastercard 9900', 95.00, 'Low Carb'),
  (11, 'Kevin Hart', 'Vegan', 'kevin@example.com', 'Amex 1235', 85.00, 'High Protein'),
  (12, 'Laura Palmer', 'Vegetarian', 'laura@example.com', 'Discover 6789', 70.00, 'Low Calorie'),
  (13, 'Michael Scott', 'None', 'michael@example.com', 'Visa 2468', 105.00, 'High Fiber'),
  (14, 'Nina Dobrev', 'Gluten-Free', 'nina@example.com', 'Mastercard 1357', 55.00, 'Rich in Iron'),
  (15, 'Oscar Wilde', 'Keto', 'oscar@example.com', 'Amex 8642', 115.00, 'Low Carb'),
  (16, 'Pam Beesly', 'Vegan', 'pam@example.com', 'Discover 9753', 60.00, 'Low Fat'),
  (17, 'Quentin Tarantino', 'Vegetarian', 'quentin@example.com', 'Visa 3579', 130.00, 'High Protein'),
  (18, 'Rachel Green', 'None', 'rachel@example.com', 'Mastercard 4680', 80.00, 'Low Sugar'),
  (19, 'Steve Rogers', 'Gluten-Free', 'steve@example.com', 'Amex 1597', 100.00, 'Rich in Vitamins'),
  (20, 'Tina Fey', 'Keto', 'tina@example.com', 'Discover 7531', 90.00, 'Low Carb');

-- Sample GroceryStore Table
INSERT INTO GroceryStore (Retailer_ID, GLocation)
VALUES 
  (1, 'Downtown Market'),
  (2, 'Uptown Grocers'),
  (3, 'Central Fresh'),
  (4, 'Green Valley Grocery'),
  (5, 'Neighborhood Mart'),
  (6, 'City Fresh'),
  (7, 'SuperMart'),
  (8, 'Budget Foods'),
  (9, 'Organic Oasis'),
  (10, 'Market Square'),
  (11, 'Fresh Farm'),
  (12, 'Corner Store'),
  (13, 'Happy Foods'),
  (14, 'Urban Grocers'),
  (15, 'Local Market'),
  (16, 'Prime Foods'),
  (17, 'Green Basket'),
  (18, 'Food Land'),
  (19, 'Harvest Market'),
  (20, 'Quality Grocers');

-- Sample GroceryList Table
INSERT INTO GroceryList (List_ID, Customer_ID, Price_Range, Nutritional_Info)
VALUES 
  (1, 1, '$10-$50', 'Low Sugar'),
  (2, 2, '$20-$70', 'Organic'),
  (3, 3, '$5-$30', 'High Fiber'),
  (4, 4, '$15-$60', 'Low Calorie'),
  (5, 5, '$10-$40', 'Rich in Vitamins'),
  (6, 6, '$20-$80', 'Low Fat'),
  (7, 7, '$10-$50', 'High Protein'),
  (8, 8, '$15-$65', 'Gluten-Free'),
  (9, 9, '$5-$35', 'Low Carb'),
  (10, 10, '$20-$70', 'Organic'),
  (11, 11, '$10-$55', 'Low Sugar'),
  (12, 12, '$15-$60', 'High Fiber'),
  (13, 13, '$10-$50', 'Low Calorie'),
  (14, 14, '$20-$80', 'Rich in Iron'),
  (15, 15, '$10-$45', 'Low Fat'),
  (16, 16, '$15-$65', 'High Protein'),
  (17, 17, '$10-$50', 'Gluten-Free'),
  (18, 18, '$20-$70', 'Low Carb'),
  (19, 19, '$5-$35', 'Organic'),
  (20, 20, '$15-$60', 'High Fiber');

-- Sample Ingredient Table
INSERT INTO Ingredient (Ingredient_ID, IName, Nutritional_Info, Substitutes, Price_Range)
VALUES 
  (1, 'Tomato', 'Vitamin C, Low Calorie', 'Chicken', '$10-$20'),
  (2, 'Spinach', 'Iron, Vitamin K', 'Lettuce', '$5-$15'),
  (3, 'Carrot', 'Beta Carotene, Fiber', 'Broccoli', '$5-$10'),
  (4, 'Broccoli', 'Vitamin C, Fiber', 'Carrot', '$5-$20'),
  (5, 'Chicken Breast', 'High Protein, Low Fat', 'Turkey Breast', '$10-$25'),
  (6, 'Quinoa', 'High Protein, Gluten-Free', 'Spinach', '$5-$15'),
  (7, 'Salmon', 'Omega-3, High Protein', 'Tuna', '$10-$25'),
  (8, 'Avocado', 'Healthy Fats, Fiber', 'Hummus', '$10-$50'),
  (9, 'Bell Pepper', 'Vitamin C, Antioxidants', 'Celery', '$10-$15'),
  (10, 'Cucumber', 'Hydrating, Low Calorie', 'Pickle', '$10-$20'),
  (11, 'Egg', 'Protein, Vitamins', 'Quail Eggs', '$5-$10'),
  (12, 'Lettuce', 'Low Calorie, Fiber', 'Cabbage', '$5-$20'),
  (13, 'Beef', 'High Protein, Iron', 'Chicken', '$10-$40'),
  (14, 'Mushroom', 'Vitamin D, Antioxidants', 'Olives', '$10-$40'),
  (15, 'Yogurt', 'Probiotics, Calcium', 'Smoothie', '$10-$25'),
  (16, 'Blueberries', 'Antioxidants, Fiber', 'Strawberries', '$10-$15'),
  (17, 'Oats', 'Fiber, Heart Healthy', 'Peanuts', '$5-$15'),
  (18, 'Almonds', 'Healthy Fats, Protein', 'Cashews', '$5-$10'),
  (19, 'Banana', 'Potassium, Vitamin B6', 'Apple', '$10-$25'),
  (20, 'Strawberry', 'Vitamin C, Fiber', 'Blackberries', '$10-$15');

-- Sample Recipe Table
INSERT INTO Recipe (Recipe_ID, RName, Cooking_Instructions, RDescription, Nutritional_Info, Expected_Price, Is_Private_Visibility)
VALUES 
  (1, 'Tomato Soup', 'Boil tomatoes and blend.', 'A comforting soup.', 'Low Calorie', 10, FALSE),
  (2, 'Spinach Salad', 'Mix spinach with dressing.', 'A fresh salad.', 'High Iron', 8, FALSE),
  (3, 'Carrot Cake', 'Bake grated carrots with spices.', 'A sweet dessert.', 'Rich in Fiber', 12, FALSE),
  (4, 'Broccoli Stir Fry', 'Stir fry broccoli with garlic.', 'A healthy stir fry.', 'Low Calorie', 9, FALSE),
  (5, 'Grilled Chicken', 'Grill chicken breast until cooked.', 'A protein-packed meal.', 'High Protein', 15, FALSE),
  (6, 'Quinoa Bowl', 'Mix quinoa with veggies.', 'A hearty bowl.', 'Gluten-Free', 11, FALSE),
  (7, 'Baked Salmon', 'Bake salmon with herbs.', 'A delicious seafood dish.', 'Omega-3 Rich', 18, FALSE),
  (8, 'Avocado Toast', 'Toast bread and top with avocado.', 'A simple snack.', 'Healthy Fats', 7, FALSE),
  (9, 'Pepper Stir Fry', 'Stir fry bell peppers with soy sauce.', 'A vibrant dish.', 'Antioxidants', 10, FALSE),
  (10, 'Cucumber Salad', 'Mix sliced cucumbers with vinegar.', 'A refreshing salad.', 'Hydrating', 6, FALSE),
  (11, 'Egg Omelette', 'Whisk eggs and cook with fillings.', 'A classic breakfast.', 'Protein Rich', 5, FALSE),
  (12, 'Garden Lettuce Wraps', 'Wrap lettuce around fillings.', 'A light meal.', 'Low Calorie', 8, FALSE),
  (13, 'Beef Stew', 'Slow cook beef with vegetables.', 'A hearty stew.', 'High Protein', 16, FALSE),
  (14, 'Mushroom Risotto', 'Cook rice with mushrooms and broth.', 'A creamy dish.', 'Rich in Vitamin D', 14, FALSE),
  (15, 'Yogurt Parfait', 'Layer yogurt with fruit and granola.', 'A healthy dessert.', 'Calcium Rich', 7, FALSE),
  (16, 'Blueberry Muffins', 'Bake muffins with fresh blueberries.', 'A tasty treat.', 'Antioxidants', 9, FALSE),
  (17, 'Oats Porridge', 'Cook oats with milk and honey.', 'A warm breakfast.', 'Heart Healthy', 6, FALSE),
  (18, 'Almond Smoothie', 'Blend almonds with banana and milk.', 'A creamy smoothie.', 'Protein Rich', 8, TRUE),
  (19, 'Banana Bread', 'Bake bread with mashed bananas.', 'A classic treat.', 'Potassium Rich', 10, FALSE),
  (20, 'Strawberry Shortcake', 'Layer cake with strawberries and cream.', 'A delightful dessert.', 'Vitamin C Rich', 12, TRUE);

-- Sample RecipeIngredient Table
INSERT INTO RecipeIngredient (Recipe_ID, Ingredient_ID)
VALUES 
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 7),
  (8, 8),
  (9, 9),
  (10, 10),
  (11, 11),
  (12, 12),
  (13, 13),
  (14, 14),
  (15, 15),
  (16, 16),
  (17, 17),
  (18, 18),
  (19, 19),
  (20, 20);

-- Sample MealPlan Table
INSERT INTO MealPlan (Meal_Plan_ID, MName, Duration, Expected_Price, RDescription, Nutritional_Info)
VALUES 
  (1, 'Weekly Plan', 7, 50, 'Balanced meals for a week.', 'High Protein'),
  (2, 'Vegetarian Plan', 5, 40, 'All vegetarian meals.', 'Rich in Fiber'),
  (3, 'Budget Plan', 7, 30, 'Cost-effective meals.', 'Low Calorie'),
  (4, 'Fitness Plan', 7, 60, 'High protein for workouts.', 'High Protein'),
  (5, 'Detox Plan', 3, 25, 'Cleanse and detox.', 'Low Sugar'),
  (6, 'Keto Plan', 7, 55, 'Low carb meals.', 'Low Carb'),
  (7, 'Vegan Plan', 5, 45, 'All vegan options.', 'Vegan'),
  (8, 'Gluten-Free Plan', 7, 50, 'No gluten meals.', 'Gluten-Free'),
  (9, 'Mediterranean Plan', 7, 65, 'Balanced Mediterranean diet.', 'Healthy Fats'),
  (10, 'Quick Meals Plan', 3, 20, 'Meals in under 30 mins.', 'Low Calorie'),
  (11, 'Family Plan', 7, 70, 'Meals for the whole family.', 'Balanced'),
  (12, 'Luxury Plan', 7, 100, 'Gourmet meals.', 'Rich in Nutrients'),
  (13, 'High Energy Plan', 7, 80, 'Energy boosting meals.', 'High Protein'),
  (14, 'Weight Loss Plan', 7, 45, 'Low calorie meals.', 'Low Fat'),
  (15, 'Muscle Gain Plan', 7, 65, 'Protein rich meals.', 'High Protein'),
  (16, 'Organic Plan', 7, 60, 'Organic ingredients.', 'Organic'),
  (17, 'Seasonal Plan', 7, 50, 'Seasonal recipes.', 'Varied Nutrients'),
  (18, 'Comfort Food Plan', 7, 55, 'Comforting meals.', 'High Carb'),
  (19, 'Balanced Diet Plan', 7, 60, 'Well balanced meals.', 'Balanced'),
  (20, 'Holiday Plan', 7, 75, 'Festive recipes.', 'Rich in Flavors');

-- Sample MealPlanRecipe Table
INSERT INTO MealPlanRecipe (Recipe_ID, Meal_Plan_ID)
VALUES 
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 7),
  (8, 8),
  (9, 9),
  (10, 10),
  (11, 11),
  (12, 12),
  (13, 13),
  (14, 14),
  (15, 15),
  (16, 16),
  (17, 17),
  (18, 18),
  (19, 19),
  (20, 20);

-- Sample ReviewRating Table
INSERT INTO ReviewRating (Review_ID, Customer_ID, Recipe_ID, Rating, RDescription)
VALUES 
  (1, 1, 1, 5, 'Excellent and flavorful soup!'),
  (2, 2, 2, 4, 'Great salad, but could use more dressing.'),
  (3, 3, 3, 5, 'Delicious and moist carrot cake!'),
  (4, 4, 4, 4, 'Tasty stir fry with a hint of garlic.'),
  (5, 5, 5, 5, 'Perfectly grilled chicken, very satisfying.'),
  (6, 6, 6, 4, 'Quinoa bowl was filling and nutritious.'),
  (7, 7, 7, 5, 'Baked salmon was fresh and well-cooked.'),
  (8, 8, 8, 4, 'Avocado toast was simple but delightful.'),
  (9, 9, 9, 4, 'Pepper stir fry had a nice crunch.'),
  (10, 10, 10, 5, 'Cucumber salad was refreshing.'),
  (11, 11, 11, 5, 'Egg omelette was fluffy and tasty.'),
  (12, 12, 12, 4, 'Lettuce wraps were light and healthy.'),
  (13, 13, 13, 5, 'Beef stew was hearty and flavorful.'),
  (14, 14, 14, 4, 'Mushroom risotto was creamy and rich.'),
  (15, 15, 15, 5, 'Yogurt parfait was a perfect dessert.'),
  (16, 16, 16, 4, 'Blueberry muffins were moist and sweet.'),
  (17, 17, 17, 5, 'Oats porridge warmed me up on a cold day.'),
  (18, 18, 18, 4, 'Almond smoothie was creamy and energizing.'),
  (19, 19, 19, 5, 'Banana bread was perfectly baked.'),
  (20, 20, 20, 4, 'Strawberry shortcake was delightfully sweet.');

-- Sample Restocks Table
INSERT INTO Restocks (Store_ID, Ingredient_ID)
VALUES 
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 7),
  (8, 8),
  (9, 9),
  (10, 10),
  (11, 11),
  (12, 12),
  (13, 13),
  (14, 14),
  (15, 15),
  (16, 16),
  (17, 17),
  (18, 18),
  (19, 19),
  (20, 20);
