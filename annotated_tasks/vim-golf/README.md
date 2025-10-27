## Files

### tests/test_outputs.py

test_outputs.py should be a python test file that uses pytest.

Inside this file, we write the tests that were defined in task.yaml.
Make sure that these tests are defined in the task!
Notice that we describe the tests in this block in task.yaml:

```
The test case is one particular popular challenge on vimgolf, and validating that the file exists, the string inside is a valid solution, and the length is at most 1.5 times the best submission on the leaderboard.
We also check that the start, end, score, and challenge files all exist.
We also check that the start and end files match the challenge in vimgolf.
```

Some common commands and use cases and explanations are provided:

`tb run --agent oracle --task-id vim-golf --dataset-path annotated_tasks`
This command will run the oracle (solution.sh) and run the test_outputs.py after the solution runs.
You must use this to make sure that your solution works.

`tb run --agent claude-code --model anthropic/claude-sonnet-4-5-20250929 -t vim-golf --n-attempts 10 --dataset-path annotated_tasks`
This command will run the claude-sonnet-4.5 model with the claude-code agent 10 times. It will run test_outputs.py at the end,
and will print how many successes happened (resolved trials) and how many fails (unresolved trials), as well as a few other
statistics.

`tb run --agent codex --model openai/gpt-5 -t vim-golf --n-attempts 10 --dataset-path annotated_tasks`
This command will run the gpt-5 model with the codex agent 10 times. It will run test_outputs.py at the end,
and will print how many successes happened (resolved trials) and how many fails (unresolved trials), as well as a few other
statistics.

Notice the `--dataset-path annotated_tasks` flag

### docker-compose.yaml

This file will need to be changed if you have an additional service you want to deploy in the agent's environment.

