Basic Instructions:
===================

To run the program use python3 on Main.py. There are also optional command line arguments shown below. The current set of dependencies is 'numpy', 'pandas', 'matplotlib', 'python-docx' and 'xlsxwriter'. ```pip install numpy pandas matplotlib python-docx xlsxwriter``` will install them all. Additionally, if you are running the C version of the algorithms your device will need gcc installed and the permissions to use it as the program will compile the C code with gcc (if the compiled versions do not exist in the files) when started.

options: \
  -h, --help     show this help message and exit \
  -r, --reduced  run a significantly reduced testing suite of just Old and New Memoized Crazy being run, on my machine doing this takes the runtime from about 24 hours to about 15 minutes \
  -e, --example  generate some random example data, used to test the data processor therefore it does not run the python or C implementations of the algorithms \
  -p, --python   run the original python implementations of the algorithm versions instead of the C versions (NOT IMPLEMENTED YET, PYTHON VERSIONS WILL ALWAYS RUN) \
  -c, --compile  compile the C versions at startup without checking if they already exist (NOT IMPLEMENTED YET, NOTHING TO COMPILE)

Also be aware that running this program will always wipe all previously recorded data, including graphs, data tables, and solution conflicts. If you want to save any previous data move it out of the generated files directory.

For a saved version of the generated data, as well as other documents relating to stress testing with worse case scenarios check out my misc files repository for this project found [here.](https://github.com/bananathrowingmachine/FastPartitionExperimentDocs)

File Directory:
===============

This is the expected file directory, relative to Main.py. Make sure the python files are where they need to be to make everything work. This also shows the output directory tree that the program will create, also relative to Main.py.

```bash
├── data_processing_code
│   ├── DisagreeProcessor.py
│   ├── MainDataProcessor.py
│   └── MiscDataCode.py
├── experiment_code
│   ├── ComplexityExperiment.py
│   └── versions
│       ├── MemoizedNormal.py
│       ├── OldMemoizedCrazy.py
│       ├── NewMemoizedCrazy.py
│       ├── RecursiveNormal.py
│       ├── TabulatedCrazy.py
│       └── TabulatedNormal.py
├── generated_files
│   ├── data_tables
│   ├── graphs
│   └── solution_conflicts
└── Main.py
```

Details on the project as a whole:
==================================

Originally started because I wanted to see how fast my version of a partition algorithm was, I then remembered that python seemingly has good data collection, so I decided to make a program that fully tests, records, and charts the data. However since parition algorithms have a runtime dependent on 2 (mostly) independent variables (the absolute sum of a set can be influenced by it's integer count to a degree), this project very quickly spiraled as I was now desinging how to make sets with random numbers but absolute sums within good bounds, which in the end uses a gaussian distribution random number generator, a whole load of checks and verifications, tickers to prevent infinite loops and infinite recursion, readjusting standard deviations, percentile math to find a good absolute sum target, and quite a bit more. Designing a good random set builder with the constraints was quite the challenge. I also decided I wanted to multithread this just to show off I could do it well, so there's that too.

Details on how much work is my own:
===================================

Not everything in this project is completely my work. Since it varies by who I took some ideas from or got help from, by how much, and everything else, credits to each are by file.

However, while it's not fully my work, a majority is, including the entirety of Main.py (the 2nd most important file), ComplexityExperiment.py (the most important and complex file) and MiscDataCode.py (data transfer and misc data processing), as well as how the entire system was designed to interact with each other. For example, while I recieved a good chunk of help for DataProcessor.py, and used the textbook for my algorithms course at university for help with the algorithms being tested, everything that takes a environment parameters that are to be tested, converts it into a set, inputs said set into each algorithm, obtains the raw results, minorly processes the raw data into averages, sends it through the experimenter into the orchestrator to the be processed, and then finally gets sent by the orchestrator to the data processors is all me.

TLDR: I just needed some assistance one the edges, but all the linking and combining to make a fully functional program was me.

Low level operations of the entire project:
===========================================

This entire project has 4 main sections, going from top to bottom. At the very top is the orchestrator, also known as Main.py. This file is what starts the program, manages the running of the collector and the processors, manages data transfer between the collector and the processors, and everything else linking those 2 sections of the program together, and does so running both on different threads, where it divides the collectors work in a way that means it doesn't do too much work over and over, while also giving the processors chunks at a time so that the graphs can be built while data is being collected and have it not take up all my memory.

Next are the data processors, and the data collector on an equal level, so I'll start with the data processors, which is mostly DataProcessor.py with a little bit of special rare data processed by MiscDataCode.py, which also packages the data for easier use in DataProcessor.py. These take the (mostly) raw data, and coverts it into data tables, charts, graphs, statistics, and basically everything revolving around displaying the data. The only thing they don't do is that they recieve the average of 50 runs per algorithm per set of conditions. The actual raw numbers would be too much, so they are averaged right away in the collector but that is all the data not processed by the processors.

After that is the data collector. This section collects the data from the raw algorithms at the final layer. However since the algorithms being tested also all need inputs to run on, the collector is also what creates the problem sets for each algorithm by using a bunch of math to create randomly generated sets with absolute sums near a certain benchmark using a gaussian distribution of numbers with a constantly adjusting deviation, that it also determines. Since determining the benchmarks over and over would be a waste, this part does things in integer count batches, where it will run all the tests for 1 integer count of sets, put all of that data into a neat 2D numpy array, and send it to the orchestrator, which gives it to the thread that runs the processors. To also help speed things up, this file will split into 12-15 independent active threads all at once, 1 for each algorithm, and then 3 for each individual test, where an individual test specifically means running the same generated set (which therefore has the same conditions) on all active algorithms.

Finally, it's the algorithms layer. This has all 6 variations of the partition algorithm that I am testing. They will all take in a set given to them, and determine if it can be partitioned into 2 equal subsets. Each variation also counts their iteration counts, to see which one is asymptotically faster in x given conditions. The 6 variations are:

Memoized Normal, which is a recursive algorithm that records previously solved problems so it doesn't solve them again.

Old Memoized Crazy, which is Memoized Normal with the abs-value trick added on top to include extremely aggressive pruning.

New Memoized Crazy, which is an experimental version of Memoized Crazy to try and make it even faster.

Tabulated Normal, which uses a bottom up iterative tabulation approach.

Tabulated Crazy, which is Tabulated Normal with the same hueristics as Memoized Crazy.

Recursive Normal, which is a basic exponential time recursive algorithm. This one is hard coded to shut off after a set has more then 25 integers to save time.
