# shifoxona

### Enpoint: `doctors/`

#### Description

The `get` method retrieves all doctors from the database and returns them as a serialized response.

#### Returns

- `Response`: A Django REST Framework response object containing the serialized data of all doctors.

#### Response Format

The response data will be in the following format:

```json
{
    "Status": true,
    "doctors": [
        {
            "name": "", 
            "branch": 1,
	    "img": url
            "desc": "",
            "desc2": ""
        },
       ...
    ]
}
```

### Enpoint: `branches/`

#### Description

The `get` method retrieves all branches from the database and returns them as a serialized response.

#### Returns

- `Response`: A Django REST Framework response object containing the serialized data of all branches.

#### Response Format

The response data will be in the following format:

```json
{
    "Status": true,
    "doctors": [
        {
            "name": "", 
            "img": url,
            "desc": "",
            "desc2": ""
        },
       ...
    ]
}
```
