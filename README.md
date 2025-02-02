Here's the updated README file for your project "BurgerPizza" with the additional installation instructions for the chatbot:

---

# NutriMate

## Overview

NutriMate is a web application designed to help users plan their diets and interact with a chatbot for additional assistance. The project consists of two main sections: a Diet Planner and a Chatbot.

## Sections

### Diet Planner

The Diet Planner section includes various HTML files that provide the user interface for planning meals and tracking nutritional intake.

#### Running the Diet Planner

To run the Diet Planner, navigate to the project directory and execute the following command:

```bash
python3 main.py
```

### Chatbot

The Chatbot section allows users to interact with a virtual assistant that can answer questions and provide dietary advice.

#### Running the Chatbot

Before running the Chatbot, install the necessary software using the following commands:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run phi3
```

After installation, navigate to the project directory and execute the following command to run the chatbot:

```bash
python3 chatbot.py
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/burgerpizza.git
```

2. Navigate to the project directory:

```bash
cd burgerpizza
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Install additional software for the Chatbot:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run phi3
```

## Usage

- To use the Diet Planner, open a web browser and go to the local server address provided by running `main.py`.
- To interact with the Chatbot, follow the instructions given after running `chatbot.py`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, please reach out to [your email address].

---

Feel free to customize the content to better match your specific project details and preferences.
