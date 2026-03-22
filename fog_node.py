import json
from datetime import datetime
from decision_module import TrafficController

class SmartIntersectionFogNode:
    def __init__(self, node_id, location):
        self.node_id = node_id
        self.location = location
        self.controller = TrafficController()
        self.log_file = "fog_sync_log.json"

    def process_traffic(self, density_score):
        # 1. Get decision from logic module
        action = self.controller.get_action(density_score)
        
        # 2. Create the data packet (for Cloud/History)
        packet = {
            "timestamp": datetime.now().isoformat(),
            "node_id": self.node_id,
            "congestion_index": density_score,
            "decision": action,
            "status": "OPTIMAL"
        }

        # 3. Local Logging (Simulating Fog Storage)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(packet) + "\n")
            
        return action

# Example Test
if __name__ == "__main__":
    node = SmartIntersectionFogNode("FOG_01", "Main_Junction")
    print(f"Decision for 85% traffic: {node.process_traffic(85)}")