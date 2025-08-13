**O aplikaciji**

Ova aplikacija simulira ponašanje jednog jata ptica ili plova riba. Na početku se slučajno generira 20 agenata koji predstavljaju člana jata i kreću se u slučajnom pravcu. Prilaskom drugom agentu dolazi do izranjajućeg ponašanja jednog jata.

**Uvodne napomene**

Prije nego što se pokrene aplikacija, potrebno je ispuniti određene preduvijete.
Potrebno je imati instaliran Prosody server. Za instalaciju pogledajte na [Prosody IM](https://prosody.im/).
Nakon instalacije i pokretanja servera, potrebno je dodati agente
   ```bash
   prosodyctl adduser boid0@localhost
   ```
Agenti su od boid0 do boid19, a password je pass.

Nakon toga preporuka je učiniti sljedeće:

**Kreiranje virtualno okruženje**:
   ```bash
   python3 -m venv .VAS
   ```

**Aktiviranje virtualnog okruženja**:
   ```bash
   source .VAS/bin/activate
   ```

**Instaliranje potrebnih biblioteka**:
   ```bash
   pip install -r requirements.txt
   ```
