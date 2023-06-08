## API service aimed at helping automate the pet adoption process

- JWT authentication
- Supports different user types, with different level of permissions including a customized is_admin user and
anonymous telegram user
- Partial integration with Telegram API
- Customized admin panel at /admin/
- Documentation at api/schema/swagger-ui/
- Scheduled celery tasks
- Adoption requests can be created without prior authorization
- Supports complex filtering scenarios

## Endpoints available:

### TEMPORAL_OWNER:

- [POST] /temporal_owner/register/ (register temporal owner)
- [POST] /temporal_owner/login/ (login temporal owner)
- [GET] /temporal_owner/manage (info about temporal owner)
- [PUT] /temporal_owner/manage (all temporal_owner data update)
- [PATCH] /temporal_owner/manage (partial temporal_owner data update)
- [POST] /temporal_owner/token (get temporal owner JWT token)
- [POST] /temporal_owner/token/refresh (update temporal owner access token)

### ADOPTER:

- [POST] /adopter/api/telegram/ (register anonymous_user id)
- [POST] /adopter/api/telegram/{pet_id} (create adoption request with related adopter object)
- [GET] /adopter/ (list if all adopters)
- [GET] /adopter/{id} (detail about adopter)
- [PUT] /adopter/{id} (update adopter instance)
- [PATCH] /adopter/{id} (partial update of adopter instance)
- [DELETE] /adopter/{id} (delete adopter instance)

### PET:

- [POST] /pet/ (create pet instance)
- [GET] /pet/ (list if all pets)
- [GET] /pet/{id} (detail about pet)
- [PUT] /pet/{id} (update pet instance)
- [PATCH] /pet/{id} (partial update of pet instance)
- [DELETE] /pet/{id} (delete pet instance)
- [GET] /pet/urgent_adoption_pets_list/ (get a list of all pets that need an urgent adoption)
- [GET] /pet/get_real_dog_age/ (get a list of all dogs with age that is equivalent to a human's age)
- [GET] /pet/get_age_statistics/ (get age statistics values based on all registered pets)
- [GET] /pet/city/ (get a list of all pets filtered by a chosen city)
- [GET] /pet/city/{str:city} (get a list of all pets filtered by requested city)

### ADOPTION_REQUEST:

- [POST] /adoption_request/ (create adoption request with related adopter object)
- [GET] /adoption_request/ (list if all adoption requests)
- [GET] /adoption_request/{id} (detail about adoption request)
- [PUT] /adoption_request/{id} (update adoption request)
- [PATCH] /adoption_request/{id} (partial update of adoption request)
- [DELETE] /adoption_request/{id} (delete adoption request)
- [GET] /adoption_request/get_statistics (get adoption statistics)
- PUT] /adoption_request/approve/{id} (approve adoption request)



