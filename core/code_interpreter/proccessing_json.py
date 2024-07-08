import json
import ast

def proccess_result(result: str):
    try:
        user_code = result[result.index("def"):result.index('[{\"')]
        json_start = result.rindex('"}}]') + 4
        json_part = result[json_start:].strip()
        result_dict = ast.literal_eval(json_part)
        result_dict["user_code"] = user_code.strip()
        return result_dict
    except (ValueError, SyntaxError) as e:
        return None

