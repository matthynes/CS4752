Matthew Hynes (201200318)

- I didn't have enough time to properly implement iterative-deepening so rather than get it partially working I
decided to stick with "vanilla" Alpha-Beta.

- For some reason, running the AI with a time limit (even a large one of, say, 5000ms) causes it to perform
significantly worse than one with a depth limit. I'm not sure why but upon trying to debug it I saw the depth limit
would occasionally get as high as 38 but the performance didn't take a hit. So I think the alpha_beta function may be
 getting with incorrect parameters or terminating prematurely when there's a time limit.
  Nevertheless, it still manages to win 8-0 against the Random opponent every time; but stands no chance against an
  AI with a depth limit of 3 or higher.

- Despite iterating only through legal moves in the alpha-beta function, sometimes an illegal move would be returned.
 Thus I had to add an additional check at the end of the get_move function and return a random legal move if it tried
  to return an illegal one. However, this only happened once every test run (~15 games) so the results shouldn't be
  thrown off, this was mainly so the program wouldn't exit when trying to test it.

- As an aside, an AI with a depth limit of 3 proves a formidable opponent. Setting the limit to 4 or higher causes
the program to take a moderate performance hit but the AI is near impossible to beat.
