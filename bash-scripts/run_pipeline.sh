#!usr/bin/bash

# -------------------- Source the virtual environment --------------------
cd ..
cd ..
source bemo/bin/activate
#TODO: make it automatically connect to ds4
cd koubeisically/scripts
chmod 777 bluetooth.sh web.sh

# -------------------- Run the pipeline --------------------
echo "Running the pipeline..."
cd koubeisically

python3 -m src.main

echo "Press Enter to stop the pipeline..."
read -r
echo "Script ending."