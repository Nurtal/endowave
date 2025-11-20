# ENDOWAVE

## Overview
Simple and accessible project to plays with frequency in rnaseq

## RoadMap
- [x] get benchmark data, fuck precisesads
- [x] transform raw counts into vst
- [ ] get a gene module decomposition (chaussabel for exemple)
- [ ] turn into signal
- [ ] compute PSD embedding
- [ ] endotype prediction

## 1. Get Data
- [ ] GSE88884 -> big lupus
- [x] GSE152004 -> small alergy
- [ ] GSE201530 -> covid
- [ ] GSE65682 -> sepsis
- [ ] GSE199881 -> pulmonary

## 3. Gene Module
- [ ] MSigDB Hallmark gene sets
- [ ] Reactome Pathways
- [ ] KEGG Pathways
- [ ] Chaussabel Modules
- [ ] Gene Ontology (GO: Biological Process)
- [ ] ImmPort gene modules
- [ ] DoRothEA Regulons (TF-target modules)
- [ ] PROGENy Pathways (signaux dérivés de perturbations)

## Journal
- 2025-11-14 : Focus in small alergy data, set up the pipeline for this dataset and check whats give best results between counts, fpkm and tpm -> apparement c'est VST qui par design a le plus de chances de marcher
- 2025-11-14 : Apparement pour faire du "vrai" VST il faut impérativement R, sauf que c'est de la merde, j'y ai passé pas loin d'une heure à installer des packages à la con dans tous les sens et rien ne marche, donc go approximation du vst avec une approche full python
- 2025-11-15 : Beaucoups de modules de genes différent, surement un parametre qu'il va falloir explorer, on se focus sur MSIgDB Hallmark pour le moment
- 2025-11-20 : Computation du PSD et de la FFT, ça tourne bien, les deux renvoients deux vecteurs : la liste des frequences et une mesure associé (amplitude pour FFT et 'puissance' pour PSD), l'idée c'est de construire un embedding utile pour faire de la startification à partir de ça
