import uniform_distribution as ud
import erlang_distribution as ed


def main():
    while True:
        print(
            "\n\nВыберите закон распределения: \n"
            "   1) Равномерное распределение;\n"
            "   2) Распределение Эрланга;\n"
            "   0) Завершить выполнение программы.\n"
        )
        try:
            menu_item = int(input("Введите номер пункта меню: "))
        except ValueError:
            print("Ошибка. Введено некорректное значение пункта меню!")
            continue

        match menu_item:
            case 1:
                uniform_params = ud.get_interval_a_b()
                if uniform_params is None:
                    continue
                ud.draw_uniform_distribution_graphs(ud.UniformDistribution(*uniform_params))
            case 2:
                erlang_params = ed.get_k_and_lambda()
                if erlang_params is None:
                    continue
                ed.draw_erlang_distribution_graphs(ed.ErlangDistribution(*erlang_params))
            case 0:
                exit(0)
            case _:
                print("Ошибка. Выбран неверный пункт меню!")


if __name__ == '__main__':
    main()
