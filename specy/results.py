
from colors import red, blue, green

def print_results(head_block, time_elapsed):
    seconds = time_elapsed.microseconds/1000000.0
    tree = build_tree(head_block)
    tests_ran, tests_passed, percent_passed = count_tests(tree)
    print("\n{0}".format("-"*80))
    print("Ran {2} tests in {3:.4f}s\nPassed {0}%, failed {1}".format(percent_passed,  
                                                    tests_ran - tests_passed, tests_ran, seconds))
    print("\nproperties\n{0}".format("="*40))
    print_loop(tree)


def print_loop(tree, level=0):
    if tree["passed"] == False:
        c = red
    elif tree["passing_children"] == False:
        c = blue
    else:
        c = green

    if "before_" not in tree["description"]:
        print("{}{}".format("  "*level, c(tree["description"])))
    for child in tree["children"]:
        print_loop(child, level=level+1)



def build_tree(head_block):
    tree = {"description": None, "children": [], "was_test": None, "passed":None, 
            "passing_children": True}
    description = head_block.description
    if head_block.block_name == "it":
        tree["was_test"] = True
        tree["passed"]   = head_block.passed
    tree["description"] = description

    for child in head_block.child_blocks:
        sub_tree = build_tree(child)
        if not sub_tree["passing_children"] or sub_tree["passed"] ==  False:
            tree["passing_children"] = False
        tree["children"].append(sub_tree)

    return tree


def count_tests(tree):
    tests = 0
    passed = 0

    if tree["was_test"]:
        tests = tests + 1
        if tree["passed"]:
            passed = passed + 1

    for child in tree["children"]:
        t,p,per = count_tests(child)
        tests = tests + t
        passed = passed + p

    if tests > 1:
        percent_passed = passed*100/tests
    else:
        percent_passed = 100
    return tests, passed, percent_passed