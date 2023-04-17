Dear Student,

I'm happy to announce that you've managed to get **30** out of 43 points for this assignment.
There still exist some issues that should be addressed before the deadline: **2023-01-26 06:00:00 UTC (+0000)**. For further details, please refer to the following list:

<details><summary>Joint arrow is calculated correctly &gt;&gt; typechecker was looking for &#x27;{b: Bool,n: Nat} -&gt; {b: Bool,n: Nat}&#x27; \/ &#x27;{u: Nat,b: Bool} -&gt; {u: Nat,b: Bool}&#x27;, got exception: NameError(&quot;name &#x27;meet_l&#x27; is not defined&quot;)</summary></details>
<details><summary>Joint arrow defaults to top when there is no arg meet type &gt;&gt; typechecker was looking for &#x27;Unit -&gt; Unit&#x27; \/ &#x27;Nat -&gt; Unit&#x27;, got exception: NameError(&quot;name &#x27;meet_l&#x27; is not defined&quot;)</summary></details>
<details><summary>Joint variant is wide enough &gt;&gt; typechecker was looking for &#x27;&lt;u: Unit,n: Nat&gt;&#x27; \/ &#x27;&lt;u: Unit,b: Bool&gt;&#x27;, got exception: NameError(&quot;name &#x27;F&#x27; is not defined&quot;)</summary></details>
<details><summary>Joint variant handles shared labels &gt;&gt; typechecker was looking for &#x27;&lt;r: {u: Unit,n: Nat}&gt;&#x27; \/ &#x27;&lt;r: {u: Unit,b: Bool}&gt;&#x27;, got exception: NameError(&quot;name &#x27;final_dict&#x27; is not defined&quot;)</summary></details>
<details><summary>Joint variant handles both shared and disjoint labels &gt;&gt; typechecker was looking for &#x27;&lt;r: {u: Unit,n: Nat},n: Nat&gt;&#x27; \/ &#x27;&lt;r: {u: Unit,b: Bool},b: Bool&gt;&#x27;, got exception: NameError(&quot;name &#x27;F&#x27; is not defined&quot;)</summary></details>
<details><summary>Met record is wide enough &gt;&gt; typechecker was looking for &#x27;{u: Unit,n: Nat}&#x27; /\ &#x27;{u: Unit,b: Bool}&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met record handles shared labels &gt;&gt; typechecker was looking for &#x27;{r: {u: Unit,n: Nat}}&#x27; /\ &#x27;{r: {u: Unit,b: Bool}}&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met record handles both shared and disjoint labels &gt;&gt; typechecker was looking for &#x27;{r: {u: Unit,n: Nat},n: Nat}&#x27; /\ &#x27;{r: {u: Unit,b: Bool},b: Bool}&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met record defaults to none if there is no meet type &gt;&gt; typechecker was looking for &#x27;{r: Unit,n: Nat}&#x27; /\ &#x27;{r: Nat,b: Bool}&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met variant is narrow enough &gt;&gt; typechecker was looking for &#x27;&lt;u: Unit,n: Nat&gt;&#x27; /\ &#x27;&lt;u: Unit,b: Bool&gt;&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met variant handles shared labels &gt;&gt; typechecker was looking for &#x27;&lt;r: {u: Unit,n: Nat}&gt;&#x27; /\ &#x27;&lt;r: {u: Unit,b: Bool}&gt;&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met variant handles both shared and disjoint labels &gt;&gt; typechecker was looking for &#x27;&lt;r: {u: Unit,n: Nat},n: Nat&gt;&#x27; /\ &#x27;&lt;r: {u: Unit,b: Bool},b: Bool&gt;&#x27;, got exception: NotImplementedError()</summary></details>
<details><summary>Met variant defaults to none if there is no meet type &gt;&gt; typechecker was looking for &#x27;&lt;r: Unit,n: Nat&gt;&#x27; /\ &#x27;&lt;r: Nat,b: Bool&gt;&#x27;, got exception: NotImplementedError()</summary></details>

-----------
I remain your faithful servant\
_Bobot_