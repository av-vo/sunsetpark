## pypwaves
-----
An editted version of [pypwaves](https://github.com/adamchlus/pypwaves)


**Summary of edits made:**

* Switch to python 3 syntax

* Decode `duration_anchor` as signed long (i.e. `=l`) and apply scale and offset

* Decode `sample` as unsigned char (i.e. `=B`)

* The indexing part is skipped for now