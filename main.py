# import streamlit as st
# import pandas as pd

# # Read data from CSV file
# df = pd.read_csv("products.csv")

# # Convert Product Prices to integers
# df["Product Prices"] = df["Product Prices"].str.replace("₮", "").str.replace(",", "").astype(int)

# # Initialize session state
# if "cart" not in st.session_state:
#     st.session_state.cart = set()  # Use a set to store unique items
#     st.session_state.total_cost = 0

# # Streamlit app
# st.title("Burger Web App")

# # Sidebar for user input
# budget = st.sidebar.number_input("Enter your budget:", min_value=1000, step=1000)

# # Filter products based on budget
# filtered_products = df[df["Product Prices"] <= budget]

# # Display selected items
# selected_items = st.multiselect("Select items to add to your cart:", filtered_products["Product Names"].tolist())

# # Remove canceled items from the cart
# canceled_items = set(st.session_state.cart) - set(selected_items)
# for canceled_item in canceled_items:
#     item_price = df.loc[df["Product Names"] == canceled_item, "Product Prices"].values[0]
#     st.session_state.cart.remove(canceled_item)
#     st.session_state.total_cost -= item_price

# # Update cart and display remaining budget
# for item in selected_items:
#     item_price = df.loc[df["Product Names"] == item, "Product Prices"].values[0]
#     if st.session_state.total_cost + item_price <= budget:
#         st.session_state.cart.add(item)  # Use add() method for sets
#         st.session_state.total_cost += item_price
#     else:
#         st.warning(f"Cannot add {item} to cart. Exceeds budget.")

# # Display cart items
# st.sidebar.title("Your Cart")
# cart_display = "\n".join(st.session_state.cart) if st.session_state.cart else "No items in your cart."
# st.sidebar.text_area("Items in your cart:", cart_display)

# # Display remaining budget
# remaining_budget = budget - st.session_state.total_cost
# st.sidebar.text(f"Remaining Budget: {remaining_budget} ₮")

# # Display available items that can be afforded with remaining budget
# affordable_products = df[df["Product Prices"] <= remaining_budget]
# st.subheader("Available Items")
# st.table(affordable_products[["Product Names", "Product Prices"]])

# # Alert if remaining budget is below 1000
# if remaining_budget < 1000:
#     st.warning("Your remaining budget is below 1000. You can't buy more products.")









import streamlit as st
import pandas as pd

# Read data from CSV file
df = pd.read_csv("products.csv")

# Convert Product Prices to integers
df["Product Prices"] = df["Product Prices"].str.replace("₮", "").str.replace(",", "").astype(int)

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = set()  # Use a set to store unique items
    st.session_state.total_cost = 0

# Streamlit app
st.title("Burger Web App")

# Sidebar for user input
budget = st.sidebar.number_input("Enter your budget:", min_value=1000, step=1000)

# Filter products based on budget
filtered_products = df[df["Product Prices"] <= budget]

# Display selected items as buttons in a row
st.subheader("Select items to add to your cart:")
for item in filtered_products["Product Names"]:
    if st.button(f"Add {item} to cart"):
        item_price = df.loc[df["Product Names"] == item, "Product Prices"].values[0]
        if st.session_state.total_cost + item_price <= budget:
            st.session_state.cart.add(item)
            st.session_state.total_cost += item_price
        else:
            st.warning(f"Cannot add {item} to cart. Exceeds budget.")

# Display cart items as buttons
st.sidebar.title("Your Cart")
st.sidebar.subheader("Items in your cart:")
for item in st.session_state.cart:
    st.sidebar.button(item)

# Display remaining budget
remaining_budget = budget - st.session_state.total_cost
st.sidebar.text(f"Remaining Budget: {remaining_budget} ₮")

# Display available items that can be afforded with remaining budget
affordable_products = df[df["Product Prices"] <= remaining_budget]
st.subheader("Available Items")
st.table(affordable_products[["Product Names", "Product Prices"]])

# Alert if remaining budget is below 1000
if remaining_budget < 1000:
    st.warning("Your remaining budget is below 1000. You can't buy more products.")
