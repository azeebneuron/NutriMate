from agents.dietician import user
from agents.gemini_dietician import Gemini_agent
from flask import Flask, render_template, request, redirect, url_for
# from dietician import DietForm
# from agents.recipe_agent import recipe_agent
from uagents import Bureau

app = Flask(__name__)

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    bureau.add(Gemini_agent)
    bureau.add(user)
    bureau.run()