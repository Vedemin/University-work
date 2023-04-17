Dear Student,

I'm happy to announce that you've managed to get **16** out of 28 points for this assignment.\
There still exist some issues that should be addressed before the deadline: 2022-12-21 11:15:00 CET (+0100). For further details, please refer to the following list:

<details><summary>Record should be evaluated correctly &gt;&gt; evaluator got wrong end result, got: {0 = 0, 2 = succ 0, label = if true then false else true}, expected {0 = 0, 2 = succ 0, label = false},</summary>* input = {0 = 0, 2 = succ 0, label = if true then false else true}<br>* detailed comparison: TypedLambdaProgram(term=TmRecord(info=Info(lineno=1, column=0), records=OrderedDict([('0', TmZero(info=Info(lineno=1, column=6))), ('2', TmSucc(info=Info(lineno=1, column=9), number=TmZero(info=Info(lineno=1, column=14)))), ('label', TmIf(info=Info(lineno=1, column=25), condition=TmTrue(info=Info(lineno=1, column=28)), if_true=TmFalse(info=Info(lineno=1, column=38)), if_else=TmTrue(info=Info(lineno=1, column=49))))])), name_context=[]) vs TypedLambdaProgram(term=TmRecord(info=Info(lineno=1, column=0), records=OrderedDict([('0', TmZero(info=Info(lineno=1, column=6))), ('2', TmSucc(info=Info(lineno=1, column=9), number=TmZero(info=Info(lineno=1, column=14)))), ('label', TmFalse(info=Info(lineno=1, column=38)))])), name_context=[])</details>
<details><summary>Projection should be evaluated correctly &gt;&gt; evaluator got wrong end result, got: {label = 0}.label, expected 0,</summary>* input = {label = 0}.label<br>* detailed comparison: TypedLambdaProgram(term=TmProjection(info=Info(lineno=1, column=0), record=TmRecord(info=Info(lineno=1, column=0), records=OrderedDict([('label', TmZero(info=Info(lineno=1, column=10)))])), label='label'), name_context=[]) vs TypedLambdaProgram(term=TmZero(info=Info(lineno=1, column=10)), name_context=[])</details>
<details><summary>Typecheck should pass correct cases &gt;&gt; typechecker should find type Bool, instead got None</summary>&nbsp;- program 'case <u = unit> as <u:Unit, b:Bool> of <u = x> => false | <b = x> => x'</details>
<details><summary>Tagging should be evaluated correctly &gt;&gt; evaluator got wrong end result, got: &lt;n:pred succ succ 0&gt; as &lt;u: Unit,b: Bool,n: Nat&gt;, expected &lt;n:succ 0&gt; as &lt;u: Unit,b: Bool,n: Nat&gt;,</summary>* input = <n:pred succ succ 0> as <u: Unit,b: Bool,n: Nat><br>* detailed comparison: TypedLambdaProgram(term=TmTagging(info=Info(lineno=1, column=0), label='n', term=TmPred(info=Info(lineno=1, column=5), number=TmSucc(info=Info(lineno=1, column=10), number=TmSucc(info=Info(lineno=1, column=15), number=TmZero(info=Info(lineno=1, column=20))))), type=VariantType(variants_types=OrderedDict([('u', <BaseType.Unit: 'Unit'>), ('b', <BaseType.Bool: 'Bool'>), ('n', <BaseType.Nat: 'Nat'>)]))), name_context=[]) vs TypedLambdaProgram(term=TmTagging(info=Info(lineno=1, column=0), label='n', term=TmSucc(info=Info(lineno=1, column=15), number=TmZero(info=Info(lineno=1, column=20))), type=VariantType(variants_types=OrderedDict([('u', <BaseType.Unit: 'Unit'>), ('b', <BaseType.Bool: 'Bool'>), ('n', <BaseType.Nat: 'Nat'>)]))), name_context=[])</details>
<details><summary>Case should be evaluated correctly &gt;&gt; evaluator got wrong end result, got: case &lt;u:unit&gt; as &lt;u: Unit,b: Bool&gt; of &lt;u=x&gt; =&gt; false | &lt;b=x&gt; =&gt; x, expected false,</summary>* input = case <u:unit> as <u: Unit,b: Bool> of <u=x> => false | <b=x> => x<br>* detailed comparison: TypedLambdaProgram(term=TmCase(info=Info(lineno=1, column=0), term=TmTagging(info=Info(lineno=1, column=5), label='u', term=TmUnit(info=Info(lineno=1, column=10)), type=VariantType(variants_types=OrderedDict([('u', <BaseType.Unit: 'Unit'>), ('b', <BaseType.Bool: 'Bool'>)]))), vars=OrderedDict([('u', 'x'), ('b', 'x')]), branches=OrderedDict([('u', TmFalse(info=Info(lineno=1, column=50))), ('b', TmVar(info=Info(lineno=1, column=69), index=0, context_length=1))])), name_context=[]) vs TypedLambdaProgram(term=TmFalse(info=Info(lineno=1, column=50)), name_context=[])</details>
<details><summary>Typecheck should detect invalid tag type &gt;&gt; typechecker should have found the &#x27;TagInvalidType&#x27; error (program: &#x27;&lt;u = unit&gt; as &lt;u:Bool, n:Nat&gt;)&#x27;</summary></details>
<details><summary>Typecheck should detect case invalid labels &gt;&gt; typechecker should have found the &#x27;CaseInvalidLabels&#x27; error (program: &#x27;case &lt;u = unit&gt; as &lt;u:Unit, b:Bool&gt; of &lt;u = x&gt; =&gt; false | &lt;c = x&gt; =&gt; x)&#x27;</summary></details>
<details><summary>Typecheck should detect case divergent branches &gt;&gt; typechecker should have found the &#x27;CaseDivergentBranches&#x27; error (program: &#x27;case &lt;u = unit&gt; as &lt;u:Unit, n:Nat&gt; of &lt;u = x&gt; =&gt; false | &lt;n = x&gt; =&gt; x)&#x27;</summary></details>

-----------
I remain your faithful servant\
_Bobot_