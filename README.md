# CG4002-External-Comms

This is the external communications script for NUS Computer Engineering Capstone project module CG4002 taken in AY24/25 Semester 1 for Group B13.

## How to use

1) Open three separate terminals.
2) Connect to SoC VPN via forticlient if not connected to SoC WiFi in NUS.
3) On terminal 1, cd to file path of eval server and run python3 WebSocketServer.py. Then, open index.html in eval_Server folder and log in. Host: 127.0.0.1, Password: [16 character AES key set by your group]
4) On terminal 2, run `ssh -R 8888:127.0.0.1:[port no. shown in index.html] xilinx@makerslab-fpga-37.d2.comp.nus.edu.sg` to setup reverse ssh tunneling. (Change to appropriate Ultra 96 address for your group)
5) On terminal 3, run `ssh xilinx@makerslab-fpga-37.d2.comp.nus.edu.sg` and cd into /DO_NOT_DELETE/CG4002-External_Comms and activate the python virtual environment using the command `source /etc/profile.d/pynq_venv.sh`
5) If running 1-player or 2-player test with evaluation server, run `sudo -E python3 main.py`
6) If running free play, run `sudo -E python3 free_play_main.py`
7) Upon successful connection, evaluation server should show "successfully connected" we can turn on the hardware and wait for TCP connection from internal communications side.
