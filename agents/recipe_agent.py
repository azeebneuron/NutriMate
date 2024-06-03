from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model
import random

class Message(Model):
    message: str

Gemini_Address = "agent1qwg20ukwk97t989h6kc8a3sev0lvaltxakmvvn3sqz9jdjw4wsuxqa45e8l"  # Replace with your Gemini API key

user = Agent(
    name="user",
    port=5000,
    seed="user secret phrase",
    endpoint=["http://localhost:5000/submit"],
)

fund_agent_if_low(user.wallet.address())

def find_recipes(ingredients):
    # Implementing a mock dynamic recipe search based on the provided ingredients
    all_recipes = {
        "Chicken Alfredo": ["chicken", "pasta", "cream", "parmesan", "garlic"],
        "Vegetable Stir Fry": ["bell pepper", "carrot", "broccoli", "soy sauce", "garlic"],
        "Pasta Primavera": ["pasta", "tomato", "zucchini", "parmesan", "olive oil"],
        "Mushroom Risotto": ["rice", "mushroom", "parmesan", "garlic", "onion"],
        "Beef Tacos": ["beef", "tortilla", "tomato", "lettuce", "cheese"]
    }

    matching_recipes = []

    for recipe, ingredients_list in all_recipes.items():
        if any(ingredient in ingredients_list for ingredient in ingredients):
            matching_recipes.append(recipe)

    if not matching_recipes:
        matching_recipes.append("No matching recipes found. Try different ingredients.")

    return matching_recipes

async def handle_message(ctx: Context, message: str):
    ingredients = [ingredient.strip().lower() for ingredient in message.split(',')]
    recipes = find_recipes(ingredients)
    response = "Here are some recipes you can make with the provided ingredients:\n"
    for idx, recipe in enumerate(recipes, start=1):
        response += f"{idx}. {recipe}\n"
    await ctx.send(Gemini_Address, Message(message=response))

@user.on_message(model=Message)
async def user_message_handler(ctx: Context, sender: str, msg: Message):
    await handle_message(ctx, msg.message)

if __name__ == "__main__":
    user.run()
