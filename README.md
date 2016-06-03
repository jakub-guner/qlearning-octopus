# qlearning-octopus
W przypadku dodawania nowej funkcji aproksymującej: 
  - definicje funkcji zamieścić w features.py, uaktualnić również funkcję getFeatures()
  - w głównym pliku agenta zwiększyć rozmiar tablicy na wagi
  - do pliku z wagami dodać jakieś wartości (np 1) na końcu każdej lini

Plik features.py powinien się znajdować w folderze z agentem
  
Do zmiany:
- wywalić normalizacje
- wywalic bias
- alpha = 0.005
- discount = 1 
- jedna decyzja co ileś kroków, (5-10) + sumowanie rewardów w tym czasie
- czas w featurach
- zmienic w stepie max z get-q-value (minQ = -inf) 
