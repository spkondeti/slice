import sys
from scanner import Scanner

class Slice:

    def __init__(self):
        self.had_error = False
        self.had_rt_error = False

    @staticmethod
    def main(*args):
        if(len(args) > 2):
            print("Usage: slice [script]")
            sys.exit(64)
        elif (len(args) == 2):
            Slice().run_file(args[1])
        else:
            Slice().run_shell()

    def run_file(self,path:str):
        try:
            with open(path) as f:
                data = f.readlines()
                lines = "".join(data)
        except IOError as e:
            print("File Not Found")
            sys.exit(74)
        self.run(lines)
        if(self.had_error):
            sys.exit(65)
        if(self.had_rt_error):
            sys.exit(70)

    def run_shell(self):
        print("Welcome to Slice")
        print("Press Ctrl-C/Ctrl-D to exit")
        while True:
            try:
                str_input = input("> ")
                if str_input and str_input[0] == chr(4):
                    raise EOFError
                self.run(str_input)
                self.had_error = False
            except (KeyboardInterrupt, EOFError):
                self.clean_quit()

    def clean_quit(self):
        print("Sayonara!")
        sys.exit(0)

    def run(self,source):
        scanner = Scanner(source)
        tokens = scanner.get_tokens()
        for token in tokens:
            print(token)

    def error(self,line,message):
        err_message = f"[line {line}] Error : {message}"
        print(err_message)
        print(message,file=sys.stderr)
        self.had_error = True

Slice().main(slice,"surya.txt")