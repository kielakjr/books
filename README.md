# 📚 Books & Reviews API

Projekt REST API do zarządzania książkami i ich recenzjami, zbudowany w oparciu o **FastAPI** i **SQLALCHEMY**

---

## 🚀 Funkcje

- CRUD dla książek i recenzji
- Automatyczne przeliczanie średniej oceny książki po dodaniu/edycji/usunięciu recenzji
- Walidacja danych wejściowych z użyciem Pydantic
- Obsługa błędów (404, 422, itd.)

---

## 🛠️ Stos technologiczny

- **FastAPI** - backend REST
- **SQLAlchemy 2.0** - ORM
- **Pydantic** - walidacja schematów
- **Uvicorn** - serwer ASGI

---

## 🧪 Endpointy API

### 📖 Książki

| Metoda | Endpoint         | Opis                       |
|--------|------------------|----------------------------|
| `GET`  | `/books/`        | Pobierz wszystkie książki |
| `GET`  | `/books/{id}`    | Pobierz konkretną książkę |
| `POST` | `/books/`        | Dodaj nową książkę        |
| `PATCH`  | `/books/{id}`    | Zaktualizuj książkę       |
| `DELETE` | `/books/{id}`  | Usuń książkę              |

### 📝 Recenzje

| Metoda | Endpoint                          | Opis                             |
|--------|-----------------------------------|----------------------------------|
| `POST` | `/books/{book_id}/reviews/`       | Dodaj recenzję do książki        |
| `PATCH`  | `/reviews/{review_id}`            | Zaktualizuj recenzję             |
| `DELETE` | `/reviews/{review_id}`          | Usuń recenzję                    |

---

## ⚙️ Instalacja

### 1. Klonuj repozytorium

```bash
git clone https://github.com/kielakjr/books.git
cd books
