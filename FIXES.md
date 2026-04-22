## 1. frontend/app.js

- Line: const API_URL = "http://localhost:8000";
- Problem: API URL was hardcoded to localhost. In Docker, localhost refers to the frontend container itself.
- fix: Replaced hardcoded URL with API_URL environment variable.
  const API_URL = process.env.API_URL;

## 2. api/main.py

- Line: r = redis.Redis(host="localhost", port=6379);
- Problem: Redis host was hardcoded to localhost. API container could not reach Redis container.
- fix: Replaced localhost with REDIS_HOST and REDIS_PORT environment variables.
  r = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=int(os.getenv("REDIS_PORT", 6379)),
  decode_responses=True
  )

## 3. worker/worker.py

- Line: r = redis.Redis(host="localhost", port=6379);
- Problem: Redis host was hardcoded to localhost. Worker container could not reach Redis container.
- fix: Replaced localhost with REDIS_HOST and REDIS_PORT environment variables.
  r = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=int(os.getenv("REDIS_PORT", 6379)),
  decode_responses=True
  )

## 4. api/.env

- Line: REDIS_PASSWORD=supersecretpassword123
- Problem: env file were committed. It violates deployment security requirements.
- fix: Removed .env from repository and created .env.example.
  REDIS_HOST=redis
  REDIS_PORT=6379
  API_URL=http://api:8000

## 5. api/main.py

- Line: status.decode()
- Problem: Redis response manually decoded. It conflicts with decode_responses=True.
- fix: Returned Redis value directly.
  return {"job_id": job_id, "status": status}

## 6. api/main.py and worker/worker.py

- Line: 
- Problem: REDIS_PORT crashed when environment variable was empty.int('') raises ValueError.
- Fix: Added fallback using os.getenv("REDIS_PORT") or 6379.
