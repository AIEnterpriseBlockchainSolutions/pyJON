class JONSyntaxError(Exception):
    def __init__(self, line_number: int, file: str | None) -> None:
        super().__init__(f"Syntax error at line f{line_number}" + ("" if not file else " of file '{file}'") )

class JONTypeAlreadyExists(Exception):
    def __init__(self, name: str, line_number: int, file: str | None) -> None:
        super().__init__(f"Type '{name}' at line f{line_number}" + ("" if not file else " of file '{file}'")+" has already been defined" )