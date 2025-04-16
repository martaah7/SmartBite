-- Copy and paste this into directory, connect to mysql, run commands below in order to populate the database with tables
-- CREATE DATABASE healthApp;
-- USE healthApp;
--  source ./createDatabase.sql

-- Employee Table
CREATE TABLE Employee (
    Employee_ID INT PRIMARY KEY,
    EName VARCHAR(255)
);

-- Customers Tableingredient
CREATE TABLE Customers (
    Customer_ID INT PRIMARY KEY,
    CName VARCHAR(255) NOT NULL, 
    Dietary_Preference VARCHAR(255),
    Contact_Info VARCHAR(255) NOT NULL UNIQUE, 
    Payment_Info VARCHAR(255) NOT NULL,
    Expenses DECIMAL(7,2) CHECK (Expenses >= 0),
    Nutritional_Info VARCHAR(255)
);

-- GroceryStore Table
CREATE TABLE GroceryStore (
    Retailer_ID INT PRIMARY KEY,
    GLocation VARCHAR(255)
);

-- GroceryList Table
CREATE TABLE GroceryList (
    List_ID INT NOT NULL PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Price_Range VARCHAR(255) NOT NULL,
    Nutritional_Info VARCHAR(255),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);

-- Ingredient Table
CREATE TABLE Ingredient (
    Ingredient_ID INT PRIMARY KEY,
    IName VARCHAR(255) NOT NULL,
    Nutritional_Info VARCHAR(255),
    Substitutes VARCHAR(255),
    Price_Range VARCHAR(255) NOT NULL
);

-- Recipe Table
CREATE TABLE Recipe (
    Recipe_ID INT PRIMARY KEY,
    RName VARCHAR(255) NOT NULL,
    Cooking_Instructions VARCHAR(1023),
    RDescription VARCHAR(511),
    Nutritional_Info VARCHAR(255),
    Expected_Price INT CHECK (Expected_Price > 0), 
    Is_Private_Visibility BOOLEAN
    -- ingredients being handled by the recipe ingredient table
);

-- This table handles effectively storing the ingredients needed for each recipe
-- since you can't use an array to store all the ids as an attribute in the recipe table
-- primary key is (recipe id, ingredient id)
CREATE TABLE RecipeIngredient (
    Recipe_ID INT NOT NULL,
    Ingredient_ID INT NOT NULL,
    PRIMARY KEY (Recipe_ID, Ingredient_ID),
    FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID),
    FOREIGN KEY (Ingredient_ID) REFERENCES Ingredient(Ingredient_ID)
);

-- MealPlan Table
CREATE TABLE MealPlan (
    Meal_Plan_ID INT PRIMARY KEY,
    MName VARCHAR(255) NOT NULL,
    Duration INT, -- number of days the meal plan should cover
    Expected_Price INT CHECK (Expected_Price > 0), -- estimate value of the expected price
    RDescription VARCHAR(511),
    Nutritional_Info VARCHAR(255)
);

-- This table handles effectively storing the recipes needed for each meal plan
-- primary key is (meal plan id id, recipe id)
CREATE TABLE MealPlanRecipe (
    Recipe_ID INT NOT NULL,
    Meal_Plan_ID INT NOT NULL,
    PRIMARY KEY (Meal_Plan_ID, Recipe_ID),
    FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID),
    FOREIGN KEY (Meal_Plan_ID) REFERENCES MealPlan(Meal_Plan_ID)
);

--  ReviewRating Table
CREATE TABLE ReviewRating (
    Review_ID INT PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Recipe_ID INT NOT NULL,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    RDescription VARCHAR(511),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID)
);

--  Restocks Table
CREATE TABLE Restocks (
    Store_ID INT NOT NULL,
    Ingredient_ID INT NOT NULL,
    PRIMARY KEY (Store_ID, Ingredient_ID),
    FOREIGN KEY (Store_ID) REFERENCES GroceryStore(Retailer_ID),
    FOREIGN KEY (Ingredient_ID) REFERENCES Ingredient(Ingredient_ID)
);
