# ProGeek Backend Dokumentáció

## Fő technológiák

- Django 5
- Neon PostgreSQL (külső DB)
- Cloudinary (képfeltöltés, tárolás)
- JWT authentikáció
- Custom User modell
- .env titkosítás

## Fő modulok

- Blog (BlogPost, BlogSection, SectionImage, SectionVideo)
- News
- Events
- Auth (regisztráció, aktiváció, email)

## Fő funkciók

- Fájl- és képfeltöltés Cloudinary-ra (CloudinaryField)
- Képek automatikus törlése Cloudinary-ból, ha a modell törlődik
- User regisztráció, aktiváció, email küldés
- REST API, JWT authentikáció
- Automata tesztek
- Admin felület

## Beállítások

- Minden titkos adat a backend/.env fájlban
- Cloudinary: `CLOUDINARY_URL=cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>`
- Neon DB: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_SCHEMA
- Email: EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

## Migrációk

- Minden modellváltoztatás után: `python manage.py makemigrations` és `python manage.py migrate`

## Képfeltöltés

- Minden kép Cloudinary-ra megy
- Törléskor a kép is törlődik a felhőből (signals)

## Verziókövetés

- Utolsó nagy változás: CloudinaryField-re váltás, signals a képek törléséhez

## Fejlesztői javaslatok

- Egységtesztek minden fő funkcióra
- API dokumentáció (Swagger, drf-spectacular)
- Kód review, refaktorálás

## Frissítési napló

- 2025.10.04: CloudinaryField-re váltás, automatikus képtörlés signals-szal
- 2025.10.03: Cloudinary storage beállítás, .env migrálás, JWT, email aktiváció

---

Ha új funkció vagy változás történik, ezt a dokumentációt frissíteni kell!
