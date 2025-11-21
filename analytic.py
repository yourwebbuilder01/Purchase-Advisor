#!/bin/env python3
import json
import os
import time
import random
from datetime import datetime

class PurchaseAdvisor:
    def __init__(self):
        self.user_data_file = "purchase_history.json"
        self.user_data = self.load_user_data()
        
    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as f:
                return json.load(f)
        return {"purchases": []}

    def save_user_data(self):
        with open(self.user_data_file, 'w') as f:
            json.dump(self.user_data, f, indent=2)

    def show_loading(self, message, duration=2):
        print(f"\n{message}")
        for i in range(101):
            bar = "[" + "█" * (i // 2) + " " * (50 - i // 2) + "]"
            print(f"{bar} {i}%", end='\r')
            time.sleep(duration / 100)
        print()

    def calculate_score(self, price, savings, income, usage, monthly_spending):
        # Can you afford it safely?
        emergency_fund = income * 3  # 3 months of expenses
        remaining_savings = savings - price
        safety_score = min(1.0, remaining_savings / emergency_fund)
        
        # Is it good value for money?
        if usage > 0:
            cost_per_use = price / (usage * 12)  # Cost per use over a year
            value_score = min(1.0, 1.0 / (cost_per_use + 0.1))  # Lower cost = higher score
        else:
            value_score = 0.1
        
        # Is it within your means?
        income_ratio = price / income
        if income_ratio <= 0.03: affordability_score = 1.0
        elif income_ratio <= 0.07: affordability_score = 0.7
        elif income_ratio <= 0.15: affordability_score = 0.4
        else: affordability_score = 0.1
        
        # Monthly spending impact
        spending_ratio = monthly_spending / income if income > 0 else 1
        if spending_ratio <= 0.6: spending_score = 1.0
        elif spending_ratio <= 0.8: spending_score = 0.7
        elif spending_ratio <= 1.0: spending_score = 0.4
        else: spending_score = 0.1
        
        return (safety_score * 0.3) + (value_score * 0.3) + (affordability_score * 0.2) + (spending_score * 0.2)

    def get_number(self, prompt):
        while True:
            try:
                value = input(f"   {prompt}: $ " if "cost" in prompt or "savings" in prompt or "income" in prompt or "spending" in prompt else f"   {prompt}: ")
                number = float(value)
                if number >= 0:
                    return number
                print("   Please enter a positive number")
            except:
                print("   Please enter a valid number")

    def get_usage(self):
        print("\n   How often will you use it?")
        print("   1. Multiple times daily (90+ times/month)")
        print("   2. Daily (30 times/month)")
        print("   3. Several times weekly (15 times/month)")
        print("   4. Weekly (4 times/month)")
        print("   5. Occasionally (1-2 times/month)")
        print("   6. Rarely (less than once/month)")
        
        while True:
            try:
                choice = input("   Choose 1-6: ")
                usage_map = {
                    '1': 90,  # Multiple times daily
                    '2': 30,  # Daily
                    '3': 15,  # Several times weekly
                    '4': 4,   # Weekly
                    '5': 1.5, # Occasionally
                    '6': 0.5  # Rarely
                }
                if choice in usage_map:
                    return usage_map[choice]
                print("   Please choose 1-6")
            except:
                print("   Please enter a valid choice")

    def print_header(self):
        print("╔══════════════════════════════════════════════════╗")
        print("║                PURCHASE ADVISOR                 ║")
        print("║           Smart Spending Decisions              ║")
        print("╚══════════════════════════════════════════════════╝")
        print()

    def print_section(self, title):
        print(f"╭─ {title} {'─' * (50 - len(title))}╮")

    def print_line(self, text="", fill_char=" "):
        if text:
            print(f"│ {text:{50}}{fill_char}│")
        else:
            print(f"│{fill_char * 52}│")

    def print_footer(self):
        print("╰──────────────────────────────────────────────────╯")

    def run(self):
        os.system('clear')
        self.print_header()
        
        self.print_section("Purchase Information")
        item = input("   What do you want to buy? ")
        
        self.print_line()
        self.print_section("Financial Details")
        price = self.get_number("How much does it cost")
        
        # Get usage frequency with descriptive options
        usage = self.get_usage()
        
        savings = self.get_number("How much do you have in savings")
        income = self.get_number("What's your monthly income")
        monthly_spending = self.get_number("How much do you spend monthly (bills, food, etc)")
        self.print_footer()
        
        # Analyze
        print("\n")
        self.print_section("Analysis Progress")
        self.show_loading("   Analyzing your finances", 1.5)
        time.sleep(0.3)
        self.show_loading("   Checking purchase value", 1.2)
        time.sleep(0.3)
        self.show_loading("   Evaluating monthly budget", 1.0)
        self.print_footer()
        
        score = self.calculate_score(price, savings, income, usage, monthly_spending)
        
        # Show results
        print("\n")
        self.print_section("Purchase Analysis Results")
        self.print_line(f"Item: {item}")
        self.print_line(f"Cost: ${price:,.2f}")
        
        # Show usage description
        usage_desc = ""
        if usage >= 90: usage_desc = "Multiple times daily"
        elif usage >= 30: usage_desc = "Daily"
        elif usage >= 15: usage_desc = "Several times weekly"
        elif usage >= 4: usage_desc = "Weekly"
        elif usage >= 1: usage_desc = "Occasionally"
        else: usage_desc = "Rarely"
        
        self.print_line(f"Usage: {usage_desc}")
        self.print_line(f"Smart Score: {score:.0%}")
        self.print_line()
        
        if score >= 0.8:
            self.print_line("✅ EXCELLENT BUY")
            self.print_line("This is a great purchase!")
            self.print_line("Good value and fits your budget well.")
        elif score >= 0.6:
            self.print_line("✅ GOOD BUY") 
            self.print_line("This is a reasonable purchase.")
            self.print_line("You'll get good use from it.")
        elif score >= 0.4:
            self.print_line("⚠️  THINK ABOUT IT")
            self.print_line("Consider waiting or alternatives.")
            self.print_line("Sleep on it for a few days.")
        else:
            self.print_line("❌ RECONSIDER")
            self.print_line("Not the best use of money now.")
            self.print_line("Your money could work better elsewhere.")
        
        self.print_line()
        self.print_section("Financial Impact")
        
        # Show details
        remaining = savings - price
        emergency_months = remaining / income if income > 0 else 0
        cost_per_use = price / (usage * 12) if usage > 0 else price
        monthly_spending_ratio = monthly_spending / income if income > 0 else 0
        
        self.print_line(f"Savings after purchase: ${remaining:,.2f}")
        self.print_line(f"Emergency fund: {emergency_months:.1f} months")
        self.print_line(f"Cost per use: ${cost_per_use:.2f}")
        self.print_line(f"Monthly spending: {monthly_spending_ratio:.0%} of income")
        
        # Additional insights
        self.print_line()
        if cost_per_use < 1:
            self.print_line("💡 Great value! Cost per use is very low")
        elif cost_per_use < 5:
            self.print_line("💡 Good value for money")
        else:
            self.print_line("💡 Consider if you'll really use it enough")
            
        if emergency_months >= 3:
            self.print_line("💡 Healthy emergency fund remaining")
        elif emergency_months >= 1:
            self.print_line("💡 Emergency fund is getting low")
        else:
            self.print_line("💡 Warning: Emergency fund depleted")
        
        self.print_footer()
        
        # Save to history
        purchase_data = {
            'item': item,
            'price': price,
            'score': score,
            'usage': usage,
            'monthly_spending': monthly_spending,
            'date': datetime.now().isoformat()
        }
        self.user_data['purchases'].append(purchase_data)
        self.save_user_data()
        
        print("\n")
        self.print_section("Complete")
        self.print_line("Decision saved to purchase history")
        self.print_line("Thank you for using Purchase Advisor!")
        self.print_footer()
        print()

if __name__ == "__main__":
    advisor = PurchaseAdvisor()
    advisor.run()
