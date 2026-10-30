def tt_entails(kb_func, alpha_func, symbols):
    """
    Determines if the Knowledge Base (KB) entails a query (alpha)
    using truth-table enumeration.
    """
    def tt_check_all(kb, alpha, symbols, model):
        if not symbols:  # Base case: empty list of symbols
            if kb(model):
                return alpha(model)
            else:
                return True  # When KB is false, always return true
        else:
            p = symbols[0]
            rest = symbols[1:]
            
            # Create two branches: one where P is True, one where P is False
            model_true = model.copy()
            model_true[p] = True
            
            model_false = model.copy()
            model_false[p] = False
            
            return (tt_check_all(kb, alpha, rest, model_true) and 
                    tt_check_all(kb, alpha, rest, model_false))
            
    return tt_check_all(kb_func, alpha_func, symbols, {})


# --- STUDENT INFORMATION INPUT ---
print("==================================================")
name = input("Enter your Name: ")
usn = input("Enter your USN: ")
print("==================================================")


# --- DISPLAY STUDENT CREDENTIALS ---
print("\n" + "=" * 50)
print(f"NAME : {name.upper()}")
print(f"USN  : {usn.upper()}")
print("=" * 50)


# --- PROBLEM SETUP ---

# 1. Define the propositional symbols involved
symbols = ['P', 'Q', 'R']

# 2. Define the Knowledge Base logic function
# KB consists of: Q -> P, P -> ~Q, and Q v R
def kb_formula(model):
    p = model['P']
    q = model['Q']
    r = model['R']
    
    sentence1 = (not q) or p          # Q -> P
    sentence2 = (not p) or (not q)    # P -> ~Q
    sentence3 = q or r                # Q v R
    
    # KB is true only when all individual sentences are true
    return sentence1 and sentence2 and sentence3


# --- EVALUATING THE OBSERVATION BOOK QUESTIONS ---

print("\n--- Truth Table Enumeration Inference Results ---")

# ii) Does KB entail R?
entails_r = tt_entails(kb_formula, lambda m: m['R'], symbols)
print(f"ii) Does KB entail R?          -> {entails_r}")

# iii) Does KB entail R -> P?
entails_r_to_p = tt_entails(kb_formula, lambda m: (not m['R']) or m['P'], symbols)
print(f"iii) Does KB entail R -> P?    -> {entails_r_to_p}")

# iv) Does KB entail Q -> R?
entails_q_to_r = tt_entails(kb_formula, lambda m: (not m['Q']) or m['R'], symbols)
print(f"iv) Does KB entail Q -> R?    -> {entails_q_to_r}")


# --- BONUS: DISPLAYING THE TRUTH TABLE MODELS ---
print("\n--- Complete Truth Table Models ---")
print(f"{'P':<6} {'Q':<6} {'R':<6} || {'Q->P':<6} {'P->~Q':<6} {'QvR':<6} || {'KB Status'}")
print("-" * 60)
for p in [True, False]:
    for q in [True, False]:
        for r in [True, False]:
            m = {'P': p, 'Q': q, 'R': r}
            s1 = (not q) or p
            s2 = (not p) or (not q)
            s3 = q or r
            kb_true = s1 and s2 and s3
            status = "MODEL (KB is True)" if kb_true else "False"
            print(f"{str(p):<6} {str(q):<6} {str(r):<6} || {str(s1):<6} {str(s2):<6} {str(s3):<6} || {status}")
print("=" * 60)
