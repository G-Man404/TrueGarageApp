def check_order_status_text(order):
    tasks_text = ""
    for i in range(len(order['tasks'])):
        task = order['tasks'][i]
        tasks_text += f"{i+1}. {task['work']['name']}\n{task['work']['price']}руб. х {task['count']}шт.\n{task['status']}\n"
    supplies_text = ""
    for i in range(len(order['supplies'])):
        supplies = order['supplies'][i]
        supplies_text += f"{i + 1}. {supplies['supply']['name']}\n{supplies['supply']['price']}руб. х {supplies['count']}шт.\n"
    total = sum(task['work']['price'] * task['count'] for task in order['tasks']) + sum(supplies['supply']['price'] * supplies['count'] for supplies in order['supplies'])
    order_status = ""
    if order["status"] == "В очереди":
        order_status = "💤<b>В очереди</b>"
    elif order["status"] == "В работе":
        order_status = "🛠<b>В работе</b>"
    elif order["status"] == "Готов":
        order_status = "✅<b>Готов</b>"
    text = f"""
Заказ-наряд: <b>{order['number']}</b>\n
Статусы работ: 
{order_status}\n
<i>Список работ</i>:
{tasks_text}
<i>Список запчастей</i>:
{supplies_text}
Итого по заказ-наряду:
{total} руб.
    """
    return text