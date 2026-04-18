import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta

def generate_ecommerce_data(num_users=1000, num_events=20000):
    np.random.seed(42)
    
    # Base data
    user_ids = [i for i in range(1000, 1000 + num_users)]
    categories = {
        'electronics.smartphone': 250,
        'electronics.laptop': 800,
        'appliances.kitchen.refrigerator': 600,
        'computers.peripherals.mouse': 25,
        'apparel.shoes': 80,
        'apparel.tshirt': 20
    }
    brands = ['Samsung', 'Apple', 'Xiaomi', 'Dell', 'LG', 'Nike', 'Adidas']
    
    events = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_events):
        user_id = np.random.choice(user_ids)
        # Simulate sessions
        session_id = str(uuid.uuid4())
        num_session_events = np.random.randint(1, 10)
        
        # User behavior weights
        # Most users just view, some cart, few purchase
        # High drop off at cart is intended for the analysis
        
        category = np.random.choice(list(categories.keys()))
        price = categories[category] + np.random.uniform(-10, 10)
        brand = np.random.choice(brands)
        product_id = np.random.randint(10000, 11000)
        
        current_time = start_date + timedelta(days=np.random.randint(0, 30), 
                                            hours=np.random.randint(0, 24),
                                            minutes=np.random.randint(0, 60))
        
        # Step 1: View (100% of session starts)
        events.append([
            current_time, 'view', product_id, 1, category, brand, price, user_id, session_id
        ])
        
        # Step 2: Cart (30% chance)
        if np.random.random() < 0.3:
            current_time += timedelta(minutes=np.random.randint(1, 5))
            events.append([
                current_time, 'cart', product_id, 1, category, brand, price, user_id, session_id
            ])
            
            # Step 3: Purchase (25% chance of those who carted -> ~7.5% total)
            # High friction simulation: 75% drop off at cart
            if np.random.random() < 0.25:
                current_time += timedelta(minutes=np.random.randint(1, 10))
                events.append([
                    current_time, 'purchase', product_id, 1, category, brand, price, user_id, session_id
                ])

    df = pd.DataFrame(events, columns=[
        'event_time', 'event_type', 'product_id', 'category_id', 
        'category_code', 'brand', 'price', 'user_id', 'user_session'
    ])
    
    df = df.sort_values('event_time')
    df.to_csv('data/events.csv', index=False)
    print(f"Generated {len(df)} events in data/events.csv")

if __name__ == "__main__":
    generate_ecommerce_data()
