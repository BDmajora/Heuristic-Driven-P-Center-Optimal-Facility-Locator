from src.network_manager import NetworkManager
from src.model_logic import PCenterSolver
from src.visualizer import MapVisualizer

def main():
    # Initialize network manager and load map data

    PROVINCE_CSV = {
    "Alberta":                  "data/census/98-401-X2021006_English_CSV_data_Prairies.csv",
    "British Columbia":         "data/census/98-401-X2021006_English_CSV_data_BritishColumbia.csv",
    "Manitoba":                 "data/census/98-401-X2021006_English_CSV_data_Prairies.csv",
    "New Brunswick":            "data/census/98-401-X2021006_English_CSV_data_Atlantic.csv",
    "Newfoundland and Labrador":"data/census/98-401-X2021006_English_CSV_data_Atlantic.csv",
    "Northwest Territories":    "data/census/98-401-X2021006_English_CSV_data_Territories.csv",
    "Nova Scotia":              "data/census/98-401-X2021006_English_CSV_data_Atlantic.csv",
    "Nunavut":                  "data/census/98-401-X2021006_English_CSV_data_Territories.csv",
    "Ontario":                  "data/census/98-401-X2021006_English_CSV_data_Ontario.csv",
    "Prince Edward Island":     "data/census/98-401-X2021006_English_CSV_data_Atlantic.csv",
    "Quebec":                   "data/census/98-401-X2021006_English_CSV_data_Quebec.csv",
    "Saskatchewan":             "data/census/98-401-X2021006_English_CSV_data_Prairies.csv",
    "Yukon":                    "data/census/98-401-X2021006_English_CSV_data_Territories.csv",
    }
    
    place = input("Please enter a Canadian city (e.g. Coaldale, Alberta): ") + ", Canada"
    province = place.split(",")[1].strip().replace(", Canada", "")

    pop_path = PROVINCE_CSV.get(province)
    if pop_path is None:
        raise ValueError(f"Unrecognized province: '{province}'. Check spelling.")
    p_count= int(input("How many Hospitals? "))

    manager = NetworkManager(place)
    graph = manager.load_graph()
    
    # Select random sample points and calculate distance matrix
    demand_weights = manager.load_demand_from_shapefile("data/DAdata/lda_000b21a_e.shp", "data/PopulationData/98-401-X2021006_English_CSV_data_Prairies.csv")
    demand_nodes = list(demand_weights.keys())
    distances = manager.compute_distances(demand_nodes)
    print(f"done with distance")
    # Solve p-center problem to locate facilities
    # p_count = # of Hospitals
    solver = PCenterSolver(demand_nodes, distances, p_count=p_count, weights=demand_weights)
    hospitals, max_dist = solver.solve()


    # Print optimization status and facility locations
    print(f"\nStatus: Optimal")
    print(f"Maximized Equity Distance: {max_dist:.3f} meters")
    for i, h in enumerate(hospitals, 1):
        print(f"Hospital {i} Location (Node ID): {h}")

    # Generate and save spatial visualization
    viz = MapVisualizer(graph)
    viz.save_map(hospitals, filename=f"images/{place}_p={p_count}.png")

if __name__ == "__main__":
    main()