Projekt zawiera kompletną infrastrukturę z Docker Compose, w tym backend Flask, bazę PostgreSQL, reverse proxy NGINX, dwie sieci Dockerowe i seedowanie danych. Pipeline CI buduje obraz i uruchamia testy bez zależności od bazy, a CD jest uruchamiany ręcznie za pomocą workflow_dispatch.
Celem projektu jest demonstracja:
- konteneryzacji aplikacji,
- separacji środowisk (frontend / backend),
- automatycznego budowania i testowania (CI),
- ręcznego wdrażania (CD).

-  🧱 Architektura
- **Flask** – aplikacja backendowa
- **PostgreSQL** – baza danych
- **NGINX** – reverse proxy
- **Docker & Docker Compose** – orkiestracja kontenerów
- **GitHub Actions** – pipeline CI/CD

### Sieci Dockerowe
- `front_net` – komunikacja NGINX ↔ świat zewnętrzny
- `back_net` – komunikacja aplikacja ↔ baza danych

- Struktura projektu
- projektrdevops/
├── .github/workflows/
│ ├── ci.yml
│ └── cd.yml
├── app/
│ ├── src/
│ │ └── main.py
│ ├── tests/
│ │ └── test_health.py
│ ├── seed/
│ │ └── run_seed.py
│ └── requirements.txt
├── docker/
│ └── nginx.conf
├── Dockerfile
├── docker-compose.yml
└── README.md

Dockerfile wykorzystuje **3 etapy**:
1. **builder** – instalacja zależności
2. **test** – uruchomienie testów pytest
3. **final** – lekki obraz produkcyjny

Testy są wykonywane **w trakcie budowania obrazu**, co zapewnia poprawność aplikacji już na etapie CI.

## 🔄 Docker Compose

Uruchamiane serwisy:
- `app` – Flask backend
- `db` – PostgreSQL
- `nginx` – reverse proxy
- `seed_runner` – jednorazowe seedowanie danych

Uruchomienie lokalne:
docker compose up -d

Zatrzymanie:
docker compose down
