Dear Student,

I'm happy to announce that you've managed to get **13** out of 25 points for this assignment.\
There still exist some issues that should be addressed before the deadline: 2022-11-23 11:15:00 CET (+0100). For further details, please refer to the following list:

<details><summary>Typecheck should detect incorrect if guard &gt;&gt; [Type Error] guard of conditional is not a boolean, got &#x27;None&#x27;</summary>- program: if (\x:Bool.0) then true else false<br>- type context: []<br>- position: Info(lineno=1, column=0)<br><br>During handling of the above exception, another exception occurred:<br>the error contains incorrect error details:<br>- tip: this test requires support for typechecking `TmAbs`, `TmTrue`, `TmFalse` terms<br>- got ('None',), <br>- expected ('Bool -> Bool',) <br>- program: 'if (\x:Bool. x) then true else false'</details>
<details><summary>Typecheck should detect incorrect if guard &gt;&gt; typechecker should have found the &#x27;IfInvalidGuard&#x27; error (program: &#x27;(\x:Nat-&gt;Nat. if x then 0 else succ 0) (\x:Nat. succ x))&#x27;</summary></details>
<details><summary>Typecheck should detect divergent if branches &gt;&gt; [Type Error] branches of conditional have different types: &#x27;None&#x27; and &#x27;Bool&#x27;</summary>- program: if false then (\x:Bool.0) else true<br>- type context: []<br>- position: Info(lineno=1, column=0)<br><br>During handling of the above exception, another exception occurred:<br>the error contains incorrect error details:<br>- tip: this test requires support for typechecking `TmFalse`, `TmTrue`, `TmAbs`<br>- got ('None', 'Bool'), <br>- expected ('Bool -> Bool', 'Bool') <br>- program: 'if false then (\x:Bool. x) else true'</details>
<details><summary>Typecheck should detect divergent if branches &gt;&gt; typechecker should have found the &#x27;IfDivergentBranches&#x27; error (program: &#x27;(\x:Nat-&gt;Nat. if true then x else 0) (\x:Nat. x))&#x27;</summary></details>
<details><summary>Typecheck should detect unnatural arguments &gt;&gt; typechecker should have found the &#x27;UnnaturalArg&#x27; error (program: &#x27;(\x:Nat-&gt;Nat. iszero x) (\x:Nat. succ x))&#x27;</summary></details>
<details><summary>Typecheck should detect invalid type annotation &gt;&gt; typechecker should have found the &#x27;InvalidType&#x27; error (program: &#x27;(\x:Bolo.x) true)&#x27;</summary></details>
<details><summary>Typecheck should detect invalid type annotation &gt;&gt; typechecker should have found the &#x27;InvalidType&#x27; error (program: &#x27;(\x:Nat-&gt;Nut. x 0) (\x:Nat. succ x))&#x27;</summary></details>
<details><summary>Typecheck should detect invalid type annotation &gt;&gt; typechecker should have found the &#x27;InvalidType&#x27; error (program: &#x27;(\x:Nat-&gt;Nat-&gt;Nut. x 0) (\x:Nat. succ x))&#x27;</summary></details>
<details><summary>Typecheck should detect invalid arg type &gt;&gt; typechecker should have found the &#x27;InvalidArgType&#x27; error (program: &#x27;(\x:Nat. succ 0) true)&#x27;</summary></details>
<details><summary>Typecheck should detect invalid arg type &gt;&gt; typechecker should have found the &#x27;InvalidArgType&#x27; error (program: &#x27;(\x:Nat-&gt;Nat.x 0) (\x:Nat. iszero x))&#x27;</summary></details>
<details><summary>Typecheck should detect invalid function type &gt;&gt; typechecker should have found the &#x27;InvalidFunType&#x27; error (program: &#x27;(\x:Nat. x 0) 0)&#x27;</summary></details>
<details><summary>Typecheck should detect invalid function type &gt;&gt; typechecker should have found the &#x27;InvalidFunType&#x27; error (program: &#x27;(iszero 0) 0)&#x27;</summary></details>

-----------
I remain your faithful servant\
_Bobot_