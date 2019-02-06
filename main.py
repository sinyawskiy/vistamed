from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QTabWidget, QDialog
from PyQt5.QtWidgets import QApplication, QToolBar, QAction, QMainWindow
from sqlalchemy import exc, create_engine, orm
from db import Base
from dialogs import AddWishItem
from widgets import WishTable
import sys


class MainWindow(QMainWindow):
    def __init__(self, db_session):
        self.wish_table = None
        QMainWindow.__init__(self)
        self.init_ui()
        self.db_session = db_session
        self.display_data()
        self.show()

    def init_ui(self):
        self.set_and_center_the_window(1024, 768)
        self.setWindowTitle('Список желаний')
        self.setWindowIcon(QIcon(r'img/star.png'))

        wish_action = QAction(
            QIcon(r'img/star.png'), 'Добавить новое желание', self
        )
        wish_action.triggered.connect(self.add_wish)

        toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        toolbar.addActions(
            [wish_action]
        )

    def display_data(self):
        try:
            self.wish_table = WishTable(self. db_session, self)
            tab_widget = QTabWidget()
            tab_widget.addTab(self.wish_table, "Желания")
            self.setCentralWidget(tab_widget)
        except exc.IntegrityError as errmsg:
            print(errmsg)
            self.db_session.rollback()
            self.db_session.close()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Критическая ошибка базы данных")
            msg.setWindowTitle("Критическая ошибка")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)

    def add_wish(self):
        try:
            wish_window = AddWishItem(self.db_session)
            if wish_window.exec_() == QDialog.Accepted:
                self.db_session.commit()
                print("Закоммитили")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            self.db_session.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Критическая ошибка базы данных")
            msg.setWindowTitle("Критическая ошибка")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
        else:
            print('Все успешно')
        finally:
            self.db_session.close()
            self.wish_table.fill_table()

    def set_and_center_the_window(self, x, y):
        self.resize(1280, 768)
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

# CREATE DATABASE IF NOT EXISTS wishlist CHARACTER SET utf8 COLLATE utf8_general_ci;
# GRANT ALL PRIVILEGES ON wishlist.* TO 'wishlist'@'localhost' IDENTIFIED BY 'wishlist'

DB = {
    'host': 'localhost',
    'port': 3306,
    'login': 'wishlist',
    'username': 'wishlist',
    'password': 'wishlist',
    'database': 'wishlist'
}


def run():
    db_engine = create_engine('mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(**DB))
    db_session = orm.Session(bind=db_engine)
    Base.metadata.create_all(db_engine)

    app = QApplication([])
    app.processEvents()
    main_window = MainWindow(db_session)
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
