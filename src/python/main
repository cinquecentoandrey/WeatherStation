import lib

def main():

    lib.serial.readyRead.connect(lib.read_func)
    lib.ui.open_button.clicked.connect(lib.portOpen)
    lib.ui.close_button.clicked.connect(lib.portClose)
    lib.ui.show()
    lib.app.exec()

if __name__ == '__main__':
    main()
