# RouterGraph

[![Airtel 5G Router Monitoring](https://img.shields.io/badge/Airtel-5G%20Router%20Monitoring-blue)](https://github.com/jeff283/RouterGraph)
[![Python Tool](https://img.shields.io/badge/Python-Network%20Monitoring-green)](https://github.com/jeff283/RouterGraph)
[![Network Metrics](https://img.shields.io/badge/Network-Metrics%20Visualization-orange)](https://github.com/jeff283/RouterGraph)

A Python-based tool for monitoring and visualizing Airtel 5G router network performance metrics in real-time.

**Author:** [chaud](https://github.com/jeff283) - *Network monitoring enthusiast and developer*

**[Visit My GitHub Profile](https://github.com/jeff283) for more useful tools and projects**

## Overview

RouterGraph connects to a router's API (default: http://192.168.1.1) and collects key network performance metrics, including:
- Signal strength (RSRP)
- Signal quality (RSRQ)
- Signal-to-Noise Ratio (SINR)
- Download speeds
- Upload speeds

The collected data is displayed in real-time graphical charts, providing an intuitive way to monitor your network performance over time.

## Compatibility

This tool is specifically designed to work with the Airtel 5G Router and has been tested to be fully compatible with its API structure and data format.

## Features

- **Real-time Monitoring**: Continuously updates network metrics every second
- **Visual Data Representation**: Four-panel visualization showing different network metrics
- **Connection Quality Analysis**: Calculates and displays an overall connection quality score
- **Signal Strength Categorization**: Converts technical RSRP values to user-friendly categories
- **Speed Formatting**: Displays network speeds in appropriate units (Kbps or Mbps)
- **Historical Data**: Maintains recent history of network performance

## Requirements

```
requests
matplotlib
numpy
pandas
beautifulsoup4
lxml
```

## Installation

1. Clone this repository or download the files
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

The project includes two main modules:

### 1. Basic Router Information (router_info.py)

Provides basic network status information and visualization:

```
python router_info.py
```

### 2. Advanced Router Metrics (router_metrics.py)

Offers more detailed metrics and analysis of your router's performance:

```
python router_metrics.py
```

## Configuration

By default, the application connects to a router at `http://192.168.1.1`. If your router has a different IP address, you can specify it when running the scripts:

```python
# In your code
router = RouterAPI(base_url="http://your.router.ip")
# or
metrics = RouterMetrics(base_url="http://your.router.ip")
```

## Project Structure

- `router_info.py` - Basic router monitoring with visualization
- `router_metrics.py` - Advanced router metrics with detailed analysis
- `requirements.txt` - Python package dependencies

## Notes

- This application is designed for routers with a compatible API endpoint at `/cgi-bin/http.cgi`
- SSL warnings are disabled as most routers use self-signed certificates
- The application uses Matplotlib with TkAgg backend for interactive plotting

## Keywords

- Airtel 5G Router Monitoring
- Network Performance Visualization
- RSRP RSRQ SINR Monitoring
- Python Network Tools
- Router API Integration
- Real-time Network Metrics
- Signal Strength Visualization
- Bandwidth Monitoring Tool
- 5G Router Performance Analysis
- Network Quality Dashboard

## Citation

If you use this tool in your work or research, please cite:

```
@software{chaud_routergraph_2025,
  author = {chaud},
  title = {RouterGraph: Real-time Airtel 5G Router Monitoring Tool},
  year = {2025},
  url = {https://github.com/jeff283/RouterGraph}
}
```

## License

This project is open source and available under the MIT License.

## Last Updated

April 23, 2025

---
*RouterGraph is developed and maintained by [chaud](https://github.com/jeff283). For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/jeff283/RouterGraph).*