from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''


def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py

    # Fixed the bug in schema under properties -> name -> type. Pet schema had name.type as integer
    # instead of expected type of string
    validate(instance=response.json(), schema=schemas.pet)


'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''


@pytest.mark.parametrize("status", [("available"), ("sold"), ("pending")])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)

    # validate the response code
    assert response.status_code == 200
    for pet_schema in response.json():
        pet_status = pet_schema.get('status')
        # validate the pet status is equal to expected status
        assert pet_status == status
        # validate pet schema
        validate(instance=pet_schema, schema=schemas.pet)


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''

# parameterized to test for edge cases
@pytest.mark.parametrize("pet_id", [("1"), ("-1"), ("$")])
def test_get_by_id_404(pet_id):
    pet_get_by_pet_id = "/pets" + pet_id

    # validated the response status code get_by_pet_id
    assert api_helpers.get_api_data(pet_get_by_pet_id).status_code == 404
