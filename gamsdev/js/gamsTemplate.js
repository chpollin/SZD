!(function(e) {
  var t = {};
  function n(r) {
    if (t[r]) return t[r].exports;
    var o = (t[r] = { i: r, l: !1, exports: {} });
    return e[r].call(o.exports, o, o.exports, n), (o.l = !0), o.exports;
  }
  (n.m = e),
    (n.c = t),
    (n.d = function(e, t, r) {
      n.o(e, t) || Object.defineProperty(e, t, { enumerable: !0, get: r });
    }),
    (n.r = function(e) {
      "undefined" != typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(e, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(e, "__esModule", { value: !0 });
    }),
    (n.t = function(e, t) {
      if ((1 & t && (e = n(e)), 8 & t)) return e;
      if (4 & t && "object" == typeof e && e && e.__esModule) return e;
      var r = Object.create(null);
      if (
        (n.r(r),
        Object.defineProperty(r, "default", { enumerable: !0, value: e }),
        2 & t && "string" != typeof e)
      )
        for (var o in e)
          n.d(
            r,
            o,
            function(t) {
              return e[t];
            }.bind(null, o)
          );
      return r;
    }),
    (n.n = function(e) {
      var t =
        e && e.__esModule
          ? function() {
              return e.default;
            }
          : function() {
              return e;
            };
      return n.d(t, "a", t), t;
    }),
    (n.o = function(e, t) {
      return Object.prototype.hasOwnProperty.call(e, t);
    }),
    (n.p = ""),
    n((n.s = 0));
})([
  function(e, t, n) {
    "use strict";
    function r(e, t) {
      for (var n = 0; n < t.length; n++) {
        var r = t[n];
        (r.enumerable = r.enumerable || !1),
          (r.configurable = !0),
          "value" in r && (r.writable = !0),
          Object.defineProperty(e, r.key, r);
      }
    }
    n.r(t);
    var o = (function() {
      function e() {
        !(function(e, t) {
          if (!(e instanceof t))
            throw new TypeError("Cannot call a class as a function");
        })(this, e);
      }
      var t, n, o;
      return (
        (t = e),
        (n = [
          {
            key: "buildQuery",
            value: function(e, t) {
              e.on("submit", function() {
                if ((e = t.val().toLowerCase()).startsWith('"'))
                  var e,
                    n =
                      "/archive/objects/query:cantus.phrase/methods/sdef:Query/get?params=" +
                      ("%245%7C" + (e = e.slice(1, -1)));
                else
                  n =
                    "/archive/objects/query:cantus.fulltext/methods/sdef:Query/get?params=" +
                    ("%245%7C" + e);
                return (window.location.href = n), !1;
              });
            }
          }
        ]) && r(t.prototype, n),
        o && r(t, o),
        e
      );
    })();
    function i(e, t) {
      for (var n = 0; n < t.length; n++) {
        var r = t[n];
        (r.enumerable = r.enumerable || !1),
          (r.configurable = !0),
          "value" in r && (r.writable = !0),
          Object.defineProperty(e, r.key, r);
      }
    }
    function a(e, t, n) {
      return (
        t in e
          ? Object.defineProperty(e, t, {
              value: n,
              enumerable: !0,
              configurable: !0,
              writable: !0
            })
          : (e[t] = n),
        e
      );
    }
    var u = new ((function() {
      function e() {
        var t = this;
        !(function(e, t) {
          if (!(e instanceof t))
            throw new TypeError("Cannot call a class as a function");
        })(this, e),
          a(this, "query", void 0),
          a(this, "fixHashJump", function(e) {
            var t =
              arguments.length > 1 && void 0 !== arguments[1]
                ? arguments[1]
                : 0;
            if (!e)
              throw new ReferenceError(
                "No elements given to fixHashjump -> Aborting fixHashJump."
              );
            e.click(function(e) {
              var n = e.target.getAttribute("href");
              e.preventDefault(),
                setTimeout(function() {
                  if (n) {
                    n = n.substring(1, n.length);
                    var e = document.getElementById(n);
                    if (!e)
                      throw new ReferenceError(
                        "Elem is not defined! Can't find element with hash(=id) \"".concat(
                          n,
                          '" . Aborting fixHashJump.'
                        )
                      );
                    var r = $(e).offset();
                    if (!r)
                      throw new ReferenceError(
                        "Can't access given elements offset. Aborting fixHashJump. Tried to jump to: \"".concat(
                          e,
                          '"'
                        )
                      );
                    var o = r.top;
                    if (!o)
                      throw new ReferenceError(
                        'ElemPos is not defined! Aborting fixHashJump. Given elem was: "'.concat(
                          e,
                          '"'
                        )
                      );
                    var i = $("nav");
                    if (!i)
                      throw new ReferenceError(
                        "Nav is not defined! Aborting fixHashJump."
                      );
                    var a = o - i.height(),
                      u = $(window).scrollTop();
                    u - o > -t && u - o < t
                      ? window.scrollTo({ top: a, behavior: "smooth" })
                      : window.scrollTo({ top: a, behavior: void 0 });
                  }
                }, 1);
            });
          }),
          a(this, "repairHashLoadJump", function() {
            var e =
              arguments.length > 0 && void 0 !== arguments[0]
                ? arguments[0]
                : $("nav");
            if (!e)
              throw new ReferenceError(
                "Can't acces the <nav> element. Aborting repairHashLoadJump at gamsTemplateJs."
              );
            if ("" !== window.location.hash) {
              var t = window.location.hash;
              t = t.substring(1, t.length);
              var n = document.getElementById(t);
              if (!n)
                throw new ReferenceError(
                  "Can't repair the hash-jump onload. Unable to select the element which id corresponds to given hash: ".concat(
                    t
                  )
                );
              var r = $(n).offset();
              if (!r)
                throw new ReferenceError(
                  "Can't access given elements offset. Aborting fixHashJump."
                );
              var o = r.top,
                i = o - e.height();
              setTimeout(function() {
                window.scrollTo({ top: i, behavior: "auto" });
              }, 1);
            }
          }),
          a(this, "alertSmallDevice", function() {
            var e =
                arguments.length > 0 && void 0 !== arguments[0]
                  ? arguments[0]
                  : 900,
              t =
                arguments.length > 1 && void 0 !== arguments[1]
                  ? arguments[1]
                  : "Your device is too small to display all of the web-content. Please use the desktop version for the full functionality.";
            arguments.length > 2 && void 0 !== arguments[2] && arguments[2];
            if (document.documentElement.clientWidth < e) return confirm(t);
          }),
          a(this, "verifyInCurURL", function(e) {
            return -1 !== window.location.href.indexOf(e);
          }),
          a(this, "getCurrentUrl", function() {
            return window.location.href;
          }),
          a(this, "detectUserLang", function() {
            var e = t.getCurrentUrl(),
              n = e.indexOf("&locale=") + "&locale=".length;
            return e.substring(n, n + 2);
          }),
          a(this, "checkGerman", function() {
            return "de" === t.detectUserLang();
          }),
          (this.query = new o());
      }
      var t, n, r;
      return (
        (t = e),
        (n = [
          {
            key: "setHttpsIfHttp",
            value: function() {
              var e =
                "You've loaded the page with http instead of https. Cantus will only work via https. Reload page with https?";
              this.verifyInCurURL("locale=de") &&
                (e =
                  "Die Seite wurde mit http geladen. Cantus funktioniert jedoch nur mit https. Seite neu laden via https?"),
                "https:" !== location.protocol &&
                  confirm(e) &&
                  (location.protocol = "https:");
            }
          }
        ]) && i(t.prototype, n),
        r && i(t, r),
        e
      );
    })())();
    window.gamsTemplateJs = u;
  }
]);
