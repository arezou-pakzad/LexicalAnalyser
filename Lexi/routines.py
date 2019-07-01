class Routine:
    def __init__(self, name):
        self.name = name

save_routine = Routine('#save')
label_routine = Routine('#label')
while_routine = Routine('#while')
push_one_routine = Routine("#push_one")
push_zero_routine = Routine('#push_zero')
jp_save_routine = Routine('#jp_save')
jp_routine = Routine('#jp')
push_string_routine = Routine('#push_string')
pid_routine = Routine('#pid')
array_element_routine = Routine('#array_element')
get_array_with_index_routine = Routine('#get_array_with_index')
make_id_routine = Routine('#make_id')
make_array_routine = Routine('#make_array')
new_scope_routine = Routine('#new_scope')
expression_end_routine = Routine('#expression_end')
assignment_routine = Routine('#assignmnet')
minus_factor_routine = Routine('#minus_factor')
mult_routine = Routine('#mult')
push_number_routine = Routine('#push_number')
addop_routine = Routine('#addop')
relop_routine = Routine('#relop')
push_arg_routine = Routine('#push_arg')
call_routine = Routine('#call')
make_function_routine = Routine('#make_function')
add_symbol_param_routine = Routine('#add_symbol_param')
add_array_param_routine = Routine('#add_array_param')
return_routine = Routine('#return')
