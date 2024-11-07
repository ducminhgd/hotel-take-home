# Ascenda take home assignment: Hotel Data Merge

Assignment: https://gist.github.com/Attila24/ab7133f86f7fc83de7996877d92ba88b

## Installation

Require Python 3.9+.

1. Install Python dependencies with:

    ```bash
    pip install -U pip
    pip install -r requirements.txt
    ```

2. Run project `python hotel_merge/main.py`.
3. Run tests `pytest tests`.

## Documentation

### Environment variables

- `ACME_URL_ENDPOINT`: URL of ACME API.
- `PATAGONIA_URL_ENDPOINT`: URL of Patagonia API.
- `PAPERFLIES_URL_ENDPOINT`: URL of Paperflies API.
- `CACHE_TTL`: time-to-live of a cache, in seconds. Default is 10 seconds.

### Why I choose python?

Because there are some field that:

- Can be mixed of `null`, `string`, `float` or missing. For e.g: `lat` or `lng`.
- Can be mixed of `null`, `string` or `list`. For e.g: `amenities` or `images`.

Python is good at serializing those cases. Another candidate is PHP.

### Project layout

- `hotel_merge`: contains all the code for our application.
  - `models`: contains models for our system, suppliers, and validators for them.
  - `helpers.py`: contains helper functions.
  - `main.py`: the entry point of our application, used to define the HTTP API.
  - `repository.py`: contains functions that provide the data.
  - `settings.py`: contains all the configuration parameters for application.
- `tests`: contains unit tests for our system.

### How do I merge those data?

1. In `models/hotel.py`, I defined the classes considered as our unified models and used in our system.
2. Other models file, such as `models/patagonia.py`, `models/acme.py`, `models/paperflies.py` are used to defined the models of suppliers.
3. I used single dispatch approach to unify information from suppliers to our model.
4. A hotel with an invalid ID or Destination ID is considered as an error record.
5. For sanitizing data:
   
   - [x] Remove redundant empty spaces in both sides of strings.
   - [x] Remove duplicate strings in `amenities`
   - [x] Remove duplicate images in `images`. Images are considered duplicated if they have the same Captions and URLs.
   - [x] Remove duplicate booking conditions in `booking_conditions`

6. Amenities in data of Patagonia are represented as a list of strings, that would be merged into `amenities.general`.

### Steps for add new supplier

1. Add new module of models in `models` folder.
2. Add new method for single dispatching into class `Hotel` in `models/hotel.py`.
3. Add new endpoint and serializing-data class into `settings.py`

### CI/CD

- [x] Create a test job.
- [x] Scan source code (with https://github.com/aquasecurity/trivy)
- [x] Scan image (with https://github.com/aquasecurity/trivy)

### Improvements

> This section lists the improvements that can be made to the project if it is not just a take-home assignment.

1. Scaling the project
   1. We have to use a database to store our data, which is the model `Hotel`.
      1. I suggest we can use a relational database such as MySQL or PostgreSQL (preferred, and use `pgbouncer` for global connection pool management).
   2. Apply distributed caching, I suggest to use Redis 6. Using Write Around - Cache Aside strategy.
   3. If we have to serve a huge number of requests, we can consider to write hotels data into JSON files and upload to CDN.
2. Optimize Amenities: some suppliers may not categorize their amenities, such as Patagonia. So there are two approaches:
   1. Merge all amenities into `general` field.
   2. Categorize amenities into categories. This approach costs more effort, but I suggest that we should do it to have more detailed data.
3. Data type of coordinates should be string, not float. Because some suppliers may provide "long float numbers" for more detail coordinates, in some programing languages, or especially Javascript (we are using JSON resposes), they are converted into strings.
4. If we have a lot of data, pagination for this API is highly recommended.