import pandas as pd
import numpy as np

# Load dataset from CSV
def load_dataset():
    try:
        dataset = pd.read_csv("property_data.csv")
        print("✅ Dataset loaded successfully!")
        return dataset
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

# Calculate property value based on dataset and user inputs
def calculate_property_value(details, dataset):
    try:
        # Filter dataset based on location and property type
        filtered_data = dataset[
            (dataset['location'].str.lower() == details['location'].lower()) &
            (dataset['property_type'].str.lower() == details['property_type'].lower())
        ]
        
        if filtered_data.empty:
            print("⚠️ No matching data found in the dataset. Using default valuation method.")
            return calculate_default_value(details)
        
        # Calculate average price per square foot for the filtered data
        avg_price_per_sqft = filtered_data['price'].mean() / filtered_data['size'].mean()
        
        # Base value calculation
        base_value = details['size'] * avg_price_per_sqft
        
        # Adjustments
        bedroom_adj = details['bedrooms'] * 15000
        bathroom_adj = details['bathrooms'] * 10000
        age_adj = -details['age'] * 2000
        renovation_adj = details['renovations'] * 25000
        
        estimated_value = base_value + bedroom_adj + bathroom_adj + age_adj + renovation_adj
        
        return round(estimated_value, -3)  # Round to nearest thousand
    except Exception as e:
        print(f"❌ Error calculating property value: {e}")
        return calculate_default_value(details)

# Default valuation method (fallback if dataset is not available or no matching data)
def calculate_default_value(details):
    # Hypothetical base prices per square foot
    location_base = {
        'new york': 800, 'los angeles': 700, 'chicago': 600,
        'houston': 500, 'miami': 650, 'default': 550
    }
    
    prop_type_factor = {
        'house': 1.0, 'apartment': 0.9, 'condo': 0.85,
        'townhouse': 0.95, 'default': 0.9
    }
    
    # Get base price
    location = details['location'].lower()
    base_price_per_sqft = location_base.get(location, location_base['default'])
    
    # Get property type factor
    prop_type = details['property_type'].lower()
    type_factor = prop_type_factor.get(prop_type, prop_type_factor['default'])
    
    # Calculate base value
    base_value = details['size'] * base_price_per_sqft * type_factor
    
    # Adjustments
    bedroom_adj = details['bedrooms'] * 15000
    bathroom_adj = details['bathrooms'] * 10000
    age_adj = -details['age'] * 2000
    renovation_adj = details['renovations'] * 25000
    
    estimated_value = base_value + bedroom_adj + bathroom_adj + age_adj + renovation_adj
    
    return round(estimated_value, -3)  # Round to nearest thousand

# Validate user input
def get_valid_input(prompt, input_type=str, range_check=None):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("Please provide some information.")
            
            if input_type == int:
                user_input = int(user_input)
                if range_check and (user_input < range_check[0] or user_input > range_check[1]):
                    print(f"Please enter a number between {range_check[0]} and {range_check[1]}.")
                    continue
            elif input_type == float:
                user_input = float(user_input)
            
            return user_input
        except ValueError as e:
            print("Invalid input. Please try again.")

# Main chatbot function
def property_chatbot():
    # Load dataset
    dataset = load_dataset()
    
    # Wait for user to initiate conversation
    print("\n")  # Initial empty line
    user_input = input("").strip()  # Wait for any user input
    while not user_input:
        user_input = input("").strip()
    
    # Start conversation after user initiation
    print("\n🌟 Welcome to PrimeEstimate Pro! 🌟")
    print("Hi there! I'm here to help you estimate your property's current market value.")
    print("Let's start with some basic details about your property.\n")
    
    details = {}
    
    # Location
    details['location'] = get_valid_input(
        "📍 In which city is your property located? ",
        str
    )
    
    # Property Type
    details['property_type'] = get_valid_input(
        "🏠 What type of property is it? (House/Apartment/Condo/Townhouse) ",
        str
    )
    
    # Size
    details['size'] = get_valid_input(
        "📏 What is the approximate size in square feet? ",
        float,
        (100, 10000)
    )
    
    # Bedrooms
    details['bedrooms'] = get_valid_input(
        "🛏️ How many bedrooms? ",
        int,
        (1, 10)
    )
    
    # Bathrooms
    details['bathrooms'] = get_valid_input(
        "🚿 How many bathrooms? ",
        int,
        (1, 10)
    )
    
    # Age
    details['age'] = get_valid_input(
        "📅 How old is the property (in years)? ",
        int,
        (0, 200)
    )
    
    # Renovations
    details['renovations'] = get_valid_input(
        "🔨 How many major renovations have been done? ",
        int,
        (0, 10)
    )
    
    # Calculate estimate
    if dataset is not None:
        estimated_value = calculate_property_value(details, dataset)
    else:
        print("⚠️ Using default valuation method as dataset is unavailable.")
        estimated_value = calculate_default_value(details)
    
    print(f"""
📊 Based on the current market trends and your provided information:
✅ Estimated Property Value: ${estimated_value:,.2f}

Thank you for using PrimeEstimate Pro! For a detailed valuation, 
we recommend consulting with a licensed appraiser in your area.
""")

if __name__ == "__main__":
    property_chatbot()