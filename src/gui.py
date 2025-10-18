from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QSlider, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt
import visualization as vz


class PopulationDialog(QDialog):
    def __init__(self, country, year, population, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Population Details")

        layout = QVBoxLayout()

        country_label = QLabel(f"<b>Country:</b> {country}")
        year_label = QLabel(f"<b>Year:</b> {year}")
        population_label = QLabel(f"<b>Population:</b> {int(population):,}")

        layout.addWidget(country_label)
        layout.addWidget(year_label)
        layout.addWidget(population_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)


class PopulationGrowthApp(QMainWindow):
    def __init__(self, data_processor, visualizer):
        super().__init__()
        self.data_processor = data_processor
        self.visualizer = visualizer
        self.data = None

        self.setWindowTitle("Population Growth Visualizer")
        self.setGeometry(100, 100, 600, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.heading_label = QLabel("POPULATION GROWTH VISUALIZER")
        self.heading_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #4b0082;")
        self.layout.addWidget(self.heading_label)

        self.country_label = QLabel("Select Country:")
        self.country_label.setStyleSheet("font-size: 12pt; color: #4b0082;")
        self.layout.addWidget(self.country_label)
        self.country_dropdown = QComboBox()
        self.country_dropdown.setStyleSheet(
            "font-size: 12pt; color: white; background-color: #4b0082; border-radius: 5px; padding: 5px;"
        )
        self.layout.addWidget(self.country_dropdown)

        self.year_label = QLabel("Select Year:")
        self.year_label.setStyleSheet("font-size: 12pt; color: #4b0082;")
        self.layout.addWidget(self.year_label)
        self.year_dropdown = QComboBox()
        self.year_dropdown.setStyleSheet(
            "font-size: 12pt; color: white; background-color: #4b0082; border-radius: 5px; padding: 5px;"
        )
        self.layout.addWidget(self.year_dropdown)

        # Start Year Slider
        self.start_year_label = QLabel("Start Year:")
        self.start_year_label.setStyleSheet("font-size: 12pt; color: #4b0082;")
        self.layout.addWidget(self.start_year_label)
        self.start_year_slider = QSlider(Qt.Horizontal)
        self.start_year_slider.setStyleSheet(
            "QSlider::groove:horizontal { background: #ddd; height: 6px; }"
            "QSlider::handle:horizontal { background: #4b0082; width: 12px; border-radius: 6px; }"
        )
        self.start_year_slider.valueChanged.connect(self.update_start_year_label)
        self.layout.addWidget(self.start_year_slider)
        self.start_year_display = QLabel("2000")
        self.start_year_display.setStyleSheet("font-size: 12pt; color: #4b0082;")
        self.layout.addWidget(self.start_year_display)

        # End Year Slider
        self.end_year_label = QLabel("End Year:")
        self.end_year_label.setStyleSheet("font-size: 12pt; color: #4b0082;")
        self.layout.addWidget(self.end_year_label)
        self.end_year_slider = QSlider(Qt.Horizontal)
        self.end_year_slider.setStyleSheet(
            "QSlider::groove:horizontal { background: #ddd; height: 6px; }"
            "QSlider::handle:horizontal { background: #4b0082; width: 12px; border-radius: 6px; }"
        )
        self.end_year_slider.valueChanged.connect(self.update_end_year_label)
        self.layout.addWidget(self.end_year_slider)
        self.end_year_display = QLabel("2023")
        self.end_year_display.setStyleSheet("font-size: 12pt; color: #4b0082;")
        self.layout.addWidget(self.end_year_display)

        self.check_population_button = QPushButton("Check Population")
        self.check_population_button.setStyleSheet("background-color: #4b0082; color: white; font-weight: bold;")
        self.check_population_button.clicked.connect(self.check_population)
        self.layout.addWidget(self.check_population_button)

        self.generate_chart_button = QPushButton("Generate Chart")
        self.generate_chart_button.setStyleSheet("background-color: #4b0082; color: white; font-weight: bold;")
        self.generate_chart_button.clicked.connect(self.generate_charts)
        self.layout.addWidget(self.generate_chart_button)

        self.output_label = QLabel("")
        self.layout.addWidget(self.output_label)

        self.load_data_backend()

    def load_data_backend(self):
        self.data = self.data_processor.load_data()
        if self.data is not None:
            countries = self.data['country'].unique()
            self.country_dropdown.addItems(countries)

            year_columns = [col for col in self.data.columns if "population" in col]
            years = sorted([int(col.split()[0]) for col in year_columns])

            self.year_dropdown.addItems(map(str, years))
            self.start_year_slider.setMinimum(min(years))
            self.start_year_slider.setMaximum(max(years))
            self.start_year_slider.setValue(min(years))
            self.end_year_slider.setMinimum(min(years))
            self.end_year_slider.setMaximum(max(years))
            self.end_year_slider.setValue(max(years))
        else:
            self.output_label.setText("Failed to load data. Please check the backend.")

    def update_start_year_label(self):
        self.start_year_display.setText(str(self.start_year_slider.value()))

    def update_end_year_label(self):
        self.end_year_display.setText(str(self.end_year_slider.value()))

    def check_population(self):
        country = self.country_dropdown.currentText()
        year = self.year_dropdown.currentText()
        column_name = f"{year} population"

        if self.data is not None and column_name in self.data.columns:
            population = self.data.loc[self.data['country'] == country, column_name].values
            if len(population) > 0:
                dialog = PopulationDialog(country, year, population[0], self)
                dialog.exec_()
            else:
                self.output_label.setText(f"No data available for {country} in {year}.")
        else:
            self.output_label.setText("No data available. Please check the backend.")

    def generate_charts(self):
        country = self.country_dropdown.currentText()
        start_year = self.start_year_slider.value()
        end_year = self.end_year_slider.value()

        if start_year > end_year:
            self.output_label.setText("Error: Start year must be less than or equal to end year.")
            return

        filtered_data = self.data_processor.filter_data(self.data, country, start_year, end_year)

        if filtered_data is not None and not filtered_data.empty:
            filtered_data = self.data_processor.calculate_growth_rate(filtered_data)
            vz.Visualizer.plot_population_trend(filtered_data, country)
            vz.Visualizer.plot_growth_rate(filtered_data, country)
        else:
            self.output_label.setText(f"Error: No data for {country} in the selected year range.")
