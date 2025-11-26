Welcome to StayRelevant, a project that helps individuals observe predictions of the economic stnading of the United States. The program uses a Linear Regression Line, which uses data provided by the Federal Reserve, in order to make these predictions.

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

I do not currently have a front end, so in order to run this program, you will need to:

First, pull the project into your Visual Studio Code IDE:

Then, ensure that your directory is in the StayRelevant directory, not to be confused with the stay-relevant directory:

-- navigate to the "back_end.py" file located in the folder named: "server".

-- find line 238 in the file, which should have a variable labeled "user_input".

   --- By changing the value of the variable, you would be able to run the linear regression model to predict the outputs for: GDP, CPI, PPI, PCE, INCOME, and Inflation:

-- After changing the value or leaving it alone, just press the run button and watch everything unfold!
   
   --- The final output will indicate whether or not the economy is in a bad state in the given year, based on the growth of each section.
   --- The program will also output the training epochs to show the cost as it iterates through each epoch.

--- Happy Coding and Thanks for Reading! 