import os

from api import PetFriends
from settings import valid_email, invalid_email, valid_password, invalid_password

pf = PetFriends()

#Тест №1
#Тест с проверкой неверного указания url
def test_get_api_key_for_valid_user_url(email = valid_email, password = valid_password):
    status, result = pf.get_api_key_url(email, password)
    assert status == 200
    assert 'key' in result

#Тест №2
#Негативный тест. Проверяем ввод неверного пароля.
def test_get_api_key_for_valid_user_invalid_password(email = valid_email, password = invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#Тест №3
#Негативный тест. Проверяем ввод неверного email.
def test_get_api_key_for_valid_user_invalid_email(email = invalid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#Тест №4
#Негативный тест. Запрашиваем список питомцев, но напишем что список пустой.
def test_get_all_pets_with_valid_key_null(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_a_null_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) == 0
#Получили ошибку, что список не пустой 100!=0 Expected :0 Actual   :100

#Тест №5
#тест с некорректным именем питомца
def test_add_a_new_pets_with_invalid_data(name='945588484030300384847473904-4-59493%#', animal_type='Попугай',
                                     age='', pet_photo='images/popugaj11.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Тест №6
#тест с некорректным графическим форматов фотографии
def test_add_a_new_pets_with_invalid_data_foto(name='945588484030300384847473904-4-59493%#', animal_type='Попугай',
                                     age='', pet_photo='images/popugaj11.jpe'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
#Ошибка:FileNotFoundError

#Тест №7
#тест без указания возраста
def test_add_a_new_pets_with_invalid_age(name='Кеша', animal_type='Попугай',
                                     age='', pet_photo='images/popugaj11.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Тест №8
#тест на удаления питомца, возьмем id 3 питомца, которого нет в списке.
def test_successful_delete_self_pet_3():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кеша", "попугай", "2", "images/voln1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][2]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

#ошибка: индекс третьего питомца не найден, pet_id = my_pets['pets'][2]['id'] IndexError: list index out of range

#Тест №9
#обновление информации питомца, которого нет в списке
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][2]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
#IndexError: list index out of range

#Тест №10
#Проверка без указания возраста при обновлении информации о питомце

def test_successful_update_self_pet_info_age(name='Барсик', animal_type='Котэ', age=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
# В данном случае возраст питомца остается прежним