以下為 **Chapter 5 — The ARM Instruction Set（encoding）** 的考試導向題目集。  
作答規則：直接在每題下方作答；每題最後都有【範圍】標示。

---

# 一、填空題（概念＋欄位辨識）

**1.** ARM 指令的 condition field（cond）位於 bits[____:____]，共有 ____ 種可能值。  
【範圍：Conditional execution — The ARM Condition Code Field】  

**2.** CPSR 的四個條件旗標為 N/Z/C/V，分別代表：N=________、Z=________、C=________、V=________。  
【範圍：Conditional execution — CPSR / condition flags】  

**3.** 在 ARM condition codes 中，`EQ` 的執行條件是 Z ________；`NE` 的執行條件是 Z ________。  
【範圍：Conditional execution — ARM Condition Codes】  

**4.** `NV=1111` 在 cond field 中屬於 ________（可用/不可用）狀態；`AL` 屬於 ________（預設/保留）狀態。  
【範圍：Conditional execution — Condition Field】  

**5.** 例外進入（Exception entry）時，會把「下一條指令位址」存到 ________（暫存器），把 CPSR 存到 ________（暫存器）。  
【範圍：Exceptions — Exception Entry】  

**6.** 請填出 vector address：SWI=0x________，IRQ=0x________，FIQ=0x________。  
【範圍：Exceptions — Exception Vector Addresses】  

**7.** SWI 指令的 encoding 形式為：`cond ____ ____ ____ imm24`（請填 4 個位元）。  
【範圍：SWI — Software Interrupt encoding】  

**8.** Data processing instruction 的 encoding 主軸為：`cond 00 ____ opcode ____ Rn Rd Operand2`（請填 I 與 S 的位置）。  
【範圍：Data processing — Data Processing Instruction Binary Encoding】  

**9.** `opcode[24:21]` 中，`ADD` 的 opcode 值為 ________（4-bit）；`MOV` 的 opcode 值為 ________。  
【範圍：Data processing — Data Processing Instructions (opcode table)】  

**10.** Single word/unsigned byte data transfer 的關鍵欄位 P/U/B/W/L 的意義分別是：P=________、U=________、B=________、W=________、L=________。  
【範圍：Data transfer — single transfer binary encoding】  

**11.** `MRS{cond} Rd, CPSR|SPSR` 是「status register → general register」；`MSR{cond} CPSR_<field>|SPSR_<field>, Rm/#imm` 是「general register/imm → ________」。  
【範圍：Data transfer — MRS/MSR】  

**12.** `CLZ{cond} Rd, Rm` 的功能是：將 Rm 的 ________ 個數寫到 Rd。  
【範圍：Others — CLZ】  

---

# 二、是非題（對/錯＋理由）

**13.** 在 ARM state，中每一條指令都會依據 cond field 與 CPSR 的 N/Z/C/V 決定是否執行。  
（對 / 錯，請說明。）  
【範圍：Conditional execution — Condition Field】  

**14.** `CS` 與 `HS` 是同一個 condition 的不同 mnemonic，用於不同語境（加法 carry vs unsigned compare）。  
（對 / 錯，請說明。）  
【範圍：Conditional execution — Alternative Mnemonics】  

**15.** Exception entry 會 disable IRQ；若進入的是 FIQ，還會 disable 進一步的 FIQ。  
（對 / 錯，請說明。）  
【範圍：Exceptions — Exception Entry】  

**16.** 「先恢復 CPSR 再恢復 PC」與「先恢復 PC 再恢復 CPSR」都可行，因為兩者互不影響。  
（對 / 錯，請說明教材指出的問題點。）  
【範圍：Exceptions — Some Problem in Exception Return】  

**17.** `MOVS pc, r14` 的 `S` 僅代表「更新 N/Z/C/V」，與例外返回無關。  
（對 / 錯，請說明教材對 `S` special form 的描述。）  
【範圍：Exceptions — Solution I】  

**18.** `B {L} {cond} <expression>` 的跳躍是 PC-relative；教材給的可達範圍約 ±32MB。  
（對 / 錯，請說明。）  
【範圍：Branch — Branch and Branch with Link】  

**19.** `BX/BLX` 的用途之一是切換處理器去執行 Thumb instructions；教材指出此機制在 ARM v5T 可用。  
（對 / 錯，請說明。）  
【範圍：Branch — Branch and Exchange】  

**20.** `SWP{cond}{B} Rd, Rm, [Rn]` 中，`B=1` 表示 word swap、`B=0` 表示 byte swap。  
（對 / 錯，請說明。）  
【範圍：Data transfer — SWP】  

**21.** 在 LDR/STR 的 post-indexed form 中，base register 的更新發生在 memory access 之前。  
（對 / 錯，請用 P=0 的文字說明。）  
【範圍：Data transfer — single transfer encoding / pre vs post】  

**22.** `BKPT` 是 unconditional，主要用於 software debugging purposes。  
（對 / 錯，請說明。）  
【範圍：Others — BKPT】  

---

# 三、簡答題（考試可直接寫）

**23.** 列出教材的三類 Exception groups（用自己的話描述即可），並各舉一個例子。  
【範圍：Exceptions — Exception Groups】  

**24.** 例外向量表中「0x00000014」在教材被問到：它為何存在/為何現在不在表中？請用一段話回答。  
【範圍：Exceptions — Address Exceptions】  

**25.** 例外返回的 Solution I：分別說明「SWI/undefined」與「IRQ/FIQ/prefetch abort」與「data abort」返回時用的指令形式，以及為何有 `#4` 或 `#8` 的差異。  
【範圍：Exceptions — Solution I】  

**26.** 例外返回的 Solution II：`LDMFD r13!, {r0-r3,pc}^` 中 `^` 在教材代表什麼？這種做法依賴了什麼前提？  
【範圍：Exceptions — Solution II】  

**27.** 說明 branch/loop 的典型寫法：教材範例用 `MOV r0,#10`、`SUBS`、`BNE` 做 10 次迴圈，請解釋 `SUBS` 與 `BNE` 如何配合。  
【範圍：Branch — Example / Branch Conditions】  

**28.** SWI 的 processor actions（教材列的 5 個 bullet）分別是什麼？請逐條列出。  
【範圍：SWI — Processor Actions for SWI (1)】  

**29.** 請解釋教材 SWI handler 範例的每個關鍵步驟意義：  
`STMF sp!, {r0-r12,r14}`、`LDR r10,[r14,#-4]`、`BIC r10,#0xff000000`、`BL service_routine`、`LDMFD sp!, {r0-r12,pc}^`。  
【範圍：SWI — A SWI Handler】  

**30.** ARM Angel 的 SWI types 表中，`SWI_WriteC`、`SWI_Write0`、`SWI_Exit` 各做什麼？（用一句話各自回答即可）  
【範圍：SWI — Types of SWIs in ARM Angel】  

---

# 四、指令集與 encoding 應用題（欄位→語意）

**31.** 在 data processing encoding 中，`S` bit 的目的為何？教材用 64-bit addition 的例子（`ADDS` + `ADC`）要你表達的重點是什麼？  
【範圍：Data processing — Data Processing Instructions (2)】  

**32.** 請從 opcode 表中挑出「只更新 CPSR、不寫回 Rd」的四個指令，並說明它們分別使用哪種運算（AND/EOR/SUB/ADD）。  
【範圍：Data processing — opcode table（TST/TEQ/CMP/CMN）】  

**33.** 請解釋 data processing 的 Operand2 兩大類來源：立即數（含 #rot）與移位暫存器（shift by imm / shift by Rs），並指出教材圖上各自對應哪些欄位名稱。  
【範圍：Data processing — Data Processing Instruction Binary Encoding】  

**34.** 依教材的 multiply syntax，寫出下列兩個指令的語意（用公式表示）：  
(1) `MLA{cond}{S} Rd, Rm, Rs, Rn`  
(2) `UMLAL{cond}{S} RdLo, RdHi, Rm, Rs`  
【範圍：Multiply — Assembler Syntax / multiply types table】  

**35.** single transfer（LDR/STR）有 pre-index 與 post-index 兩種 assembler syntax。請各寫出一行通用形式，並說明 `{!}` 與 `{T}` 各代表什麼語意（教材文字描述即可）。  
【範圍：Data transfer — Assembler Syntax (LDR/STR)】  

**36.** halfword/signed byte transfer 的 encoding 圖中，immediate offset 被拆成 `Imm[7:4]` 與 `Imm[3:0]`，同時也支援用 `Rm` 當 offset register。請說明「為何同一張圖要同時列 immediate 與 Rm」的設計意義（用教材欄位呈現回答即可）。  
【範圍：Data transfer — Half-word and Signed Byte Data Transfer Instruction Binary Encoding】  

**37.** `MSR` 的 `<field>` 有 c/x/s/f 四種。請逐一寫出它們對應的 PSR 位元範圍（PSR[??:??]），並說明「只更新 flags」時應使用哪個 field。  
【範圍：Data transfer — MSR field mask】  

**38.** 依教材 MSR 範例：  
先 `MRS r0, CPSR`，再 `BIC r0, r0, #&1f`，再 `ORR r0, r0, #&12`，最後 `MSR CPSR_c, r0`。  
請說明這段程式的目的與每一步對 CPSR 的哪個欄位動手腳。  
【範圍：Data transfer — MSR/MRS example】  

**39.** Coprocessor instructions 分成三大類：data operations / data transfers / register transfers。請分別對應教材給的 mnemonic（CDP、LDC/STC、MRC/MCR），並用一句話描述各自的資料流向。  
【範圍：Coprocessor — Coprocessor Instructions / syntax】  

**40.** `CLZ` 的範例中：`MOV r0,#0x100` 之後 `CLZ r1,r0` 得到 r1=23。請用「bit pattern」的角度解釋為何是 23（不必寫出全部 32 bits，可用概念描述）。  
【範圍：Others — CLZ example】  

---

# 使用提醒（只放策略，不放答案）

* 是非題一定要用「教材文字」回扣（例如：Solution I/II、P=1/P=0、`^` 的意義），否則很容易被判答非所問。  
* encoding 題先把欄位寫成一行：`cond | opcode | S | Rn | Rd | ...`，再回答語意，會更像正式考卷答案。  
* SWI handler 題先交代「為什麼從 LR-4 讀指令」，再交代「如何取 imm24」與「如何分派服務」。
