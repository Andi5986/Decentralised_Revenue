import numpy as np

def calculate_payment_per_unit(row, base_price, active_user_factor, task_age_factor, total_task_factor, ether_price_factor):
    """
    Calculate the payment per unit task.
    """
    active_users = row['Active Users']
    task_age = row['Total Tasks'] - row['New Tasks']
    total_tasks = row['Total Tasks']
    ether_price = row['Ether to USD']

    return (
        base_price
        - active_user_factor * np.log(active_users + 1)
        + task_age_factor * np.log(task_age + 1)
        + total_task_factor * np.log(total_tasks + 1)
        - ether_price_factor * np.log(ether_price + 1)
    )

