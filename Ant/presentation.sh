#! /bin/bash
clear
figlet "Complexity of Langton's Ant 2002"
#xdg-open Others/Article/2002-Gajardo-ComplexityOfLangtonAnts.pdf&
#xdg-open Others/ColorCodeBig.png&
python LangtonsAnt.py -i Tests/BigDemo.png -s 50
python LangtonsAnt.py -i Tests/LangtonsAnt.png -s 7
python LangtonsAnt.py -i Tests/LangtonsAntRandom.png -s 7
python LangtonsAnt.py -i Tests/LangtonsAnts.png -s 7
python LangtonsAnt.py -i Tests/Highway.png
python LangtonsAnt.py -i Tests/Paths.png
python LangtonsAnt.py -i Tests/Junctions.png
python LangtonsAnt.py -i Tests/Yes.png
python LangtonsAnt.py -i Tests/NOT+HighWay.png
python LangtonsAnt.py -i Tests/AND+HighWay.png
python LangtonsAnt.py -i Tests/Duplicate.png
python LangtonsAnt.py -i Tests/Cross.png
python LangtonsAnt.py -i "Tests/AND+HighWay Reversed.png"
figlet "Thank You!"
