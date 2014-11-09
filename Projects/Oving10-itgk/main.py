# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 00:06:24 2014

@author: kristian
"""

from skumleskogen import *
import time

hukommelse = {}
debug_on = True
sti_totalt = ["inn"]
noder_med_lås = set()
forrige_retning = []


class MovementException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return str(self.error)


def start_solving():
    print("Er inngang:", er_inngang())

    nøkler = 0

    while True:
        debug()
        husk_node()

        if er_stank():
            if gaa_tilbake():
                sti_totalt.append("STANK! tilbake til " + str(nummer()))
                kom_fra_retning = forrige_retning.pop(len(forrige_retning) - 1)
            continue

        if er_nokkel():
            if plukk_opp():
                nøkler += 1
                sti_totalt.append("plukket nøkkel " + str(nøkler))
            continue

        if (not hukommelse[nummer()]["venstre"]) \
                or kan_låse_opp(nummer(), nøkler, "venstre"):
            try:
                hukommelse[nummer()]["lås"][0] = False
                hukommelse[nummer()]["superlås"][0] = False
                besøk_node("venstre")
            except MovementException as ex:
                print(ex)
            else:
                forrige_retning.append("venstre")
                sti_totalt.append("venstre " + str(nummer()))
                continue

        if (not hukommelse[nummer()]["høyre"]) \
                or kan_låse_opp(nummer(), nøkler, "høyre"):
            try:
                hukommelse[nummer()]["lås"][1] = False
                hukommelse[nummer()]["superlås"][1] = False
                besøk_node("høyre")
            except MovementException as ex:
                print(ex)
            else:
                forrige_retning.append("høyre")
                sti_totalt.append("høyre " + str(nummer()))
                continue

        if er_laas():
            noder_med_lås.add(nummer())

            if er_superlaas():
                if nøkler >= 2:
                    utfall = laas_opp()
                    if utfall:
                        nøkler -= 2
                        sti_totalt.append("låste opp sl " + str(nøkler))
                        if nummer() in noder_med_lås:
                            noder_med_lås.remove(nummer())
                        continue
                else:
                    noder_med_lås.add(nummer())
            else:
                if nøkler >= 1:
                    utfall = laas_opp()
                    if utfall:
                        nøkler -= 1
                        sti_totalt.append("låste opp s " + str(nøkler))
                        if nummer() in noder_med_lås:
                            noder_med_lås.remove(nummer())
                        continue

        if er_utgang():
            gaa_ut()
            return

        # Vi er stuck. Noen noder må være låste.
    
        har_lås = er_laas()
        har_superlås = er_superlaas()
        if har_lås and har_superlås:
            # Låsen var ikke en vanlig lås, men superlås.
            har_lås = False
        
        if barn_har_lås(nummer()):
            har_lås = True
        if barn_har_superlås(nummer()):
            har_superlås = True

        if gaa_tilbake():
            sti_totalt.append("tilbake til " + str(nummer()))
            kom_fra_retning = forrige_retning.pop(len(forrige_retning) - 1)
            print("kom fra:", kom_fra_retning)
            if har_lås:
                print("har lås")
                if kom_fra_retning == "venstre":
                    hukommelse[nummer()]["lås"][0] = True
                else:
                    hukommelse[nummer()]["lås"][1] = True
            if har_superlås:
                print("har superlås")
                if kom_fra_retning == "venstre":
                    hukommelse[nummer()]["superlås"][0] = True
                else:
                    hukommelse[nummer()]["superlås"][1] = True
                    print(hukommelse[nummer()])
        else:
            print("KLARTE IKKE Å GÅ TILBAKE!!!")
            return


def kan_låse_opp(n, nøkler, retning):
    indeks = 0
    if retning == "høyre":
        indeks = 1

    if hukommelse[n]["lås"][indeks] and (nøkler >= 1):
        return True
    if hukommelse[n]["superlås"][indeks] and (nøkler >= 2):
        return True
    return False


def barn_har_lås(n):
    return hukommelse[n]["lås"][0] or hukommelse[n]["lås"][1]


def barn_har_superlås(n):
    return hukommelse[n]["superlås"][0] or hukommelse[n]["superlås"][1]


def husk_node():
    n = nummer()
    if n not in hukommelse:
        hukommelse[n] = {"venstre": False, "høyre": False,
                         "lås": [False, False], "superlås": [False, False]}


def besøk_node(retning):
    n = nummer()
    utfall = False

    if retning == "venstre":
        utfall = gaa_venstre()
    elif retning == "høyre":
        utfall = gaa_hoyre()
    else:
        print("Ugyldig retning oppgitt!", n, retning)
        return

    if utfall:
        hukommelse[n][retning] = True
    else:
        if er_laas():
            raise MovementException("Er låst")
        else:
            raise MovementException("Er blindvei")


def debug():
    if debug_on:
        print("/"*25 + "DEBUG:" + "/"*25)
        print(("Nummer: {n}\n" +
              "Type:\n    " +
              "i: {i}, l: {l}, sl: {sl}, st: {st}, nk: {nk}, v: {v}, u: {u}" +
              "\nLabel: {la}")
              .format(n=nummer(), i=er_inngang(), l=er_laas(),
                      sl=er_superlaas(), st=er_stank(), u=er_utgang(),
                      v=er_vanlig(), nk=er_nokkel(), la=label(nummer())))


def main():
    # Initialisation.
    def get_hours():
        return time.asctime().split(' ')[4]
    start_time = time.time()
    print("Starting. Time:", get_hours())

    # Start solving the maze.
    try:
        start_solving()

    # In case of failure, e.g. a rabbit ate you.
    except Exception as e:
        print("Exception occured:")
        print(e)
        print("Exciting. Time:", get_hours())

    # Done, do final actions.
    finally:
        print("Ran for {0} seconds.".format(
            abs(
                round(start_time - time.time(), 4))))
    print("Maze completed.")
    print(sti_totalt)

if __name__ == "__main__":
    main()
