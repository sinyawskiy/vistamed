from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import QPushButton, QWidget, QFormLayout, QDialog
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QHBoxLayout, QStackedLayout

from db import WishItem
from .exitmethods import Dialog


class AddWishItem(Dialog):
    def __init__(self, db_session):
        super(Dialog, self).__init__()
        self.db_session = db_session
        QStackedLayout(self)
        self.layout().addWidget(self.get_edit_layout())
        self.init_window()

    def get_edit_layout(self):

        edit_info_widget = QWidget()
        edit_info_layout = QFormLayout(edit_info_widget)

        self.title_edit = QLineEdit()
        edit_info_layout.addRow(
            '<b>Название:<font color="red">*</font></b>', self.title_edit
        )
        self.price_edit = QLineEdit()
        edit_info_layout.addRow(
            'Цена:', self.price_edit
        )
        self.url_edit = QLineEdit()
        edit_info_layout.addRow(
            'Ссылка', self.url_edit
        )
        self.description_edit = QLineEdit()
        edit_info_layout.addRow(
            'Описание', self.description_edit
        )

        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.back)
        self.add_button = QPushButton('Добавить и выйти')
        self.add_button.clicked.connect(self.validate_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.back_button)
        buttons_layout.addWidget(self.add_button)
        edit_info_layout.addRow(buttons_layout)

        return edit_info_widget

    @pyqtSlot()
    def back(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Данные не сохранятся')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Ок')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Отменить')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            self.layout().setCurrentIndex(0)
            self.setFixedSize(800, 450)
            QDialog.accept(self)

    @pyqtSlot()
    def validate_input(self):
        if not self.title_edit.text():
            QMessageBox.warning(
                self, 'Предупреждение', "Поле: 'Название' -- обязательноe"
            )

        try:
            wish_item = WishItem()
            wish_item.title = self.title_edit.text()
            try:
                price = float(self.price_edit.text())
            except ValueError:
                price = 0
            wish_item.price = price
            wish_item.url = self.url_edit.text()
            wish_item.description = self.description_edit.text()

            self.db_session.add(wish_item)
        except (Exception,) as errmsg:
            print(errmsg)
            QMessageBox.warning(
                self, 'Ошибка',
                'Другой пользователь ввел изменения'
            )
        finally:
            QDialog.accept(self)

    def init_window(self):
        self.setFixedSize(800, 450)
        self.setWindowModality(2)
        self.setWindowTitle('Добавление желания')
        self.setWindowIcon(QIcon(r'pics/star.png'))


class EditWishItem(Dialog):
    def __init__(self, db_session, wish_item):
        super(Dialog, self).__init__()
        self.db_session = db_session
        self.wish_item = wish_item
        self.sti = QStandardItemModel()
        QStackedLayout(self)
        self.layout().addWidget(self.get_edit_layout())
        self.set_lines()
        self.init_window()

    def init_window(self):
        self.setFixedSize(800, 450)
        self.setWindowModality(2)
        self.setWindowTitle('{}. {}'.format(self.wish_item._id, self.wish_item.title))
        self.setWindowIcon(QIcon(r'pics/star.png'))

    def get_edit_layout(self):

        edit_info_widget = QWidget()
        edit_info_layout = QFormLayout(edit_info_widget)

        self.title_edit = QLineEdit()
        edit_info_layout.addRow(
            '<b>Название:<font color="red">*</font></b>', self.title_edit
        )
        self.price_edit = QLineEdit()
        edit_info_layout.addRow(
            'Цена:', self.price_edit
        )
        self.url_edit = QLineEdit()
        edit_info_layout.addRow(
            'Ссылка', self.url_edit
        )
        self.description_edit = QLineEdit()
        edit_info_layout.addRow(
            'Описание', self.description_edit
        )

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_wish_item)
        self.back_button = QPushButton('Назад')
        self.back_button.clicked.connect(self.back)
        self.refresh_button = QPushButton('Сбросить')
        self.refresh_button.clicked.connect(self.refresh)
        self.edit_button = QPushButton('Сохранить и выйти')
        self.edit_button.clicked.connect(self.validate_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.back_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.edit_button)
        edit_info_layout.addRow(buttons_layout)

        return edit_info_widget

    def set_lines(self):
        self.title_edit.setText(self.wish_item.title)
        self.price_edit.setText('{}'.format(self.wish_item.price))
        self.url_edit.setText(self.wish_item.url)
        self.description_edit.setText(self.wish_item.description)

    @pyqtSlot()
    def back(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Данные не сохранятся')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Ок')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Отменить')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            self.db_session.rollback()
            self.sti.clear()
            self.set_lines()
            self.layout().setCurrentIndex(0)
            self.setFixedSize(800, 450)
            QDialog.accept(self)

    @pyqtSlot()
    def refresh(self):
        self.db_session.rollback()
        self.set_lines()
        self.sti.clear()

    @pyqtSlot()
    def delete_wish_item(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Уведомление')
        msg_box.setText('Подтвердить удаление')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Да')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Нет')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            try:
                self.db_session.delete(self.wish_item)
            except Exception:
                QMessageBox.warning(
                    self, 'Ошибка',
                    'Другой пользователь ввел изменения'
                )
            finally:
                QDialog.accept(self)

    @pyqtSlot()
    def validate_input(self):
        if not self.title_edit.text():
            QMessageBox.warning(
                self, 'Предупреждение', "Поле: 'Название' -- обязательноe"
            )

        try:
            self.wish_item.title = self.title_edit.text()
            self.wish_item.price = float(self.price_edit.text())
            self.wish_item.url = self.url_edit.text()
            self.wish_item.description = self.description_edit.text()

            self.db_session.add(self.wish_item)
        except (Exception,) as errmsg:
            print(errmsg)
            QMessageBox.warning(
                self, 'Ошибка',
                'Другой пользователь ввел изменения'
            )
        finally:
            QDialog.accept(self)



