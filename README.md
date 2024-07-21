# JSON parser
## Local install

```bash
git clone https://github.com/Quad3/vk_tz.git
cd vk_tz
```
Build Docker container
```bash
docker-compose up -d --build
```
Create .json schema, copy it to project folder and run next command with this file
```bash
docker-compose exec app python src/gen_model.py path-in/project_folder/your_file.json
docker-compose exec app python src/gen_router.py path-in/project_folder/your_file.json
```
or run commands below to check existing json files
```bash
docker-compose exec app python src/gen_model.py src/data-json/new_test.json
docker-compose exec app python src/gen_router.py src/data-json/new_test.json
```

Restart FastAPI app

```bash
docker-compose restart app
```
Visit http://localhost:5000/docs


Add kind


## Review
`gen_model.py` generates pydantic model from json schema

`gen_router.py` generates FastAPI controllers
- POST:/{kind}/
- PUT:/{kind}/{uuid}/{configuration}/
- PUT:/{kind}/{uuid}/{settings}/
- PUT:/{kind}/{uuid}/{state}/
- DELETE:/{kind}/{uuid}/
- GET:/{kind}/{uuid}/
- GET:/{kind}/{uuid}/state/


## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker
- ~~Kubernetes~~
