# Test -- Chapter 6：Support for High-level Programming Languages（含 6.1 fixed-point arithmetic、6.2 inline assembly）

教材來源（本次整合為同一章節視角）：
- `part 21 Chapter 6 Support for high-level programming languages/chapter6_Support_for_high_level_language.pdf`
- `part 21 Chapter 6 Support for high-level programming languages/new_APCS.pdf`
- `part 22 Chapter 6.1 fixed-point arithmetic/chapter6.1_fixpoint_arithmetic.pdf`
- `part 23 Chapter 6.2 Inline assembly codes/chapter6.2_inline_asm.pdf`

作答方式：請直接在每題下方 `> 答：` 後作答；需要畫圖/表格可直接用文字排版。

---

## 一、名詞與觀念（短答）

**1.** 什麼是「Architectural support for High-level language」？請列出教材在 Introduction/Outline 點到的至少 4 個支援面向。（出題範圍：Chapter 6 Introduction/Outline）  
> 答：

---

**2.** 請用一句話分別定義：subroutine / function / procedure。（出題範圍：Functions and procedures - Terminology）  
> 答：

---

**3.** 請說明 arguments 與 parameters 的差異，並用教材的 `func(100,200)` 例子標示哪個是 arguments、哪個是 parameters。（出題範圍：Functions and procedures - Terminology）  
> 答：

---

**4.** 為什麼需要 calling convention？請用「caller 與 callee 可能是不同人寫的」這個情境說明會出現的兩類問題。（出題範圍：Functions and procedures - Situation 1/2, Calling convention）  
> 答：

---

**5.** 什麼是 caller-saved 與 callee-saved？各用一句話說明「誰負責保存、在什麼時機保存/還原」。（出題範圍：Functions and procedures - Situation 2）  
> 答：

---

## 二、資料型別與浮點（概念＋判斷）

**6.** IEEE-754 single precision 的欄位大小（esize/fsize/vsize）各是多少？並寫出教材給的數值公式（含 sign/exponent/fraction）。（出題範圍：Floating-Point Data Types）  
> 答：

---

**7.** IEEE-754 的保留值：請分別寫出「0、±infinity、NaN、denormalized number」在 exponent 與 fraction 的條件。（出題範圍：Reserved Numbers in IEEE 754）  
> 答：

---

**8.** 是非題：denormalized number 的 exponent 為 0，fraction 為 0。對/錯？請說明。（出題範圍：Reserved Numbers in IEEE 754）  
> 答：

---

**9.** 教材提到 Packed Decimal Floating-Point（96 bits）與 Extended Packed Decimal（128 bits）。請寫出它們各自用了幾個 words，並指出 exponent 以什麼方式表示。（出題範圍：IEEE 754 Packed Decimal formats）  
> 答：

---

## 三、Expressions 與 Operand 存取

**10.** 教材說「3 address format is good for compilers」。請解釋這句話可能在編譯器生成碼上帶來的好處（至少 2 點）。（出題範圍：Expressions）  
> 答：

---

**11.** 指標運算題：`int *p; int i=1; p = p + i;` 若 p 在 `r0`、i 在 `r1`，教材給的 ARM 指令是什麼？並解釋為何要 `LSL #2`。（出題範圍：Expressions - Pointer arithmetic）  
> 答：

---

**12.** 請列出教材「Accessing Operands」的 4 種 operand 來源（例如：constant、local、global…）。（出題範圍：Accessing Operands）  
> 答：

---

## 四、Conditional Statements（if / switch）

**13.** 請把下列 if/else 翻成「不使用分支、只用條件 MOV」的版本（依教材示範）：  
```c
if (a > b) c = a;
else       c = b;
```
假設 `a` 在 `r0`、`b` 在 `r1`、`c` 在 `r2`。（出題範圍：Conditional Statements (1)）  
> 答：

---

**14.** 請把下列「complex if..else」翻成分支版本骨架（依教材）：需要出現 `BLE ELSE`、`B ENDIF`、`ELSE:`、`ENDIF:`。  
（出題範圍：Conditional Statements (2)）  
> 答：

---

**15.** switch-case 題：教材先示範「連續 CMP/BEQ」的做法，請說明這種做法在 case 很多時的缺點。（出題範圍：switch…case (2)）  
> 答：

---

**16.** jump table 題：  
1) `DCD`（`.word`）在 jump table 中扮演什麼角色？  
2) `LDRLS pc, [r1, r0, LSL #2]` 這行的效果是什麼？（請用一句話描述控制流程）  
（出題範圍：switch…case (3)）  
> 答：

---

**17.** 教材（backup）提到：若 switch 的條件 x 範圍很大，可以使用 hash function。請用自己的話說明這樣做的目的。（出題範圍：switch…case (4) backup）  
> 答：

---

## 五、Loops（for / while / do…while）

**18.** 教材 for-loop 範例中，請指出「終止條件判斷」與「迴圈回跳」分別是哪兩類指令。（出題範圍：For Loops）  
> 答：

---

**19.** while-loop 題：教材在 While Loops (1) 討論把 branch instruction 移到後面，讓 loop body 較少 branch 干擾。請用 2–3 句話解釋這個改寫想達成的效果。（出題範圍：While Loops (1)）  
> 答：

---

**20.** do…while 與 while 的差異是什麼？請用「至少執行一次」的角度回答，並對照教材的分支位置。（出題範圍：Do…While Loops）  
> 答：

---

## 六、AAPCS/APCS、Stack、Function Entry/Exit

**21.** AAPCS/APCS 的目的：請列出教材在 (AAPCS) (1)/(2) 提到的至少 3 個「規則/定義項目」。（出題範圍：Procedure Call Standard for ARM Architecture）  
> 答：

---

**22.** Stack 題：請分別定義 descending vs ascending、full vs empty，並指出 AAPCS/armclang 使用哪一種 stack。（出題範圍：new_APCS - Stack, AAPCS）  
> 答：

---

**23.** 多重 load/store 與 stack mode：請寫出教材表格中「Full descending」對應的 store/load 指令助記（mnemonic），並說明 PUSH/POP 分別等價於哪個。（出題範圍：new_APCS - Load/Store Multiple Instructions）  
> 答：

---

**24.** BL/LR 題：教材說如果 subroutine 內再呼叫另一個 subroutine，原本的 return address（LR）會被第二次 `BL` 覆寫。請用 2–3 句話說明「問題怎麼發生」與「教材的解法」。（出題範圍：Recall: Branch and Link Instructions）  
> 答：

---

**25.** 請寫出教材給的「保存 LR 與工作暫存器」的典型做法（需包含 `STMFD r13!, {..., r14}` 與 `LDMFD r13!, {..., pc}` 的精神）。（出題範圍：Recall: Branch and Link Instructions (3)）  
> 答：

---

**26.** Function entry 題：教材給的 prologue 片段：  
```asm
MOV  ip, sp
PUSH {fp, ip, lr, pc}
SUB  fp, ip, #4
```
請逐行說明各行的目的。（出題範圍：Function Entry/Exit - new_APCS, Chapter6 slides）  
> 答：

---

**27.** Function exit 題：教材比較 old gcc 與 new gcc 的退出序列。請描述兩者差異，並說明 new gcc 版本為何會出現 `BX lr`。（出題範圍：new_APCS - Function Exit (Old GCC)/(APCS)）  
> 答：

---

**28.** Leaf function 題：教材說 leaf function 可用 `MOV pc, lr` 直接回傳。請解釋「leaf」的含義，以及為何它能有 minimal calling overhead。（出題範圍：Function Entry/Exit (1)）  
> 答：

---

**29.** `-mapcs-frame` 與 `-fomit-frame-pointer` 題：請解釋教材對這兩個選項的描述（各一句話即可）。（出題範圍：Observation - `arm-none-eabi-gcc -S -mapcs-frame`）  
> 答：

---

**30.** Inline function 題：  
1) inline function 為何能加速？  
2) 教材提到 GCC 未最佳化時可能不會 inline，需加什麼 attribute？  
（出題範圍：Inline Function / Inline Function in GCC）  
> 答：

---

## 七、Memory / Alignment / Struct layout

**31.** 請畫出教材「ARM C Program Address Space Model」的區段順序（code/static data/heap/stack/unused），並標示 sp、sl、low-water mark 出現在哪個區域附近。（出題範圍：Use of Memory - Address Space Model）  
> 答：

---

**32.** 對齊題：教材給出 alignment 規則（byte/half-word/word）。請分別寫出它們允許的位址條件。（出題範圍：Memory Issues - alignment）  
> 答：

---

**33.** struct padding 題：請解釋為何 `struct S1 { char c; int x; short s; }` 會產生 padding；並說明教材如何透過調整欄位順序降低浪費。（出題範圍：Normal/Efficient Structure Memory Allocation）  
> 答：

---

**34.** packed struct 題：教材示範 `__packed struct`。請說明 packed 的效果，以及可能帶來的代價（提示：與 alignment 有關）。（出題範圍：Packed Structure Memory Allocation, Memory Issues）  
> 答：

---

**35.** GCC attribute 題：`int x __attribute__ ((aligned (16)));` 這行宣告代表什麼？（出題範圍：Variable Alignment in GCC (1)）  
> 答：

---

## 八、Chapter 6.1 fixed-point arithmetic（計算/轉換）

**36.** fixed-point 的核心想法：教材用「把小數點都點在固定位置」來解釋。請用自己的話說明這句話的意思。（出題範圍：Fixed Point: Idea）  
> 答：

---

**37.** Q format 題：教材說 exponent `e` 通常記為 `q`。請解釋 q 的含義（用一句話即可）。（出題範圍：Fixed Point Arithmetic (3) / Q format）  
> 答：

---

**38.** 轉換題：在教材的例子中，`q = 14` 時，`0x00004000` 代表的十進位值是多少？請寫出你的推導。（出題範圍：Fixed Point Arithmetic (3)）  
> 答：

---

**39.** exponent change 題：請寫出教材給的「從 exponent p 轉成 r」的 mantissa shift 規則（分 `r >= p` 與 `p > r` 兩種）。（出題範圍：Change of Exponent）  
> 答：

---

**40.** 二進位小數點題：教材示範 `a = 0101.0110₂` 與 `a = 010.10110₂`。請說明同一個 bit pattern 改變小數點位置時，十進位值會如何改變。（出題範圍：Example (binary) / Q Format）  
> 答：

---

**41.** 是非題：fixed-point 的加減法只要用 `ADD`/`SUB` 就行，不需要管 exponent。對/錯？請說明。（出題範圍：Addition and Subtraction / Change of Exponent）  
> 答：

---

**42.** 比較題：教材在 Conclusion 說 fixed-point 相較於 software emulation (IEEE-754) 的優缺點是什麼？請各寫 1 點。（出題範圍：Fixed-point Conclusion）  
> 答：

---

## 九、Chapter 6.2 inline assembly（語法/陷阱）

**43.** `asm` 與 `__asm__` 的差異是什麼？教材建議在 `-ansi`/`-std` 編譯選項下用哪一個？為什麼？（出題範圍：GNU Inline Assembly (1)）  
> 答：

---

**44.** 轉義字元題：教材提到 `\\n` 與 `\\t`。它們在 inline asm template 中各代表什麼？（出題範圍：GNU Inline Assembly (2)）  
> 答：

---

**45.** 請寫出 extended asm 的基本格式（四段：template / output / input / clobbered）。（出題範圍：Extended Asm basic format）  
> 答：

---

**46.** constraint 題：教材範例使用 `\"=r\"(b)` 與 `\"r\"(a)`。請解釋 `=r` 與 `r` 分別表示什麼（用一句話即可）。（出題範圍：GNU Inline Assembly (4)）  
> 答：

---

**47.** clobber 題：教材說要告訴 GCC `r1` 會被 asm 修改。若沒有把 `r1` 寫在 clobber list，可能會造成什麼類型的錯誤？（出題範圍：GNU Inline Assembly (4)）  
> 答：

---

**48.** `asm-qualifiers` 題：`volatile` 的用途是什麼？教材列出 GCC optimizer 可能對 asm 做的兩種處理，請各寫 1 個。（出題範圍：asm-qualifiers: volatile）  
> 答：

---

**49.** symbolic name 題：教材說 operand 格式可寫 `[asmSymbolicName] constraint (cvariablename)`。請說明 `asmSymbolicName` 的用途。（出題範圍：Operands format / asmSymbolicName）  
> 答：

---

**50.** `asm goto` 題：  
1) `asm goto` 解決什麼需求？  
2) 為什麼教材說它「implicitly volatile」？  
（出題範圍：Jump to Label Outside the Block / asm goto）  
> 答：

---

**51.** `cc` clobber 題：教材在 `asm goto` 範例把 `cc` 放在 clobbered register。請解釋 `cc` 代表什麼、為何要宣告它被 clobber。（出題範圍：asm goto example）  
> 答：

---
