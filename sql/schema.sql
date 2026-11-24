
-- Таблица приёмов пищи
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица блюд
CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    calories INTEGER NOT NULL CHECK (calories > 0),
    meal_id INTEGER NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meals(id)
);

-- Таблица ингредиентов
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    unit TEXT NOT NULL DEFAULT 'шт'
);

-- Связующая таблица блюд и ингредиентов
CREATE TABLE IF NOT EXISTS dish_ingredients (
    dish_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,

    PRIMARY KEY (dish_id, ingredient_id),

    FOREIGN KEY (dish_id)
        REFERENCES dishes(id)
        ON DELETE CASCADE,

    FOREIGN KEY (ingredient_id)
        REFERENCES ingredients(id)
        ON DELETE CASCADE
);
