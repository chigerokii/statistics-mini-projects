# Статистика для бизнеса: мини-проекты

🇷🇺 Русский · [🇬🇧 English](#-english)

Два компактных учебных проекта с прикладной статистикой: A/B-тест и оценка риска.

| Проект | Задача | Методы | Результат |
|---|---|---|---|
| [A/B-тест: средний чек и ARPU](ab-test-average-check/ab_test_average_check.ipynb) | Повлияло ли изменение на средний чек? | Проверка корректности сплита (баланс групп, дубликаты, пересечения пользователей), выбросы по IQR, отчёт по метрикам, t-тест | ARPU 2,02 vs 2,04, p = 0,67: эффекта нет |
| [Меры риска в автостраховании](insurance-risk-measures/insurance_risk_measures.ipynb) | Какие группы клиентов самые рисковые для страховщика? | Дисперсия, СКО, положительная и отрицательная полудисперсия, максимальный ущерб, рисковый капитал (VaR 95%) | Женщины и штат 07 рискованнее остальных групп. Лучшая мера в этой задаче — рисковый капитал |

## A/B-тест: средний чек и ARPU

- **Данные:** ~10 тыс. заказов, группы `control` и `variant`.
- **Проверка сплита:** группы сбалансированы, дубликаты удалены, пользователи, попавшие в обе группы, исключены. Это частая ошибка, которую важно ловить до расчёта метрик.
- **Метрики:** total_orders, total_revenue, unique_users, ARPU, средний чек.
- **Вывод:** различий нет (p = 0,67), раскатывать изменение по этой метрике нет оснований.

## Меры риска в автостраховании

- **Данные:** 6 773 страховые выплаты: штат, рисковый класс, пол, возраст, сумма выплаты.
- Своя функция для **положительной и отрицательной полудисперсии** (во встроенных библиотеках её нет), сводные таблицы мер риска по полу и по штатам.
- **Выводы:** по всем мерам женщины — более рисковая группа. Среди штатов лидирует STATE 07: 4 из 6 мер риска у него максимальные. Для страховщика лучшей мерой выбран **рисковый капитал (95%-я квантиль выплат)**: он описывает возможные потери с заданной вероятностью и устойчив к выбросам.

## Стек

Python · pandas · NumPy · SciPy · seaborn

```bash
pip install pandas numpy scipy seaborn matplotlib openpyxl jupyter
```

---

## 🇬🇧 English

**Business statistics: two mini-projects**

- **A/B test on average order value and ARPU.** Validated the split (group balance, duplicates, users exposed to both variants), removed outliers with the IQR rule, built a metrics report and ran a t-test. ARPU was 2.02 vs 2.04 with p = 0.67, so there is no significant effect.
- **Risk measures in car insurance.** 6,773 claims; variance, standard deviation, upper and lower semivariance (custom function), maximum loss and VaR at 95%, compared by gender and state. Female policyholders and state 07 are the riskiest groups. VaR was chosen as the most suitable measure because it is robust to outliers and directly interpretable as a loss level.

**Stack:** Python, pandas, NumPy, SciPy, seaborn.
