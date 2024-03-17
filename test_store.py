import json
import random
import string

from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''


@pytest.fixture
def create_pet_test_data():
    def create_request():
        pet_id = random.randint(1, 99)
        pet_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
        pet_type = random.choice(['cat', 'dog', 'fish'])
        pet_status = random.choice(['available'])

        request_data = {
            "id": pet_id,
            "name": pet_name,
            "type": pet_type,
            "status": pet_status
        }

        return json.dumps(request_data)

    return create_request


def test_patch_order_by_id(create_pet_test_data):
    # create pet data
    create_pets_endpoint = "/pets"
    pet_request_data = create_pet_test_data()
    pet_id = json.loads(pet_request_data).get('id')

    create_pets_response = api_helpers.post_api_data(create_pets_endpoint, json.loads(pet_request_data))

    assert create_pets_response.status_code == 201
    assert create_pets_response.json().get('id') == pet_id

    # create order
    create_order_endpoint = "/store/order"
    create_order_request_data = {"pet_id": pet_id}
    create_order_response = api_helpers.post_api_data(create_order_endpoint,
                                                      json.loads(json.dumps(create_order_request_data)))

    assert create_order_response.status_code == 201

    # validate order schema
    validate(instance=create_order_response.json(), schema=schemas.order)

    # update the order with pet status
    order_id = create_order_response.json().get('id')
    patch_request_data = {"status": "pending"}
    create_patch_order_response = api_helpers.patch_api_data(create_order_endpoint + "/" + order_id,
                                                             json.loads(json.dumps(patch_request_data)))
    assert create_patch_order_response.status_code == 200
    assert create_patch_order_response.json().get('message') == "Order and pet status updated successfully"
