# BirdPipeline

Python pipeline za obradu audio zapisa ptica i taksonomskih podataka, izrađen u sklopu kolegija **Pristup podacima iz programskog koda**.

Projekt koristi:
- Python
- MongoDB
- MinIO
- Docker
- PyMongo
- MinIO Python SDK
- Requests
- aves.regoch.net API

## Funkcionalnosti

Pipeline omogućuje:
- dohvat taksonomskih podataka o vrstama ptica
- spremanje taksonomije u MongoDB
- sprječavanje dupliciranih taksonomskih zapisa
- obradu audio datoteka iz lokalnog direktorija
- upload audio datoteka u MinIO
- jedinstvenu identifikaciju audio objekata
- spremanje metapodataka audio datoteka u MongoDB
- povezivanje audio datoteka s geografskom lokacijom
- slanje audio zapisa na classification API
- spremanje rezultata klasifikacije u MongoDB
- povezivanje rezultata klasifikacije s audio datotekom i taksonomskim zapisom

## Pokretanje projekta

Za pokretanje projekta potrebno je imati instalirano:
- Python 3
- Docker Desktop
- Git

Klonirati repozitorij:

```bash
git clone <URL_REPOZITORIJA>
cd PPPK-BirdPipeline
```

Kreirati virtualno okruženje:

```bash
python -m venv .venv
```

Na Windowsu ga aktivirati:

```bash
.venv\Scripts\activate
```

Na Linuxu ili macOS-u:

```bash
source .venv/bin/activate
```

Instalirati potrebne pakete:

```bash
pip install -r requirements.txt
```


Pokrenuti MongoDB i MinIO:

```bash
docker compose up -d
```

Provjeriti kontejnere:

```bash
docker ps
```

Trebali bi biti aktivni:
- `bird_mongodb`
- `bird_minio`

MinIO konzola dostupna je na:

```text
http://localhost:9001
```

Podaci za prijavu:

```text
Username: minioadmin
Password: minioadmin
```

Audio datoteke za obradu staviti u:

```text
data/audio/
```

Pokrenuti pipeline:

```bash
python main.py
```

Pipeline zatim:
1. spaja se na MongoDB
2. spaja se na MinIO
3. provjerava postoji li taksonomija
4. dohvaća taksonomiju ako je potrebno
5. sprema taksonomske podatke u MongoDB
6. obrađuje audio datoteke
7. uploada ih u MinIO
8. sprema metadata u MongoDB
9. šalje audio zapise na classification API
10. sprema uspješne klasifikacije u MongoDB

## MongoDB kolekcije

Projekt koristi:
- `birds`
- `audio_files`
- `classifications`

`birds` sadrži taksonomske podatke.

`audio_files` sadrži metadata audio datoteka.

`classifications` sadrži rezultate klasifikacije i povezuje ih s audio zapisom i taksonomskim zapisom.

## MinIO

Audio datoteke spremaju se u bucket:

```text
bird-audio
```

Svaki objekt dobiva jedinstveni UUID naziv.

## Zaustavljanje servisa

```bash
docker compose down
```

Za potpuno uklanjanje podataka:

```bash
docker compose down -v
```

Napomena: opcija `-v` briše MongoDB podatke i MinIO objekte.
