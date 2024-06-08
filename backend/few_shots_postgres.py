few_shots_postgresnew = [
    {
        'User question': "give me project details of projects of customer2",
        'SQL Query': "SELECT id, project_name, billing_type, project_description,pm_nav_id as project_manager, start_date, end_date FROM project_detail WHERE customer_id = 2;",
        'SQL Response': "Here are the project details of projects for customer 2: 1. Project Name: project1 - Billing Type: Fixed Price - Project Description: project_description - Project Type: Engineering - Start Date: Not specified - End Date: Not specified - Project Manager: NAV00005 2. Project Name: project6 - Billing Type: Time & Material - Project Description: project_description - Project Type: Consulting - Start Date: Not specified - End Date: Not specified - Project Manager: NAV00003. Please let me know if you need more information."
    },
    {
        'User question': "give me project details and it's total revenue in year 2024 for customer11",
        'SQL Query': "SELECT pd.id, pd.project_name, pd.billing_type, pd.project_description, pd.pm_nav_id as 'Project Manager', pd.start_date, pd.end_date, SUM(pr.total) AS total_revenue FROM project_detail pd JOIN project_revenue pr ON pr.project_id = pd.id WHERE pd.customer_id = 11 AND pr.fy=2024 GROUP BY pd.id;",
        'SQL Response': "The project details and total revenue for customer 11 in the year 2024 are as follows:\n - Project ID: 46\n - Project Name: project46\n - Billing Type: Time & Material\n - Project Description: project_description\n - Project Manager: NAV00005\n - Start Date: Not specified\n - End Date: Not specified\n - Total Revenue: $641.0\n\nIf you need more information or have any other queries, feel free to ask!"
    }

    
]