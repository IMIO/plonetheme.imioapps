====================
ploneteme.imioapps
====================

Site theme shared between imio's applications.

Fixed header :
--------------

From version 2.1, the hader is now fixed, to remove this, add this to a ploneCustom.css :

div#portal-header {
   position: relative;
}
#portal-top div#emptyviewlet {
    padding-top: 0em;
}