# Тестовое задание для HardQode - API для системы обучения

## Описание
Простое API на Django Rest Framework + Django для вывода информации о продуктах, уроках и статистике 
просмотра уроков пользователями.

## Установка
1. Копируем репозиторий
2. Создаем виртуальное окружение `python -m venv env`
3. Устанавливаем зависимости `pip install -r requirements.txt`
4. Загружаем начальные данные в БД `python manage.py loaddata products lessons user_lesson_info user_products users`

## Доступные endpoint API
- `/api/<int:user_id>/products/` - вывод списка всех уроков по всем продуктам пользователя
- `/api/<int:user_id>/products/<int:product_id>/` - вывод списка всех уроков по выбранному продукту пользователя
- `/api/statistics/` - вывод статистики по продуктам

## ТЗ:

### Построение архитектуры(3 балла)
В этом задании у нас есть три бизнес-задачи на хранение:
1.	Создать сущность продукта. У продукта должен быть владелец. Необходимо добавить сущность для сохранения доступов к продукту для пользователя.
2.	Создать сущность урока. Урок может находиться в нескольких продуктах одновременно. В уроке должна быть базовая информация: название, ссылка на видео, длительность просмотра (в секундах).
3.	Урок могут просматривать множество пользователей. Необходимо для каждого фиксировать время просмотра и фиксировать статус “Просмотрено”/”Не просмотрено”. Статус “Просмотрено” проставляется, если пользователь просмотрел 80% ролика.

### Написание запросов(7 баллов)
В этом пункте потребуется использовать выполненную вами в прошлом задании архитектуру:
1.	Реализовать API для выведения списка всех уроков по всем продуктам к которым пользователь имеет доступ, с выведением информации о статусе и времени просмотра.
2.	Реализовать API с выведением списка уроков по конкретному продукту к которому пользователь имеет доступ, с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика.
3.	Реализовать API для отображения статистики по продуктам. Необходимо отобразить список всех продуктов на платформе, к каждому продукту приложить информацию:
    1.	Количество просмотренных уроков от всех учеников.
    2.	Сколько в сумме все ученики потратили времени на просмотр роликов.
    3.	Количество учеников занимающихся на продукте.
    4.	Процент приобретения продукта (рассчитывается исходя из количества полученных доступов к продукту деленное на общее количество пользователей на платформе).

