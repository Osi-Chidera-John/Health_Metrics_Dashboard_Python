import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import os

# DATA GENERATION (For testing only)


def generate_sample_data(days=7):
    """Generate sample data for testing"""
    data = []
    start = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        day = start + timedelta(days=i)
        data.append({
            'date': day.strftime('%Y-%m-%d'),
            'steps': random.randint(3000, 12000),
            'calories': random.randint(1500, 2800),
            'sleep': round(random.uniform(5.0, 8.5), 1),
            'water': random.randint(4, 10)
        })
    
    return pd.DataFrame(data)


# DATA MANAGEMENT

def load_data():
    """Load data with priority: user data > sample data > empty"""
    
    os.makedirs('data', exist_ok=True)
    
    # Check for user data first
    if os.path.exists('data/user_data.csv'):
        df = pd.read_csv('data/user_data.csv')
        if not df.empty:
            print("\n📂 Loading YOUR data...")
            return df, 'user'
    
    # Check for sample data
    if os.path.exists('data/sample_data.csv'):
        df = pd.read_csv('data/sample_data.csv')
        if not df.empty:
            print("\n Loading sample data (for testing)...")
            return df, 'sample'
    
    # No data
    print("\n No data found.")
    return pd.DataFrame(columns=['date', 'steps', 'calories', 'sleep', 'water']), 'empty'

def save_data(df, data_type='user'):
    """Save data to the appropriate file"""
    
    os.makedirs('data', exist_ok=True)
    
    if data_type == 'user':
        df.to_csv('data/user_data.csv', index=False)
        print("💾 Data saved to 'data/user_data.csv'")
    else:
        df.to_csv('data/sample_data.csv', index=False)
        print("💾 Sample data saved to 'data/sample_data.csv'")

def has_user_data(df):
    """Check if DataFrame contains real user data"""
    return not df.empty

 
# DASHBOARD FUNCTIONS

def show_dashboard(df, data_type):
    """Show dashboard with the current data"""
    
    if df.empty:
        print("\n📭 No data available! Add entries or generate sample data.")
        return
    
    print("\n" + "="*50)
    if data_type == 'user':
        print("📊 YOUR HEALTH DASHBOARD")
    elif data_type == 'sample':
        print("🧪 TEST DASHBOARD (Sample Data)")
    else:
        print("  📊 HEALTH DASHBOARD")
    print("="*50)
    
    # Calculate stats
    avg_steps = df['steps'].mean()
    avg_calories = df['calories'].mean()
    avg_sleep = df['sleep'].mean()
    avg_water = df['water'].mean()
    
    print(f"\n 📊 Based on {len(df)} entries:")
    print(f"   🚶 Average Steps: {avg_steps:,.0f}")
    print(f"   🔥 Average Calories: {avg_calories:,.0f}")
    print(f"   😴 Average Sleep: {avg_sleep:.1f} hours")
    print(f"   💧 Average Water: {avg_water:.1f} glasses")
    
    # Tips
    print("\n TIPS:")
    if avg_steps >= 10000:
        print("  ✅  Great step count!")
    elif avg_steps >= 7500:
        print("   👍 Good steps! Aim for 10,000.")
    else:
        print("   🚶 Try to reach 10,000 steps daily.")
    
    if avg_sleep >= 7:
        print("    ✅ Good sleep!")
    else:
        print("   😴 Aim for 7-8 hours of sleep.")
    
    if avg_water >= 8:
        print("  ✅ Good hydration!")
    else:
        print("   💧 Drink at least 8 glasses of water.")
    
    # Charts
    show_charts(df)

def show_charts(df):
    """Create charts from the data"""

    print("\nGenerating charts.....")
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Your Health Dashboard', fontsize=15, fontweight="bold")
    
    # Chart for Steps taken
    axes[0,0].plot(df['date'], df['steps'], 'b-o')
    axes[0,0].axhline(y=10000, color='g', linestyle='--')
    axes[0,0].set_title('Steps')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Chart for Sleep
    axes[0,1].bar(df['date'], df['sleep'], color='purple')
    axes[0,1].axhline(y=7, color='orange', linestyle='--')
    axes[0,1].set_title('Sleep (hours)')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Chart for Calories
    axes[1,0].plot(df['date'], df['calories'], 'r-', marker="o")
    axes[1,0].set_title('Calories')
    axes[1,0].tick_params(axis='x', rotation=45)
    
     # Chart for Water
    axes[1,1].bar(df['date'], df['water'], color='skyblue')
    axes[1,1].axhline(y=8, color='blue', linestyle='--')
    axes[1,1].set_title('Water (glasses)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    fig.suptitle(" Your Health Summary", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    

# ADD ENTRY

def add_entry(df, data_type):
    """Add a new entry from user input"""
    
    print("\n📝 ADD TODAY'S ENTRY")
    print("-" * 30)
    
    try:
        steps = int(input("Steps walked today: "))
        calories = float(input("Calories burned: "))
        sleep = int(input("Hours of sleep: "))
        water = int(input("Glasses of water: "))
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        new_entry = pd.DataFrame([{
            'date': today,
            'steps': steps,
            'calories': calories,
            'sleep': sleep,
            'water': water
        }])
        
        df = pd.concat([df, new_entry], ignore_index=True)
        
        # When user adds data, it becomes USER data
        data_type = 'user'
        save_data(df, data_type)
        
        print("\n✅ Entry added successfully!")
        return df, data_type
        
    except ValueError:
        print("\n❌ Invalid input. Please enter numbers only.")
        return df, data_type


# MENU

def show_menu(df, data_type):
    """Main menu loop"""
    
    while True:
        print("\n" + "="*40)
        print("🏥 HEALTH DASHBOARD")
        print("="*40)
        print(f"📊 Current data: {'YOUR data' if data_type == 'user' else 'Sample data' if data_type == 'sample' else 'No data'}")
        print("="*40)
        print("1️⃣  View Dashboard")
        print("2️⃣  Add Today's Entry")
        print("3️⃣  Generate Sample Data (for testing)")
        print("4️⃣  Clear All Data")
        print("5️⃣  Exit")
        
        choice = input("\nChoose (1-5): ")
        
        if choice == '1':
            show_dashboard(df, data_type)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            df, data_type = add_entry(df, data_type)
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Generate sample data
            days = input("How many days of sample data? (default: 7): ")
            days = int(days) if days else 7
            
            df = generate_sample_data(days)
            data_type = 'sample'
            save_data(df, data_type)
            print(f"\n Generated {days} days of sample data for testing!")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Clear data
            confirm = input(" Are you sure? This will delete ALL data. (y/n): ")
            if confirm.lower() == 'y':
                df = pd.DataFrame(columns=['date', 'steps', 'calories', 'sleep', 'water'])
                data_type = 'empty'
                # Delete files
                if os.path.exists('data/user_data.csv'):
                    os.remove('data/user_data.csv')
                if os.path.exists('data/sample_data.csv'):
                    os.remove('data/sample_data.csv')
                print("\n All data cleared!")
            input("\nPress Enter to continue...")
            
        elif choice == '5':
            print("\n Stay healthy buddy! Goodbye!")
            break
            
        else:
            print("\nInvalid choice.")
            input("\nPress Enter to continue...")

# MAIN PROGRAM

def main():
    """Main program"""
    
    print("\n" + "="*50)
    print(" WELCOME TO YOUR HEALTH DASHBOARD")
    print("="*50)
    
    # Load existing data
    df, data_type = load_data()
    
    # If no data at all, ask what to do
    if data_type == 'empty':
        print("\nWhat would you like to do?")
        print("1️⃣  Start entering your own data")
        print("2️⃣  Generate sample data to test")
        print("3️⃣  Exit")
        
        choice = input("\nChoose (1-3): ")
        
        if choice == '1':
            print("\n Starting with empty data. Use option 2 to add entries!")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            days = input("How many days of sample data? (default: 30): ")
            days = int(days) if days else 30
            
            df = generate_sample_data(days)
            data_type = 'sample'
            save_data(df, data_type)
            print(f"\n Generated {days} days of sample data for testing!")
            input("\nPress Enter to continue...")
            
        else:
            print("\n Goodbye!")
            return
    
    # Show the main menu
    show_menu(df, data_type)

if __name__ == "__main__":
    main()