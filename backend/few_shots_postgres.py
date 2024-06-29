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
    },
    {
        'User question': "Who all are working for NC?",
        'SQL Query': "SELECT full_name FROM employees WHERE navikenz_id IN (SELECT employee_navikenz_id FROM project_peopleallocation WHERE customer_id = (SELECT id FROM customer WHERE name LIKE '%NC%'));",
        'SQL Response': ""
    },
    {
        'User question': "Give me project status of Project51?",
        'SQL Query': "select * from project_status where project_id in (select id from project_detail where project_name='project51');",
        'SQL Response': ""
    },
    {
        'User question': "who all did not fill timesheets for the all the XYZ customer projects?",
        'SQL Query': "SELECT employee_navikenz_id FROM timesheet_whutil WHERE project_id in (SELECT id FROM project_detail WHERE customer_id = (SELECT id FROM customer WHERE name LIKE '%XYZ%')) AND total = 0;",
        'SQL Response': "There is no employee left to fill the timesheets for XYZ project"
    },
    {
        'User question': "Give me the list of resources who are working on projects which are worth more than $25K in revenue for each month. ",
        'SQL Query': "SELECT r.title, r.description FROM resources r JOIN project_team pt ON r.id = pt.proj_team_bus_func_id JOIN project_revenue pr ON pt.project_id = pr.project_id WHERE pr.jan > 25000 AND pr.feb > 25000 AND pr.mar > 25000 AND pr.apr > 25000 AND pr.may > 25000 AND pr.jun > 25000 AND pr.jul > 25000 AND pr.aug > 25000 AND pr.sep > 25000 AND pr.oct > 25000 AND pr.nov > 25000 AND pr.dec > 25000 ORDER BY pr.fy, pr.jan, pr.feb, pr.mar, pr.apr, pr.may, pr.jun, pr.jul, pr.aug, pr.sep, pr.oct, pr.nov, pr.dec;",
        'SQL Response': ""
    },
    {
        'User question':"Who is the Architect working on BW?",
        'SQL Query':"select full_name from employees where navikenz_id in (select employee_navikenz_id from project_peopleallocation where role like '%Architect%' and customer_id=(select id from customer where name like '%BW%'));",
        'SQL Response': ""
    }
]