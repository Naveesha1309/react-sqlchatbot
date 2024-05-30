few_shots_groqnew = [
    {
        'User question': "Tell me total number of female students studying artificial intelligence/ai",
        'SQL Query': "SELECT COUNT(*) FROM employees WHERE `gender` = 'Female' AND `department_id` = (SELECT `department_id` FROM departments WHERE `department_name` = 'Data Engineering')",
        'SQL Response': "There are total 4 female students studying artificial intelligence/AI (Data Engineering Batch)"
    }
]