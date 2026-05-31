# Chapter 6：Support for High-level Programming Languages（含 6.1 fixed-point arithmetic、6.2 inline assembly）

教材來源（本次整合為同一章節視角）：
- `part 21 Chapter 6 Support for high-level programming languages/chapter6_Support_for_high_level_language.pdf`
- `part 21 Chapter 6 Support for high-level programming languages/new_APCS.pdf`
- `part 22 Chapter 6.1 fixed-point arithmetic/chapter6.1_fixpoint_arithmetic.pdf`
- `part 23 Chapter 6.2 Inline assembly codes/chapter6.2_inline_asm.pdf`

---

## Summary（考點總結）
- 高階語言（High-level language）對架構的需求：資料型別、運算（expressions）、控制流程（if/switch/loops）、函式呼叫（calling convention）、記憶體使用（stack/heap/alignment）、run-time environment。
- ARM 指令/架構支援編譯器產生碼的關鍵：3-address format、位移配合位址計算（pointer arithmetic / array index scaling）、條件碼配合條件執行、分支＋跳躍表（jump table）。
- IEEE-754 浮點：single/double 格式、保留值（0/±∞/NaN/denormalized）是常考名詞與判斷題。
- 呼叫慣例（AAPCS/APCS）是「不同人/不同編譯器」可互相呼叫與 link 的前提：參數/回傳值規則、caller-saved vs callee-saved、stack frame/backtrace、stack 模式（full/empty、ascending/descending）。
- 記憶體：ARM C compiler 會做對齊（alignment），struct 會有 padding；`__attribute__((aligned(n)))` / `packed` 會直接改 layout（考題常要你畫出位址配置）。
- 6.1 fixed-point：用整數指令模擬小數（固定小數點），核心是 Q format（q=小數位數）與 shift 對齊 exponent；速度快於純軟體 IEEE-754 emulation，但精度/表示範圍受限。
- 6.2 inline asm：GNU extended asm 語法、constraint、clobber、`volatile`、`asm goto` 是常考「能不能寫對」的細節題。

---

## Outline（章節結構 / 出題順序）
1. Abstraction in software design
2. Data types
3. Floating-point data types（IEEE-754）
4. Expressions（3-address、pointer arithmetic、operand 存取位置）
5. Conditional statements（if/else、switch/case、jump table、DCD）
6. Loops（for / while / do…while 的典型翻譯）
7. Functions and procedures
   - Terminology：subroutine / function / procedure、arguments vs parameters
   - 為何需要 calling convention（不同人寫 caller/callee）
   - AAPCS/APCS：register use、argument passing、result return
   - BL / LR 被覆寫問題與解法（用 stack 保存）
   - Function entry/exit（含 new/old GCC 差異）
   - Tail continued functions、inline function（`always_inline`）
8. Use of Memory
   - ARM C program address space model（code/static/heap/stack）
   - stack 行為（呼叫深度 vs stack size）
   - alignment / padding / packed / `__attribute__`
9. Run-time environment
   - toolchain / ANSI C library 與 embedded 的限制
   - minimal run-time library：除法、stack-limit check、crt0、`_exit()`
10. Chapter 6.1 fixed-point arithmetic
11. Chapter 6.2 inline assembly codes

---

## 關鍵名詞表（關鍵名詞＋一句話考試定義）
| 名詞 | 一句話定義（考試可寫） |
|---|---|
| High-level language | 用較高抽象描述程式，編譯器負責把型別/運算/控制流程/呼叫等需求映射到機器指令與記憶體模型。 |
| Assembly-level abstraction | 直接以指令、暫存器、位址等低階元素描述程式，需自行處理呼叫、保存暫存器、資料布局等細節。 |
| ASCII | 字元編碼；ARM 對 char 的支援通常靠 byte load/store 指令。 |
| Endianness | 多位元組資料在記憶體的位元組順序；教材提到 little-endian / big-endian。 |
| IEEE-754 | 浮點表示標準，以 sign/exponent/fraction 欄位表示 single/double 等格式。 |
| Sign / Exponent / Fraction | IEEE-754 的三個欄位：符號、指數、尾數（fraction/mantissa）。 |
| Single precision | IEEE-754 單精度：vsize=32、esize=8、fsize=23。 |
| Double precision | IEEE-754 雙精度：vsize=64、esize=11、fsize=52。 |
| NaN (Not a Number) | exponent=最大值且 fraction 非 0 的 IEEE-754 保留值，用於表示非數值結果。 |
| Infinity | exponent=最大值且 fraction=0 的 IEEE-754 保留值（±∞）。 |
| Denormalized number | exponent=0 且 fraction 非 0 的 IEEE-754 表示，用於極小數值（無法 normalize）。 |
| 3-address format | 指令格式利於編譯器做暫存器配置與運算排程（教材：對 compilers 友善）。 |
| Pointer arithmetic | 指標加上索引時需依元素大小做 scaling（例：int 索引用 `LSL #2`）。 |
| Literal pool | 常數在程式碼附近的常數池；教材列為 operand 來源之一。 |
| Local variable (stack) | 區域變數常配置在 stack 上，透過 sp/fp 相對位址存取。 |
| Static area (global) | 全域/靜態資料配置在 static data 區，程式啟動時已存在。 |
| Conditional execution | ARM 可用條件碼搭配條件指令（例：`MOVGT`/`MOVLE`）減少分支。 |
| CMP | 透過比較設定 condition codes，供後續條件分支/條件指令使用。 |
| switch/case | 多分支選擇結構；可用連續比較分支或 jump table 加速。 |
| Jump table | 以表格存放目標位址（例如 `DCD method_i`），用索引做間接跳轉。 |
| DCD / .word | 組譯器 directive：保留一個 word 並以指定 expression 初始化（可用來做 jump table）。 |
| for / while / do…while | 三種 loop-control 結構；教材示範其典型 ARM 分支翻譯模板。 |
| Subroutine | 泛稱被高層 routine 呼叫的程式片段（教材 terminology）。 |
| Function | 會回傳值的 subroutine（例：`c = max(a,b)`）。 |
| Procedure | 執行某操作但不以「函式名回傳值」的 subroutine（例：`printf(...)`）。 |
| Arguments | 呼叫端傳入的運算式/值（教材：passed to a function call）。 |
| Parameters | 被呼叫端接收的值（教材：received by the function）。 |
| Calling convention | 事先約定參數/回傳值/暫存器保存/stack 使用方式，讓不同人/不同工具產生的程式可互相呼叫。 |
| Caller-saved | 若 caller 在呼叫後仍要用某暫存器舊值，caller 必須在呼叫前自行保存並在回來後還原。 |
| Callee-saved | callee 若要使用某些暫存器，需自行保存並在 return 前還原，保證 caller 看到的值不變。 |
| AAPCS / APCS | ARM Procedure Call Standard；定義 register 使用、stack 模式、backtrace frame、參數/回傳值傳遞等規則。 |
| Full / Empty stack | sp 指向「最後一個項目」（full）或「下一個空位」（empty）的定義。 |
| Descending / Ascending stack | stack 往低位址成長（descending）或往高位址成長（ascending）的定義。 |
| Full descending stack | AAPCS/armclang 使用的 stack 模式；PUSH/POP 指令也假設此模式。 |
| PUSH / POP | 在 full descending stack 下，PUSH 等價於 `STMDB/STMFD`；POP 等價於 `LDMIA/LDMFD`（教材表格）。 |
| STMFD / LDMFD | Store/Load multiple 指令的 stack 用法（full descending 對應）。 |
| LR (link register) | `BL` 會把 return address 寫入 LR；若 subroutine 再呼叫別的 subroutine，需先保存 LR。 |
| BL (branch and link) | 呼叫子程序的分支指令，會覆寫 LR；教材示範保存/還原 LR 的必要性。 |
| Stack frame | 每個 function 在 stack 上的配置（含保存的暫存器/返回資訊/區域變數），可用於 backtrace。 |
| Frame pointer (fp) | 指向目前 function 的 stack frame（教材：fp points to backtrace structure）。 |
| Tail continued functions | 編譯器讓程式「直接從被接續的函式 return」，避免額外 return/跳轉開銷（教材用語）。 |
| Inline function | 把呼叫展開成程式碼，消除 function-call overhead；GCC 可用 `always_inline` 強制。 |
| `__attribute__((always_inline))` | GCC 在未開最佳化時也可用此屬性促使 inline（教材說明）。 |
| Address space model | 標準 ARM C 程式位址空間：code/static/heap/stack（含 sp、sl、low-water mark）。 |
| Heap | 動態配置區（位於 static data 與 stack 之間，通常往上成長）。 |
| Stack | 呼叫/區域變數等使用的記憶體區，與呼叫深度相關。 |
| Alignment | 對齊：byte/half-word/word 的位址對齊規則；非對齊存取通常較低效。 |
| Padding | struct 欄位之間為了 alignment 插入的空洞；可透過重排欄位降低浪費。 |
| `__packed` / `packed` | 強制 struct 欄位緊密排列（可能造成非對齊存取）。 |
| `__attribute__((aligned(n)))` | 指定變數或欄位的對齊邊界（例：`aligned(16)`）。 |
| Run-time environment | 程式執行所需的工具/函式庫/啟動與終止流程；embedded 通常只有 minimal 版本。 |
| crt0 | 程式啟動碼：初始化 stack/heap 後呼叫 `main`（教材提到 initialization）。 |
| `_exit()` | 程式終止流程的一部分：flush/close streams、移除暫存檔並回到控制端（教材列點）。 |
| Fixed-point | 用整數儲存 mantissa，假設 exponent（q）在編譯期固定，透過 shift 對齊小數點來運算。 |
| Q format / q | fixed-point 常用記法：q 表示小數位數（fraction bits），值可視為 mantissa 經 2 的冪縮放。 |
| Exponent change (shift) | fixed-point 改變 q：`n << (r-p)` 或 `n >> (p-r)` 來對齊 exponent。 |
| Software emulation (IEEE-754) | 無硬體浮點支援時以軟體模擬 IEEE-754；相對 fixed-point 通常較慢。 |
| Inline assembly | 在 C 程式中嵌入組合語言；GNU 提供 `asm`/`__asm__` 與 extended asm。 |
| Extended asm | `asm ( template : outputs : inputs : clobbers )`；可把 C 變數與暫存器/指令串接。 |
| Constraint | extended asm 的 placement 限制字串（例：`"r"` 表示放在 register）。 |
| Clobber list | 告訴 GCC 哪些暫存器（或 `cc`）會被 asm 修改，避免 GCC 錯誤重用。 |
| `asm volatile` | 防止 GCC 因「看似無用」而刪除或搬移 asm（教材：避免被 discard / moved）。 |
| `asm goto` | 允許 asm 跳到 C labels；此語句隱含 volatile（教材）。 |
| `cc` clobber | 宣告 asm 會改變 condition codes，避免 GCC 用錯旗標結果（教材在 asm goto 範例）。 |

---

## 使用提醒
- 看到「if/switch/loop」題：先畫出控制流程，再對照教材模板（`CMP`＋條件分支、jump table 的 `DCD`＋間接跳轉、for/while/do-while 的典型結構）。
- 看到「呼叫/保存暫存器」題：先判斷 caller-saved vs callee-saved 的責任歸屬，再寫出對應的 PUSH/POP（或 STM/LDM）與 LR 保存。
- 看到「alignment/struct」題：用 byte address 逐格畫出 padding；再用欄位重排或 `packed/aligned` 說明差異與代價。
- 看到「fixed-point」題：先鎖定 q（小數位數）與縮放因子，再用 shift 做 exponent 對齊後才加減。
- 看到「inline asm」題：一定要寫完整 extended asm 四段（template/outputs/inputs/clobbers），並明確列出會被改到的暫存器與 `cc`。 

