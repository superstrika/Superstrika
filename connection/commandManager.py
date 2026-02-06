
def runCommand(cmd: str) -> None:
    """
    :param cmd: the command to execute: <code>#<param1>#<param2>#<param3> ...
    :type cmd: str
    :return: None
    :rtype: None
    """
    cmd = cmd.split("#")

    try:
        command: int = int(cmd[0])
    except ValueError:
        print("Command not a number!")
        return

    if len(cmd) > 1:
        params: list = cmd[1:]

        for i in range(len(params)):
            if (params[i][0] == "$"):
                try:
                    params[i] = float(params[i][1:])
                except ValueError:
                    print(f"Param {params[i]} a number!")
                    params[i] = ""
    else:
        params: None = None

    match command:
        case 1:
            print(f"Command executed: 1 with params: {params}")

        case 2:
            print(f"Command executed: 2 with params: {params}")


"""
Command Guide:
1. ball found. Template: 1#<ballX>#<ballY>#<BlueGoalX>#<BlueGoalY>#<YellowGoalX>#<YellowGoalY>
   Example: 1#0.0#100#0#250#0#0#0
2. 
"""



