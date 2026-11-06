def is_variable(x):
    """
    Helper function to determine if a term is a variable.
    By standard convention, variables start with a lowercase letter (e.g., x, y).
    """
    return isinstance(x, str) and len(x) > 0 and x.islower()

def is_constant(x):
    """
    Helper function to determine if a term is a constant.
    By standard convention, constants start with an uppercase letter (e.g., Riya, Apple).
    """
    return isinstance(x, str) and len(x) > 0 and x[0].isupper()

def occurs_check(var, expr):
    """
    Checks if a variable occurs inside an expression.
    """
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occurs_check(var, sub_expr) for sub_expr in expr)
    return False

def apply_substitution(subst, expr):
    """
    Applies a substitution dictionary to an expression.
    """
    if not subst or subst == "NIL":
        return expr
    if isinstance(expr, str):
        return subst.get(expr, expr)
    if isinstance(expr, list):
        return [apply_substitution(subst, item) for item in expr]
    return expr

def unify(psi1, psi2):
    """
    Implements the Unification Algorithm following the slide rules.
    """
    # Step 1: If psi1 or psi2 is a variable or constant
    if isinstance(psi1, str) or isinstance(psi2, str):
        if psi1 == psi2:
            return "NIL"
        elif is_variable(psi1):
            if occurs_check(psi1, psi2):
                return "FAILURE"
            return {psi1: psi2}
        elif is_variable(psi2):
            if occurs_check(psi2, psi1):
                return "FAILURE"
            return {psi2: psi1}
        else:
            return "FAILURE"

    # Step 2: Predicate symbols must match
    if psi1[0] != psi2[0]:
        return "FAILURE"

    # Step 3: Argument count must match
    if len(psi1) != len(psi2):
        return "FAILURE"

    # Step 4: Set Substitution set(SUBST) to empty
    subst = {}

    # Step 5: Iterating over elements
    for i in range(1, len(psi1)):
        s = unify(psi1[i], psi2[i])
        
        if s == "FAILURE":
            return "FAILURE"
        
        if s != "NIL":
            # Apply substitutions to the remainder of the lists
            for j in range(i + 1, len(psi1)):
                psi1[j] = apply_substitution(s, psi1[j])
                psi2[j] = apply_substitution(s, psi2[j])
            
            # Compose substitution mapping updates
            for key in subst:
                subst[key] = apply_substitution(s, subst[key])
            subst.update(s)

    return "NIL" if not subst else subst

def parse_expression(input_str):
    """
    Parses a string like 'Eats(x, Apple)' into standard array structure: ['Eats', 'x', 'Apple']
    """
    input_str = input_str.strip().replace(" ", "")
    if "(" not in input_str or not input_str.endswith(")"):
        raise ValueError("Invalid syntax framework.")
    
    predicate, args_str = input_str.split("(", 1)
    args_str = args_str[:-1]
    args = args_str.split(",") if args_str else []
    return [predicate] + args

def format_expression(parsed_list):
    """
    Reconstructs list format ['Eats', 'Riya', 'Apple'] back to string 'Eats(Riya, Apple)'
    """
    return f"{parsed_list[0]}({', '.join(parsed_list[1:])})"

# --- Interactive Terminal ---
if __name__ == "__main__":
    print("=" * 60)
    name = input("Enter your Name: ").strip()
    usn = input("Enter your USN: ").strip()
    print("=" * 60)
    
    print("\n[Test Example Case from Slide]")
    print("Expression A: Eats(x, Apple)")
    print("Expression B: Eats(Riya, y)")
    print("-" * 60)
    
    try:
        str1 = input("Enter first expression (or press Enter for default): ").strip()
        if not str1: str1 = "Eats(x, Apple)"
        
        str2 = input("Enter second expression (or press Enter for default): ").strip()
        if not str2: str2 = "Eats(Riya, y)"
        
        expr1 = parse_expression(str1)
        expr2 = parse_expression(str2)
        
        # Keep an unaltered copy for final output rendering
        original_expr1 = list(expr1) 
        
        print("\n" + "=" * 60)
        print(f"Name : {name}")
        print(f"USN  : {usn}")
        print("=" * 60)
        print("RUNNING UNIFICATION PROCESS")
        print("-" * 60)
        
        result = unify(expr1, expr2)
        
        print(f"Substitutions Found : {result}")
        
        if result != "FAILURE":
            # Reconstruct final string expression by applying the resolved mappings
            final_parsed = apply_substitution(result, original_expr1)
            print(f"Unified Expression  : {format_expression(final_parsed)}")
        else:
            print("Unified Expression  : Unified expressions could not be resolved.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nParsing Error: {e}")
