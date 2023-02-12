"""
Python 3.9 программа считывает страницу и сохраняет ее в pdf файле
Название файла config.py

Version: 0.1
Author: Andrej Marinchenko
Date: 2023-02-12
"""
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPageLayout, QPageSize
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loader = QWebEngineView()
    loader.setZoomFactor(1)
    layout = QPageLayout()
    layout.setPageSize(QPageSize(QPageSize.A4Extra))
    layout.setOrientation(QPageLayout.Portrait)

    loader.load(QUrl('https://github.com/Sindou-dedv'))
    loader.page().pdfPrintingFinished.connect(lambda *args: QApplication.exit())

    def emit_pdf(finished):
        loader.page().printToPdf(r"pdf\test.pdf", pageLayout=layout)

    loader.loadFinished.connect(emit_pdf)
    sys.exit(app.exec_())

