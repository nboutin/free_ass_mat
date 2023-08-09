# Creation contrat

1. Initialisation
a. type de contrat
- assitant maternel agree
- garde enfant a domicile

b. copie contrat precedent: oui/non

2. Information principales
a. enfant accueilli
- né: oui/non
- sexe: fille/garcon
- prenom
- nom de famille
- date de naissance
- handicap, maladie, inadaptation: oui/non

b. Information complementaires
- lien utilisateur avec enfant: pere/mere/tuteur/parent 1/2
- region habitation assitant maternel: France, alsace/lorraine, DOM, TOM
- zone scolaire
- ass_mat sexe

c. Fraterie
- autre enfant de la famille avec la meme ass_mat: bool
- Selection enfant fraterie

d. Reprise ancienneté
- acceuil_commence_et_premier_salaire_versé : bool
    - oui
        - date debut contrat
        - avanenant : bool

3. type de contrat
- CDI/CDD

4. Organisation horaire
a. type de planning
- 1 semaine type d'acceuil
- 1 semaine type d'acceuil periode scolaire et 1 semaine type d'acceuil periode vacances scolaires
- plusieurs semaines type (a,b,c, horaire soir/matin)
- jour et/ou horaire inconnu, planning variable
- jour ou horaire occasionnel

b. definition des semaines
- par semaine type
    - par jour
        - crénaux horaire (1 ou multiple)
        - repas au domicile de l'ass_mat
            - petit-dejeuner/dejeuner/gouter/diner
            - fournit par assmat/parent/aucun
- adaptation des horaraires
    - ass_mat accepte/refuse/exceptionnel travail en dehors des creneaux horaires

5. Calendrier
a. debut du contrat=premier jour acceuil enfant
b. fin du contrat
    - moins 1 an, 1 an, ne sais pas
c. absence et conges
- nombre semaine vacances ass_mat (5 min)
- nombre semaine entiere absence enfant (en dehors des semaines de cp et absence ass_mat)
    -> annee complete ou incomplete
d. repartition des semaines
- nombre semaine type 1/2/...
e. modification du planning
- modifiable: bool
    - oui
        - delais de prevenance
f. jours perles deductibles
- nombre de jour perles

6. Remuneration
a. tarif horaire
- tarif brut ou net
- est-elle titulaire du titre professionnel de branche "Assistant maternel - Garde d'enfant": bool
- action sur hausse des cotisations salariales: re-evaluer ou non le tarif brut
b. Heures majorees
- majoration heures additionnelle/complementaire: %
- majoration heure supplementaire: % (min 10%)
Les heures additionnelles sont des heures travaillées en plus des horaires prévus au contrat. Elles sont donc payées chaque mois en supplément.
Notez qu'une heure additionnelle peut également être considérée comme supplémentaire si le volume de la semaine dépasse 45h.
c. Autre majoration
- jour de repas legal: dimanche(defaut)
- majoration jour de repos: % (min 25%)
- majoration heure tardives/de nuit:
    - heure apres
    - heures avant
    - majoration: % ou tarif souahaité
d. indemnite entretien
- minimum conventionnel, forfaite par jour, a l'heure, 
- methode de calcul: a la minute, tranche heure entierement travaille, tranche d'heure commence
f. indemnite de repas
- par tranche d'age
    - cout petit dejeuner
    - cout dejeuner
    - cout gouter
    - cout diner
g. indemnite kilometrique
info: Les indemnités kilométriques retenues sont alors celles du barème fiscal des impôts de l'année en cours.
7. Salaire
a. mensualisation
calcul: acceuil hebdomadaire moyen (heures)
calcul: menusalisation des heures (heures/mois)
calcul: salaire brut mensualisé
calcul: salaire net mensualisé
b. augmentation annuel
- augmentation annuel: bool
    - oui: mois de revaloraisation
c. mode de paiement
- moyen de paiement: cheque, virement, espece, pajemploi plus
- date de versement du salaire au plus tard: date
- ass mat accepte CESU: bool
d. paiment des conges payes
- Quand: A seule fois avec le salaire de juin, lors de la prise principal des conges, au fur et a mesure
8. Autre points
a. Planification des conges
- conges ass mat
- semaines absence de l'enfant
b. lieu d'acceuil de l'enfant
c. periode d'essai
d. periode d'adaptation
- duree periode adaption
- Pendant l'adaptation, les heures d'absence de l'enfant (par rapport au planning classique) seront-elles déduites du salaire ?: bool
e. enfant malade
f. jours feries
- tous chomes
- tarif majoration jours feries travailles: % (min 10%)
g. fin de l'acceuil
- indemnite de rupture: 1/80, 1/60, 1/4
9. Ass Mat
a. Coordonnes
10. Document et finalisation


