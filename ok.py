import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Read data from CSV file
df = pd.read_csv("products.csv")

# Convert Product Prices to integers
df["Product Prices"] = df["Product Prices"].str.replace("₮", "").str.replace(",", "").astype(int)

# Classify into Ice Creams
ice_cream_keywords = ['шоколадтай зайрмаг', 'гүзээлзгэнэтэй зайрмаг', 'сүүтэй зайрмаг']
df.loc[df['Product Names'].str.lower().str.contains('|'.join(ice_cream_keywords), case=False), 'Category'] = 'Ice Creams'

# Classify into Snacks
snack_keywords = ['чийз стик', 'СКВИД РИНГС', 'шарсан тахиа']
df.loc[df['Product Names'].str.lower().str.contains('|'.join(snack_keywords), case=False), 'Category'] = 'Snacks'

# Classify into Burgers
burger_keywords = ['тери', 'бүлгүги', 'бийф', 'шримп', 'хаш бийф', 'чийз', 'хамбургер', 'чекин', 'хот криспи']
df.loc[df['Product Names'].str.lower().str.contains('|'.join(burger_keywords), case=False) & ~df['Category'].isin(['Ice Creams', 'Snacks']), 'Category'] = 'Burgers'

# Classify into Beverages
beverage_keywords = ['ice tea', 'seabuckthorn', 'tornado', 'mirinda', 'mount dew', '7up', 'pepsi']
df.loc[df['Product Names'].str.contains('|'.join(beverage_keywords), case=False), 'Category'] = 'Beverages'

# Classify into Sets
set_keywords = ['set']
df.loc[df['Product Names'].str.contains('|'.join(set_keywords), case=False), 'Category'] = 'Sets'

# Drop rows with NaN values in the 'Category' column
df = df.dropna(subset=['Category'])

# Function to display item images
def display_image(image_path):
    image = Image.open(image_path)
    st.image(image, caption='', use_column_width=True)

# Streamlit App
st.title("Burger Suggester")

# Display available categories (excluding NaN)
categories = df['Category'].unique()
selected_category = st.selectbox("Select a category:", categories)

# Filter DataFrame based on selected category
filtered_df = df[df['Category'] == selected_category]

# Cart Section
st.sidebar.title("Items in your cart")  # Change the heading here

# Initialize cart as a session state variable
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Initialize total cost
total_cost = 0

# Budget Section
budget = st.sidebar.number_input("Enter your budget in Tugruk", min_value=1000, step=1000)

# Display common item image
image_path = "images/image.jpg"
display_image(image_path)

# Buttons for each item in the selected category
for index, row in filtered_df.iterrows():
    if row['Product Prices'] <= budget and budget >= 0:
        # Use a unique key for each button
        button_key = f"button_{row['Product Names']}"
        # Display item image
        image_path = f"images/{row['Product Names']}.jpg"
        display_image(image_path)
        if st.button(f"Add {row['Product Names']} (₮{row['Product Prices']})", key=button_key):
            # Add the selected item to the session state cart
            st.session_state.cart.append({'name': row['Product Names'], 'price': row['Product Prices']})
            # Deduct the item price from the budget
            budget -= row['Product Prices']
            # Update the total cost
            total_cost += row['Product Prices']

# Buttons to remove each item from the cart
remove_buttons = []
for item in st.session_state.cart:
    # Use a unique key for each remove button
    remove_button_key = f"remove_button_{item['name']}"
    remove_buttons.append(st.button(f"Remove {item['name']} (₮{item['price']})", key=remove_button_key))

# Remove items from the cart based on remove buttons
for i in reversed(range(len(st.session_state.cart))):
    if remove_buttons[i]:
        # Remove the selected item from the session state cart
        removed_item = st.session_state.cart.pop(i)
        # Add back the item price to the budget
        budget += removed_item['price']
        # Update the total cost
        total_cost -= removed_item['price']

# Display selected items in the cart
if st.session_state.cart:
    st.sidebar.write("### Selected Items:")
    for item in st.session_state.cart:
        st.sidebar.write(f"{item['name']} (₮{item['price']})")
    st.sidebar.write("### Total Cost:")
    st.sidebar.write(total_cost)
    st.sidebar.write("### Remaining Budget:")
    st.sidebar.write(budget)

    # Alert if remaining budget is less than the cost of the cheapest item
    if budget < filtered_df['Product Prices'].min():
        st.warning("Your remaining budget is not sufficient to buy any more items!")

# Analysis Section
st.title("Analysis")

# Bar chart of average prices per category
avg_prices = df.groupby('Category')['Product Prices'].mean().reset_index()
bar_chart = alt.Chart(avg_prices).mark_bar().encode(
    x='Category',
    y='Product Prices',
    tooltip=['Category', 'Product Prices']
).properties(
    title='Average Prices per Category',
    width=500
)

# Display the chart when a button is clicked
if st.session_state.cart:
    st.altair_chart(bar_chart, use_container_width=True)




# import streamlit as st
# import pandas as pd
# import altair as alt
# from PIL import Image

# # Read data from CSV file
# df = pd.read_csv("products.csv")

# # Convert Product Prices to integers
# df["Product Prices"] = df["Product Prices"].str.replace("₮", "").str.replace(",", "").astype(int)

# # Classify into Ice Creams
# ice_cream_keywords = ['шоколадтай зайрмаг', 'гүзээлзгэнэтэй зайрмаг', 'сүүтэй зайрмаг']
# df.loc[df['Product Names'].str.lower().str.contains('|'.join(ice_cream_keywords), case=False), 'Category'] = 'Ice Creams'

# # Classify into Snacks
# snack_keywords = ['чийз стик', 'СКВИД РИНГС', 'шарсан тахиа']
# df.loc[df['Product Names'].str.lower().str.contains('|'.join(snack_keywords), case=False), 'Category'] = 'Snacks'

# # Classify into Burgers
# burger_keywords = ['тери', 'бүлгүги', 'бийф', 'шримп', 'хаш бийф', 'чийз', 'хамбургер', 'чекин', 'хот криспи']
# df.loc[df['Product Names'].str.lower().str.contains('|'.join(burger_keywords), case=False) & ~df['Category'].isin(['Ice Creams', 'Snacks']), 'Category'] = 'Burgers'

# # Classify into Beverages
# beverage_keywords = ['ice tea', 'seabuckthorn', 'tornado', 'mirinda', 'mount dew', '7up', 'pepsi']
# df.loc[df['Product Names'].str.contains('|'.join(beverage_keywords), case=False), 'Category'] = 'Beverages'

# # Classify into Sets
# set_keywords = ['set']
# df.loc[df['Product Names'].str.contains('|'.join(set_keywords), case=False), 'Category'] = 'Sets'

# # Drop rows with NaN values in the 'Category' column
# df = df.dropna(subset=['Category'])

# # Function to display item images
# def display_image(image_path):
#     image = Image.open(image_path)
#     st.image(image, caption='', use_column_width=True)

# # Streamlit App
# st.title("Burger Suggester")

# # Display available categories (excluding NaN)
# categories = df['Category'].unique()
# selected_category = st.selectbox("Select a category:", categories)

# # Filter DataFrame based on selected category
# filtered_df = df[df['Category'] == selected_category]

# # Cart Section
# st.sidebar.title("Items in your cart")  # Change the heading here

# # Initialize cart as a session state variable
# if 'cart' not in st.session_state:
#     st.session_state.cart = []

# # Initialize total cost
# total_cost = 0

# # Budget Section
# budget = st.sidebar.number_input("Enter your budget in Tugruk", min_value=1000, step=1000)

# # Display common item image
# image_path = "images/image.jpg"
# display_image(image_path)

# # Buttons for each item in the selected category
# for index, row in filtered_df.iterrows():
#     if row['Product Prices'] <= budget and budget >= 0:
#         # Use a unique key for each button
#         button_key = f"button_{row['Product Names']}"
#         # Display item image
#         image_path = f"images/{row['Product Names']}.jpg"
#         display_image(image_path)
#         if st.button(f"Add {row['Product Names']} (₮{row['Product Prices']})", key=button_key):
#             # Add the selected item to the session state cart
#             st.session_state.cart.append({'name': row['Product Names'], 'price': row['Product Prices']})
#             # Deduct the item price from the budget
#             budget -= row['Product Prices']
#             # Update the total cost
#             total_cost += row['Product Prices']

# # Buttons to remove each item from the cart
# remove_buttons = []
# for item in st.session_state.cart:
#     # Use a unique key for each remove button
#     remove_button_key = f"remove_button_{item['name']}"
#     remove_buttons.append(st.button(f"Remove {item['name']} (₮{item['price']})", key=remove_button_key))

# # Remove items from the cart based on remove buttons
# for i in reversed(range(len(st.session_state.cart))):
#     if remove_buttons[i]:
#         # Remove the selected item from the session state cart
#         removed_item = st.session_state.cart.pop(i)
#         # Add back the item price to the budget
#         budget += removed_item['price']
#         # Update the total cost
#         total_cost -= removed_item['price']

# # Display selected items in the cart
# if st.session_state.cart:
#     st.sidebar.write("### Selected Items:")
#     for item in st.session_state.cart:
#         st.sidebar.write(f"{item['name']} (₮{item['price']})")
#     st.sidebar.write("### Total Cost:")
#     st.sidebar.write(total_cost)
#     st.sidebar.write("### Remaining Budget:")
#     st.sidebar.write(budget)

#     # Alert if remaining budget is less than the cost of the cheapest item
#     if budget < filtered_df['Product Prices'].min():
#         st.warning("Your remaining budget is not sufficient to buy any more items!")

# # Analysis Section
# st.title("Analysis")

# # Bar chart of average prices per category
# avg_prices = df.groupby('Category')['Product Prices'].mean().reset_index()
# bar_chart = alt.Chart(avg_prices).mark_bar().encode(
#     x='Category',
#     y='Product Prices',
#     tooltip=['Category', 'Product Prices']
# ).properties(
#     title='Average Prices per Category',
#     width=500
# )

# # Display the chart when a button is clicked
# if st.session_state.cart:
#     st.altair_chart(bar_chart, use_container_width=True)
