Basic Instructions:
=

To run the program, run Main.py, either be clicking your IDE's run program command or by running python3 Main.py in a terminal located inside the directory Main.py is located in.

Do note that running a full experiment is extremely computationally expensive, so as a failsafe (and to help out my friend who is helping me with the data processing but has a computer that'd probably explode for a full set), you will need to specifically ask for a full set to be generated. To do this, press "f" at the first prompt, then "f" again to confirm. Additionally for ease of use, both prompts are on a 10 second timeout. If the first prompt times out, the program will generate a example set of data, and if the second one times out it will proceed with a full set.

Also be aware that running this program will always wipe all previously recorded data, including graphs, data tables, and solution conflicts. If you want to save any previous data move it out of the generated files directory.

File Directory:
=
This is the expected file directory, relative to Main.py. Make sure the python files are where they need to be to make everything work. This also shows the output directory tree that the program will create, also relative to Main.py.
```bash
.
├── data_processing_code
│   ├── DataProcessor.py
│   └── MiscDataCode.py
├── experiment_code
│   ├── ComplexityExperiment.py
│   └── versions
│       ├── MemoizedCrazy.py
│       ├── MemoizedNormal.py
│       ├── RecursiveNormal.py
│       └── TabulatedNormal.py
├── generated files
│   ├── data tables
│   │   └── table.txt
│   ├── graphs
│   │   └── graph.txt
│   └── solution conflicts
│       └── disgaree.txt
└── Main.py
```

Details on the project as a whole:
=
Originally started because I wanted to see how fast my version of a partition algorithm was, I then remembered that python seemingly has good data collection, so I decided to make a program that fully tests, records, and charts the data. However since parition algorithms have a runtime dependent on 2 (mostly) independent variables (the absolute sum of a set can be influenced by it's integer count to a degree), this project very quickly spiraled as I was now desinging how to make sets with random numbers but absolute sums within good bounds, which in the end uses a gaussian distribution random number generator, a whole load of checks and verifications, tickers to prevent infinite loops and infinite recursion, readjusting standard deviations, percentile math to find a good absolute sum target, and quite a bit more. Designing a good random set builder with the constraints was quite the challenge. I also decided I wanted to multithread this just to show off I could do it well, so there's that too. 

Details on how much work is my own:
=
Not everything in this project is completely my work. Since it varies by who I took some ideas from or got help from, by how much, and everything else, credits to each are by file. 

However, while it's not fully my work, a majority is, including the entirety of Main.py (the 2nd most important file), ComplexityExperiment.py (the most important and complex file) and MiscDataCode.py (data transfer and misc data processing), as well as how the entire system was designed to interact with each other. For example, while I recieved a good chunk of help for DataProcessor.py, and used the textbook for my algorithms course at university for help with the algorithms being tested, everything that takes a environment parameters that are to be tested, converts it into a set, inputs said set into each algorithm, obtains the raw results, minorly processes the raw data into averages, sends it through the experimenter into the orchestrator to the be processed, and then finally gets sent by the orchestrator to the data processors is all me. 

TLDR: I just needed some assistance one the edges, but all the linking and combining to make a fully functional program was me. 

Low level operations of the entire project:
=
This entire project has 4 main sections, going from top to bottom. At the very top is the orchestrator, also known as Main.py. This file is what starts the program, manages the running of the collector and the processors, manages data transfer between the collector and the processors, and everything else linking those 2 sections of the program together, and does so running both on different threads, where it divides the collectors work in a way that means it doesn't do too much work over and over, while also giving the processors chunks at a time so that the graphs can be built while data is being collected and have it not take up all my memory.

Next are the data processors, and the data collector on an equal level, so I'll start with the data processors, which is mostly DataProcessor.py with a little bit of special rare data processed by MiscDataCode.py, which also packages the data for easier use in DataProcessor.py. These take the (mostly) raw data, and coverts it into data tables, charts, graphs, statistics, and basically everything revolving around displaying the data. The only thing they don't do is that they recieve the average of 20 runs per algorithm per set of conditions. The actual raw numbers would be too much, so they are averaged right away in the collector but that is all the data not processed by the processors. 

After that is the data collector. This section collects the data from the raw algorithms at the final layer. However since the algorithms being tested also all need inputs to run on, the collector is also what creates the problem sets for each algorithm by using a bunch of math to create randomly generated sets with absolute sums near a certain benchmark using a gaussian distribution of numbers with a constantly adjusting deviation, that it also determines. Since determining the benchmarks over and over would be a waste, this part does things in integer count batches, where it will run all the tests for 1 integer count of sets, put all of that data into a neat 2D numpy array, and send it to the orchestrator, which gives it to the thread that runs the processors. To also help speed things up, this file will split into 12 independent active threads all at once, 1 for each algorithm, and then 3 to 4 for each individual test (if the basic recursive algorithm is being run, it's 3 individual tests running at once, if not, it's 4), where an individual test specifically means running the same generated set (which therefore has the same conditions) on all active algorithms (again, since the basic recursive algorithm in shut off early). 

Finally, it's the algorithms layer. This has all 4 variations of the partition algorithm that I am testing. They will all take in a set given to them, and determine if it can be partitioned into 2 equal subsets. Each variation also counts their iteration counts, to see which one is asymptotically faster in x given conditions. The 4 variations are:

Memoized Crazy, which is a recursive algorithm that records previously solved problems so it doesn't do them again, and uses some crazy math to make things go even faster.

Memoized Normal, which is like above but without the crazy math.

Tabulated Normal, which uses a bottom up tabulation approach.

Recursive Normal, which is a basic exponential time recursive algorithm. This one is hard coded to shut off after a set has more then 25 integers.