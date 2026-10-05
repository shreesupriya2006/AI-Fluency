"""
Day 6 - JSON Schema argument validator
"""


def validate_arguments(arguments,schema):
    # Check that arguments are an object
    if not isinstance(arguments,dict):
        return "Arguments must be a JSON object."

    properties = schema.get("properties",{})
    required = schema.get("required",[])

    # 1. Check missing required arguments
    for name in required:
        if name not in arguments:
            return (
                f"Missing required argument '{name}'. "
                f"Expected: {', '.join(required)}"
            )

    # 2. Check invented/extra arguments
    extra = set(arguments)-set(properties)

    if extra:
        return (
            f"Unexpected argument(s): {', '.join(sorted(extra))}. "
            f"Allowed: {', '.join(properties)}"
        )

    # 3. Check argument types and enum values
    for name,value in arguments.items():
        rule = properties[name]
        expected_type = rule.get("type")

        if expected_type == "string":
            if not isinstance(value,str):
                return (
                    f"Argument '{name}' must be a string, "
                    f"but got {type(value).__name__}: {value}"
                )

        elif expected_type == "number":
            if isinstance(value,bool) or not isinstance(value,(int,float)):
                return (
                    f"Argument '{name}' must be a number, "
                    f"but got {type(value).__name__}: {value}"
                )

        elif expected_type == "integer":
            if isinstance(value,bool) or not isinstance(value,int):
                return (
                    f"Argument '{name}' must be an integer, "
                    f"but got {type(value).__name__}: {value}"
                )

        # 4. Check enum values
        if "enum" in rule and value not in rule["enum"]:
            return (
                f"Argument '{name}' must be one of "
                f"{rule['enum']}, got {value}"
            )

    return None