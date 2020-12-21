// function launched when empty viewlet is loaded (before complete document ready)
function init_plonetheme_imioapps() {
    resizeHeader();
    highlight_test();
}

// as header is fixed, we need to compute emptyviewlet heights dynamically
// in case header is two lines high
// generate CSS for the faceted table header as stikcy need to know top departure
function resizeHeader() {
    portal_header_height = $("#portal-header").height();
    $("#emptyviewlet").height(portal_header_height);
    var sheet = document.createElement('style');
    sheet.innerHTML = "table.faceted-table-results th {top: " + portal_header_height + "px;}";
    document.body.appendChild(sheet);
}
$(window).resize(resizeHeader);

// when using a imio-test instance, highlight header
function highlight_test() {
    var url = $("link[rel='canonical']").attr('href');
    if (url.includes('imio-test')) {
        $("div#portal-header")[0].style.background = "#d00";
    }
}
