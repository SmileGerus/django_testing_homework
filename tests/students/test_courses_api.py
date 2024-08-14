import pytest
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_one_course(client, courses_factory):
    course = courses_factory(_quantity=1)
    responce = client.get(f'/api/v1/courses/')
    data = responce.json()
    
    assert data[0]['name'] == course[0].name 


@pytest.mark.django_db
def test_get_all_courses(client, courses_factory):
    courses = courses_factory(_quantity=10)
    responce = client.get('/api/v1/courses/')
    data = responce.json()
    
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name 


@pytest.mark.django_db
def test_get_one_course_filtered_id_1(client, courses_factory):
    course = courses_factory(_quantity=1)
    responce = client.get(f'/api/v1/courses/{course[0].id}/')
    data = responce.json()
    
    assert data['name'] == course[0].name 


@pytest.mark.django_db
def test_get_one_course_filtered_id_1(client, courses_factory):
    course = courses_factory(_quantity=1)
    responce = client.get(f'/api/v1/courses/', {'id': course[0].id})
    data = responce.json()
    
    assert data[0]['name'] == course[0].name 
    

@pytest.mark.django_db
def test_get_one_course_filtered_name(client, courses_factory):
    course = courses_factory(_quantity=1)
    responce = client.get('/api/v1/courses/', {'name': course[0].name})
    data = responce.json()
    
    assert data[0]['name'] == course[0].name


@pytest.mark.django_db
def test_post_course(client):
    responce = client.post('/api/v1/courses/', data={'name': 'test'})
    
    assert responce.status_code == 201


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    course = courses_factory(_quantity=1)
    responce = client.patch(f'/api/v1/courses/{course[0].id}/', data={'name': 'test'})
    
    assert responce.status_code == 200
    
    
@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    course = courses_factory(_quantity=1)
    responce = client.delete(f'/api/v1/courses/{course[0].id}/')
    
    assert responce.status_code == 204

