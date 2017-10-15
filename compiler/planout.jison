%lex

%%

"#"(.)*(\n|$)                             /* skip comments */
\s+                                       /* skip whitespace */

"true"                                    return 'TRUE'
"false"                                   return 'FALSE'
"null"                                    return 'NULL'
"@"                                       return 'JSON_START'

"switch"                                  return 'SWITCH';
"if"                                      return 'IF';
"else"                                    return 'ELSE';

"return"                                  return 'RETURN';

[a-zA-Z_][a-zA-Z0-9_]*                    return 'IDENTIFIER'

[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?         { yytext = Number(yytext); return 'CONST'; }
\"(\\.|[^\\"])*\"                         { yytext = yytext.substr(1, yyleng-2); return 'CONST'; }
\'[^\']*\'                                { yytext = yytext.substr(1, yyleng-2); return 'CONST'; }

"<-"                                      return 'ARROW_ASSIGN'
"||"                                      return 'OR'
"&&"                                      return 'AND'
"??"                                      return 'COALESCE'
"=="                                      return 'EQUALS'
">="                                      return 'GTE'
"<="                                      return 'LTE'
"!="                                      return 'NEQ'
"=>"                                      return 'THEN'
";"                                       return 'END_STATEMENT'

"="|":"|"["|"]"|"("|")"|","|"{"|"}"|"+"|"%"|"*"|"-"|"/"|"%"|">"|"<"|"!"
                                          return yytext

/lex

%token ARROW_ASSIGN
%token AND
%token CONST
%token DEFAULT
%token ELSE
%token END_STATEMENT
%token EQUALS
%token GTE
%token IDENTIFIER
%token IF
%token JSON_START
%token LTE
%token NEQ
%token OR
%token COALESCE
%token SWITCH
%token THEN
%token RETURN

%left '!'
%left OR AND COALESCE
%left EQUALS NEQ LTE GTE '>' '<'
%left '+' '-'
%left '*' '/' '%'
%left '(' '!'
%left '['

%%

start
  : rules_list
    { $$ = {"op": "seq", "seq": $1}; return $$; }
  ;

rules_list
  : /* empty */
    { $$ = []; }
  | rules_list rule
    { $$ = $1; $$.push($2); }
  ;

rule
  : expression
    { $$ = $1; }
  | expression END_STATEMENT
    { $$ = $1; }
  | IDENTIFIER '=' simple_expression END_STATEMENT
    { $$ = {"op": "set", "var": $1, "value": $3}; }
  | IDENTIFIER ARROW_ASSIGN simple_expression END_STATEMENT
    { $$ = {"op": "set", "var": $1, "value": $3}; }
  ;

expression
  : switch_expression
    { $$ = $1; }
  | if_expression
    { $$ = $1; }
  | return_expression
    { $$ = $1; }
  ;

simple_expression
  : IDENTIFIER
    { $$ = {"op": "get", "var": $1}; }
  | TRUE
   { $$ = true; }
  | FALSE
   { $$ = false; }
  | NULL
   { $$ = null; }
  | '[' array ']'
    { $$ = {"op": "array", "values": $2}; }
  | IDENTIFIER '(' arguments ')'
    { $$ = $3; $$["op"] = $1; }
  | simple_expression '[' simple_expression ']'
    { $$ = {"op": "index", "base": $1, "index": $3}; }
  | '{' rules_list '}'
    { $$ = {"op": "seq", "seq": $2}; }
  | '(' simple_expression ')'
    { $$ = $2; }
  | CONST
    { $$ = $1; }
  | JSON_START json { $$ = {"op": "literal", "value": $2}; }
  | simple_expression '%' simple_expression
    { $$ = {"op": "%", "left": $1, "right": $3}; }
  | simple_expression '/' simple_expression
    { $$ = {"op": "/", "left": $1, "right": $3}; }
  | simple_expression '>' simple_expression
    { $$ = {"op": ">", "left": $1, "right": $3}; }
  | simple_expression '<' simple_expression
    { $$ = {"op": "<", "left": $1, "right": $3}; }
  | simple_expression EQUALS simple_expression
    { $$ = {"op": "equals", "left": $1, "right": $3}; }
  | simple_expression NEQ simple_expression
    { $$ = {"op": "not", "value": {"op": "equals", "left": $1, "right": $3}}; }
  | simple_expression LTE simple_expression
    { $$ = {"op": "<=", "left": $1, "right": $3}; }
  | simple_expression GTE simple_expression
    { $$ = {"op": ">=", "left": $1, "right": $3}; }
  | simple_expression '+' simple_expression
    { $$ = {"op": "sum", "values": [$1, $3]}; }
  | simple_expression '-' simple_expression
    { $$ = {"op": "sum", "values": [$1, {"op": "negative", "value": $3}]}; }
  | simple_expression '*' simple_expression
    { $$ = {"op": "product", "values": [$1, $3]}; }
  | '-' simple_expression
    { $$ = {"op": "negative", "value": $2}; }
  | '!' simple_expression
    { $$ = {"op": "not", "value": $2}; }
  | simple_expression OR simple_expression
    { $$ = {"op": "or", "values": [$1, $3]}; }
  | simple_expression COALESCE simple_expression
    { $$ = {"op": "coalesce", "values": [$1, $3]}; }
  | simple_expression AND simple_expression
    { $$ = {"op": "and", "values": [$1, $3]}; }
  ;

array
  : /* empty */
    { $$ = []; }
  | simple_expression
    { $$ = [$1]; }
  | array ',' simple_expression
    { $$ = $1; $$.push($3); }
  ;

json: /* true, false, null, etc. */
  IDENTIFIER { $$ = JSON.parse($1); }
  | CONST { $$ = $1; }
  | TRUE { $$ = true; }
  | FALSE { $$ = false; }
  | NULL { $$ = null; }
  | '-' json_neg_num {$$ = $2; }
  | '[' json_array ']' { $$ = $2; }
  | '{' json_map '}' { $$ = $2; }
  ;

json_array: /* empty */ { $$ = []; }
  | json { $$ = []; $$.push($1); }
  | json_array ',' json { $$ = $1; $$.push($3); }
  ;

json_map: /* empty */ { $$ = {}; }
  | json ':' json { $$ = {}; $$[$1] = $3; }
  | json_map ',' json ':' json { $$ = $1; $$[$3] = $5; }
  ;

json_neg_num: CONST { $$ = -$1; };

arguments
  : /* empty */
    { $$ = {}; }
  | arguments_list
    { $$ = $1; }
  | values_list
    { if ($1["values"].length > 1) {
        $$ = $1;
      } else {
        $$ = {"value": $1["values"][0]};
      }
    }
  ;

arguments_list
  : IDENTIFIER '=' simple_expression
    { $$ = {}; $$[$1] = $3; }
  | arguments_list ',' IDENTIFIER '=' simple_expression
    { $$ = $1; $$[$3] = $5; }
  ;

values_list
  : simple_expression
    { $$ = {}; $$["values"] = [$1]; }
  | values_list ',' simple_expression
    { $$ = $1; $$["values"].push($3); }
  ;

switch_expression
  : SWITCH '{' cases_list '}'
    { $$ = {"op": "switch", "cases": $3}; }
  ;

if_expression
  : IF '(' simple_expression ')' simple_expression optional_else_expression
    { $$ = {"op": "cond", "cond": [{"if": $3, "then": $5}]};
      if ($6["cond"]) {
        $$["cond"] = $$["cond"].concat($6["cond"]);
      }
    }
  ;

return_expression
  : RETURN simple_expression
   { $$ = {"op": "return", "value": $2} }
;

optional_else_expression
  : /* empty */
    { $$ = {}; }
  | ELSE if_expression
    { $$ = $2; }
  | ELSE simple_expression
    { $$ = {"op": "cond", "cond": [{"if": true, "then": $2}]}; }
  ;

cases_list
  : /* empty */
    { $$ = []; }
  | cases_list case END_STATEMENT
    { $$ = $1; $$.push($2); }
  ;

case
  : simple_expression THEN expression
    { $$ = {"op": "case", "condidion": $1, "result": $3}; }
  ;
