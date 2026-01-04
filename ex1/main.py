import pulp


def solve_production_optimization():
    """
    Вирішує задачу лінійного програмування для максимізації виробництва
    Лимонаду та Фруктового соку з урахуванням обмежень ресурсів.
    
    Обмеження:
    - Вода: 2 одиниці на Лимонад + 1 одиниця на Фруктовий сік <= 100
    - Цукор: 1 одиниця на Лимонад <= 50
    - Лимонний сік: 1 одиниця на Лимонад <= 30
    - Пюре з фруктів: 2 одиниці на Фруктовий сік <= 40
    """
    # Створення моделі оптимізації
    model = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)
    
    # Змінні рішення: кількості для виробництва
    lemonade = pulp.LpVariable('Lemonade', lowBound=0, cat='Continuous')
    fruit_juice = pulp.LpVariable('FruitJuice', lowBound=0, cat='Continuous')
    
    # Цільова функція: максимізація загального виробництва
    model += lemonade + fruit_juice, "Total_Products"
    
    # Обмеження ресурсів
    model += 2 * lemonade + 1 * fruit_juice <= 100, "Water_Constraint"
    model += 1 * lemonade <= 50, "Sugar_Constraint"
    model += 1 * lemonade <= 30, "Lemon_Juice_Constraint"
    model += 2 * fruit_juice <= 40, "Mashed_Fruit_Constraint"
    
    # Розв'язання задачі
    model.solve()
    
    # Перевірка статусу рішення
    status = pulp.LpStatus[model.status]
    
    if status == 'Optimal':
        # Витягнення результатів
        lemonade_qty = pulp.value(lemonade)
        fruit_juice_qty = pulp.value(fruit_juice)
        total_production = lemonade_qty + fruit_juice_qty
        
        # Виведення результатів
        print("=" * 50)
        print("РЕЗУЛЬТАТИ ОПТИМІЗАЦІЇ ВИРОБНИЦТВА")
        print("=" * 50)
        print(f"Статус: {status}")
        print(f"\nОптимальний план виробництва:")
        print(f"  Лимонад:      {lemonade_qty:.2f} одиниць")
        print(f"  Фруктовий сік: {fruit_juice_qty:.2f} одиниць")
        print(f"  Всього:       {total_production:.2f} одиниць")
        print("=" * 50)
        
        # Перевірка використання ресурсів
        print("\nВикористання ресурсів:")
        print(f"  Вода:         {2 * lemonade_qty + fruit_juice_qty:.2f} / 100")
        print(f"  Цукор:        {lemonade_qty:.2f} / 50")
        print(f"  Лимонний сік: {lemonade_qty:.2f} / 30")
        print(f"  Пюре з фруктів: {2 * fruit_juice_qty:.2f} / 40")
        
        return {
            'status': status,
            'lemonade': lemonade_qty,
            'fruit_juice': fruit_juice_qty,
            'total': total_production
        }
    else:
        print(f"Оптимізація не вдалася. Статус: {status}")
        return None


if __name__ == "__main__":
    solve_production_optimization()

