# Makefile for the partition algorithm and it's test suite
# Made by bananathrowingmachine
# [date]

GOOGLETEST = /home/user/vscode/GOOGLETEST

fastPartitionTests: testingSuite.o vertex.o fastPartition.o dpTable.o
	g++ -Wall -o fastPartitionTests -L$(GOOGLETEST)/lib testingSuite.o vertex.o fastPartition.o dpTable.o -lgtest -lgtest_main

testingSuite.o: testingSuite.cpp
	g++ -Wall -c -I$(GOOGLETEST)/googletest/include -L$(GOOGLETEST)/lib testingSuite.cpp -lgtest -lgtest_main

vertex.o: vertex.cpp vertex.h
	g++ -Wall -c -I./headers ./source/vertex.cpp 

fastPartition.o: fastPartition.cpp fastPartition.h
	g++ -Wall -c -I./headers ./source/fastPartition.cpp 

dpTable.o: dpTable.cpp dpTable.h
	g++ -Wall -c -I./headers ./source/dpTable.cpp 

test: fastPartitionTests
	./fastPartitionTests

clean:
	rm -f fastPartitionTests *.o
