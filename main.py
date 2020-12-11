from sys import exit
from PyQt5 import QtWidgets
from restaurant import terminal


def main():
    app = QtWidgets.QApplication([])
    terminal_1 = terminal.Terminal()
    if terminal_1.worked:
        terminal_1.show()
        exit(app.exec())


if __name__ == "__main__":
    main()
