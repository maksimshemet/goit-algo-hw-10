import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt


def target_func(x):
    """
    Цільова функція для інтегрування: f(x) = x^2
    
    Args:
        x: значення аргументу
        
    Returns:
        значення функції x^2
    """
    return x**2


def monte_carlo(func, a, b, num_samples=10000):
    """
    Обчислює інтеграл функції методом Монте-Карло.
    
    Метод базується на випадковому вибіркуванні точок у діапазоні [a, b]
    та обчисленні середнього значення функції.
    
    Args:
        func: функція для інтегрування
        a: нижня межа інтегрування
        b: верхня межа інтегрування
        num_samples: кількість випадкових точок (за замовчуванням 10000)
        
    Returns:
        наближене значення інтегралу
    """
    # Генерація випадкових точок у діапазоні [a, b]
    random_x = np.random.uniform(a, b, num_samples)
    
    # Обчислення значень функції у випадкових точках
    random_y = func(random_x)
    
    # Обчислення інтегралу: середнє значення функції * ширина інтервалу
    integral_mc = (b - a) * np.mean(random_y)
    
    return integral_mc


def plot_integration(func, a, b, exact_value, mc_results=None):
    """
    Створює графік функції з виділеною областю інтегрування.
    
    Args:
        func: функція для побудови графіка
        a: нижня межа інтегрування
        b: верхня межа інтегрування
        exact_value: точне значення інтегралу
        mc_results: словник з результатами Монте-Карло (опціонально)
    """
    # Створення діапазону значень для x
    x = np.linspace(-0.5, 2.5, 400)
    y = func(x)
    
    # Створення графіка
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Побудова графіка функції
    ax.plot(x, y, 'r', linewidth=2, label=f'f(x) = x²')
    
    # Заповнення області під кривою
    ix = np.linspace(a, b, 100)
    iy = func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3, label='Область інтегрування')
    
    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    
    # Додавання вертикальних ліній для меж інтегрування
    ax.axvline(x=a, color='gray', linestyle='--', linewidth=1.5, label=f'x = {a}')
    ax.axvline(x=b, color='gray', linestyle='--', linewidth=1.5, label=f'x = {b}')
    
    # Формування заголовка з інформацією про інтеграл
    title = f'Інтегрування f(x) = x² від {a} до {b}\n'
    title += f'Точне значення: {exact_value:.6f}'
    
    if mc_results:
        # Додавання найкращого результату Монте-Карло до заголовка
        best_n = max(mc_results.keys())
        best_result = mc_results[best_n]
        title += f' | Монте-Карло ({best_n:,} точок): {best_result:.6f}'
    
    ax.set_title(title, fontsize=11)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def main():
    """
    Головна функція для обчислення та візуалізації інтегралу.
    """
    # Межі інтегрування
    a = 0  # Нижня межа інтегрування
    b = 2  # Верхня межа інтегрування
    
    # Різні кількості точок для методу Монте-Карло
    sample_sizes = [100, 1000, 10000, 100000, 1000000]
    
    print("=" * 70)
    print("ОБЧИСЛЕННЯ ІНТЕГРАЛУ МЕТОДОМ МОНТЕ-КАРЛО")
    print("=" * 70)
    print(f"Функція: f(x) = x²")
    print(f"Межі інтегрування: [{a}, {b}]\n")
    
    # Обчислення інтегралу методом Монте-Карло для різних кількостей точок
    integrals_mc = {}
    
    for n in sample_sizes:
        integrals_mc[n] = monte_carlo(target_func, a, b, n)
        error = abs(integrals_mc[n] - (8/3))  # Точне значення інтегралу x² від 0 до 2 = 8/3
        print(f"Монте-Карло ({n:>7,} точок): {integrals_mc[n]:.8f} | Похибка: {error:.8f}")
    
    # Обчислення точного значення інтегралу за допомогою scipy
    exact_result, error_estimate = spi.quad(target_func, a, b)
    
    print("\n" + "-" * 70)
    print(f"Точне значення інтегралу (scipy.quad): {exact_result:.10f}")
    print(f"Оцінка похибки: {error_estimate:.2e}")
    print("=" * 70)
    
    # Порівняння результатів
    print("\nПорівняння з точним значенням:")
    for n in sample_sizes:
        relative_error = abs(integrals_mc[n] - exact_result) / exact_result * 100
        print(f"  {n:>7,} точок: похибка {relative_error:.4f}%")
    
    # Візуалізація
    print("\nПобудова графіка...")
    plot_integration(target_func, a, b, exact_result, integrals_mc)
    
    return {
        'exact': exact_result,
        'monte_carlo': integrals_mc
    }


if __name__ == "__main__":
    main()

