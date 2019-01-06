# BATTERY STATUS DISPLAY

Returns laptop battery status in graphical icon, for Windows Subsystem for Linux. 

## Example
```
79% [xx ]•
```

## Getting Started
The following examples will show you how to install and setup the battery_status script to easily use it from the commandline.

### Prerequisites
Make sure you have Python (version 2.7) installed.


### Installation
To install the script, follow the steps listed below:  

1.  Clone this repository into your preferred directory.  
    ```
    git clone https://github.com/jaspreetpanesar/battery_status.git
    ```

2.  Create an entry in your .bashrc with an alias pointing to the battery_status.py scipt.  
    ```
    alias battery='python /path/to/battery_status/battery_status.py'
    ```

3.  Reload bashrc file.
    ```
    source ~/.bashrc
    ```

### How to Use
1.  To see battery capacity and small icon:
    ```
    battery -m
    ```
2.  To show battery_status help:
    ```
    battery -h
    ```
3.  To see all battery information:
    ```
    battery -d
    ```
4.  To see values in colour, add -c option. Example:
    ```
    battery -dc
    ```

## Author
Jaspreet Panesar 

## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
