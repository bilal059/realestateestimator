from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
def load_dataset(property_data):
    try:
        dataset = pd.read_csv(file_path)
        print("✅ Dataset loaded successfully!")
        return dataset
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

# Calculate property value
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

# Default valuation method
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

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for property valuation
@app.route("/estimate", methods=["POST"])
def estimate():
    # Get user inputs from the form
    details = {
        "location": request.form["location"],
        "property_type": request.form["property_type"],
        "size": float(request.form["size"]),
        "bedrooms": int(request.form["bedrooms"]),
        "bathrooms": int(request.form["bathrooms"]),
        "age": int(request.form["age"]),
        "renovations": int(request.form["renovations"])
    }
    
    # Load dataset
    dataset = load_dataset("property_data.csv")
    
    # Calculate property value
    if dataset is not None:
        estimated_value = calculate_property_value(details, dataset)
    else:
        print("⚠️ Using default valuation method as dataset is unavailable.")
        estimated_value = calculate_default_value(details)
    
    # Return the result as JSON
    return jsonify({"estimated_value": estimated_value})

if __name__ == "__main__":
    app.run(debug=True)