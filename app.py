import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Example data
employees = pd.DataFrame({
    'ID': range(1, 11),
    'Name': ['Employee ' + str(i) for i in range(1, 11)],
    'Role': ['Cleaner'] * 5 + ['Supervisor'] * 5,
    'Contact': ['contact' + str(i) + '@example.com' for i in range(1, 11)],
    'Status': ['Active'] * 10,
    'Hire Date': [datetime(2023, 1, i + 1) for i in range(10)],
    'Salary': [3000 + i * 100 for i in range(10)]
})

locations = pd.DataFrame({
    'ID': range(1, 11),
    'Name': ['Location ' + str(i) for i in range(1, 11)],
    'Address': ['Address ' + str(i) for i in range(1, 11)],
    'Status': ['Operational'] * 10,
    'Type': ['Office'] * 5 + ['Residential'] * 5,
    'Square Footage': [1000 + i * 100 for i in range(10)]
})

inventory = pd.DataFrame({
    'ID': range(1, 11),
    'Item': ['Item ' + str(i) for i in range(1, 11)],
    'Quantity': [10] * 10,
    'Location': ['Location ' + str(i % 10 + 1) for i in range(1, 11)],
    'Category': ['Cleaning Supplies'] * 10,
    'Last Updated': [datetime(2023, 1, i + 1) for i in range(10)],
    'Cost': [5.0 + i for i in range(10)]
})

checklists = {
    'Checklist ' + str(i): ['Task ' + str(j) for j in range(1, 11)] for i in range(1, 11)
}

# Streamlit App
st.title('Cleaning Business Management App')

# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Select a page:', ['Home', 'Employees', 'Locations', 'Inventory', 'Checklists'])

# Home page
if page == 'Home':
    st.header('Welcome to the Cleaning Business Management App')
    st.write('Use the sidebar to navigate through the app.')
    st.write('This app helps you manage your cleaning business effectively, providing features for managing employees, locations, inventory, and cleaning checklists.')
    st.subheader('Statistics')
    st.metric('Total Employees', employees.shape[0])
    st.metric('Total Locations', locations.shape[0])
    st.metric('Total Inventory Items', inventory.shape[0])
    st.metric('Total Checklists', len(checklists))
    
    st.subheader('Monthly Summary')
    monthly_summary = pd.DataFrame({
        'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'Revenue': np.random.randint(10000, 20000, size=12),
        'Expenses': np.random.randint(5000, 10000, size=12)
    })
    st.write(monthly_summary)
    st.line_chart(monthly_summary.set_index('Month'))

# Employees page
elif page == 'Employees':
    st.header('Employees Management')
    st.write('### Employee List')
    st.write(employees)

    st.write('### Add New Employee')
    with st.form('add_employee'):
        name = st.text_input('Name')
        role = st.selectbox('Role', ['Cleaner', 'Supervisor'])
        contact = st.text_input('Contact')
        status = st.selectbox('Status', ['Active', 'Inactive'])
        hire_date = st.date_input('Hire Date')
        salary = st.number_input('Salary', min_value=0)
        submitted = st.form_submit_button('Add Employee')
        if submitted:
            new_id = employees['ID'].max() + 1
            employees = employees.append({'ID': new_id, 'Name': name, 'Role': role, 'Contact': contact, 'Status': status, 'Hire Date': hire_date, 'Salary': salary}, ignore_index=True)
            st.success('Employee added successfully!')
            st.write(employees)

    st.write('### Update Employee Status')
    with st.form('update_employee_status'):
        emp_id = st.number_input('Employee ID', min_value=1, max_value=int(employees['ID'].max()))
        new_status = st.selectbox('New Status', ['Active', 'Inactive'])
        new_salary = st.number_input('New Salary', min_value=0)
        submitted = st.form_submit_button('Update Status and Salary')
        if submitted:
            employees.loc[employees['ID'] == emp_id, 'Status'] = new_status
            employees.loc[employees['ID'] == emp_id, 'Salary'] = new_salary
            st.success('Employee status and salary updated successfully!')
            st.write(employees)

# Locations page
elif page == 'Locations':
    st.header('Locations Management')
    st.write('### Locations List')
    st.write(locations)

    st.write('### Add New Location')
    with st.form('add_location'):
        name = st.text_input('Location Name')
        address = st.text_input('Address')
        status = st.selectbox('Status', ['Operational', 'Closed'])
        location_type = st.selectbox('Type', ['Office', 'Residential'])
        square_footage = st.number_input('Square Footage', min_value=0)
        submitted = st.form_submit_button('Add Location')
        if submitted:
            new_id = locations['ID'].max() + 1
            locations = locations.append({'ID': new_id, 'Name': name, 'Address': address, 'Status': status, 'Type': location_type, 'Square Footage': square_footage}, ignore_index=True)
            st.success('Location added successfully!')
            st.write(locations)

    st.write('### Update Location Status')
    with st.form('update_location_status'):
        loc_id = st.number_input('Location ID', min_value=1, max_value=int(locations['ID'].max()))
        new_status = st.selectbox('New Status', ['Operational', 'Closed'])
        new_square_footage = st.number_input('New Square Footage', min_value=0)
        submitted = st.form_submit_button('Update Status and Square Footage')
        if submitted:
            locations.loc[locations['ID'] == loc_id, 'Status'] = new_status
            locations.loc[locations['ID'] == loc_id, 'Square Footage'] = new_square_footage
            st.success('Location status and square footage updated successfully!')
            st.write(locations)

# Inventory page
elif page == 'Inventory':
    st.header('Inventory Management')
    st.write('### Inventory List')
    st.write(inventory)

    st.write('### Add New Inventory Item')
    with st.form('add_inventory'):
        item = st.text_input('Item Name')
        quantity = st.number_input('Quantity', min_value=1)
        location = st.selectbox('Location', locations['Name'])
        category = st.text_input('Category')
        last_updated = st.date_input('Last Updated')
        cost = st.number_input('Cost', min_value=0.0, format="%.2f")
        submitted = st.form_submit_button('Add Inventory Item')
        if submitted:
            new_id = inventory['ID'].max() + 1
            inventory = inventory.append({'ID': new_id, 'Item': item, 'Quantity': quantity, 'Location': location, 'Category': category, 'Last Updated': last_updated, 'Cost': cost}, ignore_index=True)
            st.success('Inventory item added successfully!')
            st.write(inventory)

    st.write('### Update Inventory Quantity')
    with st.form('update_inventory_quantity'):
        inv_id = st.number_input('Inventory ID', min_value=1, max_value=int(inventory['ID'].max()))
        new_quantity = st.number_input('New Quantity', min_value=1)
        new_cost = st.number_input('New Cost', min_value=0.0, format="%.2f")
        last_updated = st.date_input('Last Updated')
        submitted = st.form_submit_button('Update Quantity and Cost')
        if submitted:
            inventory.loc[inventory['ID'] == inv_id, 'Quantity'] = new_quantity
            inventory.loc[inventory['ID'] == inv_id, 'Cost'] = new_cost
            inventory.loc[inventory['ID'] == inv_id, 'Last Updated'] = last_updated
            st.success('Inventory quantity and cost updated successfully!')
            st.write(inventory)

# Checklists page
elif page == 'Checklists':
    st.header('Cleaning Checklists/Project Management')
    
    checklist_selection = st.selectbox('Select a checklist', list(checklists.keys()))
    st.write('### Tasks for ' + checklist_selection)
    st.write(checklists[checklist_selection])

    st.write('### Add New Checklist')
    with st.form('add_checklist'):
        checklist_name = st.text_input('Checklist Name')
        tasks = st.text_area('Tasks (separate by commas)').split(',')
        assigned_employee = st.selectbox('Assign to Employee', employees['Name'])
        due_date = st.date_input('Due Date')
        submitted = st.form_submit_button('Add Checklist')
        if submitted:
            checklists[checklist_name] = tasks
            st.success(f'Checklist "{checklist_name}" added successfully and assigned to {assigned_employee} with due date {due_date}!')
            st.write(checklists)

    st.write('### Update Checklist')
    with st.form('update_checklist'):
        checklist_to_update = st.selectbox('Select a checklist to update', list(checklists.keys()))
        updated_tasks = st.text_area('Updated Tasks (separate by commas)').split(',')
        new_assigned_employee = st.selectbox('Reassign to Employee', employees['Name'])
        new_due_date = st.date_input('New Due Date')
        submitted = st.form_submit_button('Update Checklist')
        if submitted:
            checklists[checklist_to_update] = updated_tasks
            st.success(f'Checklist "{checklist_to_update}" updated successfully and reassigned to {new_assigned_employee} with new due date {new_due_date}!')
            st.write(checklists)

st.sidebar.write('---')
st.sidebar.header('Example Data')
if st.sidebar.button('Show Employees'):
    st.sidebar.write(employees)
if st.sidebar.button('Show Locations'):
    st.sidebar.write(locations)
if st.sidebar.button('Show Inventory'):
    st.sidebar.write(inventory)
if st.sidebar.button('Show Checklists'):
    st.sidebar.write(checklists)
