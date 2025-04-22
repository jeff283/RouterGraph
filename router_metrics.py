import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import requests

class RouterMetrics:
    def __init__(self, base_url="http://192.168.1.1"):
        self.base_url = base_url
        self.session = requests.Session()
        # Disable SSL warning since most routers use self-signed certificates
        requests.packages.urllib3.disable_warnings()
        
        self.metrics_history = {
            'timestamp': [],
            'connection_quality': [],
            'download_speed': [],
            'upload_speed': [],
            'signal_strength': [],
            'network_type': []
        }
        
        # Initialize the plot
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        self.fig.suptitle('Router Performance Metrics', fontsize=16)
        
        # Initialize empty lines
        self.lines = {
            'quality': self.ax1.plot([], [], 'b-', label='Connection Quality')[0],
            'download': self.ax2.plot([], [], 'g-', label='Download Speed')[0],
            'upload': self.ax3.plot([], [], 'r-', label='Upload Speed')[0],
            'signal': self.ax4.plot([], [], 'purple', label='Signal Strength')[0]
        }
        
        # Set up the plots
        self.setup_plots()
        
        # Store start time for relative time plotting
        self.start_time = time.time()

    def setup_plots(self):
        """Set up the initial plot configuration."""
        # Connection Quality plot
        self.ax1.set_title('Connection Quality')
        self.ax1.set_xlabel('Time (minutes)')
        self.ax1.set_ylabel('Quality Score (%)')
        self.ax1.grid(True)
        self.ax1.set_ylim(0, 100)
        
        # Download Speed plot
        self.ax2.set_title('Download Speed')
        self.ax2.set_xlabel('Time (minutes)')
        self.ax2.set_ylabel('Speed (Mbps)')
        self.ax2.grid(True)
        
        # Upload Speed plot
        self.ax3.set_title('Upload Speed')
        self.ax3.set_xlabel('Time (minutes)')
        self.ax3.set_ylabel('Speed (Mbps)')
        self.ax3.grid(True)
        
        # Signal Strength plot
        self.ax4.set_title('Signal Strength')
        self.ax4.set_xlabel('Time (minutes)')
        self.ax4.set_ylabel('RSRP (dBm)')
        self.ax4.grid(True)
        
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
                    return data
            return None
        except requests.RequestException as e:
            print(f"Error getting network information: {e}")
            return None

    def calculate_connection_quality(self, sinr, rsrp, rsrq):
        """Calculate a user-friendly connection quality score from 0-100"""
        # Normalize SINR (typically ranges from -20 to 30)
        sinr_score = max(0, min(100, (sinr + 20) * 2))
        
        # Normalize RSRP (typically ranges from -140 to -40)
        rsrp_score = max(0, min(100, (rsrp + 140) * 1))
        
        # Normalize RSRQ (typically ranges from -20 to 0)
        rsrq_score = max(0, min(100, (rsrq + 20) * 5))
        
        # Weighted average of all three metrics
        return (sinr_score * 0.4 + rsrp_score * 0.4 + rsrq_score * 0.2)

    def get_signal_strength_category(self, rsrp):
        """Convert RSRP to a user-friendly signal strength category"""
        if rsrp >= -70:
            return "Excellent"
        elif rsrp >= -80:
            return "Good"
        elif rsrp >= -90:
            return "Fair"
        elif rsrp >= -100:
            return "Poor"
        else:
            return "Very Poor"

    def format_speed(self, speed_kbps):
        """Convert speed from kbps to a human-readable format"""
        if speed_kbps >= 1000:
            return f"{speed_kbps/1000:.1f} Mbps"
        return f"{speed_kbps:.0f} Kbps"

    def process_router_data(self, data):
        """Process raw router data into user-friendly metrics"""
        try:
            # Extract basic metrics
            sinr = float(data.get('SINR', 0))
            rsrp = float(data.get('RSRP', 0))
            rsrq = float(data.get('RSRQ', 0))
            download_speed = float(data.get('netWanRxRate', 0))
            upload_speed = float(data.get('netWanTxRate', 0))
            network_type = data.get('network_type_str', 'Unknown')

            # Calculate user-friendly metrics
            connection_quality = self.calculate_connection_quality(sinr, rsrp, rsrq)
            signal_strength = self.get_signal_strength_category(rsrp)
            
            # Store metrics with timestamp
            current_time = time.time() - self.start_time
            self.metrics_history['timestamp'].append(current_time)
            self.metrics_history['connection_quality'].append(connection_quality)
            self.metrics_history['download_speed'].append(download_speed)
            self.metrics_history['upload_speed'].append(upload_speed)
            self.metrics_history['signal_strength'].append(rsrp)
            self.metrics_history['network_type'].append(network_type)

            # Create user-friendly report
            report = {
                "Connection Status": {
                    "Overall Quality": f"{connection_quality:.1f}%",
                    "Signal Strength": signal_strength,
                    "Network Type": network_type
                },
                "Speed": {
                    "Download": self.format_speed(download_speed),
                    "Upload": self.format_speed(upload_speed)
                },
                "Technical Details": {
                    "IP Address": data.get('wan_ip', 'Unknown'),
                    "DNS Servers": f"{data.get('wan_dns', 'Unknown')}, {data.get('wan_dns2', 'Unknown')}",
                    "Gateway": data.get('wan_gateway', 'Unknown')
                }
            }

            return report

        except Exception as e:
            return {"error": f"Error processing router data: {str(e)}"}

    def update_plot(self, frame):
        """Update the plot with new data"""
        # Get new data from router
        network_info = self.get_network_info()
        if network_info:
            # Process the new data
            self.process_router_data(network_info)
        
        if not self.metrics_history['timestamp']:
            return list(self.lines.values())

        # Convert timestamps to minutes
        times = [t/60 for t in self.metrics_history['timestamp']]
        
        # Update each line
        self.lines['quality'].set_data(times, self.metrics_history['connection_quality'])
        self.lines['download'].set_data(times, [s/1000 for s in self.metrics_history['download_speed']])
        self.lines['upload'].set_data(times, [s/1000 for s in self.metrics_history['upload_speed']])
        self.lines['signal'].set_data(times, self.metrics_history['signal_strength'])
        
        # Adjust axis limits
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.relim()
            ax.autoscale_view()
        
        # Keep only last 30 points for better visualization
        if len(self.metrics_history['timestamp']) > 30:
            for key in self.metrics_history:
                self.metrics_history[key] = self.metrics_history[key][-30:]
        
        return list(self.lines.values())

def main():
    # Initialize the metrics class
    metrics = RouterMetrics()
    print("Starting network monitoring... Press Ctrl+C to stop.")
    
    # Create animation with explicit save_count to avoid warning
    ani = FuncAnimation(metrics.fig, metrics.update_plot, 
                       interval=1000,  # Update every second
                       blit=True,
                       save_count=100)
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main() 