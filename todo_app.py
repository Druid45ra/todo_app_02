import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox,
    QComboBox, QDateEdit, QDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon

# Setări globale
DB_NAME = "tasks.db"
CATEGORIES = ["Personal", "Muncă", "Studii", "Altele"]
PRIORITIES = ["Scăzută", "Medie", "Ridicată"]

# === DatabaseManager ===
class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                deadline TEXT,
                priority TEXT,
                category TEXT
            )
        """)
        self.conn.commit()

    def add_task(self, description, deadline, priority, category):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (description, deadline, priority, category) VALUES (?, ?, ?, ?)",
            (description, deadline, priority, category)
        )
        self.conn.commit()

    def get_tasks(self, category=None):
        cursor = self.conn.cursor()
        if category == "Toate" or category is None:
            cursor.execute("SELECT id, description, deadline, priority, category FROM tasks ORDER BY deadline ASC")
        else:
            cursor.execute(
                "SELECT id, description, deadline, priority, category FROM tasks WHERE category = ? ORDER BY deadline ASC",
                (category,)
            )
        return cursor.fetchall()

    def get_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT description, deadline, priority, category FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone()

    def update_task(self, task_id, description, deadline, priority, category):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tasks SET description = ?, deadline = ?, priority = ?, category = ? WHERE id = ?",
            (description, deadline, priority, category, task_id)
        )
        self.conn.commit()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

# === CustomEditDialog ===
class CustomEditDialog(QDialog):
    def __init__(self, description, deadline, priority, category):
        super().__init__()
        self.setWindowTitle("Editează Task")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.desc_input = QLineEdit()
        self.desc_input.setText(description)
        layout.addWidget(QLabel("Descriere:"))
        layout.addWidget(self.desc_input)

        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        if deadline:
            self.deadline_edit.setDate(QDate.fromString(deadline, "yyyy-MM-dd"))
        else:
            self.deadline_edit.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Deadline:"))
        layout.addWidget(self.deadline_edit)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(PRIORITIES)
        self.priority_combo.setCurrentText(priority)
        layout.addWidget(QLabel("Prioritate:"))
        layout.addWidget(self.priority_combo)

        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        self.category_combo.setCurrentText(category)
        layout.addWidget(QLabel("Categorie:"))
        layout.addWidget(self.category_combo)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Salvează")
        self.cancel_btn = QPushButton("Anulează")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        self.setLayout(layout)

    def get_data(self):
        return (
            self.desc_input.text().strip(),
            self.deadline_edit.date().toString("yyyy-MM-dd"),
            self.priority_combo.currentText(),
            self.category_combo.currentText()
        )

# === ToDoApp principal ===
class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List App")
        self.resize(550, 600)
        self.setMinimumSize(500, 550)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #0078d7;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 6px;
                padding: 10px 15px;
                font-weight: 600;
                border: none;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
            QPushButton:disabled {
                background-color: #a6a6a6;
                color: #e1e1e1;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 5px;
                font-size: 15px;
            }
            QLabel#statusLabel {
                color: #0078d7;
                font-weight: 600;
                margin-top: 10px;
            }
            QLabel {
                font-weight: 600;
            }
        """)

        self.db = DatabaseManager(DB_NAME)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Introdu un nou task...")
        self.task_input.setClearButtonEnabled(True)
        self.layout.addWidget(self.task_input)

        extra_layout = QHBoxLayout()
        extra_layout.setSpacing(15)

        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate())
        extra_layout.addWidget(QLabel("Deadline:"))
        extra_layout.addWidget(self.deadline_edit)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(PRIORITIES)
        self.priority_combo.setCurrentIndex(1)
        extra_layout.addWidget(QLabel("Prioritate:"))
        extra_layout.addWidget(self.priority_combo)

        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        extra_layout.addWidget(QLabel("Categorie:"))
        extra_layout.addWidget(self.category_combo)

        self.layout.addLayout(extra_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.add_btn = QPushButton("Adaugă")
        self.edit_btn = QPushButton("Editează")
        self.delete_btn = QPushButton("Șterge")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        self.layout.addLayout(btn_layout)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrează după categorie:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Toate")
        self.filter_combo.addItems(CATEGORIES)
        filter_layout.addWidget(self.filter_combo)
        self.layout.addLayout(filter_layout)

        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.task_list)

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.layout.addWidget(self.status_label)

        self.add_btn.clicked.connect(self.add_task)
        self.edit_btn.clicked.connect(self.edit_task)
        self.delete_btn.clicked.connect(self.delete_task)
        self.task_input.returnPressed.connect(self.add_task)
        self.task_list.itemSelectionChanged.connect(self.update_buttons_state)
        self.filter_combo.currentIndexChanged.connect(self.load_tasks)

        self.load_tasks()
        self.update_buttons_state()

    def load_tasks(self):
        self.task_list.clear()
        selected_category = self.filter_combo.currentText()
        tasks = self.db.get_tasks(selected_category)
        for task_id, desc, deadline, priority, category in tasks:
            deadline_str = deadline if deadline else "Fără deadline"
            item_text = f"{task_id}: {desc} | Deadline: {deadline_str} | Prioritate: {priority} | Categorie: {category}"
            self.task_list.addItem(item_text)
        self.status_label.setText(f"{len(tasks)} task-uri afișate.")

    def add_task(self):
        desc = self.task_input.text().strip()
        if not desc:
            QMessageBox.warning(self, "Eroare", "Task-ul nu poate fi gol!")
            return
        deadline = self.deadline_edit.date().toString("yyyy-MM-dd")
        priority = self.priority_combo.currentText()
        category = self.category_combo.currentText()

        self.db.add_task(desc, deadline, priority, category)
        self.task_input.clear()
        self.deadline_edit.setDate(QDate.currentDate())
        self.priority_combo.setCurrentIndex(1)
        self.category_combo.setCurrentIndex(0)
        self.load_tasks()
        self.status_label.setText("Task adăugat cu succes!")
        self.task_input.setFocus()

    def edit_task(self):
        current = self.task_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Eroare", "Selectează un task pentru editare!")
            return
        task_id = int(current.text().split(":")[0])
        row = self.db.get_task(task_id)
        if not row:
            QMessageBox.warning(self, "Eroare", "Task-ul nu a fost găsit!")
            return

        dialog = CustomEditDialog(*row)
        if dialog.exec():
            new_desc, new_deadline, new_priority, new_category = dialog.get_data()
            if not new_desc:
                QMessageBox.warning(self, "Eroare", "Descrierea nu poate fi goală!")
                return
            self.db.update_task(task_id, new_desc, new_deadline, new_priority, new_category)
            self.load_tasks()
            self.status_label.setText("Task editat cu succes!")

    def delete_task(self):
        current = self.task_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Eroare", "Selectează un task pentru ștergere!")
            return
        task_id = int(current.text().split(":")[0])
        reply = QMessageBox.question(
            self, "Confirmare",
            "Ești sigur că vrei să ștergi acest task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_task(task_id)
            self.load_tasks()
            self.status_label.setText("Task șters cu succes!")

    def update_buttons_state(self):
        has_selection = self.task_list.currentItem() is not None
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
