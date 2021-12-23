import random

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from students.models import Course


# проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_course_retrieve(client, course_factory):
    courses = course_factory(_quantity=7)
    ids = [course.id for course in courses]
    id = random.choice(ids)
    url = reverse('courses-detail', kwargs={'pk': id})
    response = client.get(url)
    course_from_db = Course.objects.get(id=id)
    assert response.status_code == HTTP_200_OK
    assert course_from_db.id == response.data.get('id')
    assert course_from_db.name == response.data.get('name')


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    for course in response.data:
        course_from_db = Course.objects.filter(id=course['id']).first()
        assert course_from_db is not None
        assert course_from_db.name == course['name']


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_course_filter_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url_base = reverse('courses-list')
    ids = [course.id for course in courses]
    id = random.choice(ids)
    url = url_base + f'?id={id}'
    course_from_db = Course.objects.get(id=id)
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert course_from_db.id == response.data[0]['id']
    assert course_from_db.name == response.data[0]['name']


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_course_filter_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url_base = reverse('courses-list')
    names = [course.name for course in courses]
    name = random.choice(names)
    course_from_db = Course.objects.get(name=name)
    url = url_base + f'?name={name}'
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert course_from_db.id == response.data[0]['id']
    assert course_from_db.name == response.data[0]['name']


# тест успешного создания курса
@pytest.mark.parametrize(
    ['name', 'expected_status'],
    (
            ('',  HTTP_400_BAD_REQUEST),
            ('some_name', HTTP_201_CREATED)
    )
)
@pytest.mark.django_db
def test_course_create(client, name, expected_status):
    url = reverse('courses-list')
    payload = {
        'name': name
    }
    response = client.post(url, payload)
    assert response.status_code == expected_status
    if response.status_code == HTTP_201_CREATED:
        assert name == response.data['name']


# тест успешного обновления курса
@pytest.mark.parametrize(
    ['new_name', 'expected_result'],
    (
            ('', HTTP_400_BAD_REQUEST),
            ('some_new_name', HTTP_200_OK)
    )
)
@pytest.mark.django_db
def test_course_update(client, course_factory, new_name, expected_result):
    course = course_factory()
    url = reverse('courses-detail', kwargs={'pk': course.id})
    payload = {
        'name': new_name
    }
    response = client.patch(url, payload, content_type='application/json')
    assert response.status_code == expected_result
    if response.status_code == HTTP_200_OK:
        assert new_name == response.data['name']


# тест успешного удаления курса
@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT

