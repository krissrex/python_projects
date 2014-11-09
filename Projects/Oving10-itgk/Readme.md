## Øving 10 i ITGK

Kjør main.py. For å bruke kartet lagret i skumleskogen2.py, erstatt 

```py
from skumleskogen import *
```
med
```py
from skumleskogen2 import *
```

---
### Oppgaven

[Oppgave 10.pdf](https://itgk.idi.ntnu.no/oving/2014/oving10-python.pdf "oving-10-python.pdf")
> #### Skumleskogen
Som del av din ferd til Dragvoll idrettssenterTM for å avlegge eksamen i ITGK er du nødt til å traversere
Skumleskogen. Skumleskogen er, som alle skumle skoger, formet som en labyrint (figur 1). Å komme inn
i skogen er ikke noe problem, men siden utgangen av skogen er låst, er det er ikke mulig å forlate uten å
finne de forskjellige nøklene gjemt i de aller skumleste hjørnene av skogen. Som om ikke det var nok så huser
skogen noen skikkelig skumle skapninger, nærmere bestemt søte menneskespisende kaniner. Hvis du skulle
være så uheldig å møte på en kanin så ville jo det bety en garantert død, men heldigvis gir menneskespisende
kaniner fra seg en ekkel stank som kan kjennes noen meter unna.
Hvordan kan du løse dette problemet og komme deg til eksamen før kl 08:50?
#### Oppgavebeskrivelse
I denne oppgaven skal du skrive et program som løser et labyrintspill representert som et tre. Målet med
spillet er å komme seg fra inngangsnoden til utgangsnoden, men på veien til utgangsnoden befinner det seg
noder som du ikke kan traversere uten å “låse opp” først (låsnoder). For å låse opp låsnoder må du først
samle nøkler ved besøke nøkkelnoder i treet og “plukke opp nøkkelen“. Noen ganger så betyr dette at du må
snu og utforske en annen retning i jakt på en nøkkel. I tillegg til låsnoder finnes det såkalte superlåsnoder
som krever to nøkler for å bli låst opp. Til slutt inneholder treet kanin-noder, som er dødelige (dvs. at du
taper spillet hvis du besøker de), og stank-noder, som har den funksjon at de alltid befinner seg ved siden av
kanin-noder.
Figurene 1, 2, og 3 illustrerer tre forskjellige representasjoner av den samme instansen (dvs. brettet) av
spillet. Den siste figuren, figur 3 er en mye enklere representasjon enn det grafiske bildet i figur 1.
I stedet for å skrive kode som traverserer dette treet, skal du bruke et rammeverk, dvs. en samling med
ferdige funksjoner, for å løse denne oppgaven. Rammeverket er implementert i fila skumleskogen.py som er
lagt ved øvingen, og består av en rekke funksjoner som utfører forskjellige handlinger eller gir informasjon
om noden man er i. Rammeverket holder styr på hvor man er i treet og sjekker alltid hvorvidt en handling
du prøver å utføre er lovlig. Rammeverket er beskrevet i detalj i tabell 2. Husk å inkludér rammeverket ved
å skrive “from skumleskogen import *” i starten av svarfilen din.
Den interne representasjonen som rammeverket jobber med er det binære treet i figur 3 som består av noder
av forskjellige typer2
. De forskjellige nodene og deres funksjon er beskrevet i tabell 1.

