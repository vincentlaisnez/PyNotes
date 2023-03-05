from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QListWidget, QTextEdit, QGridLayout, QInputDialog,
                               QListWidgetItem)

from api.note import Note, get_notes


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyNotes")
        self.setup_ui()
        self.populate_notes()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.btn_createNote = QPushButton("Créer une note")
        self.lw_notes = QListWidget()
        self.te_contenu = QTextEdit()

    def modify_widgets(self):
        css_file = "ressources/style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        self.main_layout = QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_createNote, 0, 0, 1, 1)
        self.main_layout.addWidget(self.lw_notes, 1, 0, 1, 1)
        self.main_layout.addWidget(self.te_contenu, 0, 1, 2, 1)

    def setup_connections(self):
        self.btn_createNote.clicked.connect(self.create_note)
        self.te_contenu.textChanged.connect(self.save_note)
        self.lw_notes.itemSelectionChanged.connect(self.populate_note_content)
        QShortcut(QKeySequence("Delete"), self.lw_notes, self.delete_selected_note)

    # END UI

    def add_note_to_listwidget(self, note):
        lw_item = QListWidgetItem(note.title)
        lw_item.note = note
        self.lw_notes.addItem(lw_item)

    def create_note(self):
        titre, resultat = QInputDialog.getText(self, "Ajouter une note", "Titre: ")
        if resultat and titre:
            note = Note(title=titre)
            note.save()
            self.add_note_to_listwidget(note)

    def delete_selected_note(self):
        if selected_item := self.get_selected_lw_item():
            if resultat := selected_item.note.delete():
                self.lw_notes.takeItem(self.lw_notes.row(selected_item))

    def get_selected_lw_item(self):
        if selected_items := self.lw_notes.selectedItems():
            return selected_items[0]
        return None

    def populate_notes(self):
        notes = get_notes()
        for note in notes:
            self.add_note_to_listwidget(note)

    def populate_note_content(self):
        if selected_item := self.get_selected_lw_item():
            self.te_contenu.setText(selected_item.note.content)
        else:
            self.te_contenu.clear()

    def save_note(self):
        if selected_item := self.get_selected_lw_item():
            selected_item.note.content = self.te_contenu.toPlainText()
            selected_item.note.save()


if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    main_window.resize(550, 600)
    main_window.show()
    app.exec()
