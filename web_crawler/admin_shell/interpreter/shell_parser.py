from web_crawler.admin_shell.interpreter.shell_commands import command_map
from web_crawler.admin_shell.interpreter.shell_commands import command_expected_args

#parsed command object
class ParsedCommand:
    def __init__(self,cmd,args:tuple = None):
        self.cmd =cmd
        self.args = args


#exceptions during parsing
class InvalidSyntax(Exception):
    pass

class Invalid_command(InvalidSyntax):
    pass

class Missing_all_args(InvalidSyntax):
    pass

class Missing_some_args(InvalidSyntax):
    pass 

class Extra_args(InvalidSyntax):
    pass


def parser(words:list[str]) ->ParsedCommand:
    command = words[0].lower()

    if not command in command_map:
        raise Invalid_command(f"Invalid Command:'{command}'.")
    
    cmd = command_map[command]
    args = None
    provided_args_num = len(words)-1 

    
    if cmd in command_expected_args:
        req_num_args = command_expected_args[cmd]

        if provided_args_num > req_num_args:
            raise Extra_args(f"Invalid syntax: Extra argument(s).\nCommand:'{command}' expects only {req_num_args} argument(s)")
        
        elif provided_args_num == 0:
            raise Missing_all_args(f"Invalid syntax: Missing all argument(s).\nCommand:'{command}' expects {req_num_args} argument(s)")

        elif provided_args_num < req_num_args:
            raise Missing_some_args(f"Invalid syntax: Missing some argument(s).\nCommand:'{command}' expects {req_num_args} argument(s). Provided argument(s):{provided_args_num}")

        args = tuple(words[1:])

    elif provided_args_num>0:
        raise Extra_args(f"Invalid syntax: Extra argument(s).\nCommand:'{command}' expects 0 argument(s)")

    return ParsedCommand(cmd,args)