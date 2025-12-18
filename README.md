1. Cel projektu

Celem projektu było stworzenie kompletnego środowiska DevOps dla prostej aplikacji webowej opartej o Flask + PostgreSQL, działającej w całości w środowisku Docker, z wykorzystaniem:

wieloetapowego Dockerfile,

Docker Compose (sieci, wolumeny, seeder),

testów automatycznych (pytest),

GitHub Actions (CI/CD),

minimalnej infrastruktury jako kodu (IaC) w Azure (Bicep).

Projekt został wykonany w wersji minimalnej, ale kompletnej, zgodnie z wymaganiami zadania.

2. Opis aplikacji

Aplikacja backendowa została napisana w Pythonie z użyciem frameworka Flask.
Udostępnia proste API HTTP oraz komunikuje się z bazą danych PostgreSQL.

Dostępne endpointy:

GET / – strona startowa aplikacji,

GET /health – sprawdzenie stanu aplikacji,

GET /health/db – sprawdzenie połączenia z bazą danych,

GET /users – pobranie listy użytkowników,

POST /users – dodanie nowego użytkownika.

Aplikacja korzysta z przykładowego modelu danych Users (id, name, email).

3. Dockerfile – wieloetapowy build

Projekt wykorzystuje 3-etapowy Dockerfile:

 Etap 1 – builder

Bazuje na obrazie python:3.11-slim,

Instaluje wszystkie zależności z requirements.txt,

Kopiuje kod aplikacji,

Służy jako baza dla testów i obrazu finalnego.

 Etap 2 – test

Korzysta z etapu builder,

Uruchamia testy automatyczne (pytest),

W przypadku niepowodzenia testów build zostaje przerwany.

 Etap 3 – final

Lekki obraz produkcyjny,

Zawiera tylko kod aplikacji i wymagane zależności,

Wykorzystywany w środowisku runtime przez Docker Compose.

4. Docker Compose

Środowisko uruchamiane jest przy pomocy Docker Compose i składa się z następujących usług:

 app (Flask)

Uruchamiana z obrazu finalnego,

Podłączona do sieci front_net oraz back_net,

Zależna od bazy danych i kontenera seedującego.

 nginx

Reverse proxy dla aplikacji Flask,

Przekazuje ruch HTTP do backendu,

Logi zapisywane są do wolumenu nginx_logs.

 db (PostgreSQL)

Trwałe dane zapisywane w wolumenie db_data,

Działa wyłącznie w sieci back_net.

 seed_runner

Jednorazowy kontener seedujący bazę danych,

Tworzy przykładowe dane (min. 5 rekordów),

Generuje pliki seed.log oraz users.csv,

Zapisuje dane do wolumenu seed_output,

Po zakończeniu działania kontener się zatrzymuje.

5. Sieci i wolumeny
Sieci Docker:

front_net – komunikacja NGINX ↔ Flask,

back_net – komunikacja Flask ↔ PostgreSQL.

Wolumeny:

db_data – dane PostgreSQL,

nginx_logs – logi serwera NGINX,

seed_output – pliki generowane przez seeder.

6. Testy automatyczne (pytest)

Projekt zawiera testy napisane w pytest, spełniające wymagania minimalne:

test jednostkowy,

test logiki aplikacji,

test endpointu HTTP (/health).

Testy uruchamiane są automatycznie w etapie test Dockerfile, co gwarantuje, że obraz produkcyjny powstaje tylko wtedy, gdy wszystkie testy zakończą się sukcesem.

7. GitHub Actions – CI/CD

Projekt wykorzystuje GitHub Actions:

 CI Pipeline

Uruchamiany przy push oraz pull_request,

Wykonuje:

Checkout repozytorium,

Build obrazu (etap builder),

Uruchomienie testów (pytest),

Build obrazu finalnego,

Push obrazu do registry (GHCR),

Skan bezpieczeństwa CodeQL.

 CD Pipeline

Uruchamiany ręcznie lub na podstawie tagów,

Pobiera obraz,

Wykonuje docker compose pull oraz docker compose up -d,

Restartuje środowisko aplikacji.

8. Infrastructure as Code (Azure)

Projekt zawiera minimalną konfigurację Infrastructure as Code w Azure, zapisaną w pliku Bicep.

W katalogu infra/ znajduje się plik main.bicep, który definiuje:

Resource Group,

Azure Container Registry (ACR).

Środowisko produkcyjne nie jest uruchamiane w Azure – Azure wykorzystywane jest wyłącznie jako IaC oraz registry, zgodnie z wymaganiami zadania.

9. Struktura repozytorium
.
├── app/
│   ├── src/
│   ├── tests/
│   ├── seed/
│   │   └── run_seed.py
│   └── requirements.txt
│
├── docker/
│   └── nginx.conf
│
├── Dockerfile
├── docker-compose.yml
│
├── infra/
│   └── main.bicep
│
└── .github/workflows/
    ├── ci.yml
    └── codeql.yml

10. Podsumowanie

Projekt spełnia wszystkie wymagania zadania:

kompletne środowisko Docker,

testy automatyczne,

CI/CD,

seeder bazy danych,

Infrastructure as Code w Azure.

Całość została przygotowana w sposób modularny, czytelny oraz zgodny z podstawowymi zasadami DevOps.