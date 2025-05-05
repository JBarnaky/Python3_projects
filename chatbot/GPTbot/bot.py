from dataclasses import dataclass
import os
import openai
from dotenv import load_dotenv, find_dotenv
import panel as pn
from typing import List, Dict, Any, Optional

# Load environment variables
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")


@dataclass
class OrderSummary:
    """Structured representation of a food order."""
    pizza: Dict[str, float]  # e.g., {"size": "large", "price": 12.95}
    toppings: List[Dict[str, float]]  # e.g., [{"name": "extra cheese", "price": 2.00}]
    drinks: List[Dict[str, Any]]  # e.g., [{"size": "large", "price": 3.00}]
    sides: List[Dict[str, Any]]  # e.g., [{"size": "medium", "price": 3.50}]
    total_price: float


class OpenAIService:
    """Handles interactions with the OpenAI API."""
    
    def __init__(self, model: str = "gpt-3.5-turbo-0125"):
        self.model = model

    def get_completion(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        Get a completion from the OpenAI Chat API.

        Args:
            messages: List of message dicts with "role" and "content".
            temperature: Degree of randomness in output (0.0 to 1.0).

        Returns:
            The assistant's response content.

        Raises:
            Exception: If API call fails.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message["content"]
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}") from e


class OrderBot:
    """Business logic for the OrderBot service."""
    
    MENU = """
    You are OrderBot, an automated service to collect orders for a pizza restaurant. \
    You first greet the customer, then collect the order, and then ask if it's pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final time if the customer wants to add anything else. \
    If it's a delivery, you ask for an address. Finally, you collect the payment. \
    Make sure to clarify all options, extras, and sizes to uniquely identify the item from the menu. \
    You respond in a short, very conversational friendly style. \
    
    Menu:
    - Pepperoni pizza: $12.95 (large), $10.00 (medium), $7.00 (small)
    - Cheese pizza: $10.95 (large), $9.25 (medium), $6.50 (small)
    - Eggplant pizza: $11.95 (large), $9.75 (medium), $6.75 (small)
    - Fries: $4.50 (large), $3.50 (medium)
    - Greek salad: $7.25
    - Toppings:
        - Extra cheese: $2.00
        - Mushrooms: $1.50
        - Sausage: $3.00
        - Canadian bacon: $3.50
        - AI sauce: $1.50
        - Peppers: $1.00
    - Drinks:
        - Coke: $3.00 (large), $2.00 (medium), $1.00 (small)
        - Sprite: $3.00 (large), $2.00 (medium), $1.00 (small)
        - Bottled water: $5.00
    """

    def __init__(self):
        self.context = [{"role": "system", "content": self.MENU}]
        self.openai_service = OpenAIService()

    def process_user_input(self, prompt: str) -> str:
        """Process a user message and return the assistant's response."""
        self.context.append({"role": "user", "content": prompt})
        response = self.openai_service.get_completion(self.context)
        self.context.append({"role": "assistant", "content": response})
        return response

    def generate_order_summary(self) -> OrderSummary:
        """Generate a structured JSON summary of the order."""
        summary_prompt = [
            *self.context,
            {
                "role": "system",
                "content": "Create a JSON summary of the previous food order. "
                "Itemize the price for each item. The fields should be: "
                "1) pizza (include size and price), 2) list of toppings with prices, "
                "3) list of drinks (include size and price), 4) list of sides (include size and price), "
                "5) total price."
            },
        ]
        response = self.openai_service.get_completion(summary_prompt, temperature=0)
        return OrderSummary(**eval(response))  # Simplified for demo; use JSON parser in production


class ChatUI:
    """Panel-based UI for the OrderBot."""
    
    def __init__(self, order_bot: OrderBot):
        self.order_bot = order_bot
        self.panels = []

        self.inp = pn.widgets.TextInput(value="Hi", placeholder="Enter text here…")
        self.button = pn.widgets.Button(name="Chat!")

        self.button.on_click(self._handle_button_click)

        self.dashboard = pn.Column(
            self.inp,
            pn.Row(self.button),
            pn.panel(self._get_interactive_conversation(), loading_indicator=True, height=300),
        )

    def _handle_button_click(self, event):
        """Handle button click event to process user input."""
        prompt = self.inp.value
        if not prompt.strip():
            return

        self.inp.value = ""
        response = self.order_bot.process_user_input(prompt)

        self.panels.append(pn.Row("User:", pn.pane.Markdown(prompt, width=600)))
        self.panels.append(pn.Row("Assistant:", pn.pane.Markdown(response, width=600, style={"background-color": "#F6F6F6"})))

    def _get_interactive_conversation(self):
        """Return a reactive component for the conversation."""
        return pn.bind(lambda _: pn.Column(*self.panels), self.button)

    def show(self):
        """Display the UI dashboard."""
        return self.dashboard


def main():
    """Main entry point of the application."""
    order_bot = OrderBot()
    chat_ui = ChatUI(order_bot)
    summary = order_bot.generate_order_summary()
    print("Order Summary:", summary)
    return chat_ui.show()


if __name__ == "__main__":
    pn.extension()
    main()
