## AI Assignment 01 - Kids in the Yard

**1. Which tool(s) did you use?** 
- I used DeepSeek.

**2. If you used an LLM, what was your prompt to the LLM?**
- I need to build a Python program that generates a family tree simulation that has 3 classes using an OO python implementation, following a PEP8 style guideline. The classes should be called 
            
            Person - holds a first and last name, the year they were born, the year they pass, their spouse, and their children if they have any.

            PersonFactory - reads data from the provided csv files, and hold functions to choose the needed information from the Person class and creates the Person object. 

            FamilyTree - the driver class that generates the tree and prints the menu and it's options

- The code should have the following requirements:
            
            Start with two people born in 1950
            Generate descendants until 2120 or no more children can be generated
            Each person needs these attributes: [list from Table 1]
            Data is provided in CSV files: [list files]
            User interface should allow: [list query options]

<br>

**3. What differences are there between your implementation and the LLM?**
- Generation Algorithm Approach: The LLM implemented the assignment using a depth-first recursive while I used a BFS list where I pop the parents and generate their children iteratively. 
- File Reading: I used pandas for file operations while it used Python's built-in csv module
- Spouse Generation Logic: I checked for spouse existence first, then create if needed. The LLM determined marriage probability first then created a partner.
- Child Birth Year: I evenly distributed children across the fertile window while it randomly assigned birth years within the range

<br>

**4. What changes would you make to your implementation in general based on suggestions from the LLM?**

- I would not use Pandas exclusively as it adds dependency. The LLM used the built-in Python csv module because if a file isn't available, the LLM prints a warning and continues was default files which is more realistic. 
- I would also use type hints so anyone reading the code would know will know what type to expect and it can reduce the need for comments about parameter types. 

<br>

**5. What changes would you refuse to make?**

- I would refuse to make the recursive change since the tree can get really big and it will use a lot of memory. 
- I would also refuse to change the child birth year logic as it goes against the assignment write-up
