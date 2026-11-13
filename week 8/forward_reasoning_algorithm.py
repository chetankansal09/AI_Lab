from dataclasses import dataclass
from typing import Dict, List, Optional, Generator


@dataclass(frozen=True)
class Atom:
    """Represents an atomic sentence in First-Order Logic, e.g., Missile(T1)."""
    predicate: str
    args: tuple

    def __init__(self, predicate: str, *args: str):
        object.__setattr__(self, "predicate", predicate)
        object.__setattr__(self, "args", tuple(args))

    def __str__(self) -> str:
        return f"{self.predicate}({', '.join(self.args)})"


@dataclass(frozen=True)
class Rule:
    """Represents a definite clause: p1 ^ p2 ^ ... ^ pn => q."""
    premises: List[Atom]
    conclusion: Atom

    def __str__(self) -> str:
        lhs = " ^ ".join(str(p) for p in self.premises)
        return f"{lhs} => {self.conclusion}"


def print_student_header(name: str, usn: str) -> None:
    """Prints a formatted two-column header displaying the student's Name and USN."""
    col_width = 30
    border = "+" + "-" * col_width + "+" + "-" * col_width + "+"
    print(border)
    print(f"| {'Name: ' + name:<{col_width - 2}} | {'USN: ' + usn:<{col_width - 2}} |")
    print(border)
    print()


def is_variable(term: str) -> bool:
    """Variables start with a lowercase letter; constants start with uppercase."""
    return isinstance(term, str) and len(term) > 0 and term.islower()


def unify(x, y, theta: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
    """Unifies two atomic sentences or terms under substitution theta."""
    if theta is None:
        return None
    if x == y:
        return theta
    if isinstance(x, str) and is_variable(x):
        return unify_var(x, y, theta)
    if isinstance(y, str) and is_variable(y):
        return unify_var(y, x, theta)
    if isinstance(x, Atom) and isinstance(y, Atom):
        if x.predicate != y.predicate or len(x.args) != len(y.args):
            return None
        for a, b in zip(x.args, y.args):
            theta = unify(a, b, theta)
        return theta
    return None


def unify_var(var: str, x: str, theta: Dict[str, str]) -> Optional[Dict[str, str]]:
    """Helper for unifying a variable with a term."""
    if var in theta:
        return unify(theta[var], x, theta)
    if is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    new_theta = theta.copy()
    new_theta[var] = x
    return new_theta


def subst(theta: Dict[str, str], expr):
    """Applies substitution theta to a term or atomic sentence."""
    if isinstance(expr, str):
        while is_variable(expr) and expr in theta:
            expr = theta[expr]
        return expr
    if isinstance(expr, Atom):
        return Atom(expr.predicate, *(subst(theta, arg) for arg in expr.args))
    return expr


_var_counter = 0


def standardize_variables(rule: Rule) -> Rule:
    """Replaces all variables in a rule with fresh, unique variable names."""
    global _var_counter
    _var_counter += 1
    mapping: Dict[str, str] = {}

    def rename_atom(atom: Atom) -> Atom:
        new_args = []
        for arg in atom.args:
            if is_variable(arg):
                if arg not in mapping:
                    mapping[arg] = f"{arg}_{_var_counter}"
                new_args.append(mapping[arg])
            else:
                new_args.append(arg)
        return Atom(atom.predicate, *new_args)

    new_premises = [rename_atom(p) for p in rule.premises]
    new_conclusion = rename_atom(rule.conclusion)
    return Rule(new_premises, new_conclusion)


def find_all_substitutions(
    premises: List[Atom], kb: List[Atom], theta: Optional[Dict[str, str]] = None
) -> Generator[Dict[str, str], None, None]:
    """Finds all substitutions theta such that SUBST(theta, premises) match facts in KB."""
    if theta is None:
        theta = {}
    if not premises:
        yield theta
        return

    first, rest = premises[0], premises[1:]
    first_sub = subst(theta, first)

    for fact in kb:
        new_theta = unify(first_sub, fact, theta)
        if new_theta is not None:
            yield from find_all_substitutions(rest, kb, new_theta)


def fol_fc_ask(facts: List[Atom], rules: List[Rule], query: Atom) -> Optional[Dict[str, str]]:
    """
    First-Order Logic Forward Chaining (FOL-FC-ASK).
    Returns a substitution dict if query is entailed, otherwise None (false).
    """
    kb = list(facts)

    for fact in kb:
        phi = unify(fact, query, {})
        if phi is not None:
            return phi

    iteration = 0
    while True:
        iteration += 1
        new: List[Atom] = []
        print(f"--- Iteration {iteration} ---")

        for rule in rules:
            std_rule = standardize_variables(rule)
            for theta in find_all_substitutions(std_rule.premises, kb):
                q_prime = subst(theta, std_rule.conclusion)

                already_known = any(unify(q_prime, s, {}) is not None for s in kb + new)
                if not already_known:
                    new.append(q_prime)
                    print(f"  Inferred: {q_prime}")

                    phi = unify(q_prime, query, {})
                    if phi is not None:
                        print(f"\nQuery {query} proved! Substitution: {phi}")
                        return phi

        if not new:
            print("\nNo new facts inferred. Query cannot be proved.")
            return None

        kb.extend(new)


# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # Replace with your actual Name and USN
    student_name = "CHETAN KANSAL"
    student_usn = "1WA24CS094"
    print_student_header(student_name, student_usn)

    initial_facts = [
        Atom("American", "Robert"),
        Atom("Missile", "T1"),
        Atom("Owns", "A", "T1"),
        Atom("Enemy", "A", "America"),
    ]

    knowledge_rules = [
        Rule([Atom("Missile", "x")], Atom("Weapon", "x")),
        Rule([Atom("Missile", "x"), Atom("Owns", "A", "x")], Atom("Sells", "Robert", "x", "A")),
        Rule([Atom("Enemy", "x", "America")], Atom("Hostile", "x")),
        Rule(
            [
                Atom("American", "p"),
                Atom("Weapon", "q"),
                Atom("Sells", "p", "q", "r"),
                Atom("Hostile", "r"),
            ],
            Atom("Criminal", "p"),
        ),
    ]

    goal = Atom("Criminal", "Robert")
    result = fol_fc_ask(initial_facts, knowledge_rules, goal)
    print("Result:", result if result is not None else False)
