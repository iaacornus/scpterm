# SCP Terminal v.X

View the classified SCP Foundation anomalies in your desktop.

# Syntaxes
## Signs

There are signs while tasks are running within the terminal:

1. `[=]`, denotes a happening process, with torqiouse color .
2. `[-]`, an error occurred, colored red.
3. `[+]`, task completed successfully, colored green.
4. `[:]`, yes or no input, whether to proceed or not, color varies on severity, refer to color codes below.
5. `[^]`, a confirmation input.
6. `[*]`, more complicated user input required, color varies on severity, refer to color codes below.
7. `>`, sub process, colored torqiouse, with the important subject matter colored as cyan, if there is any.

## Color codes

Color codes denotes the severity of the happening processes.

1. **red**, task failed or dangerous to proceed.
2. **green**, task completed successfully, or safe to proceed.
3. **white**, neutral operation, usually for confirmation.
4. **torqiouse**, status of the process.

# Outputs

Usually, the program outputs (`stdout`) various information about the process:

```
[02:52:20] > Fetching SCP-099                                database_init.py:43
```

Which can be broken down into:

```
[time] > <process name>                                     <process_parent>:<process_line>
```

