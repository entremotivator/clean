import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Initialize inventory data
inventory_data = [
    {"Item Name": "Disinfectant Spray", "Category": "Disinfectant", "Quantity": 50, "Price": 5.99, "Supplier": "Supplier A", "Brand": "Brand X", "Expiry Date": "2025-01-01", "Storage Location": "Warehouse 1"},
    {"Item Name": "Glass Cleaner", "Category": "Window Cleaning", "Quantity": 30, "Price": 3.49, "Supplier": "Supplier B", "Brand": "Brand Y", "Expiry Date": "2024-06-01", "Storage Location": "Warehouse 2"},
    {"Item Name": "Floor Cleaner", "Category": "Floor Cleaning", "Quantity": 20, "Price": 7.99, "Supplier": "Supplier C", "Brand": "Brand Z", "Expiry Date": "2023-12-31", "Storage Location": "Warehouse 3"},
    {"Item Name": "Hand Sanitizer", "Category": "Hand Cleaning", "Quantity": 100, "Price": 2.99, "Supplier": "Supplier D", "Brand": "Brand A", "Expiry Date": "2025-07-01", "Storage Location": "Warehouse 1"},
    {"Item Name": "Mop", "Category": "Cleaning Tools", "Quantity": 40, "Price": 10.99, "Supplier": "Supplier E", "Brand": "Brand B", "Expiry Date": "N/A", "Storage Location": "Warehouse 2"},
    {"Item Name": "Broom", "Category": "Cleaning Tools", "Quantity": 60, "Price": 6.49, "Supplier": "Supplier F", "Brand": "Brand C", "Expiry Date": "N/A", "Storage Location": "Warehouse 3"},
    {"Item Name": "Paper Towels", "Category": "Paper Products", "Quantity": 200, "Price": 0.99, "Supplier": "Supplier G", "Brand": "Brand D", "Expiry Date": "2026-01-01", "Storage Location": "Warehouse 1"},
    {"Item Name": "Trash Bags", "Category": "Waste Management", "Quantity": 100, "Price": 4.99, "Supplier": "Supplier H", "Brand": "Brand E", "Expiry Date": "N/A", "Storage Location": "Warehouse 2"},
    {"Item Name": "Bleach", "Category": "Disinfectant", "Quantity": 80, "Price": 3.99, "Supplier": "Supplier I", "Brand": "Brand F", "Expiry Date": "2024-05-01", "Storage Location": "Warehouse 3"},
    {"Item Name": "Scrub Brush", "Category": "Cleaning Tools", "Quantity": 50, "Price": 2.49, "Supplier": "Supplier J", "Brand": "Brand G", "Expiry Date": "N/A", "Storage Location": "Warehouse 1"}
]

# Convert the dictionary to a DataFrame
data = pd.DataFrame(inventory_data)

# Initialize restock history
restock_history = []

# App title
st.title('Cleaning Product Supply Inventory')

# Display the data
st.subheader('Inventory Overview')
st.dataframe(data)

# Filter by category
categories = np.append(['All'], data['Category'].unique())
selected_category = st.selectbox('Select a Category', categories)
if selected_category != 'All':
    filtered_data = data[data['Category'] == selected_category]
else:
    filtered_data = data
st.subheader(f'Products in Category: {selected_category}')
st.dataframe(filtered_data)

# Search by item name
search_term = st.text_input('Search for a product')
if search_term:
    search_results = data[data['Item Name'].str.contains(search_term, case=False)]
    st.subheader(f'Search Results for: {search_term}')
    st.dataframe(search_results)

# Add new item
st.sidebar.header('Add New Item')
new_item_name = st.sidebar.text_input('Item Name')
new_item_category = st.sidebar.selectbox('Category', data['Category'].unique())
new_item_quantity = st.sidebar.number_input('Quantity', min_value=0)
new_item_price = st.sidebar.number_input('Price', min_value=0.0, format="%.2f")
new_item_supplier = st.sidebar.text_input('Supplier')
new_item_brand = st.sidebar.text_input('Brand')
new_item_expiry_date = st.sidebar.date_input('Expiry Date')
new_item_storage_location = st.sidebar.text_input('Storage Location')

if st.sidebar.button('Add Item'):
    new_item = {
        'Item Name': new_item_name,
        'Category': new_item_category,
        'Quantity': new_item_quantity,
        'Price': new_item_price,
        'Supplier': new_item_supplier,
        'Brand': new_item_brand,
        'Expiry Date': str(new_item_expiry_date),
        'Storage Location': new_item_storage_location
    }
    data = data.append(new_item, ignore_index=True)
    st.success('Item added successfully!')
    st.experimental_rerun()

# Edit and delete functionality
st.sidebar.header('Edit or Delete Item')
item_to_edit = st.sidebar.selectbox('Select Item to Edit/Delete', data['Item Name'].unique())
selected_item = data[data['Item Name'] == item_to_edit].iloc[0]

edit_item_name = st.sidebar.text_input('Item Name', selected_item['Item Name'])
edit_item_category = st.sidebar.selectbox('Category', data['Category'].unique(), index=list(data['Category'].unique()).index(selected_item['Category']))
edit_item_quantity = st.sidebar.number_input('Quantity', min_value=0, value=selected_item['Quantity'])
edit_item_price = st.sidebar.number_input('Price', min_value=0.0, format="%.2f", value=selected_item['Price'])
edit_item_supplier = st.sidebar.text_input('Supplier', selected_item['Supplier'])
edit_item_brand = st.sidebar.text_input('Brand', selected_item['Brand'])
edit_item_expiry_date = st.sidebar.date_input('Expiry Date', pd.to_datetime(selected_item['Expiry Date']) if selected_item['Expiry Date'] != 'N/A' else None)
edit_item_storage_location = st.sidebar.text_input('Storage Location', selected_item['Storage Location'])

if st.sidebar.button('Update Item'):
    data.loc[data['Item Name'] == item_to_edit, :] = [
        edit_item_name, edit_item_category, edit_item_quantity, edit_item_price,
        edit_item_supplier, edit_item_brand, str(edit_item_expiry_date), edit_item_storage_location
    ]
    st.success('Item updated successfully!')
    st.experimental_rerun()

if st.sidebar.button('Delete Item'):
    data = data[data['Item Name'] != item_to_edit]
    st.success('Item deleted successfully!')
    st.experimental_rerun()

# Summary statistics
st.subheader('Summary Statistics')
st.write(data.describe())

# Low stock warning
low_stock_threshold = st.sidebar.number_input('Low Stock Threshold', min_value=0, value=10)
low_stock_items = data[data['Quantity'] < low_stock_threshold]
st.subheader(f'Items with Stock Below {low_stock_threshold}')
st.dataframe(low_stock_items)
for index, row in low_stock_items.iterrows():
    st.warning(f"Low stock for {row['Item Name']} - only {row['Quantity']} left!")

# Restock history
st.sidebar.header('Restock History')
restock_item = st.sidebar.selectbox('Select Item to Restock', data['Item Name'].unique())
restock_quantity = st.sidebar.number_input('Restock Quantity', min_value=0)
if st.sidebar.button('Restock Item'):
    data.loc[data['Item Name'] == restock_item, 'Quantity'] += restock_quantity
    restock_history.append({"Item Name": restock_item, "Restock Quantity": restock_quantity, "Date": str(datetime.now())})
    st.success('Item restocked successfully!')
    st.experimental_rerun()

if restock_history:
    st.subheader('Restock History')
    st.dataframe(pd.DataFrame(restock_history))

# Export to CSV
st.sidebar.header('Export Data')
if st.sidebar.button('Export to CSV'):
    data.to_csv('inventory_data.csv', index=False)
    st.success('Data exported to inventory_data.csv')

# Visualization: Category Distribution
st.subheader('Category Distribution')
category_counts = data['Category'].value_counts()
fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values, labels={'x': 'Category', 'y': 'Count'}, title='Number of Items per Category')
st.plotly_chart(fig)

# Visualization: Stock Levels
st.subheader('Stock Levels')
fig = px.bar(data, x='Item Name', y='Quantity', labels={'Quantity': 'Quantity', 'Item Name': 'Item Name'}, title='Stock Levels by Item')
st.plotly_chart(fig)
