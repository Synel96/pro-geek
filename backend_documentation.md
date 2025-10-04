# Backend API Dokumentáció (Magyar)

Ez a dokumentáció bemutatja a backend API fő végpontjait, azok funkcióját, és a válaszok formátumát.

## 1. Authentikáció

### POST /api/auth/login/

- **Leírás:** Bejelentkezés JWT sütivel.
- **Help:** Küldd el a felhasználónév és jelszó mezőket. Sikeres bejelentkezés után JWT sütit kapsz, amit a böngésző automatikusan kezel.
- **Auth:** Nem szükséges.
- **Válasz:**

```json
{
  "access": "<jwt_token>",
  "refresh": "<jwt_token>"
}
```

### POST /api/auth/logout/

- **Leírás:** Kijelentkezés, JWT süti törlése.
- **Help:** Küldd el a kérést authentikált felhasználóként. A szerver törli a JWT sütit, így kilépsz a fiókból.
- **Auth:** Szükséges.
- **Válasz:**

```json
{
  "detail": "Sikeres kijelentkezés."
}
```

### POST /api/auth/register/

- **Leírás:** Regisztráció kóddal. Sikeres regisztráció után aktivációs emailt kapsz.
- **Help:** Add meg a felhasználónév, email, jelszó és regisztrációs kód mezőket. A regisztrációs kódot adminisztrátortól kapod. Sikeres regisztráció után emailben kapsz aktivációs kódot.
- **Auth:** Nem szükséges.
- **Válasz:**

```json
{
  "detail": "Registration successful"
}
```

- **Email tartalma:**
  - Tárgy: „Fiók aktiválása”
  - Szöveg: „Köszönjük a regisztrációt! Az aktiváláshoz használd ezt a kódot: {aktivációs kód}”
  - Küldő: webapp.progeek@gmail.com

### POST /api/auth/activate/

- **Leírás:** Regisztráció megerősítése aktivációs kóddal.
- **Help:** Add meg az email címedet és az aktivációs kódot, amit emailben kaptál. Sikeres aktiváció után a fiókod aktív lesz.
- **Auth:** Nem szükséges.
- **Válasz:**

```json
{
  "detail": "Fiók aktiválva."
}
```

### POST /api/auth/forgot-password/

- **Leírás:** Elfelejtett jelszó esetén reset token kérése email alapján. Emailben kapod meg a visszaállító kódot.
- **Help:** Add meg az email címedet. Ha létezik ilyen fiók, emailben kapsz egy reset kódot, amivel új jelszót állíthatsz be.
- **Auth:** Nem szükséges.
- **Válasz:**

```json
{
  "reset_token": "<token>",
  "username": "user1"
}
```

- **Email tartalma:**
  - Tárgy: „Jelszó visszaállítás”
  - Szöveg: „Jelszó visszaállításához használd ezt a kódot: {reset token}”
  - Küldő: webapp.progeek@gmail.com

### POST /api/auth/reset-password/

- **Leírás:** Jelszó visszaállítása reset token és új jelszó megadásával.
- **Help:** Add meg az email címedet, a reset kódot (amit emailben kaptál), és az új jelszót. Sikeres visszaállítás után az új jelszóval tudsz belépni.
- **Auth:** Nem szükséges.
- **Válasz:**

```json
{
  "detail": "Jelszó sikeresen módosítva."
}
```

---

## Emailes folyamatok

- Minden email a `webapp.progeek@gmail.com` címről érkezik.
- Az aktivációs/jelszó-visszaállító email tartalmazza a szükséges kódot.
- A felhasználónak a kapott kódot vagy linket kell megadnia az aktiváció/jelszó reset végpontnál.

---

## Biztonság: Throttling, JWT, CSRF/XSRF, API védelem

- **Védett API végpontok:**

  - Blog, News, Events, minden list/detail endpoint csak authentikált (JWT sütis) user számára elérhető.
  - Hibás vagy hiányzó JWT esetén 401-es hibát kapsz.
  - Tesztek: minden védett végpontra van automata teszt, ami ellenőrzi a hozzáférést.

- **Throttling (sebességkorlát):**

  - Az API korlátozza a kérések számát: bejelentkezett felhasználó max. 100/óra, anonim max. 20/óra.
  - Hiba esetén: `429 Too Many Requests`.
  - Tesztkörnyezetben a throttling kikapcsolható, hogy a tesztek ne akadjanak el.

- **CSRF/XSRF védelem:**

  - A backend minden POST/PUT/DELETE kérésnél ellenőrzi a CSRF tokent.
  - JWT sütis authentikációnál a frontendnek a CSRF tokent is el kell küldenie a `X-CSRFToken` headerben.
  - A CSRF cookie biztonságos (`CSRF_COOKIE_SECURE=True`) és csak HTTP-n keresztül olvasható (`CSRF_COOKIE_HTTPONLY=True`).
  - Tesztek: automata teszt ellenőrzi, hogy CSRF token nélkül 401/403 hibát kapunk.

- **Security tesztek:**
  - Minden védett végpontra van teszt, ami ellenőrzi, hogy authentikáció nélkül nem elérhető.
  - Hibás JWT token esetén 401-es hibát kapsz.
  - CSRF védelem tesztelve POST/PUT/DELETE kéréseknél.

---

## API cache-elés

- A blog, hírek és események listázó végpontok (GET /api/blog/, /api/news/, /api/events/) automatikusan cache-eltek 15 percig.
- Ez azt jelenti, hogy a gyakori lekérdezések gyorsabbak lesznek, a backend és az adatbázis terhelése csökken.
- A cache-t a Redis szerver kezeli, így skálázható és megbízható.
- Ha egy rekordot módosítasz (pl. új blogot, hírt vagy eseményt hozol létre), a cache automatikusan frissül a következő lekérdezésnél.
- A cache időtartama igény szerint módosítható (alapértelmezett: 15 perc).

Ez a megoldás ideális React/Vite frontendhez, ahol a gyors API válaszok kiemelten fontosak.

---

## Keresés az API-ban

- A blog, hírek és események listázó végpontokon (GET /api/blog/, /api/news/, /api/events/) keresés támogatott.
- A kereséshez nem kell külön path, csak a `search` query paramétert kell használni:
  - Példa: `/api/news/?search=progeek`
  - Példa: `/api/events/?search=Raid Day`
- A keresés a fő szöveges mezőkre vonatkozik (pl. cím, szerző, tartalom, host, típus, helyszín).
- A frontend egyszerűen a listázó végpontot hívja meg a keresési paraméterrel, az eredmény automatikusan szűrt lesz.

Ez gyors és felhasználóbarát keresést biztosít minden fő API listázó végponton.

---

## Adatbázis (Neon PostgreSQL)

- A backend és a dbt egyaránt a Neon PostgreSQL cloud adatbázist használja.
- Az adatbázis-csatlakozási adatok a `.env` fájlban találhatók, így biztonságosan és könnyen kezelhetők.
- A Neon ingyenes verziója is bővíthető később: nagyobb tárhely, több compute, fizetős csomag, backup, SLA.
- A Neon admin felületen a kliens bármikor növelheti a kapacitást, az adatok és táblák megmaradnak.
- A migrációk, adatok, kapcsolatok automatikusan Neonban vannak, nincs szükség kódmódosításra bővítéskor.
- Production-ready, skálázható, biztonságos adatbázis, ideális modern webes backendhez.

---

## Cloudinary képfeltöltés

- A backend képfeltöltéshez a Cloudinary szolgáltatást használja.
- A Cloudinary API kulcsok a `.env` fájlban találhatók: `CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>`.
- A képek feltöltése automatikusan a Cloudinaryba történik, így nem terheli a szerver tárhelyét.
- A Cloudinary integráció biztonságos, gyors és skálázható képfeldolgozást biztosít.
- A feltöltött képek URL-je automatikusan bekerül az adatbázisba, így a frontend egyszerűen megjelenítheti őket.
- A Cloudinary admin felületen a kliens bármikor kezelheti a képeket, statisztikákat, beállításokat.
- A Cloudinary ingyenes csomagja is elegendő a legtöbb webes projekthez, később bővíthető.
