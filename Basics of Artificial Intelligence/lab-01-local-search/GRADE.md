Dear Student,

I'm happy to announce that you've managed to get **42** out of 50 points for this assignment.\
There still exist some issues that should be addressed before the deadline (2021-11-21 22:00:00 GMT). For further details, please refer to the following list:

<details><summary>Kempe chain should have result with no conflicts &gt;&gt; there are still 4 conflicts after kempe chain</summary>	- bad edges: [0, 4, 0, 0, 0, 0, 0, 0, 0]<br>	- state: (0: 1) (1: 0) (2: 0) (3: 0) (4: 1) (5: 1) (6: 1) (7: 1) (8: 2)<br>	- graph: {0: {8, 4, 5}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}</details>
<details><summary>Kempe chain should have result with no conflicts &gt;&gt; there are still 2 conflicts after kempe chain</summary>	- bad edges: [0, 0, 2, 0, 0, 0, 0, 0, 0]<br>	- state: (0: 2) (1: 0) (2: 0) (3: 0) (4: 1) (5: 1) (6: 1) (7: 1) (8: 2)<br>	- graph: {0: {8, 4, 5}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}</details>
<details><summary>Kempe chain should solve direct conflicts &gt;&gt; kempe chain fails to correctly fix direct coloring conflict</summary>	- state: (0: 1) (1: 0) (2: 0) (3: 0) (4: 1) (5: 1) (6: 1) (7: 1) (8: 2)<br>	- graph: {0: {8, 4, 5}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}</details>
<details><summary>Kempe chain should solve direct conflicts &gt;&gt; kempe chain fails to correctly fix direct coloring conflict</summary>	- state: (0: 2) (1: 0) (2: 0) (3: 0) (4: 1) (5: 1) (6: 1) (7: 1) (8: 2)<br>	- graph: {0: {8, 4, 5}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}</details>
<details><summary>Kempe chain should solve indirect conflicts &gt;&gt; kempe chain fails to fix indirect coloring conflicts:</summary>	- state: (0: 1) (1: 0) (2: 0) (3: 0) (4: 1) (5: 1) (6: 1) (7: 1) (8: 2)<br>	- graph: {0: {8, 4, 5}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}</details>
<details><summary>Kempe chain should handle cycles &gt;&gt; kempe chain doesn&#x27;t handle correctly cycles in the graph</summary>	- state: (0: 1) (1: 0) (2: 0) (3: 0) (4: 1) (5: 1) (6: 1) (7: 1) (8: 2)<br>	- graph: {0: {8, 4, 5}, 1: {4, 6}, 2: {4, 5}, 3: {6}, 4: {0, 1, 2}, 5: {0, 2}, 6: {1, 3}, 7: {8}, 8: {0, 7}}</details>

-----------
I remain your faithful servant\
_Bobot_