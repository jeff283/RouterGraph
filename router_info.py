import requests
import json
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from datetime import datetime
import pandas as pd
import os

class RouterAPI:
    def __init__(self, base_url="http://192.168.1.1"):
        self.base_url = base_url
        self.session = requests.Session()
        # Disable SSL warning since most routers use self-signed certificates
        requests.packages.urllib3.disable_warnings()
        self.history = {
            'timestamp': [],
            'RSRP': [],
            'RSRQ': [],
            'SINR': [],
            'netWanRxRate': [],
            'netWanTxRate': []
        }
        
        # Initialize the plot
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        self.fig.suptitle('Network Metrics Live Monitor', fontsize=16)
        
        # Initialize empty lines
        self.lines = {
            'RSRP': self.ax1.plot([], [], 'b-', label='RSRP')[0],
            'RSRQ': self.ax2.plot([], [], 'r-', label='RSRQ')[0],
            'SINR': self.ax3.plot([], [], 'g-', label='SINR')[0],
            'Download': self.ax4.plot([], [], 'b-', label='Download Rate')[0],
            'Upload': self.ax4.plot([], [], 'r-', label='Upload Rate')[0]
        }
        
        # Set up the plots
        self.setup_plots()
        
        # Store start time for relative time plotting
        self.start_time = time.time()

    def setup_plots(self):
        """Set up the initial plot configuration."""
        # RSRP plot
        self.ax1.set_title('RSRP over Time')
        self.ax1.set_xlabel('Time (seconds)')
        self.ax1.set_ylabel('RSRP (dBm)')
        self.ax1.grid(True)
        
        # RSRQ plot
        self.ax2.set_title('RSRQ over Time')
        self.ax2.set_xlabel('Time (seconds)')
        self.ax2.set_ylabel('RSRQ (dB)')
        self.ax2.grid(True)
        
        # SINR plot
        self.ax3.set_title('SINR over Time')
        self.ax3.set_xlabel('Time (seconds)')
        self.ax3.set_ylabel('SINR (dB)')
        self.ax3.grid(True)
        
        # Network Rates plot
        self.ax4.set_title('Network Rates over Time')
        self.ax4.set_xlabel('Time (seconds)')
        self.ax4.set_ylabel('Rate (kbps)')
        self.ax4.grid(True)
        self.ax4.legend()
        
        plt.tight_layout()

    def get_network_info(self):
        """Get network information using API call."""
        try:
            url = f"{self.base_url}/cgi-bin/http.cgi"
            payload = {
                "cmd": 133,
                "method": "GET",
                "language": "en",
                "sessionId": ""
            }
            
            response = self.session.post(url, json=payload, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # Store historical data with relative time
                    current_time = time.time() - self.start_time
                    self.history['timestamp'].append(current_time)
                    self.history['RSRP'].append(float(data.get('RSRP', 0)))
                    self.history['RSRQ'].append(float(data.get('RSRQ', 0)))
                    self.history['SINR'].append(float(data.get('SINR', 0)))
                    self.history['netWanRxRate'].append(float(data.get('netWanRxRate', 0)))
                    self.history['netWanTxRate'].append(float(data.get('netWanTxRate', 0)))
                    return data
            return None
        except requests.RequestException as e:
            print(f"Error getting network information: {e}")
            return None

    def update_plot(self, frame):
        """Update the plot with new data."""
        # Get new data
        network_info = self.get_network_info()
        
        if network_info:
            # Print current values
            print("\nCurrent Network Information:")
            print("-" * 40)
            print(f"Network Type: {network_info.get('network_type_str', 'N/A')}")
            print(f"Signal Strength (RSRP): {network_info.get('RSRP', 'N/A')} dBm")
            print(f"Signal Quality (RSRQ): {network_info.get('RSRQ', 'N/A')} dB")
            print(f"Signal to Noise Ratio (SINR): {network_info.get('SINR', 'N/A')} dB")
            print(f"Download Rate: {network_info.get('netWanRxRate', 'N/A')} kbps")
            print(f"Upload Rate: {network_info.get('netWanTxRate', 'N/A')} kbps")
            print(f"WAN IP: {network_info.get('wan_ip', 'N/A')}")
            print(f"WAN Gateway: {network_info.get('wan_gateway', 'N/A')}")
            
            # Update each line with numeric timestamps
            self.lines['RSRP'].set_data(self.history['timestamp'], self.history['RSRP'])
            self.lines['RSRQ'].set_data(self.history['timestamp'], self.history['RSRQ'])
            self.lines['SINR'].set_data(self.history['timestamp'], self.history['SINR'])
            self.lines['Download'].set_data(self.history['timestamp'], self.history['netWanRxRate'])
            self.lines['Upload'].set_data(self.history['timestamp'], self.history['netWanTxRate'])
            
            # Adjust axis limits
            for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
                ax.relim()
                ax.autoscale_view()
            
            # Keep only last 30 points for better visualization
            if len(self.history['timestamp']) > 30:
                for key in self.history:
                    self.history[key] = self.history[key][-30:]
        
        return list(self.lines.values())

def main():
    router = RouterAPI()
    print("Starting network monitoring...")
    
    # Create animation with explicit save_count to avoid warning
    ani = FuncAnimation(router.fig, router.update_plot, 
                       interval=1000,  # Update every 10 seconds
                       blit=True,
                       save_count=100)  # Limit the number of frames to cache
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main() 