# To-Do List App 🗂️
# Despre To-Do List App 🗂️

Această aplicație **To-Do List** este un instrument simplu și modern, creat pentru a te ajuta să-ți organizezi sarcinile zilnice într-un mod clar și eficient.

Proiectul este dezvoltat cu **Python** și **PyQt6**, cu un design intuitiv și funcționalități utile:
- ✅ Adaugă sarcini cu deadline, prioritate și categorie.
- ✅ Editează și actualizează rapid orice task.
- ✅ Filtrează taskurile după categorie pentru o mai bună organizare.
- ✅ Stochează toate datele local, sigur, într-o bază de date SQLite.
- ✅ UI modern, ușor de folosit, cu accent pe simplitate și productivitate.

Scopul aplicației este de a demonstra o structură clară pentru un proiect GUI Python, combinând un front-end atractiv cu o logică backend minimalistă, robustă și ușor de extins.

---

## 🧑‍💻 **Public țintă**

Proiectul este gândit pentru:
- Utilizatori care vor un mic organizator local, fără cloud.
- Programatori care vor să înțeleagă cum se implementează o aplicație desktop Python cu PyQt6 și SQLite.
- Oricine își dorește un exemplu practic de aplicație CRUD cu interfață grafică.

---

## 🚀 **Planuri de viitor**

- Export CSV/PDF.
- Notificări locale pentru deadline-uri.
- Backup automat și/sau sincronizare cloud.
- Temă light/dark.

---

## 📜 **Status**

Proiectul este public și open-source, sub licență MIT. Poți contribui, folosi, adapta și distribui liber.

---

Îți mulțumim că folosești sau contribui la acest proiect! 💙

Aceasta este o aplicație **To-Do List** modernă, dezvoltată cu **Python** și **PyQt6**, care permite:
- adăugarea rapidă de taskuri cu deadline, prioritate și categorie,
- editarea completă a unui task cu un dialog personalizat,
- filtrarea taskurilor după categorie,
- salvarea persistentă a datelor într-o bază de date SQLite locală.

---

## 📦 **Structură**

├── todo_app.py
├── requirements.txt
├── tasks.db (se generează automat)


---

## 🚀 **Cum rulezi aplicația**

1️⃣ Clonează sau descarcă proiectul.

2️⃣ (Opțional) Creează un mediu virtual:
```bash
python -m venv venv

3️⃣ Activează mediul virtual:
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

4️⃣ Instalează dependențele:
pip install -r requirements.txt

5️⃣ Rulează aplicația:
python todo_app.py

