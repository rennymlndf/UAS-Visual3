import mysql.connector as mc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

class Ui_ProductForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        
        self.setupInputFields(Form)
        self.setupButtons(Form)
        self.setupSearchAndTable(Form)
        
        self.labelResult = QtWidgets.QLabel(Form)
        self.labelResult.setText("")
        self.gridLayout.addWidget(self.labelResult, 8, 0, 1, 2)
        
        self.connectButtons()

    def setupInputFields(self, Form):
        self.inputLayout = QtWidgets.QGridLayout()
        self.labelBarkode = QtWidgets.QLabel(Form)
        self.labelBarkode.setText("Barkode")
        self.lineEditBarkode = QtWidgets.QLineEdit(Form)
        self.inputLayout.addWidget(self.labelBarkode, 0, 0)
        self.inputLayout.addWidget(self.lineEditBarkode, 0, 1)
        self.labelName = QtWidgets.QLabel(Form)
        self.labelName.setText("Nama")
        self.lineEditName = QtWidgets.QLineEdit(Form)
        self.inputLayout.addWidget(self.labelName, 1, 0)
        self.inputLayout.addWidget(self.lineEditName, 1, 1)
        self.labelKategori = QtWidgets.QLabel(Form)
        self.labelKategori.setText("Kategori")
        self.lineEditKategori = QtWidgets.QLineEdit(Form)
        self.inputLayout.addWidget(self.labelKategori, 2, 0)
        self.inputLayout.addWidget(self.lineEditKategori, 2, 1)
        self.labelQty = QtWidgets.QLabel(Form)
        self.labelQty.setText("Jumlah (Qty)")
        self.lineEditQty = QtWidgets.QLineEdit(Form)
        self.inputLayout.addWidget(self.labelQty, 3, 0)
        self.inputLayout.addWidget(self.lineEditQty, 3, 1)
        self.labelHarga = QtWidgets.QLabel(Form)
        self.labelHarga.setText("Harga")
        self.lineEditHarga = QtWidgets.QLineEdit(Form)
        self.inputLayout.addWidget(self.labelHarga, 4, 0)
        self.inputLayout.addWidget(self.lineEditHarga, 4, 1)

        self.gridLayout.addLayout(self.inputLayout, 0, 0)

    def setupButtons(self, Form):
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.pushButtonInsert = QtWidgets.QPushButton(Form)
        self.pushButtonInsert.setText("Insert Data")
        self.buttonLayout.addWidget(self.pushButtonInsert)

        self.pushButtonUpdate = QtWidgets.QPushButton(Form)
        self.pushButtonUpdate.setText("Update Data")
        self.buttonLayout.addWidget(self.pushButtonUpdate)

        self.pushButtonDelete = QtWidgets.QPushButton(Form)
        self.pushButtonDelete.setText("Delete Data")
        self.buttonLayout.addWidget(self.pushButtonDelete)

        self.pushButtonLoad = QtWidgets.QPushButton(Form)
        self.pushButtonLoad.setText("Load Data")
        self.buttonLayout.addWidget(self.pushButtonLoad)

        self.gridLayout.addLayout(self.buttonLayout, 5, 0)

    def setupSearchAndTable(self, Form):
        self.searchLayout = QtWidgets.QHBoxLayout()

        self.lineEditSearch = QtWidgets.QLineEdit(Form)
        self.lineEditSearch.setPlaceholderText("")
        self.searchLayout.addWidget(self.lineEditSearch)

        self.pushButtonSearch = QtWidgets.QPushButton(Form)
        self.pushButtonSearch.setText("Search Data")
        self.searchLayout.addWidget(self.pushButtonSearch)

        self.gridLayout.addLayout(self.searchLayout, 6, 0)

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Barkode", "Nama", "Kategori", "Qty", "Harga"])
        self.tableWidget.cellClicked.connect(self.selectRowForEditDelete)
        self.gridLayout.addWidget(self.tableWidget, 7, 0)

    def connectButtons(self):
        self.pushButtonInsert.clicked.connect(self.insertProduct)
        self.pushButtonUpdate.clicked.connect(self.updateProduct)
        self.pushButtonDelete.clicked.connect(self.deleteProduct)
        self.pushButtonLoad.clicked.connect(self.loadProducts)
        self.pushButtonSearch.clicked.connect(self.searchProduct)

    def connectDatabase(self):
        try:
            return mc.connect(
                host="localhost",
                port="3306",
                user="root",
                password="",
                database="db_penjualan"
            )
        except mc.Error as e:
            self.labelResult.setText("Gagal terhubung ke database")
            print(e)
            return None

    def insertProduct(self):
        try:
            mydb = self.connectDatabase()
            if not mydb:
                return
            cursor = mydb.cursor()

            barkode = self.lineEditBarkode.text()
            name = self.lineEditName.text()
            kategori = self.lineEditKategori.text()
            qty = self.lineEditQty.text()
            harga = self.lineEditHarga.text()

            sql = "INSERT INTO product (barkode, name, kategori, qty, harga) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (barkode, name, kategori, qty, harga))
            mydb.commit()
            self.loadProducts()
            self.labelResult.setText("Data berhasil ditambahkan")
        except mc.Error as e:
            self.labelResult.setText("Gagal menambahkan data")
            print(e)

    def loadProducts(self):
        try:
            mydb = self.connectDatabase()
            if not mydb:
                return
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM product ORDER BY id ASC")
            result = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.labelResult.setText("Data berhasil dimuat")
        except mc.Error as e:
            self.labelResult.setText("Gagal memuat data")
            print(e)

    def updateProduct(self):
        try:
            mydb = self.connectDatabase()
            if not mydb:
                return
            cursor = mydb.cursor()

            id = self.selectedId
            barkode = self.lineEditBarkode.text()
            name = self.lineEditName.text()
            kategori = self.lineEditKategori.text()
            qty = self.lineEditQty.text()
            harga = self.lineEditHarga.text()

            sql = """
            UPDATE product SET barkode = %s, name = %s, kategori = %s, qty = %s, harga = %s WHERE id = %s
            """
            cursor.execute(sql, (barkode, name, kategori, qty, harga, id))
            if cursor.rowcount == 0:
                self.labelResult.setText("ID tidak ditemukan")
            else:
                mydb.commit()
                self.loadProducts()
                self.labelResult.setText("Data berhasil diperbarui")
        except mc.Error as e:
            self.labelResult.setText("Gagal memperbarui data")
            print(e)

    def deleteProduct(self):
        try:
            mydb = self.connectDatabase()
            if not mydb:
                return
            cursor = mydb.cursor()
            id = self.selectedId

            sql = "DELETE FROM product WHERE id = %s"
            cursor.execute(sql, (id,))
            if cursor.rowcount == 0:
                self.labelResult.setText("ID tidak ditemukan")
            else:
                mydb.commit()
                self.loadProducts()
                self.labelResult.setText("Data berhasil dihapus")
        except mc.Error as e:
            self.labelResult.setText("Gagal menghapus data")
            print(e)

    def searchProduct(self):
        search_term = self.lineEditSearch.text().strip()
        if not search_term:
            self.labelResult.setText("Masukkan nama produk untuk mencari")
            return
        
        try:
            mydb = self.connectDatabase()
            if not mydb:
                return
            cursor = mydb.cursor()
            sql = "SELECT * FROM product WHERE name LIKE %s"
            cursor.execute(sql, ('%' + search_term + '%',))
            result = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            if not result:
                self.labelResult.setText("Produk tidak ditemukan")
            else:
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            self.labelResult.setText("Pencarian selesai")
        except mc.Error as e:
            self.labelResult.setText("Gagal melakukan pencarian")
            print(e)

    def selectRowForEditDelete(self, row, column):
        item_id = self.tableWidget.item(row, 0) 
        if item_id:
            self.selectedId = item_id.text()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_ProductForm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())