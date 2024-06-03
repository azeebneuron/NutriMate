

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model



class Message(Model):
    message: str

Gemini_Address = "agent1qwg20ukwk97t989h6kc8a3sev0lvaltxakmvvn3sqz9jdjw4wsuxqa45e8l" 

user = Agent(
    name="user",
    port=5000,  # Changed the port to 5000
    seed="user secret phrase",
    endpoint=["http://localhost:5000/submit"],
)

fund_agent_if_low(user.wallet.address())

def generate_diet_plan(user_data):
    age = user_data.get("age")
    height = user_data.get("height")
    weight = user_data.get("weight")
    medical_history = user_data.get("medical_history")

    diet_plan = f"Based on the information provided:\n- Age: {age}\n- Height: {height} cm\n- Weight: {weight} kg\n- Medical History: {medical_history}\n\n, generate a detailed diet plan for the user like this"
    diet_plan += "Here is a personalized diet plan for you:\n"
    diet_plan += "1. Breakfast: Oatmeal with fruits\n"
    diet_plan += "2. Lunch: Grilled chicken salad with quinoa\n"
    diet_plan += "3. Snack: Greek yogurt with nuts\n"
    diet_plan += "4. Dinner: Baked salmon with steamed vegetables\n"
    diet_plan += "5. Stay hydrated and drink plenty of water throughout the day.\n"
    diet_plan += "Please consult with a healthcare professional for more personalized advice."

    return diet_plan

@user.on_event('startup')
async def agent_startup(ctx: Context):
    # Prompting user for input data
    age = int(input('Enter your age: '))
    height = int(input('Enter your height in cm: '))
    weight = int(input('Enter your weight in kg: '))
    medical_history = str(input('Enter your medical history: '))

    # Collecting user data
    user_data = {
        "age": age,
        "height": height,
        "weight": weight,
        "medical_history": medical_history
    }

    ctx.logger.info(user.address)
    response = generate_diet_plan(user_data)
    await ctx.send(Gemini_Address, Message(message=response))
