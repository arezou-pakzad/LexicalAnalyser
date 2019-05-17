from lexical_analyser import get_token_one_by_one

#first sets
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




#follow sets
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


