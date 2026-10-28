// plonetheme.imioapps: browser body classes, red header on the test instances and
// heights of the sticky header for the sticky dashboard table header (see imioapps.css).
(function () {
    "use strict";

    function stickyHeights() {
        var header = document.getElementById("content-header");
        var nav = document.getElementById("mainnavigation-wrapper");
        var headerHeight = header ? header.offsetHeight : 0;
        var style = document.documentElement.style;
        style.setProperty("--imioapps-header-height", headerHeight + "px");
        style.setProperty(
            "--imioapps-sticky-height",
            headerHeight + (nav ? nav.offsetHeight : 0) + "px"
        );
    }

    function init() {
        var ua = navigator.userAgent.toLowerCase();
        if (/chrom/.test(ua)) {
            document.body.classList.add("using-chrome");
        }
        if (/firefox/.test(ua)) {
            document.body.classList.add("using-firefox");
        }
        var canonical = document.querySelector("link[rel='canonical']");
        var url = canonical ? canonical.href : "";
        if (url.includes(".imio-test.be") || url.includes(".imio-acceptation.be")) {
            document.body.classList.add("imioapps-test-instance");
        }
        stickyHeights();
        // header height changes with the logo loading, the window width...
        var observer = new ResizeObserver(stickyHeights);
        ["content-header", "mainnavigation-wrapper"].forEach(function (id) {
            var element = document.getElementById(id);
            if (element) {
                observer.observe(element);
            }
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
