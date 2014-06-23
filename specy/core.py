
import inspect    
from datetime import datetime

from specy.blocks import TestBlock
from specy.results import print_results


block_stack = []

def end():
    if not block_stack:
        start_time = datetime.now()

    last_func, last_line, frame = get_last_func()
    block = TestBlock(method=last_func, frame=frame)
    if block_stack:
        parent_block = block_stack[-1]
        block.register_parent(parent_block)
    block_stack.append(block)
    block.run_block()
    block_stack.remove(block)

    if not block_stack:
        time_elapsed = datetime.now() - start_time
        print_results(block, time_elapsed)


def clean(local_vars):
    good_vars = []
    for name, var in local_vars.items():
        if name[0] != '_' and inspect.isfunction(var):
            if var.__name__ not in ['end', 'when', 'item']:
                good_vars.append(var)
    return good_vars

def get_line_numbers(funcs):
    funcs_w_line_nu = []
    for f in funcs:
        line = inspect.getsourcelines(f)[1]
        funcs_w_line_nu.append((f, line))
    return funcs_w_line_nu

def get_local_vars(depth = 1):
    stack = inspect.stack()
    frames = [frame_obj[0] for frame_obj in stack]
    target_frame = frames[depth+1]
    return target_frame.f_locals, target_frame


def get_last_func():
    test_local_vars, frame = get_local_vars(2)
    funcs = clean(test_local_vars)
    funcs_w_line_nu = get_line_numbers(funcs)
    last_func = None
    last_line = 0
    for func, line in funcs_w_line_nu:
        if line > last_line:
            last_func = func
            last_line = line
    return last_func, last_line, frame
    


