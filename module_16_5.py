# Домашнее задание по теме "Шаблонизатор Jinja 2."

from fastapi import FastAPI, HTTPException, Request, Path, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated, List

# Создано приложение(объект) FastAPI
app = FastAPI()

# Шаблоны main.html, users.html в папке Templates_lesson в проекте
# объект Jinja2Templates, в качестве папки шаблонов - Templates_lesson
templates = Jinja2Templates(directory='Templates_lesson')

# Создайте пустой список
users = []

# Создание класса(модели) User, наследованный от BaseModel, который содержит поля id, username, age
class User(BaseModel):
    id: int
    username: str
    age: int


# get запрос по маршруту '/users'
#  Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
#  TemplateResponse должен подключать ранее заготовленный шаблон
#  'users.html', а также передавать в него request и список users.
#  Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
@app.get('/')
async def get_main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# get запрос по маршруту '/user/{user_id}'
# Функция по этому запросу теперь принимает аргумент request и user_id.
# Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
# а также передавать в него request и одного из пользователей - user.
# Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
@app.get('/user/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    for i in users:
        if i.id == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": i})
        raise HTTPException(status_code=404, detail=f'Пользователь не найден')

# post запрос по маршруту '/user/{username}/{age}',
# Добавляет в список users объект User.
# id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
# Все остальные параметры объекта User - переданные в функцию username и age соответственно.
# В конце возвращает созданного пользователя.
@app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str,
        Path(max_length=30, description='Введите имя')],
        age: Annotated[int,
        Path(le=200, description='Введите возраст')]):
    # присвоение следующего id пользователю
    user_id = len(users) + 1
    # присвоение значений переменной user
    user = User(id=user_id, username=username, age=age)
    # добавление новой записи в конец списка users
    users.append(user)
    return f'Пользователь {user.username} id={user.id} возраст {user.age} зарегестрирован'

# put запрос по маршруту '/user/{user_id}/{username}/{age}',
#     Обновляет username и age пользователя, если пользователь
#     с таким user_id есть в списке users и возвращает его.
#     В случае отсутствия пользователя выбрасывается исключение
#     HTTPException с описанием "User was not found" и кодом 404.
@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: Annotated[int, Path(description='Введите ID')],
                   username: Annotated[str, Path(max_length=30, description='Введите имя')],
                   age: Annotated[int, Path(le=1000, description='Введите возраст')]):
    # цикл перебора списка users
    for i in users:
        # сравнение id списка с введенным для коррекции id
        if i.id == user_id:
            # присвоение новых значений
            i.username = username
            i.age = age
            # возврат списка обновленного списка users
            return users
        # исключение в случае отсутствия пользователя с введенным id
        raise HTTPException(status_code=404, detail=f'Пользователь не найден')


# delete запрос по маршруту '/user/{user_id}'
# Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
@app.delete("/user/{user_id}")
def delete_user(user_id: Annotated[int, Path(description='Введите ID')]):
    # цикл итерации по извлечению кортежа из индекса (i) и элемента (user) списка users
    for i, user in enumerate(users):
        # сравнение введенного id с id users
        if user.id == user_id:
            # удаление записи в списке users по найденному id
            del users[i]
            # возврат измененного списка users
            return users
    # исключение в случае отсутствия пользователя с введенным id
    raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} отсутствует")
