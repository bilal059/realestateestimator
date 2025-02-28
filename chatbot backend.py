import re
import random

class RealEstateChatbot:
    def __init__(self):
        self.context = {}

    def greet(self):
        greetings = [
            "Hello! I'm your real estate assistant. How can I help you today?",
            "Hi there! Ready to estimate your property value?",
            "Welcome! Let's get started with your property details."
        ]
        return random.choice(greetings)

    def extract_details(self, user_input):
        # Extract property details using regex
        details = {}
        patterns = {
            "location": r"(?:in|at|located in)\s+([A-Za-z\s]+)",
            "property_type": r"(house|apartment|condo|townhouse)",
            "size": r"(\d+)\s*(?:sqft|square feet)",
            "bedrooms": r"(\d+)\s*(?:bedroom|bed)",
            "bathrooms": r"(\d+)\s*(?:bathroom|bath)",
            "age": r"(\d+)\s*(?:year|yr)s?\s*old",
            "renovations": r"(\d+)\s*(?:renovation|reno)"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                details[key] = match.group(1).strip()
        
        return details

    def ask_follow_up(self, missing_details):
        questions = {
            "location": "📍 In which city is your property located?",
            "property_type": "🏠 What type of property is it? (House/Apartment/Condo/Townhouse)",
            "size": "📏 What is the approximate size in square feet?",
            "bedrooms": "🛏️ How many bedrooms?",
            "bathrooms": "🚿 How many bathrooms?",
            "age": "📅 How old is the property (in years)?",
            "renovations": "🔨 How many major renovations have been done?"
        }
        return questions.get(missing_details, "Please provide more details.")

    def predict_price(self, details):
        # Dummy prediction (replace with your trained model)
        base_price = 500000  # Base price for a property
        price = base_price * (1 + int(details.get("bedrooms", 0)) * 0.1)
        return round(price, -3)  # Round to nearest thousand

    def chat(self):
        print(self.greet())
        details = {}
        required_fields = ["location", "property_type", "size", "bedrooms", "bathrooms", "age", "renovations"]

        while True:
            user_input = input("You: ").strip().lower()
            if "exit" in user_input or "quit" in user_input:
                print("Chatbot: Goodbye! Have a great day.")
                break

            # Extract details from user input
            extracted_details = self.extract_details(user_input)
            details.update(extracted_details)

            # Check for missing details
            missing_fields = [field for field in required_fields if field not in details]
            if missing_fields:
                print(f"Chatbot: {self.ask_follow_up(missing_fields[0])}")
            else:
                # All details are available, predict price
                estimated_value = self.predict_price(details)
                print(f"Chatbot: ✅ Estimated Property Value: ${estimated_value:,.2f}")
                break

# Run the chatbot
if __name__ == "__main__":
    chatbot = RealEstateChatbot()
    chatbot.chat()
