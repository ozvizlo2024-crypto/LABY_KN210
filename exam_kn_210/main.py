import os
from abc import ABC, abstractmethod
from typing import Dict, Optional
from google import genai
from google.genai import types

# ⚠️ ВСТАВТЕ СВІЙ НОВИЙ КЛЮЧ СЮДИ (Він має починатися з AIzaSy...)
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6K48QNezbf74Dm-cd2Hj9-ShNZtuT0GpBR5d9B-pRwAdA"

# ==========================================
# 1. ООП ЧАСТИНА (Класи страв та Кукбук)
# ==========================================

class Dish(ABC):
    def __init__(self, name: str, cooking_time_min: int):
        self.name = name
        self.cooking_time_min = cooking_time_min

    @abstractmethod
    def get_nutrition(self) -> dict:
        pass


class VeganDish(Dish):
    def __init__(self, name: str, cooking_time_min: int, calories: int):
        super().__init__(name, cooking_time_min)
        self.calories = calories

    def get_nutrition(self) -> dict:
        return {"calories": self.calories, "type": "vegan"}


class MeatDish(Dish):
    def __init__(self, name: str, cooking_time_min: int, calories: int, protein_g: float):
        super().__init__(name, cooking_time_min)
        self.calories = calories
        self.protein_g = protein_g

    def get_nutrition(self) -> dict:
        return {"calories": self.calories, "protein_g": self.protein_g, "type": "meat"}


class CookBook:
    def __init__(self):
        self.__recipes: Dict[str, Dish] = {}

    def add(self, dish: Dish) -> None:
        self.__recipes[dish.name.lower()] = dish

    def find(self, name: str) -> Optional[Dish]:
        return self.__recipes.get(name.lower(), None)

    def list_all(self) -> list:
        return [
            {
                "name": dish.name,
                "cooking_time_min": dish.cooking_time_min,
                "nutrition": dish.get_nutrition()
            }
            for dish in self.__recipes.values()
        ]


# ==========================================
# 2. ІНСТРУМЕНТ (TOOL) ДЛЯ AI-АГЕНТА
# ==========================================

def get_recipe_info(dish_name: str) -> dict:
    """
    Search for dish information in the cookbook by its name.
    
    Args:
        dish_name: The name of the dish to search for (e.g. 'Гарбузовий суп' or 'Стейк Рібай').
    """
    cookbook = CookBook()
    cookbook.add(VeganDish("Салат Цезар веганський", 15, 250))
    cookbook.add(VeganDish("Гарбузовий суп", 30, 180))
    cookbook.add(MeatDish("Стейк Рібай", 20, 450, 35.5))
    cookbook.add(MeatDish("Борщ з яловичиною", 60, 320, 18.2))
    cookbook.add(MeatDish("Курячі котлети", 25, 280, 22.0))

    dish = cookbook.find(dish_name)
    
    if dish:
        return {
            "found": True,
            "name": dish.name,
            "cooking_time_min": dish.cooking_time_min,
            "nutrition": dish.get_nutrition()
        }
    return {"found": False}


# ==========================================
# 3. НАЛАШТУВАННЯ ТА ЛОГІКА AI-АГЕНТА
# ==========================================

client = genai.Client()

system_instruction = (
    "Ти є кулінарним помічником. Твоє завдання — надавати інформацію про рецепти, "
    "калорійність та тип страви, а також давати рекомендації щодо харчування. "
    "Для перевірки наявності страв обов'язково викликай інструмент `get_recipe_info`. "
    "Відповідай виключно українською мовою."
)


def ask_agent(user_query: str):
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[get_recipe_info],
            temperature=0.3,
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_query,
            config=config
        )
        
        print(f"[Агент]: {response.text}")
        
    except Exception as e:
        print(f"[Помилка ШІ]: {e}")


# ==========================================
# 4. ІНТЕРАКТИВНИЙ ЗАПУСК ДЛЯ КОРИСТУВАЧА
# ==========================================

if __name__ == "__main__":
    print("==================================================")
    print("=== Кулінарний ШІ-агент запущений!             ===")
    print("=== Напишіть своє запитання та натисніть Enter ===")
    print("=== Для виходу з програми напишіть 'вихід'     ===")
    print("==================================================")
    
    while True:
        user_input = input("\nВаш запит: ")
        
        if user_input.strip().lower() in ["вихід", "exit", "quit"]:
            print("Бувай! Смачного!")
            break
            
        if not user_input.strip():
            continue
            
        ask_agent(user_input)