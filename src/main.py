from PyQt5.QtWidgets import QApplication
import data_processing as dp
import visualization as vz
from gui import PopulationGrowthApp

if __name__ == "__main__":
    app = QApplication([])  # Create the PyQt application
    window = PopulationGrowthApp(dp, vz)  # Pass data_processor and visualizer
    window.show()  # Show the main window
    app.exec_()  # Start the PyQt event loop
