import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, 
    QTableWidgetItem, QDialog, QLineEdit, QComboBox, QLabel, QHBoxLayout, QMessageBox
)
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QDialog, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QComboBox, QMessageBox, QInputDialog


# Конфигурация подключения к базе данных
DB_CONFIG = {
    'dbname': '',
    'user': '',
    'password': '',
    'host': '',
    'port': ''
}


def get_connection():
    """Создает соединение с базой данных."""
    return psycopg2.connect(**DB_CONFIG)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(200, 200, 400, 400)
        
        self.layout = QVBoxLayout()
        
        self.btn_departments = QPushButton("Управление подразделениями")
        self.btn_positions = QPushButton("Управление должностями")
        self.btn_employees = QPushButton("Управление сотрудниками")
        self.btn_advanced_view = QPushButton("Расширенный просмотр сотрудников")
        self.btn_education = QPushButton("Управление образованием")
        self.btn_history = QPushButton("Просмотр истории")
        
        self.layout.addWidget(self.btn_departments)
        self.layout.addWidget(self.btn_positions)
        self.layout.addWidget(self.btn_employees)
        self.layout.addWidget(self.btn_advanced_view)
        self.layout.addWidget(self.btn_history)
        self.layout.addWidget(self.btn_education)
        
        # Соединение кнопок с окнами
        self.btn_departments.clicked.connect(self.open_departments_window)
        self.btn_positions.clicked.connect(self.open_positions_window)
        self.btn_employees.clicked.connect(self.open_employees_window)
        self.btn_advanced_view.clicked.connect(self.open_advanced_view)
        self.btn_history.clicked.connect(self.open_history_view)
        self.btn_education.clicked.connect(self.open_education_window)  # Убираем дублирование
        
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def open_departments_window(self):
        self.departments_window = DepartmentsWindow()
        self.departments_window.exec_()
    
    def open_positions_window(self):
        self.positions_window = PositionsWindow()
        self.positions_window.exec_()
    
    def open_employees_window(self):
        self.employees_window = EmployeesWindow()
        self.employees_window.exec_()
    
    def open_advanced_view(self):
        self.advanced_view = AdvancedEmployeeView()
        self.advanced_view.exec_()
    
    def open_history_view(self):
        self.history_view = HistoryView()
        self.history_view.exec_()
    
    def open_education_window(self):  # Исправлен отступ
        self.education_window = EducationWindow()
        self.education_window.exec_()


class DepartmentsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление подразделениями")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        self.btn_add = QPushButton("Добавить")
        self.btn_update = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_update)
        self.layout.addWidget(self.btn_delete)
        
        self.setLayout(self.layout)
        
        # Соединение кнопок с функциями
        self.btn_add.clicked.connect(self.add_department)
        self.btn_update.clicked.connect(self.update_department)
        self.btn_delete.clicked.connect(self.delete_department)
        
        self.load_departments()
    
    def load_departments(self):
        """Загружает список подразделений из базы данных."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Departments")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Название"])
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
        connection.close()
    
    def add_department(self):
        """Добавляет новое подразделение."""
        name, ok = QInputDialog.getText(self, "Добавить подразделение", "Название подразделения:")
        if ok and name:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Departments (DepartmentName) VALUES (%s)", (name,))
            connection.commit()
            connection.close()
            self.load_departments()
    
    def update_department(self):
        """Обновляет выбранное подразделение."""
        row = self.table.currentRow()
        if row >= 0:
            department_id = self.table.item(row, 0).text()
            name, ok = QInputDialog.getText(self, "Изменить подразделение", "Новое название подразделения:")
            if ok and name:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE Departments SET DepartmentName = %s WHERE DepartmentID = %s", (name, department_id))
                connection.commit()
                connection.close()
                self.load_departments()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите подразделение для изменения.")
    
    def delete_department(self):
        """Удаляет выбранное подразделение."""
        row = self.table.currentRow()
        if row >= 0:
            department_id = self.table.item(row, 0).text()
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Departments WHERE DepartmentID = %s", (department_id,))
            connection.commit()
            connection.close()
            self.load_departments()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите подразделение для удаления.")


# Аналогично создаются окна PositionsWindow, EmployeesWindow, ExtendedViewWindow и HistoryWindow.

class PositionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление должностями")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        self.btn_add = QPushButton("Добавить")
        self.btn_update = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_update)
        self.layout.addWidget(self.btn_delete)
        
        self.setLayout(self.layout)
        
        # Соединение кнопок с функциями
        self.btn_add.clicked.connect(self.add_position)
        self.btn_update.clicked.connect(self.update_position)
        self.btn_delete.clicked.connect(self.delete_position)
        
        self.load_positions()
    
    def load_positions(self):
        """Загружает список должностей из базы данных."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Positions")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Зарплата"])
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
            self.table.setItem(i, 2, QTableWidgetItem(str(row[2])))
        connection.close()
    
    def add_position(self):
        """Добавляет новую должность."""
        dialog = AddEditPositionDialog()
        if dialog.exec_() == QDialog.Accepted:
            name, salary = dialog.get_data()
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Positions (PositionName, Salary) VALUES (%s, %s)", (name, salary))
            connection.commit()
            connection.close()
            self.load_positions()
    
    def update_position(self):
        """Обновляет выбранную должность."""
        row = self.table.currentRow()
        if row >= 0:
            position_id = self.table.item(row, 0).text()
            current_name = self.table.item(row, 1).text()
            current_salary = self.table.item(row, 2).text()
            dialog = AddEditPositionDialog(current_name, current_salary)
            if dialog.exec_() == QDialog.Accepted:
                name, salary = dialog.get_data()
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE Positions SET PositionName = %s, Salary = %s WHERE PositionID = %s", 
                               (name, salary, position_id))
                connection.commit()
                connection.close()
                self.load_positions()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите должность для изменения.")
    
    def delete_position(self):
        """Удаляет выбранную должность."""
        row = self.table.currentRow()
        if row >= 0:
            position_id = self.table.item(row, 0).text()
            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Positions WHERE PositionID = %s", (position_id,))
                connection.commit()
            except psycopg2.IntegrityError:
                QMessageBox.warning(self, "Ошибка", "Невозможно удалить должность, так как она используется.")
            finally:
                connection.close()
            self.load_positions()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите должность для удаления.")


class AddEditPositionDialog(QDialog):
    def __init__(self, name="", salary=""):
        super().__init__()
        self.setWindowTitle("Должность")
        self.layout = QVBoxLayout()
        
        self.label_name = QLabel("Название:")
        self.input_name = QLineEdit()
        self.input_name.setText(name)
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.input_name)
        
        self.label_salary = QLabel("Зарплата:")
        self.input_salary = QLineEdit()
        self.input_salary.setText(salary)
        self.layout.addWidget(self.label_salary)
        self.layout.addWidget(self.input_salary)
        
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_save)
        
        self.setLayout(self.layout)
    
    def get_data(self):
        """Возвращает данные из диалога."""
        return self.input_name.text(), float(self.input_salary.text())


class EmployeesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление сотрудниками")
        self.setGeometry(200, 200, 800, 500)
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        self.btn_add = QPushButton("Добавить")
        self.btn_update = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_update)
        self.layout.addWidget(self.btn_delete)
        
        self.setLayout(self.layout)
        
        # Соединение кнопок с функциями
        self.btn_add.clicked.connect(self.add_employee)
        self.btn_update.clicked.connect(self.update_employee)
        self.btn_delete.clicked.connect(self.delete_employee)
        
        self.load_employees()
    
    def load_employees(self):
        """Загружает список сотрудников из базы данных."""
        connection = get_connection()
        cursor = connection.cursor()
        query = """
        SELECT 
            e.EmployeeID, e.FirstName, ed.EducationName, d.DepartmentName, p.PositionName
        FROM Employees e
        JOIN Education ed ON e.EducationID = ed.EducationID
        JOIN Departments d ON e.DepartmentID = d.DepartmentID
        JOIN Positions p ON e.PositionID = p.PositionID
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Образование", "Подразделение", "Должность"])
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        connection.close()
    
    def add_employee(self):
        """Добавляет нового сотрудника и запись в таблицу History."""
        dialog = AddEditEmployeeDialog()
        if dialog.exec_() == QDialog.Accepted:
            first_name, education_id, department_id, position_id = dialog.get_data()
            connection = get_connection()
            cursor = connection.cursor()
            try:
                # Добавляем сотрудника в таблицу Employees
                cursor.execute(
                    """
                    INSERT INTO Employees (FirstName, EducationID, DepartmentID, PositionID)
                    VALUES (%s, %s, %s, %s) RETURNING EmployeeID
                    """,
                    (first_name, education_id, department_id, position_id)
                )
                # Получаем ID нового сотрудника
                new_employee_id = cursor.fetchone()[0]
    
                # Добавляем запись в таблицу History
                cursor.execute(
                    """
                    INSERT INTO History (EmployeeID, PositionID, Date)
                    VALUES (%s, %s, CURRENT_DATE)
                    """,
                    (new_employee_id, position_id)
                )
    
                # Фиксируем изменения
                connection.commit()
            except Exception as e:
                # Откат в случае ошибки
                connection.rollback()
                print(f"Ошибка при добавлении записи: {e}")
            finally:
                connection.close()
    
            # Обновляем список сотрудников
            self.load_employees()
    
    
    def update_employee(self):
        """Обновляет информацию о сотруднике."""
        row = self.table.currentRow()
        if row >= 0:
            employee_id = self.table.item(row, 0).text()
            current_name = self.table.item(row, 1).text()
            dialog = AddEditEmployeeDialog(current_name)
            if dialog.exec_() == QDialog.Accepted:
                first_name, education_id, department_id, position_id = dialog.get_data()
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    UPDATE Employees
                    SET FirstName = %s, EducationID = %s, DepartmentID = %s, PositionID = %s
                    WHERE EmployeeID = %s
                    """,
                    (first_name, education_id, department_id, position_id, employee_id)
                )
                connection.commit()
                connection.close()
                self.load_employees()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для изменения.")
    
    def delete_employee(self):
        """Удаляет выбранного сотрудника."""
        row = self.table.currentRow()
        if row >= 0:
            employee_id = self.table.item(row, 0).text()
            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Employees WHERE EmployeeID = %s", (employee_id,))
                connection.commit()
            except psycopg2.IntegrityError:
                QMessageBox.warning(self, "Ошибка", "Невозможно удалить сотрудника, так как он связан с записями в истории.")
            finally:
                connection.close()
            self.load_employees()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления.")


class AddEditEmployeeDialog(QDialog):
    def __init__(self, first_name="", education_id=None, department_id=None, position_id=None):
        super().__init__()
        self.setWindowTitle("Сотрудник")
        self.layout = QVBoxLayout()
        
        # Поле для имени
        self.label_name = QLabel("Имя:")
        self.input_name = QLineEdit()
        self.input_name.setText(first_name)
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.input_name)
        
        # Поле для образования
        self.label_education = QLabel("Образование:")
        self.combo_education = QComboBox()
        self.load_combobox_data("Education", self.combo_education, "EducationID", "EducationName")
        self.layout.addWidget(self.label_education)
        self.layout.addWidget(self.combo_education)
        
        # Поле для подразделения
        self.label_department = QLabel("Подразделение:")
        self.combo_department = QComboBox()
        self.load_combobox_data("Departments", self.combo_department, "DepartmentID", "DepartmentName")
        self.layout.addWidget(self.label_department)
        self.layout.addWidget(self.combo_department)
        
        # Поле для должности
        self.label_position = QLabel("Должность:")
        self.combo_position = QComboBox()
        self.load_combobox_data("Positions", self.combo_position, "PositionID", "PositionName")
        self.layout.addWidget(self.label_position)
        self.layout.addWidget(self.combo_position)
        
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_save)
        
        self.setLayout(self.layout)
    
    def load_combobox_data(self, table, combobox, id_column, name_column):
        """Заполняет данные в комбобоксы."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT {id_column}, {name_column} FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            combobox.addItem(row[1], row[0])
        connection.close()
    
    def get_data(self):
        """Возвращает данные из диалога."""
        first_name = self.input_name.text()
        education_id = self.combo_education.currentData()
        department_id = self.combo_department.currentData()
        position_id = self.combo_position.currentData()
        return first_name, education_id, department_id, position_id




#########################
class EducationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление образованием")
        self.setGeometry(200, 200, 600, 400)
        
        self.layout = QVBoxLayout()

        # Таблица для отображения всех записей об образовании
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        # Кнопки для добавления, изменения, удаления
        self.btn_add = QPushButton("Добавить")
        self.btn_update = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_update)
        self.layout.addWidget(self.btn_delete)
        
        # Соединяем кнопки с функциями
        self.btn_add.clicked.connect(self.add_education)
        self.btn_update.clicked.connect(self.update_education)
        self.btn_delete.clicked.connect(self.delete_education)
        
        self.setLayout(self.layout)
        
        # Загружаем данные образования
        self.load_education()
    
    def load_education(self):
        """Загружает все записи об образовании из базы данных."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT EducationID, EducationName FROM Education")
        rows = cursor.fetchall()
        
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Образование"])
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        
        connection.close()

    def add_education(self):
        """Добавляет новое образование."""
        text, ok = QInputDialog.getText(self, "Добавить образование", "Введите название образования:")
        if ok and text:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Education (EducationName) VALUES (%s)", (text,))
            connection.commit()
            connection.close()
            self.load_education()  # Обновляем таблицу

    def update_education(self):
        """Изменяет выбранное образование."""
        row = self.table.currentRow()
        if row >= 0:
            education_id = self.table.item(row, 0).text()
            current_name = self.table.item(row, 1).text()
            
            text, ok = QInputDialog.getText(self, "Изменить образование", "Новое название образования:", text=current_name)
            if ok and text:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE Education SET EducationName = %s WHERE EducationID = %s", (text, education_id))
                connection.commit()
                connection.close()
                self.load_education()  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите образование для изменения.")
    
    def delete_education(self):
        """Удаляет выбранное образование."""
        row = self.table.currentRow()
        if row >= 0:
            education_id = self.table.item(row, 0).text()
            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Education WHERE EducationID = %s", (education_id,))
                connection.commit()
            except psycopg2.IntegrityError:
                QMessageBox.warning(self, "Ошибка", "Невозможно удалить образование, так как оно используется в других записях.")
            finally:
                connection.close()
            self.load_education()  # Обновляем таблицу
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите образование для удаления.")





class AdvancedEmployeeView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расширенный просмотр сотрудников")
        self.setGeometry(200, 200, 1000, 600)
        
        self.layout = QVBoxLayout()
        
        # Поле поиска
        self.label_search = QLabel("Поиск:")
        self.input_search = QLineEdit()
        self.input_search.textChanged.connect(self.filter_employees)
        self.layout.addWidget(self.label_search)
        self.layout.addWidget(self.input_search)
        
        # Таблица сотрудников
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        self.setLayout(self.layout)
        self.load_employees()
    
    def load_employees(self):
        """Загружает полный список сотрудников."""
        connection = get_connection()
        cursor = connection.cursor()
        query = """
        SELECT 
            e.EmployeeID, e.FirstName, ed.EducationName, ed.EducationID,
            d.DepartmentName, d.DepartmentID, 
            p.PositionName, p.PositionID
        FROM Employees e
        JOIN Education ed ON e.EducationID = ed.EducationID
        JOIN Departments d ON e.DepartmentID = d.DepartmentID
        JOIN Positions p ON e.PositionID = p.PositionID
        """
        cursor.execute(query)
        self.employees = cursor.fetchall()  # Сохраняем полный список для фильтрации
        self.display_employees(self.employees)
        connection.close()
    
    def display_employees(self, employees):
        """Отображает сотрудников в таблице."""
        self.table.setRowCount(len(employees))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID сотрудника", "Имя", "Образование", "ID образования", 
            "Подразделение", "ID подразделения", 
            "Должность", "ID должности"
        ])
        for i, row in enumerate(employees):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
    
    def filter_employees(self):
        """Фильтрует сотрудников по введенному тексту."""
        search_text = self.input_search.text().lower()
        filtered = [
            emp for emp in self.employees
            if search_text in str(emp[1]).lower()  # Фильтр по имени
            or search_text in str(emp[4]).lower()  # Фильтр по подразделению
            or search_text in str(emp[6]).lower()  # Фильтр по должности
        ]
        self.display_employees(filtered)

class HistoryView(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр истории записей")
        self.setGeometry(200, 200, 800, 500)
        
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        self.setLayout(self.layout)
        self.load_history()
    
    def load_history(self):
        """Загружает историю с преобразованными данными."""
        connection = get_connection()
        cursor = connection.cursor()
        query = """
        SELECT 
            h.HistoryID, e.FirstName AS EmployeeName, 
            p.PositionName, h.Date
        FROM History h
        JOIN Employees e ON h.EmployeeID = e.EmployeeID
        JOIN Positions p ON h.PositionID = p.PositionID
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID записи", "Сотрудник", "Должность", "Дата"])
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

