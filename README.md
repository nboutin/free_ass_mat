# Simple AssMat

[![Python Run Tests](https://github.com/nboutin/simple_ass_mat/actions/workflows/run_tests.yml/badge.svg?branch=main)](https://github.com/nboutin/simple_ass_mat/actions/workflows/run_tests.yml)
[![Python Code Check](https://github.com/nboutin/simple_ass_mat/actions/workflows/python_code_check.yml/badge.svg?branch=main)](https://github.com/nboutin/simple_ass_mat/actions/workflows/python_code_check.yml)

Logiciel pour le calcul du salaire d'une Assistante Maternelle (AssMat) en France.

Aide pour remplir la déclaration sur le site Pajemploi.

Support contrat sur année complète et incomplète

## External links

- [pajemploi.urssaf.fr](https://www.pajemploi.urssaf.fr/pajewebinfo/cms/sites/pajewebinfo/accueil/employeur-dassistante-maternelle/je-recrute-et-jemploie/definir-les-heures-de-garde.html)
- [legifrance.gouv.fr](https://www.legifrance.gouv.fr/conv_coll/id/KALITEXT000043941642)
- [zen-avec-mon-assmat.com](https://zen-avec-mon-assmat.com/autres-elements-salaire-nounou/)

## Run Code Coverage

Configure in .coveragerc file.

    coverage run -m pytest
    coverage report -m
    coverage html
