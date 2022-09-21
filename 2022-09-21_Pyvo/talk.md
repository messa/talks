Distribuované aplikace
======================

- aplikace = váš kód plus databáze

- cloud vs. hardware

- co bývá problém? Peníze. Velikost disku, I/O disku, velikost paměti, I/O sítě. Active subset. Lokalita dat a jejich zpracování.

- rozdělovat databáze, specializace databází

- sharding aplikace místo sharding databáze - náročnost na devops,

- riziko uzamčení v SQL mindsetu a těžké škálování pomocí technik, kde už nejsou transakce, referenční integrita... Připravovat se na škálování od začátku

- rozumět, co se v databázi děje, i v low-level úrovni


Jak to máme v Leadhubu
----------------------

- hlavní části aplikace, microservices

- pods
