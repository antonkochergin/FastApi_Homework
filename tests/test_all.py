# /home/anton-kochergin/Work/FastApi_Homework/tests/test_all.py

import sys
import os
from datetime import datetime

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pydantic import ValidationError
from fastapi_app.src.schemas.posts import PostCreate, PostUpdate, Post
from fastapi_app.src.schemas.users import UserCreate, UserUpdate, User
from fastapi_app.src.schemas.categories import CategoryCreate, CategoryUpdate, Category
from fastapi_app.src.schemas.locations import LocationCreate, LocationUpdate, Location
from fastapi_app.src.schemas.comments import CommentCreate, CommentUpdate, Comment


# ==================== POSTS TESTS ====================

def test_post_create_valid():
    """Тест 1: Создание поста с валидными данными"""
    print("\n" + "=" * 50)
    print("ТЕСТ 1: Валидное создание поста")
    print("=" * 50)

    data = {
        "title": "Мой первый пост",
        "text": "Это текст моего первого поста",
        "pub_date": datetime.now().isoformat(),
        "is_published": True,
        "category_id": 1,
        "location_id": 2,
        "image": "https://example.com/image.jpg"
    }

    try:
        post = PostCreate(**data)
        print("✅ Успех! Пост создан:")
        print(f"   - title: {post.title}")
        print(f"   - text: {post.text[:30]}...")
        print(f"   - category_id: {post.category_id}")
        print(f"   - location_id: {post.location_id}")
        return True
    except ValidationError as e:
        print("❌ Ошибка! Не должно быть валидационной ошибки")
        print(e)
        return False


def test_post_title_too_short():
    """Тест 2: Заголовок слишком короткий (min_length=3)"""
    print("\n" + "=" * 50)
    print("ТЕСТ 2: Заголовок слишком короткий")
    print("=" * 50)

    data = {
        "title": "ab",  # min_length=3
        "text": "Текст поста",
        "pub_date": datetime.now().isoformat(),
        "category_id": 1,
        "location_id": 1
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_post_title_too_long():
    """Тест 3: Заголовок слишком длинный (max_length=256)"""
    print("\n" + "=" * 50)
    print("ТЕСТ 3: Заголовок слишком длинный")
    print("=" * 50)

    data = {
        "title": "a" * 300,  # max_length=256
        "text": "Текст поста",
        "pub_date": datetime.now().isoformat(),
        "category_id": 1,
        "location_id": 1
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_post_missing_required():
    """Тест 4: Отсутствует обязательное поле"""
    print("\n" + "=" * 50)
    print("ТЕСТ 4: Отсутствует обязательное поле (text)")
    print("=" * 50)

    data = {
        "title": "Заголовок",
        # нет text!
        "pub_date": datetime.now().isoformat(),
        "category_id": 1,
        "location_id": 1
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_post_update_valid():
    """Тест 5: Валидное обновление поста"""
    print("\n" + "=" * 50)
    print("ТЕСТ 5: Валидное обновление поста")
    print("=" * 50)

    data = {
        "title": "Новый заголовок",
        "is_published": False
    }

    try:
        update = PostUpdate(**data)
        print("✅ Успех! Данные для обновления созданы:")
        print(f"   - title: {update.title}")
        print(f"   - is_published: {update.is_published}")
        return True
    except ValidationError as e:
        print("❌ Ошибка! Не должно быть валидационной ошибки")
        print(e)
        return False


# ==================== USERS TESTS ====================

def test_user_create_valid():
    """Тест 6: Создание пользователя с валидными данными"""
    print("\n" + "=" * 50)
    print("ТЕСТ 6: Валидное создание пользователя")
    print("=" * 50)

    data = {
        "username": "john_doe",
        "password": "secret123",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_active": True
    }

    try:
        user = UserCreate(**data)
        print("✅ Успех! Пользователь создан:")
        print(f"   - username: {user.username}")
        print(f"   - email: {user.email}")
        print(f"   - first_name: {user.first_name}")
        print(f"   - last_name: {user.last_name}")
        return True
    except ValidationError as e:
        print("❌ Ошибка! Не должно быть валидационной ошибки")
        print(e)
        return False


def test_user_username_too_short():
    """Тест 7: Имя пользователя слишком короткое"""
    print("\n" + "=" * 50)
    print("ТЕСТ 7: Username слишком короткий (min_length=3)")
    print("=" * 50)

    data = {
        "username": "jo",  # min_length=3
        "password": "secret123",
        "email": "john@example.com"
    }

    try:
        UserCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_user_password_too_short():
    """Тест 8: Пароль слишком короткий"""
    print("\n" + "=" * 50)
    print("ТЕСТ 8: Пароль слишком короткий (min_length=8)")
    print("=" * 50)

    data = {
        "username": "john_doe",
        "password": "1234567",  # min_length=8
        "email": "john@example.com"
    }

    try:
        UserCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_user_invalid_email():
    """Тест 9: Невалидный email"""
    print("\n" + "=" * 50)
    print("ТЕСТ 9: Невалидный email")
    print("=" * 50)

    data = {
        "username": "john_doe",
        "password": "secret123",
        "email": "not-an-email"  # невалидный email
    }

    try:
        UserCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== CATEGORIES TESTS ====================

def test_category_create_valid():
    """Тест 10: Создание категории с валидными данными"""
    print("\n" + "=" * 50)
    print("ТЕСТ 10: Валидное создание категории")
    print("=" * 50)

    data = {
        "title": "Новости",
        "slug": "news",
        "description": "Категория для новостей",
        "is_published": True
    }

    try:
        category = CategoryCreate(**data)
        print("✅ Успех! Категория создана:")
        print(f"   - title: {category.title}")
        print(f"   - slug: {category.slug}")
        print(f"   - description: {category.description}")
        return True
    except ValidationError as e:
        print("❌ Ошибка! Не должно быть валидационной ошибки")
        print(e)
        return False


def test_category_slug_invalid():
    """Тест 11: Невалидный slug (только буквы, цифры, дефис и подчеркивание)"""
    print("\n" + "=" * 50)
    print("ТЕСТ 11: Невалидный slug (спецсимволы)")
    print("=" * 50)

    data = {
        "title": "Новости",
        "slug": "news!!!@@@",  # только a-z, 0-9, -, _
        "description": "Категория для новостей",
        "is_published": True
    }

    try:
        CategoryCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== LOCATIONS TESTS ====================

def test_location_create_valid():
    """Тест 12: Создание локации с валидными данными"""
    print("\n" + "=" * 50)
    print("ТЕСТ 12: Валидное создание локации")
    print("=" * 50)

    data = {
        "name": "Москва",
        "is_published": True
    }

    try:
        location = LocationCreate(**data)
        print("✅ Успех! Локация создана:")
        print(f"   - name: {location.name}")
        print(f"   - is_published: {location.is_published}")
        return True
    except ValidationError as e:
        print("❌ Ошибка! Не должно быть валидационной ошибки")
        print(e)
        return False


def test_location_name_too_long():
    """Тест 13: Название локации слишком длинное"""
    print("\n" + "=" * 50)
    print("ТЕСТ 13: Название локации слишком длинное (max_length=256)")
    print("=" * 50)

    data = {
        "name": "a" * 300,  # max_length=256
        "is_published": True
    }

    try:
        LocationCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== COMMENTS TESTS ====================

# ==================== COMMENTS TESTS ====================

def test_comment_create_valid():
    """Тест 14: Создание комментария с валидными данными"""
    print("\n" + "=" * 50)
    print("ТЕСТ 14: Валидное создание комментария")
    print("=" * 50)

    data = {
        "text": "Это мой комментарий",
        "post_id": 1
        # author_id убираем, так как его нет в CommentCreate
    }

    try:
        comment = CommentCreate(**data)
        print("✅ Успех! Комментарий создан:")
        print(f"   - text: {comment.text}")
        print(f"   - post_id: {comment.post_id}")
        # author_id убрали из вывода
        return True
    except ValidationError as e:
        print("❌ Ошибка! Не должно быть валидационной ошибки")
        print(e)
        return False


def test_comment_text_too_long():
    """Тест 15: Текст комментария слишком длинный"""
    print("\n" + "=" * 50)
    print("ТЕСТ 15: Текст комментария слишком длинный (max_length=1000)")
    print("=" * 50)

    data = {
        "text": "a" * 2000,  # max_length=1000
        "post_id": 1
        # author_id убираем
    }

    try:
        CommentCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True
# ==================== ЗАПУСК ВСЕХ ТЕСТОВ ====================

if __name__ == "__main__":
    print("\n" + "🔥" * 20)
    print("🔥 ЗАПУСК ВСЕХ ТЕСТОВ ВАЛИДАЦИИ")
    print("🔥" * 20 + "\n")

    results = []

    results.append(("Пост: валидные данные", test_post_create_valid()))
    results.append(("Пост: заголовок короткий", test_post_title_too_short()))
    results.append(("Пост: заголовок длинный", test_post_title_too_long()))
    results.append(("Пост: пропущено поле", test_post_missing_required()))
    results.append(("Пост: валидное обновление", test_post_update_valid()))

    results.append(("Пользователь: валидные данные", test_user_create_valid()))
    results.append(("Пользователь: username короткий", test_user_username_too_short()))
    results.append(("Пользователь: пароль короткий", test_user_password_too_short()))
    results.append(("Пользователь: email невалидный", test_user_invalid_email()))

    results.append(("Категория: валидные данные", test_category_create_valid()))
    results.append(("Категория: slug невалидный", test_category_slug_invalid()))

    results.append(("Локация: валидные данные", test_location_create_valid()))
    results.append(("Локация: название длинное", test_location_name_too_long()))

    results.append(("Комментарий: валидные данные", test_comment_create_valid()))
    results.append(("Комментарий: текст длинный", test_comment_text_too_long()))

    print("\n" + "📊" * 20)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
    print("📊" * 20)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        if result:
            passed += 1
        else:
            failed += 1
        print(f"{status} - {name}")

    print("\n" + "=" * 50)
    print(f"ИТОГО: Пройдено: {passed}, Провалено: {failed}")
    print("=" * 50)


# ==================== ТЕСТЫ НА ТИПЫ ДАННЫХ ====================

def test_post_category_id_wrong_type():
    """Тест 16: category_id передан строкой вместо числа"""
    print("\n" + "=" * 50)
    print("ТЕСТ 16: category_id передан строкой вместо числа")
    print("=" * 50)

    data = {
        "title": "Заголовок",
        "text": "Текст поста",
        "pub_date": datetime.now().isoformat(),
        "category_id": "not-a-number",  # строка вместо числа
        "location_id": 1
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_post_location_id_wrong_type():
    """Тест 17: location_id передан булевым значением вместо числа"""
    print("\n" + "=" * 50)
    print("ТЕСТ 17: location_id передан булевым значением вместо числа")
    print("=" * 50)

    data = {
        "title": "Заголовок",
        "text": "Текст поста",
        "pub_date": datetime.now().isoformat(),
        "category_id": 1,
        "location_id": True  # булево вместо числа
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_post_pub_date_wrong_type():
    """Тест 18: pub_date передан строкой в неверном формате"""
    print("\n" + "=" * 50)
    print("ТЕСТ 18: pub_date в неверном формате")
    print("=" * 50)

    data = {
        "title": "Заголовок",
        "text": "Текст поста",
        "pub_date": "2026-13-45",  # невалидная дата
        "category_id": 1,
        "location_id": 1
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_post_is_published_wrong_type():
    """Тест 19: is_published передан строкой вместо булева"""
    print("\n" + "=" * 50)
    print("ТЕСТ 19: is_published передан строкой вместо булева")
    print("=" * 50)

    data = {
        "title": "Заголовок",
        "text": "Текст поста",
        "pub_date": datetime.now().isoformat(),
        "is_published": "true",  # строка вместо булева
        "category_id": 1,
        "location_id": 1
    }

    try:
        PostCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== ТЕСТЫ ДЛЯ КАТЕГОРИЙ ====================

def test_category_title_wrong_type():
    """Тест 20: title категории передан числом вместо строки"""
    print("\n" + "=" * 50)
    print("ТЕСТ 20: title категории передан числом")
    print("=" * 50)

    data = {
        "title": 12345,  # число вместо строки
        "slug": "news",
        "description": "Описание",
        "is_published": True
    }

    try:
        CategoryCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_category_is_published_wrong_type():
    """Тест 21: is_published категории передан числом вместо булева"""
    print("\n" + "=" * 50)
    print("ТЕСТ 21: is_published категории передан числом")
    print("=" * 50)

    data = {
        "title": "Новости",
        "slug": "news",
        "description": "Описание",
        "is_published": 1  # число вместо булева
    }

    try:
        CategoryCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== ТЕСТЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ====================

def test_user_age_wrong_type():
    """Тест 22: age передан строкой вместо числа"""
    print("\n" + "=" * 50)
    print("ТЕСТ 22: age передан строкой вместо числа")
    print("=" * 50)

    data = {
        "username": "john_doe",
        "password": "secret123",
        "email": "john@example.com",
        "age": "twenty five"  # строка вместо числа
    }

    try:
        UserCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


def test_user_is_active_wrong_type():
    """Тест 23: is_active передан строкой вместо булева"""
    print("\n" + "=" * 50)
    print("ТЕСТ 23: is_active передан строкой вместо булева")
    print("=" * 50)

    data = {
        "username": "john_doe",
        "password": "secret123",
        "email": "john@example.com",
        "is_active": "yes"  # строка вместо булева
    }

    try:
        UserCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== ТЕСТЫ ДЛЯ КОММЕНТАРИЕВ ====================

def test_comment_post_id_wrong_type():
    """Тест 24: post_id передан строкой вместо числа"""
    print("\n" + "=" * 50)
    print("ТЕСТ 24: post_id передан строкой вместо числа")
    print("=" * 50)

    data = {
        "text": "Комментарий",
        "post_id": "one"  # строка вместо числа
    }

    try:
        CommentCreate(**data)
        print("❌ Должна быть ошибка валидации, но её нет!")
        return False
    except ValidationError as e:
        print("✅ Успех! Поймали ошибку валидации:")
        for error in e.errors():
            print(f"   - {error['loc'][0]}: {error['msg']}")
        return True


# ==================== ДОБАВИТЬ В ЗАПУСК ====================

# Добавь эти строки в секцию запуска тестов:

results.append(("Пост: category_id строка", test_post_category_id_wrong_type()))
results.append(("Пост: location_id булево", test_post_location_id_wrong_type()))
results.append(("Пост: pub_date невалидный", test_post_pub_date_wrong_type()))
results.append(("Пост: is_published строка", test_post_is_published_wrong_type()))
results.append(("Категория: title число", test_category_title_wrong_type()))
results.append(("Категория: is_published число", test_category_is_published_wrong_type()))
results.append(("Пользователь: age строка", test_user_age_wrong_type()))
results.append(("Пользователь: is_active строка", test_user_is_active_wrong_type()))
results.append(("Комментарий: post_id строка", test_comment_post_id_wrong_type()))