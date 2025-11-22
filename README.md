Практика 2 — Многоконтейнерный стенд на Docker Compose 
1) Создаем все необходимые файлы
2) поднимаем стенд в docker

```
chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$ docker compose up -d --build
[+] Building 1.2s (14/14) FINISHED
 => [internal] load local bake definitions                                                                                                                        0.0s
 => => reading from stdin 521B                                                                                                                                    0.0s
 => [internal] load build definition from Dockerfile                                                                                                              0.0s
 => => transferring dockerfile: 441B                                                                                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                               0.3s
 => [internal] load .dockerignore                                                                                                                                 0.0s
 => => transferring context: 2B                                                                                                                                   0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:a0939570b38cddeb861b8e75d20b1c8218b21562b18f301171904b544e8cf228                                 0.1s
 => => resolve docker.io/library/python:3.11-slim@sha256:a0939570b38cddeb861b8e75d20b1c8218b21562b18f301171904b544e8cf228                                         0.1s
 => [internal] load build context                                                                                                                                 0.0s
 => => transferring context: 91B                                                                                                                                  0.0s
 => CACHED [builder 2/4] WORKDIR /app                                                                                                                             0.0s
 => CACHED [stage-1 3/5] RUN useradd -m appuser && chown -R appuser /app                                                                                          0.0s
 => CACHED [builder 3/4] COPY requirements.txt .                                                                                                                  0.0s
 => CACHED [builder 4/4] RUN pip install --user --no-cache-dir -r requirements.txt                                                                                0.0s
 => CACHED [stage-1 4/5] COPY --from=builder /root/.local /home/appuser/.local                                                                                    0.0s
 => CACHED [stage-1 5/5] COPY app/ .                                                                                                                              0.0s
 => exporting to image                                                                                                                                            0.2s
 => => exporting layers                                                                                                                                           0.0s
 => => exporting manifest sha256:6256c0f8c99ae09807ed6ca03a84527703e80550f5f0bc7cdcbc4d077f2b7860                                                                 0.0s
 => => exporting config sha256:63dea60a3c77e78b184c22b3cde4f170b83d5b40ddb4c12fb6e83adf3a48be1e                                                                   0.0s
 => => exporting attestation manifest sha256:0b7d58108980fa0db4d9a8aedae50eb434ea6b4512add356dda7c6c14bd4a13e                                                     0.1s
 => => exporting manifest list sha256:7b76e15dee8084a9726b47dbef475b21fa340f3402176dfeb88633d40e27eca3                                                            0.0s
 => => naming to docker.io/library/lab2-api:latest                                                                                                                0.0s
 => => unpacking to docker.io/library/lab2-api:latest                                                                                                             0.0s
 => resolving provenance for metadata file                                                                                                                        0.0s
[+] Running 8/8
 ✔ lab2-api                   Built                                                                                                                               0.0s
 ✔ Network lab2_public        Created                                                                                                                             0.1s
 ✔ Network lab2_backend       Created                                                                                                                             0.1s
 ✔ Container lab2-traefik-1   Started                                                                                                                             1.2s
 ✔ Container lab2-redis-1     Started                                                                                                                             1.1s
 ✔ Container lab2-postgres-1  Healthy                                                                                                                             6.1s
 ✔ Container lab2-adminer-1   Started                                                                                                                             1.2s
 ✔ Container lab2-api-1       Started
```
3)Проверка

```
chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$ curl -s http://api.localhost/healthz
{"status":"ok"}chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$
chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$ curl -s http://api.localhost/db
{"db":1}chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$ curl -s http://api.localhost/cache
{"cache":"ok"}chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$
```
4)Состояние

```
chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$ docker compose ps
NAME              IMAGE                COMMAND                  SERVICE    CREATED          STATUS                    PORTS
lab2-adminer-1    adminer              "entrypoint.sh docke…"   adminer    12 minutes ago   Up 12 minutes             8080/tcp
lab2-api-1        lab2-api             "uvicorn main:app --…"   api        3 minutes ago    Up 3 minutes
lab2-postgres-1   postgres:16-alpine   "docker-entrypoint.s…"   postgres   12 minutes ago   Up 12 minutes (healthy)
lab2-redis-1      redis:7-alpine       "docker-entrypoint.s…"   redis      12 minutes ago   Up 12 minutes
lab2-traefik-1    traefik:v3.1         "/entrypoint.sh --pr…"   traefik    12 minutes ago   Up 12 minutes             0.0.0.0:80->80/tcp, [::]:80->80/tcp
```
5)Логи

```
chepyx@DESKTOP-HUJFQGD:~/TMPLabs/02_docker_compose/lab2$ docker compose logs -f api
api-1  | INFO:     Started server process [1]
api-1  | INFO:     Waiting for application startup.
api-1  | INFO:     Application startup complete.
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
api-1  | INFO:     172.18.0.2:35962 - "GET /healthz HTTP/1.1" 200 OK
api-1  | INFO:     172.18.0.2:59850 - "GET /db HTTP/1.1" 200 OK
api-1  | INFO:     172.18.0.2:59860 - "GET /cache HTTP/1.1" 200 OK
```

6)Проверяем доступность хостов и работоспособность локалок.

6.1)Traefik
<img width="1280" height="689" alt="{ED073095-6833-4454-AB81-E5AC4E2A66A0}" src="https://github.com/user-attachments/assets/ffb56be0-7a17-43ec-b47d-3b4a70502d9c"/>

6.2)Adminer
<img width="1280" height="683" alt="{82A303BB-1FFC-4AE6-ACE1-D52D3E9A5004}" src="https://github.com/user-attachments/assets/2a83ef8d-d4e8-445e-b20f-1cb3d958d082"/>

