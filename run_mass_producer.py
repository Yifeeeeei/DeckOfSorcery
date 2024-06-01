from config import *

from mass_producer_xlsx import *

if __name__ == "__main__":
    mass_producer_xlsx = MassProducerXlsx("mass_producer_params_xlsx.json")
    mass_producer_xlsx.produce()
