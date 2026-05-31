以下是 Chapter 3（ARM 組合語言 + 工具鏈）的考試向題目。請直接在題目下方作答；每題末尾皆標示出題範圍。

---

# 一、填空題（概念與語法必背）

**1.** ARM 屬於 ____ load-store ____（架構），因此只有 ____ LDR _____ / ___ STR _____ 類指令能直接存取記憶體。  
【範圍：3 ARM ISA — Introduction / load-store】  


【批改】OK

**2.** 下列四個「只更新 CPSR、但不寫回運算結果」的比較/測試指令為：____ CMP ____、___ CMN _____、___ TST _____、__ TEQ ______。  
【範圍：3 ARM ISA — Comparison Operations / CPSR】  


【批改】OK

**3.** `BIC r0, r1, r2` 的語意可寫成：`r0 := r1 AND (___ NOT _____ r2)`；`BIC` 的全名是 ___ Bit Clear _____。  
【範圍：3 ARM ISA — Bit-wise Logical Operations / BIC】  


【批改】OK

**4.** 若希望資料處理指令同時更新 N/Z/C/V，通常在 opcode 後加上字母 ___ 'S' _____（代表 ___S suuffix, 條件運算 _____）。  
【範圍：3 ARM ISA — Setting the Condition Codes】  


【批改】NG
【正解】加 `S` 代表 **Set condition codes**：此指令會依運算結果更新 CPSR 的 N/Z/C/V。
【解析】「條件執行/條件分支」是用 `{cond}`（例如 `ADDEQ`、`BNE`）去讀 CPSR 來決定要不要執行；`S` 是決定「要不要寫 flags」。

**5.** `ADC` 的 carry-in 取自 CPSR 的 ____ C 不確定  ____ 位元（bit）。  
【範圍：3 ARM ISA — Arithmetic Operations / CPSR】  


【批改】NG
【正解】`ADC` 的 carry-in 取自 CPSR 的 **C flag（bit 29）**。
【解析】CPSR 旗標位元常見排列：N(bit31)、Z(bit30)、C(bit29)、V(bit28)。

**6.** `ADD r3, r2, r1, LSL #3` 可解讀成：`r3 := r2 + ___ 8 _____ * r1`。  
【範圍：3 ARM ISA — Shifted Register Operands】  


【批改】OK

**7.** ELF 常見三段：`.text` 放 ___ code, 程式, instruction  _____，`.data` 放 ____ 已初始化 ____ 全域變數，`.bss` 放 ___ 未初始化 _____ 全域變數。  
【範圍：3.1 GAS — Object File Format / segments】  

這題不確定  
問題: 那 dynamic allocation，例如 C 中的 malloc ，會在載入時被分配，還是執行時從 bss 取哪個 symbol，再從 memory 中(某一塊 VMA 中)分配?



【批改】OK
【回覆】`malloc`/dynamic allocation 走的是 **heap（堆）**：通常是「程式執行時」由 runtime（例如 newlib）用一段可用 RAM 來做配置，不是從 `.bss` 取某個既有 symbol 直接“分配”。
- `.bss`：**靜態（static）未初始化全域/靜態變數**，載入時只要保留空間並清 0。
- heap：**動態配置**，通常由 linker script/`crt0` 先劃出 heap 範圍（例如 `_end` 後面到 stack 之前），再由 `malloc` 管理。

**8.** GAS 中 `.global main` 的目的，是讓 symbol `main` 對 ___ linker _____ 可見；`.type main,%function` 則把 `main` 標記成 ___ function _____。  
【範圍：3.1 GAS — Basic Format / directives】  


【批改】OK

**9.** Linker script 中，VMA 是 section 的「____ 執行 ____ 位址」，LMA 是 section 的「____ 載入____ 位址」。  
【範圍：3.2 Linker script — VMA/LMA】  


【批改】OK

**10.** 在 GNU ARM assembler，`NOP` 目前會被展開成 ___ MOV r0, r0 _____（一條合法且不做事的 ARM 指令）。  
【範圍：3.6 Pseudo instruction — NOP】  

【批改】OK


---

# 二、是非題（對/錯＋理由）

**11.** `LDR r0, =0x12345678` 一定會產生一條真正的 `LDR` 指令（不會產生 literal pool）。  
（對 / 錯，請說明「何時會改用 MOV/MVN、何時會用 literal pool」。）  
【範圍：3.6 Pseudo instruction — `LDR Rd,=constant` / literal pool】  

錯；  
如果後面的立即數可以直接寫入，就會產生 MOV r0, #(some_immediate_number)；  
如果後面的立即數不能直接載入\，才會先在 literal pool 中用一個 symbol 儲存對應的數字，例如:  
`x: .word (number_to_load)`  
，然後再將這個 symbol 在 VMA 時的位置，load 到 register 中，像是:  
`MOV ro, [x]`  


【批改】NG
【正解】（錯）`LDR r0, =0x12345678` **不一定**生成真正的 `LDR`；assembler 會依常數能否被「ARM immediate encoding」表示來選展開方式。
【解析】
- **可編碼立即數** → 展開成 `MOV/MVN`（一條指令，不用 literal pool）。
- **不可編碼立即數** → 生成 `ldr r0, [pc, #offset]` 並在附近放 `.word 0x12345678`（literal pool）。
你寫的方向對（MOV/MVN vs literal pool），但例子 `MOV r0, [x]` 不是正確形式；literal pool 典型是 **PC-relative LDR**。

**12.** `ADR` 可以用來取得「任意 section」內的 label 位址，因此適合跨 `.text` / `.data` 取址。  
（對 / 錯，請說明限制。）  
【範圍：3.6 Pseudo instruction — ADR 限制】  

不知道；ADR是啥小???  


【批改】NG
【正解】（錯）`ADR` 不是「任意 section 取址」。它是 **PC-relative 取址** 的 pseudo，通常只能在「同一 section/同一段程式碼附近」使用，且有可達範圍限制。
【解析】超出範圍時常用 `ADRL`（兩條指令擴範圍）或 `LDR Rd, =label`（走 literal pool/relocation）。

**13.** 巨集（macro）是在程式執行時才被呼叫並展開，因此不會增加可執行檔大小。  
（對 / 錯，請說明展開時機與後果。）  
【範圍：3.3 GAS Macro — preprocessing expansion】  

錯；  
macro 會在 link 的時候被展開成原始定義的樣子，因此呼叫越多次，有可能就會占用越多執行檔空間，等同於 重複的 instruction 寫很多次，只是在撰寫上比較方便。


【批改】NG
【正解】（錯）macro 是 **組譯（assembler/preprocess）階段**展開，不是執行期。
【解析】因此呼叫越多次＝展開後指令越多＝可執行檔可能更大（本質是 inline 展開）。你把「展開時機」寫成 link time，這點不對。

**14.** `.bss` 屬於 allocatable section：執行時需要保留空間，但不一定有需要「從檔案載入的內容」。  
（對 / 錯，請說明。）  
【範圍：3.2 Linker script — loadable vs allocatable；3.1 GAS — segments】  

不知道；這在哪一段 allocatable section 是什麼?


【批改】NG
【正解】（對）`.bss` 通常是 **allocatable**（執行時要佔 RAM 空間）但 **不需要從檔案載入內容**（no load image），常由 loader/startup code 清 0。
【解析】所以它符合「執行時要空間、但檔案中不必存初始化內容」這句話。

**15.** ARM 的 SWI 例外在向量表（vector table）對應位址為 `0x08`。  
（對 / 錯，請說明這個位址在圖中扮演的角色。）  
【範圍：3.5 SWI — Vector table / SWI handler】

不知道； 我超爛 我不會寫  


【批改】NG
【正解】（對）SWI/SVC 例外向量在 **0x08**。
【解析】向量表是「例外入口跳板」：發生 SWI 時 CPU 取向量表對應項目（0x08），跳到 handler（或先跳到一段分派碼）。

**16.** semihosting 的核心精神是：target 沒有完整 I/O 能力時，由 debugger/host OS 代辦 I/O，完成後 target 會從 semihosting SWI 的下一條指令繼續執行。  
（對 / 錯，請說明流程。）  
【範圍：3.5 SWI — Semihosting concept / implementation overview】  

不知道； 我超爛 我不會寫  


【批改】NG
【正解】（對）semihosting 是：target 透過 SWI/SVC 把 I/O 請求交給 debugger/host 代辦；服務完成後回到 SWI 的下一條繼續。
【解析】流程（概念版）：設定 reason code/參數 → `swi` 觸發 → debugger 截獲並在 host 做事 → 回傳結果（常見在 `r0`）→ target 繼續執行。

**17.** 在 WSL2 上跑 Linux GUI，仍然必須額外安裝 X server 並手動設定 `DISPLAY`。  
（對 / 錯，請說明 WSL1/WSL2 的差異。）  
【範圍：WSL/X — WSL1 vs WSL2 GUI】  

不知道； 我超爛 我不會寫  


【批改】NG
【正解】（錯，以教材筆記）在 **WSL2 + WSLg**（Windows 11 或符合版本條件）下通常不需要額外 X server，也不需要手動設 `DISPLAY`。
【解析】
- WSL1：常見要外部 X server + `DISPLAY` + `xhost`。
- WSL2：若沒有 WSLg（舊環境/設定），仍可能需要外部 X server；但教材此題在對比 WSLg 時，答案是「不必」。

**18.** ARM `B {L} {cond} <expression>` 是 PC-relative branch；教材指出其可達範圍約為 `+/- 32 Mbytes`。  
（對 / 錯，請說明「為什麼 PC-relative 有助於 PIC」。）  
【範圍：3.8 PIC — Branch range / PC-relative】  

不知道； 我超爛 我不會寫  

【批改】NG
【正解】（對）`B {L} {cond} <expr>` 是 **PC-relative branch**，可達範圍約 +/- 32MB（ARM state）。
【解析】PC-relative 只依賴「相對位移」，程式搬家（relocate）後 offset 不變，因此比絕對位址跳躍更有利於 PIC。


---

# 三、簡答題（考試可直接寫）

**19.** CPSR 的 N/Z/C/V 分別代表什麼？請描述「哪些指令會更新它」以及「它在條件分支/條件執行中的用途」。  
【範圍：3 ARM ISA — CPSR / Setting condition codes / Branch conditions】  

N: Negative, Z: Zero, C: Carry, V: Overflow.  
最常見是 TST, TEQ, CMP, CMN 會更新他，其他條件執行的、在結尾加上 s suffix 的 也會更新 CPSR。  
在條件分支中的用途是，可以讓 Branch 家族，根據 CPSR 判斷是否要 branch。  


【批改】OK

**20.** 說明 `CMP` 與 `TST` 的差別：它們各自以什麼運算更新 CPSR？為什麼不把結果寫回暫存器？  
【範圍：3 ARM ISA — Comparison Operations】  

乾我不知道他們的差別是什麼 好像有問過但是忘記了 我是大便。  
不把結果寫回 register 是因為他們的功用就是用來更新 CPSR 的，已經有一個地方記錄這些結果了，不需要額外浪費一個 register 來記錄結果。  


【批改】NG
【正解】
- `CMP Rn, Op2`：做 **減法比較**（概念上 `Rn - Op2`）只更新 CPSR。
- `TST Rn, Op2`：做 **AND 測試**（概念上 `Rn AND Op2`）只更新 CPSR。
【解析】這兩類指令的目的就是「設 flags 供條件分支/條件執行使用」，不把結果寫回可避免破壞暫存器內容。

**21.** 什麼是 shifted register operand？請用一句話說明它的好處，並以 `LSR` 與 `ASR` 的差異舉例（包含「補 0/補符號」）。  
【範圍：3 ARM ISA — Shifted register operands / LSR vs ASR】  

shift 就是在 bitwise 上進行左右位移，好處是乘法在硬體計算上會比較慢，但是如果一個乘法可以被拆分成多個 2的某個次方相加，那每個部份就可以透過 0x0001 平移得到，而 shift 在硬體上是比直接進行 MUL 來快得很多的；
在進行向右平移的時候， LSR (Logical Shift Right) 跟 ASR (Arthimetic Shift Right) 在 signed bit 會需要做不一樣的操作，LSR 就是無論如何都在左邊補 0， ASR 會保留 signed bit，接著才在 signed bit 右邊補0。


【批改】OK

**22.** 請解釋 base+offset addressing 與 write-back（`!` 或 post-index）的概念，並說明 pre-index / post-index / auto-index 在「位址更新時機」上的差異。  
【範圍：3 ARM ISA — Addressing mode / Base-plus-offset；Self Assessment #1】  

不確定 這題請幫我指出在哪個範圍 我複習一下 我有個大概印象 大概七成把握；  

base + offset 是指透過 register 加上位移，去取得記憶體中儲存的值，例如 `LDR r0, [r1, #1]`，將 [r1 + 1] 位置的 value 存入到 r0 中；  
write-back 是指說，在 addressing 完成後，更新 base register 的值，例如 `LDR r0, [r1, #1]!`，效果等同於前者，然後再 `r1 = r1 + 1`  

問題:  
`LDR r0, [r1, #1]` 是取得 [r1 + 1] 位置的 value，存到 r0 中嗎?  
[r1 + 1] 的單位是什麼? +1 bit? +1 byte? 還是 +1 word?  


【批改】NG
【正解】
- base+offset：以基底暫存器 `Rn` 加上 offset 形成有效位址（EA）。
- pre-index：`[Rn, #off]` 用 **Rn+off** 當 EA；若寫 `!`（write-back）則 **Rn := Rn+off**。
- post-index：`[Rn], #off` 用 **Rn** 當 EA，存取完才做 **Rn := Rn+off**。
- auto-index：常指「有 write-back 的 indexed addressing」（教材常把它視為 pre-index + `!` 這類）。
【回覆】`LDR r0, [r1, #1]` 的 `#1` 單位是 **byte（位址位移）**，也就是 EA = r1 + 1。
- 若你要以 word 為單位通常會用 `#4`、`#8`…（且部分系統對未對齊 word 存取有限制/會慢）。

**23.** 教材給出 block copy 範例：`LDMIA r9!, {r0-r7}` 搭配 `STMIA r10!, {r0-r7}` 與 `CMP/BNE`。請逐行說明 r9、r10、r11 的角色，以及為何 `!` 對迴圈很重要。  
【範圍：3 ARM ISA — Multiple Register Load/Store / Application】  

不知道； 我超爛 我不會寫  
我記得這個地方好像很重要，好像跟 function 的 call return 有關，但我忘記了  
r9, r10, r11 好像通常有固定的功用 但我也忘記了  


【批改】NG
【正解】（依教材 block copy 常見寫法）
- `LDMIA r9!, {r0-r7}`：從 **r9 指向的來源記憶體** 連續載入 8 個 word 到 r0~r7；`IA` = increment after；`!` 讓 **r9 += 8*4**。
- `STMIA r10!, {r0-r7}`：把 r0~r7 連續存到 **r10 指向的目的記憶體**；`!` 讓 **r10 += 8*4**。
- `CMP/BNE`：通常用 `CMP r9, r11` 搭配 `BNE loop`，其中 **r11 是來源結束位址（end pointer）或迴圈終止門檻**。
【解析】`!` 很重要，因為它把「指標前進」內建在同一條 LDM/STM；沒有 `!` 指標不動，迴圈會一直複製同一段資料（或卡住）。

**24.** 寫出一個最小 GAS 程式骨架（只需列出必要 directives 與 `main:` label 的那幾行），並逐項說明 `.section/.global/.type/.end` 的作用。  
【範圍：3.1 GAS — Basic Format (1)~(4)】  

不知道； 我超爛 我不會寫  


【批改】NG
【正解】（最小骨架示例）
```asm
.section .text
.global main
.type main, %function
main:
    @ ...
.end
```
【解析】
- `.section`：指定後續放哪個 section（如 `.text`）。
- `.global`：讓 symbol 對 linker 可見。
- `.type`：標記 symbol 型態（function/object）。
- `.end`：標記組譯檔結束。

**25.** Linker script 的 `SECTIONS` 與 `MEMORY` 分別在控制什麼？`AT(...)` 的意義是什麼？請用「把 `.text` 放 ROM、把 `.data` 放 RAM」的情境描述 VMA/LMA 可能不同的原因。  
【範圍：3.2 Linker script — SECTIONS/MEMORY/AT、VMA/LMA】  

不知道； 我超爛 我不會寫  
這是在哪一段 感覺我好像不熟


【批改】NG
【正解】
- `MEMORY`：定義可用記憶體區域（名稱、ORIGIN、LENGTH、權限如 `rx/rw`）。
- `SECTIONS`：把 input sections 對映到 output sections，並決定各 section 的 **VMA（執行位址）**。
- `AT(...)`：指定 **LMA（載入映像位址）**，常用在「VMA 在 RAM 但初始化內容放在 ROM」的情境。
【解析】例：`.text` 常常 **VMA=LMA=ROM**（直接在 ROM 執行）；`.data` 常見 **VMA=RAM、LMA=ROM**（開機時由 `crt0` 從 ROM 複製到 RAM 才能以 RAM 位址被程式使用）。

**26.** `crt0.o`（startup code）在呼叫 `main` 前通常會做哪些事？請列至少 5 項，並說明其中「ROM→RAM 複製初始化資料」為何必要。  
【範圍：3.2 Linker script & crt0 — The Executable File / Startup code】  

不知道； 我超爛 我不會寫  


【批改】NG
【正解】`crt0.o` 在呼叫 `main` 前常見工作（列任意 5 項即可）：
1) 設定 stack pointer（SP）
2) 清零 `.bss`
3) 把 `.data` 從 ROM(LMA) 複製到 RAM(VMA)
4) 設定 heap 邊界/初始化 `sbrk` 支援
5) 初始化 C runtime（如呼叫 constructors、準備 libc/newlib）
6) 設定向量/關中斷（依平台）
7) 最後 `bl main`，並處理 `exit`
【解析】ROM→RAM 複製必要：程式在執行時會用 `.data` 的 **RAM 位址（VMA）**取資料；若不先把初始化值從 ROM 映像搬到 RAM，那些全域變數初值就不會正確。

**27.** `LDR Rd, =label` 與 `LDR Rd, =constant` 在教材中的用途分別是什麼？請描述它們與「跨 section 取址」與「常數載入」的關係。  
【範圍：3.6 Pseudo instruction — `LDR Rd,=label/constant`】  

很不確定 請告訴我這是在哪一段QQQ。  

`LDR Rd, =label` 是自己要先在 .data 中，宣告某個 label x，他所占用的空間、以及值是多少，這個空間會在執行時分配，並被 LDR 將他的 address 複製給 Rd；
`LDR Rd, =constant` 是方便載入常數的寫法，如果常數是可以直接載入的立即數會轉換成對應的 MOV 指令，如果不是會在 literal pool 中宣告對應的空間儲存這個常數，並且同樣在執行時、將其對應的 address 複製給 Rd。


【批改】NG
【正解】
- `LDR Rd, =label`：把 **label 的位址（address）**放進 `Rd`（常用於跨 section 取址/取得全域物件位址）。
- `LDR Rd, =constant`：把 **常數值**放進 `Rd`（可展開成 `MOV/MVN` 或 literal pool 的 PC-relative `LDR`）。
【解析】你把 `=label` 寫成「先在 .data 宣告值再把 address 複製給 Rd」的方向不精確：重點是 **拿到 label 的位址**，label 本身可以在 `.text/.data/...`。

**28.** `ADR` 與 `ADRL` 的差別是什麼？教材提到它們分別會展開成幾條指令？若超過 `ADR` 的範圍，組譯器可能出現什麼類型的錯誤訊息（描述即可）。  
【範圍：3.6 Pseudo instruction — ADR/ADRL / range limit】  

不知道； 我超爛 我不會寫  
ADR 是什麼鬼 忘光光 我知道 pdf 是我破大防  


【批改】NG
【正解】
- `ADR`：取得附近 label 位址，通常展開成 **1 條** `ADD/SUB`。
- `ADRL`：為了更大可達範圍，展開成 **2 條** 指令。
【解析】若 label 超出 `ADR` 可達範圍，assembler 會報類似「offset out of range / relocation truncated / fixup out of range」這種範圍錯誤（描述即可）。

**29.** `.macro swap arg1,arg2` 的 swap 範例為何「看起來像函式」但本質上不同？請說明：展開時機、展開後指令數量、以及 `r1` 作為暫存帶來的副作用。  
【範圍：3.3 GAS Macro — swap example / expansion】  

在定義完成 swap 之後，可以用 `swap rA, rB` 來交換兩個 register 的值，看起來很像某種 function。  
實際上，他會在 link 時被展開成原始的定義 macro 時的樣子，也就是利用 macro 來撰寫指令，只會讓撰寫比較方便，不會減少實際執行的指令數量，在展開後看起來指令數量可能會比未展開前更多或相等。  
  
如果利用 r1 作為暫存，副作用是在使用這個 macro 時，要確認 r1 裡面沒有儲存有意義的值，否則會因為 macro 的展開，在 swap 的過程中被覆寫。  


【批改】NG
【正解】你的「指令數會變多、`r1` 暫存會覆寫」這些點是對的；但 **展開時機**應是組譯階段（macro expansion），不是 link time。
【解析】所以它“像函式”只是因為呼叫語法像，本質仍是 inline 展開的文字替換。

**30.** 請寫出一段最小的 GDB command-line 操作流程：載入 `a.out`、連到 simulator、`load` 程式、下斷點、執行、查看暫存器、dump 一段記憶體，最後退出。  
（只需列出指令序列即可。）  
【範圍：3.4 GDB command-line mode；3.1 GAS — GDB & ARM Emulator】  

不知道； 我超爛 我不會寫  


【批改】NG
【正解】（最小 command-line 範例，指令序列即可）
```gdb
file a.out
target sim
load
break main
run
info registers
x/16wx 0x00000000
quit
```
【解析】若是連 remote target，`target sim` 會換成 `target remote <host:port>`；重點是：先載入檔案與目標、再 `load`、下斷點、執行、觀察暫存器/記憶體。

**31.** semihosting 的「輸出字元」示例中，教材使用 `mov r0, #0x3`、`ldr r1, .char`、`swi 0x123456`。請解釋 r0/r1 各代表什麼意義，`swi 0x123456` 觸發了什麼類型的服務，以及返回值大概會落在哪個暫存器。  
【範圍：3.5 SWI — Semihosting on GNU Newlib / Example 1: Print a character】  

不知道； 我超爛 我不會寫  
semihosting 是什麼 我好像沒有讀到 swi 那邊 我是大便。  


【批改】NG
【正解】（教材 semihosting WriteC 類型）
- `r0 = 0x3`：reason code（例如 WriteC：輸出 1 個字元）
- `r1 = &char`：參數，指向要輸出的字元/字串位置
- `swi 0x123456`：觸發 semihosting 服務（由 debugger/host 代辦 I/O）
- 回傳值：常見放在 `r0`（成功/錯誤碼依服務而定）
【解析】這題重點是「r0 放服務代號、r1 放參數指標、swi 觸發 host 服務」。

**32.** 請用 PIC/PID 的觀點說明：為何「絕對位址的跳躍/取址」會造成 position dependent？教材如何用 PC-relative branch（offset）與 base+offset（以 r5 為 base）解決？  
【範圍：3.8 Position Independent Code/Data — PC-relative & base+offset】  

不知道； 我超爛 我不會寫  
這題完全看不懂 看來是這部分完全沒讀到 可能要加強  


【批改】NG
【正解】
- 絕對位址（例如把某個固定 address 塞進暫存器再跳/取址）會把程式綁死在特定位址，搬家就壞 → position dependent。
- PIC 作法：用 **PC-relative branch（offset）**，跳躍只依賴相對位移。
- PID/data 作法：用 **base register（例 r5）+ offset**，把「資料區基底」在執行時決定，再用 offset 取資料。
【解析】教材 pseudo code 類似：先算 `addr = r5 + offset`，再 `ldr` 取值。

**33.** WSL1 想在 Windows 上顯示 Linux GUI（例如 insight）時，需要做哪些設定？請至少寫出：X server 安裝方向、`DISPLAY` 的設定方式、`xhost` 的用途；並對照 WSL2（WSLg）為何通常不需要這些設定與其前提條件。  
【範圍：WSL/X — WSL1/WSL2】  

不知道； 我超爛 我不會寫  


【批改】NG
【正解】
- WSL1：Windows 端裝 X server（如 VcXsrv/Xming）；在 WSL 設 `DISPLAY=<Windows IP>:0`；必要時用 `xhost +`（或更安全地授權特定來源）讓 WSL 可連線顯示。
- WSL2（WSLg）：在符合版本/驅動的情況下，GUI 走 WSLg 整合，通常不必自行裝 X server 或設 `DISPLAY`。
【解析】考點是「WSL1/WSL2 的 GUI 管線不同」與 `DISPLAY/xhost` 的用途。

**34.** 請比較兩個教材提到的 ARM 模擬器/emu（例如 CPUlator、ARMSim、VisUAL、Graphical-Micro-Architecture-Simulator）：各自的支援架構版本/特色、適合用來驗證哪一類練習。  
【範圍：ARM Simulator】  

不知道； 我超爛 我不會寫  

【批改】NG
【正解】（舉例即可）
- CPUlator：線上模擬器，常見支援 ARMv7-A，適合快速驗證基本指令/記憶體配置。
- ARMSim/VisUAL：桌面工具，介面較適合練習 ISA、暫存器/flag 觀察。
- Graphical-Micro-Architecture-Simulator：偏教學用途，用來看更底層的執行/微架構示意。
【解析】重點是：各工具支援的架構版本/介面取向不同，因此適合用來練「指令效果、除錯流程、或架構觀察」的不同題型。


---

# 使用提醒（只放策略，不放答案）

* 寫題時先把「出題範圍」圈起來：ISA 題不要扯到 linker script，工具題不要扯到 CPSR，避免答非所問。  
* 需要寫指令序列（GDB/Linker script/semihosting）時，先照教材順序寫出最短可跑流程，再補理由。  
* 看到 `LDR =`、`ADR/ADRL`、macro 題，一律先回答「展開時機/展開形式」，再談優缺點，答案會更像正式考卷。
