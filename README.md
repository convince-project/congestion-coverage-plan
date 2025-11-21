installing the library

```
# Install dependencies
apt-get update && apt-get install -y \
python3 \
python3-pip \
python3-venv \
git 

# install the devices messages 
cd ~
git clone https://github.com/morpheus1820/occupancy_static_devices
cd occupancy_static_devices/static_devices_msgs
colcon build
source install/setup.bash
cd ~;
# clone the repo
git clone --branch fix/UC3 https://github.com/convince-project/congestion-coverage-plan.git;

# install it
cd  congestion-coverage-plan;

python3 -m venv create venv-congestion-coverage-plan;
source ./venv-congestion-coverage-plan/bin/activate;
touch ./venv-congestion-coverage-plan/COLCON_IGNORE;
python3 -m pip install --upgrade pip;
python3 -m pip install -e .;
export PYTHONPATH=$PYTHONPATH:`pwd`/venv-congestion-coverage-plan/lib/python3.12/site-packages;
```