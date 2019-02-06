from PyQt5 import QtCore
from functools import partial
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QTableWidget, QDialog, QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QPushButton
from db import WishItem
from dialogs import EditWishItem


class WishTable(QWidget):
    def __init__(self, db_session, parent):
        QWidget.__init__(self)
        self.db_session = db_session
        self.parent = parent
        QVBoxLayout(self)
        self.main_table = self.draw_table()
        self.layout().addWidget(self.main_table)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.fill_table()
        QApplication.restoreOverrideCursor()

    @QtCore.pyqtSlot(WishItem)
    def edit_wish_item(self, wish_item_query_obj):
        try:
            edit_wish_item_window = EditWishItem(self.db_session, wish_item_query_obj)
            if edit_wish_item_window.exec_() == QDialog.Accepted:
                self.db_session.commit()
                self.fill_table()
                QApplication.restoreOverrideCursor()
                print('Закоммитили')
        except exc.IntegrityError as errmsg:
            print(errmsg)
            self.session.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Критическая ошибка базы данных')
            msg.setWindowTitle('Критическая ошибка')
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
        else:
            print('Все успешно')

    def fill_table(self):

        self.main_table.setRowCount(0)
        wish_items = self.db_session.query(WishItem)

        for row, wish_item in enumerate(wish_items):
            print(row, wish_item)
            self.main_table.insertRow(row)
            self.main_table.setRowHeight(row, 50)
            self.main_table.setItem(row, 0, QTableWidgetItem(wish_item.title))
            self.main_table.setItem(row, 1, QTableWidgetItem('{}'.format(wish_item.price)))
            self.main_table.setItem(row, 2, QTableWidgetItem(wish_item.url))
            self.main_table.setItem(row, 3, QTableWidgetItem(wish_item.description))

            edit_button = QPushButton('Изменить')
            edit_button.clicked.connect(
                partial(self.edit_wish_item, wish_item_query_obj=wish_item)
            )
            self.main_table.setCellWidget(row, 4, edit_button)
            self.main_table.resizeColumnsToContents()

    def draw_table(self):
        main_table = QTableWidget()
        main_table.setSortingEnabled(True)
        main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        main_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        main_table.setTextElideMode(Qt.ElideNone)
        main_table.setAlternatingRowColors(True)
        main_table.setColumnCount(5)
        main_table.setHorizontalHeaderLabels(
            ['Название', 'Цена', 'Ссылка', 'Описание', '']
        )

        return main_table
