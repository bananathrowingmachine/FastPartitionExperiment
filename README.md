Basic Instructions:
=

To run the program, run Main.py, either be clicking your IDE's run program command or by running python3 Main.py in a terminal located inside the directory Main.py is located in.

Do note that running a full experiment is extremely computationally expensive, so as a failsafe (and to help out my friend who is helping me with the data processing but has a computer that'd probably explode for a full set), you will need to specifically ask for a full set to be generated. To do this, press "f" at the first prompt, then "f" again to confirm. Additionally for ease of use, both prompts are on a 10 second timeout. If the first prompt times out, the program will generate a example set of data, and if the second one times out it will proceed with a full set.

Also be aware that running this program will always wipe all previously recorded data, including graphs, data tables, and solution conflicts. If you want to save any previous data move it out of the generated files directory.

File Directory:
=
This program has a specific file directory that should be accounted for. Relative to where Main.py is located, there should DataProcessor.py, and /experiment_code. In /experiment_code there should be ComplexityExperiment.py and /versions. In /versions there should be 4 named algorithm files. The full path relative from Main.py to a algorithm file is /experiment_code/versions/"algorithm name".py. Additionally the program will create sub directories relative to it for all generated data. Relative to Main.py they will be /generated files/data tables, /generated files/graphs, /generated files/solution conflicts and /generated files/solution conflicts. When run, the program will automatically delete these directories if they exist and recreate them.

More In Depth Explanation:
=
todo