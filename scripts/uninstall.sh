#!/bin/bash
sed -i 'bash ~/Documents/.thnr/scripts/auto_updater.sh &' ~/.profile &&\
sed -i 'python ~/Documents/.thnr/main.pyw false &' ~/.profile &&\
rm -rf ~/Documents/.thnr &&\