# Resources

## Objects

**Resource**

- `name` (str): Name of the service.
- `endpoint` (str): Endpoint uri of the service.

## Methods

**GET** `/resources`

Returns a list of `Resource` objects.

No Parameters.

**GET** `/get`

Returns a `Resource` object.

Parameters:

- `name` (str): Name of the service.

**POST** `/register`

Appends a resource to the catalog.

Parameters:

- `name` (str): Name of the resource.
- `endpoint` (str): Endpoint uri of the resource without any path.
- `token` (str, Optional): A secret token which can be used to update or unregister the service.

**DELETE** `/unregister`

Removes a resource from the catalog.

Parameters:
- `name` (str): Name of the resource.
- `token` (str, Optional): Same token used in the register method.

