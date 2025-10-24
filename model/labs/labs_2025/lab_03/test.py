import numpy as np
import matplotlib.pyplot as plt

def plot_uniform_pdf(a, b):
    """
    Строит график функции плотности равномерного распределения на отрезке [a, b].
    
    Параметры:
    a (float): нижняя граница распределения
    b (float): верхняя граница распределения
    """
    if a >= b:
        raise ValueError("Нижняя граница a должна быть меньше верхней границы b")
    
    # Значения x для построения графика
    x = np.linspace(a - (b - a)*0.1, b + (b - a)*0.1, 500)
    
    # Функция плотности
    pdf = np.where((x >= a) & (x <= b), 1 / (b - a), 0)
    
    # Построение графика
    plt.figure(figsize=(8, 4))
    plt.plot(x, pdf, color='blue', lw=2)
    plt.fill_between(x, pdf, alpha=0.2, color='blue')
    plt.title(f"Функция плотности равномерного распределения\n[a={a}, b={b}]")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()
    
plot_uniform_pdf(0, 5)

