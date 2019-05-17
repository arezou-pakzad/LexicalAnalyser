from lexical_analyser import get_token_one_by_one


class Non_terminal:
    def __init__(self, name, first_set, follow_set):
        self.name = name
        self.first_set = first_set
        self.follow_set = follow_set
        self.transition_dictionary = dict()
        self.final_state = 0
        self.first_state = 0

    def set_transition_dictionary(self, transition_dictionary, final_state, first_state):
        self.transition_dictionary = transition_dictionary
        self.final_state = final_state
        self.first_state = first_state


E = Non_terminal(name='E', first_set=['int', '('], follow_set=[')', '$'])
T = Non_terminal(name='T', first_set=['int', '('], follow_set=['+', ')', '$'])
X = Non_terminal(name='X', first_set=['+', 'EPSILON'], follow_set=['$', ')'])
Y = Non_terminal(name='Y', first_set=['*', 'EPSILON'], follow_set=['+', ')', '$'])


def function(non_terminal, token):
    state = non_terminal.first_state

    while True:
        flag = False
        this_state = {key: value for key, value in non_terminal.transition_dictionary if key[0] == state}
        if (state, token) in this_state:
            state = non_terminal.transition_dictionary[(state, token)]
        elif len(this_state) > 0:
            for key, value in this_state:
                if type(key[1]) == Non_terminal and (token in key[1].first_set or
                                                     ('EPSILON' in key[1].first_set and token in key[1].follow_set)):
                    function(key[1], token)
                    state = value
                    flag = True
                    break
                    # TODO: error handling
        if not flag and (state, 'EPSILON') in this_state:
            state = non_terminal.transition_dictionary[(state, 'EPSILON')]

        token = get_token_one_by_one()

# first sets
# program	int, void
# declaration-list	int, void
# declaraion-list	EPSILON
# declaration	int, void
# var-declaration	int, void
# A	[, ;
# type-specifier	int, void
# fun-declaration	int, void
# params	void, int
# param-list	int, void
# param	int, void
# B	[, EPSILON
# compound-stmt	{
# statement-list	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM
# statement	{, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM
# expression-stmt	continue, break, ;, ID, +, -, (, NUM
# selection-stmt	if
# iteration-stmt	while
# return-stmt	return
# C	;, ID, +, -, (, NUM
# switch-stmt	switch
# case-stmts	EPSILON
# case-stmt	case
# default-stmt	default, EPSILON
# expression	ID, +, -, (, NUM
# var	ID
# D	[, EPSILON
# simple-expression	+, -, (, ID, NUM
# E	EPSILON, <, ==
# relop	<, ==
# additive-expression	+, -, (, ID, NUM
# F	EPSILON, +, -
# addop	+, -
# term	+, -, (, ID, NUM
# G	*, EPSILON
# signed-factor	+, -, (, ID, NUM
# factor	(, ID, NUM
# call	ID
# args	EPSILON, ID, +, -, (, NUM
# arg-list	ID, +, -, (, NUM
# H	,, EPSILON


# follow sets
# program	-|
# declaration-list	EOF, EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM
# declaraion-list
# declaration	int, void
# var-declaration	int, void
# A	int, void
# type-specifier	ID
# fun-declaration	int, void
# params	)
# param-list	)
# param	,, )
# B	,, )
# compound-stmt	int, void, EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# statement-list	}
# statement	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# expression-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# selection-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# iteration-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# return-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# C	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# switch-stmt	EPSILON, {, continue, break, ;, if, while, return, switch, ID, +, -, (, NUM, else
# case-stmts	default, EPSILON
# case-stmt
# default-stmt	}
# expression	;, ), ], ,, EPSILON
# var	=, *, EPSILON
# D	=, *, EPSILON
# simple-expression	;, ), ], ,, EPSILON
# E	;, ), ], ,, EPSILON
# relop	+, -, (, ID, NUM
# additive-expression	EPSILON, <, ==, ;, ), ], ,
# F	EPSILON, <, ==, ;, ), ], ,
# addop	+, -, (, ID, NUM
# term	EPSILON, +, -
# G	EPSILON, +, -
# signed-factor	*, EPSILON
# factor	*, EPSILON
# call	*, EPSILON
# args	)
# arg-list	)
# H	)
