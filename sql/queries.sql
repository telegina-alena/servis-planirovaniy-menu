SELECT
    id,
    name,
    calories
FROM dishes
ORDER BY name;

SELECT
    id,
    name,
    unit
FROM ingredients
ORDER BY name;

SELECT
    id,
    name,
    calories
FROM dishes
WHERE calories <= ?
ORDER BY calories;

SELECT
    dishes.id,
    dishes.name,
    dishes.calories
FROM dishes
JOIN meals ON dishes.meal_id = meals.id
WHERE meals.name = ?
ORDER BY dishes.name;


-- 5. Получение блюда со списком ингредиентов
SELECT
    dishes.name AS dish_name,
    ingredients.name AS ingredient_name,
    ingredients.unit
FROM dishes
JOIN dish_ingredients
    ON dishes.id = dish_ingredients.dish_id
JOIN ingredients
    ON dish_ingredients.ingredient_id = ingredients.id
WHERE dishes.id = ?
ORDER BY ingredients.name;


-- 6. Поиск блюд по названию ингредиента
SELECT
    dishes.id,
    dishes.name,
    dishes.calories
FROM dishes
JOIN dish_ingredients
    ON dishes.id = dish_ingredients.dish_id
JOIN ingredients
    ON dish_ingredients.ingredient_id = ingredients.id
WHERE ingredients.name = ?
ORDER BY dishes.name;


-- 7. Подсчёт общего количества блюд
SELECT
    COUNT(*) AS dishes_count
FROM dishes;


-- 8. Подсчёт общего количества ингредиентов
SELECT
    COUNT(*) AS ingredients_count
FROM ingredients;


-- 9. Количество блюд по приёмам пищи
SELECT
    meals.name AS meal_name,
    COUNT(dishes.id) AS dishes_count
FROM meals
LEFT JOIN dishes
    ON meals.id = dishes.meal_id
GROUP BY meals.id, meals.name
ORDER BY dishes_count DESC;


-- 10. Количество блюд, в которых используется каждый ингредиент
SELECT
    ingredients.name AS ingredient_name,
    COUNT(dish_ingredients.dish_id) AS dishes_count
FROM ingredients
LEFT JOIN dish_ingredients
    ON ingredients.id = dish_ingredients.ingredient_id
GROUP BY ingredients.id, ingredients.name
ORDER BY dishes_count DESC;


-- 11. Ингредиенты, используемые более чем в одном блюде
SELECT
    ingredients.name AS ingredient_name,
    COUNT(dish_ingredients.dish_id) AS dishes_count
FROM ingredients
JOIN dish_ingredients
    ON ingredients.id = dish_ingredients.ingredient_id
GROUP BY ingredients.id, ingredients.name
HAVING COUNT(dish_ingredients.dish_id) > 1
ORDER BY dishes_count DESC;