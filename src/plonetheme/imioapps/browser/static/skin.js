// as header is fixed, we need to compute emptyviewlet heights dynamically
// in case header is two lines high

function resizeHeader() {
    $("#emptyviewlet").height($("#portal-header").height());
}
$(window).resize(resizeHeader);

