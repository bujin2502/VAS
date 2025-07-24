**O aplikaciji**

Ova aplikacija simulira ponašanje jednog jata (ptica, riba). Na početku se slučajno generira 20 agenata koji predstavljaju člana jata i kreću se u slučajnom pravcu. Prilaskom drugom agentu dolazi do ponašanja jednog jata.

**Uvodne napomene**

Prije nego što se pokrene aplikacija, potrebno je ispuniti određene preduvijete.
Potrebno je imati instaliran Prosody server. Za instalaciju pogledajte na [Prosody IM](https://prosody.im/).
Nakon instalacije i pokretanja servera, potrebno je dodati agente
   ```bash
   prosodyctl adduser boid0@localhost
   ```
Agenti su od boid0 do boid19, a password je pass.



1. **Kreiranje virtualno okruženje**:
   ```bash
   python3 -m venv .VAS
   ```

2. **Aktiviranje virtualnog okruženja**:
   ```bash
   source .VAS/bin/activate
   ```

3. **Instaliranje potrebnih biblioteka**:
   ```bash
   pip install -r requirements.txt
   ```
