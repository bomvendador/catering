console.log('sn');
! function(e) {
    "use strict";

    function a() {
        if (t(), s(), e("select").length && e.each(e("select"), function() {
                var a = e(this).find("option:selected").text();
                e(this).wrap('<div class="select-custom"></div>').css({
                    "z-index": 10,
                    opacity: 0
                }).after('<span class="select">' + a + '</span><i class="fa fa-caret-down"></i>').change(function() {
                    var a = e("option:selected", this).text();
                    e(this).next().text(a)
                })
            }), e(".scroll-to-menu .awe-btn").on("click", function() {
                return e("html,body").animate({
                    scrollTop: e("#the-menu").offset().top
                }, 800, "easeInOutExpo"), !1
            }), e(".scroll-to-events .awe-btn").on("click", function() {
                return e("html,body").animate({
                    scrollTop: e("#events").offset().top
                }, 800, "easeInOutExpo"), !1
            }), e(".open-popup-reservation").length && e(".open-popup-reservation .awe-btn").magnificPopup({
                type: "inline",
                fixedContentPos: !1,
                fixedBgPos: !0,
                overflowY: "auto",
                closeBtnInside: !0,
                preloader: !1,
                midClick: !0,
                removalDelay: 300,
                mainClass: "my-mfp-reservation"
            }), e(".toggle-minicart").on("click", function() {
                e(".minicart-wrap").find(".minicart-body").toggleClass("cart-toggle")
            }), e("html").on("click", function() {
                e(".minicart-wrap").find(".minicart-body").removeClass("cart-toggle")
            }), e(".minicart-wrap").on("click", function(e) {
                e.stopPropagation()
            }), e(".home-slider").length) {
            var a = (e(".home-slider").bxSlider({
                autoHover: true,
                tickerHover: true,
                mode: "fade",
                auto: !0,
                speed: 1200,
                slideMargin: 0,
                pager: !0,
                controls: true,
                prevText: '<i class="mdi mdi-chevron-left hide-480"></i>',
                nextText: '<i class="mdi mdi-chevron-right hide-480"></i>',
                onSliderLoad: function(a) {
                    e(".home-slider").children().eq(a).addClass("active-slide")
                },
                onSlideBefore: function(a) {
                    e(".home-slider").children().removeClass("active-slide"), a.addClass("active-slide")
                }
            }), e(".home-slider").data("background"));
            e(".home-slider li img").before(function() {
                var t = e(this).attr("src");
                return '<div class="item-img ' + a + '" style="background-image: url(' + t + ')">'
            }), e(".home-slider").find(".image-wrap").append('<div class="awe-overlay overlay-default"></div>')
        }
        e(".event-slider").length && (e(".event-slider").bxSlider({
            mode: "fade",
            speed: 1e3,
            slideMargin: 0,
            pager: !0,
            controls: !1,
            pagerCustom: ".event-pager"

        }), r());
        var i = e(".event-pager-scroll");
        i.perfectScrollbar({
            maxScrollbarLength: 150,
            suppressScrollY: !0,
            useBothWheelAxes: !0,
            includePadding: !0,
        });
        var l = e(".see-map a").data("see-contact"),
            n = e(".see-map a").data("see-map");
        e(".see-map a").text(n), e(".see-map").delegate("a", "click", function(a) {
            a.preventDefault(), e(".contact-first").find(".contact-body").slideToggle(300), e(".contact-first").find(".awe-overlay").fadeToggle(300), e(".contact-first").find(".section-content").toggleClass("pd0"), e(this).text(n), e(".section-content").hasClass("pd0") && e(this).text(l)
        });
        var o = e(".contact-first").find(".section-content").outerHeight();
        if (e(".contact-first").height(o), e(".testimonial-slider").length && e(".testimonial-slider").owlCarousel({
                autoPlay: 2e4,
                slideSpeed: 300,
                navigation: !1,
                pagination: !0,
                singleItem: !0,
                navigationText: ['<i class="fa fa-angle-double-left"></i>', '<i class="fa fa-angle-double-right"></i>']
            }), e(".milestones-slider").length && e(".milestones-slider").owlCarousel({
                items: 5,
                itemsDesktop: [1199, 4],
                itemsDesktopSmall: [992, 3],
                itemsTablet: [767, 2],
                itemsTabletSmall: [600, 1],
                slideSpeed: 200,
                navigation: !0,
                pagination: !1,
                navigationText: ['<i class="fa fa-angle-double-left"></i>', '<i class="fa fa-angle-double-right"></i>']
            }), e(".our-story").length) {
            e(".story-slider").bxSlider({
                mode: "fade",
                speed: 600,
                slideMargin: 0,
                pager: !0,
                controls: !1,
                pagerCustom: ".story-pager"
            }), e(".story-pager").owlCarousel({
                items: 5,
                itemsCustom: [
                    [0, 3],
                    [400, 4],
                    [700, 5]
                ],
                slideSpeed: 300,
                navigation: !1,
                pagination: !1,
                addClassActive: !0,
                touchDrag: !1,
                mouseDrag: !1
            });
            var m = e(".story-pager").find(".owl-item.active").length;
            e(".story-pager .active:eq(" + m + ")").find(".line").hide(), e(".story-pager").delegate(".owl-item ", "click", function() {
                e(".story-pager").find(".owl-item").css("border", "0"), 0 == e(this).prevAll(".active").length && e(this).index() > 0 && (e(this).find(".line").fadeIn(400), e(".story-pager").trigger("owl.prev"), e(".story-pager .active:eq(" + m + ")").find(".line").fadeOut(500)), e(this).prevAll(".active").length == e(".story-pager").find(".owl-item.active").length - 1 && e(this).index() < e(".story-pager").find(".owl-item").length - 1 && (e(this).next().find(".line").fadeOut(400), e(this).find(".line").fadeIn(400), e(".story-pager").trigger("owl.next"))
            })
        }
        e(".staff-slider").length && e(".staff-slider").owlCarousel({
            items: 3,
            itemsDesktop: [1199, 3],
            itemsDesktopSmall: [992, 2],
            itemsTablet: [767, 2],
            itemsTabletSmall: [600, 1],
            slideSpeed: 300,
            navigation: !0,
            pagination: !1,
            navigationText: ['<i class="fa fa-angle-double-left"></i>', '<i class="fa fa-angle-double-right"></i>']
        }), e(".gallery-slider").length && (e(".gallery-slider").owlCarousel({
            items: 5,
            autoPlay: !0,
            itemsDesktop: [1199, 3],
            itemsDesktopSmall: [992, 3],
            itemsTablet: [767, 3],
            itemsTabletSmall: [600, 2],
            slideSpeed: 300,
            navigation: !1,
            pagination: !1,
            navigationText: ['<i class="fa fa-angle-double-left"></i>', '<i class="fa fa-angle-double-right"></i>']
        }), e(".gallery-slider").magnificPopup({
            delegate: ".gallery-item a",
            type: "image",
            closeOnContentClick: !1,
            closeBtnInside: !1,
            mainClass: "pp-gallery mfp-with-zoom mfp-img-mobile",
            image: {
                verticalFit: !0
            },
            gallery: {
                enabled: !0
            },
            zoom: {
                enabled: !0,
                duration: 300,
                opener: function(e) {
                    return e.find("img")
                }
            }
        }), e(".gallery-item a").hover(function() {
            e(".gallery-item a").addClass("grayscale"), e(this).removeClass("grayscale")
        }, function() {
            e(".gallery-item a").removeClass("grayscale")
        })), e(".pp-product-detail").length && e(".pp-product-detail").magnificPopup({
            type: "ajax"
        }), e(".accordion-wrap .collapse").on("shown.bs.collapse", function() {
            e(this).parent().find(".fa-plus").removeClass("fa-plus").addClass("fa-minus")
        }).on("hidden.bs.collapse", function() {
            e(this).parent().find(".fa-minus").removeClass("fa-minus").addClass("fa-plus")
        }), e("#send-message-form").length && e("#send-message-form").validate({
            rules: {
                name: {
                    required: !0,
                    minlength: 2
                },
                email: {
                    required: !0,
                    email: !0
                },
                message: {
                    required: !0,
                    minlength: 10
                }
            },
            messages: {
                name: {
                    required: "Please enter your name.",
                    minlength: e.format("At least {0} characters required.")
                },
                email: {
                    required: "Please enter your email.",
                    email: "Please enter a valid email."
                },
                message: {
                    required: "Please enter a message.",
                    minlength: e.format("At least {0} characters required.")
                }
            },
            submitHandler: function(a) {
                return e(a).ajaxSubmit({
                    success: function(a) {
                        e("#contact-content").slideUp(600, function() {
                            e("#contact-content").html(a).slideDown(600)
                        })
                    }
                }), !1
            }
        })
    }

    function t() {
        {
            var a = e(".navigation"),
                t = 0,
                i = a.data("menu-type"),
                s = window.innerWidth;
            e(".minicart-wrap")
        }
        i >= s && (t = 1, e("header.header").prependTo("body"), e("body").prepend('<div class="menu-mobile"></div>'), a.appendTo(".menu-mobile"), e(".open-menu-mobile").show().before(e(".minicart-wrap"))), e(window).resize(function() {
            {
                var a = e(".navigation"),
                    i = a.data("menu-type"),
                    s = window.innerWidth;
                e(".minicart-wrap")
            }
            i >= s && !t && (t = 1, e("header.header").prependTo("body"), e("body").prepend('<div class="menu-mobile"></div>'), a.appendTo(".menu-mobile"), e(".open-menu-mobile").show().before(e(".minicart-wrap"))), s > i && t && (t = 0, e("header.header").prependTo("#page-wrap"), e(".menu-mobile").remove(), a.appendTo("header.header .container"), e(".navigation .nav").after(e(".minicart-wrap")), e(".open-menu-mobile").hide())
        });
        var l = e(window).height(),
            n = l - e("header.header").height();
        e(".home-fullscreen").height(n), e(".onepage .home-fullscreen").height(l), p.any() || e(window).on("scroll", function() {
            var a = e(window).scrollTop(),
                t = e(window).height() - 100;
            a > 0 && t >= a ? e(".onepage").closest("body").find("header.header").addClass("header-anim") : e(".onepage").closest("body").find("header.header").removeClass("header-anim")
        });
        var r = e(".nav .menu-item-has-children");
        e("html").on("click", function() {
            e("#page-wrap, .header").removeClass("toggle-translate"), e(".open-menu-mobile").removeClass("open-menu-active"), e(".menu-mobile").removeClass("fixSfr"), setTimeout(function() {
                i >= s && (e("html, body").removeClass("overflow-hidden"), e(".menu-mobile").removeClass("overflow-auto"), r.children(".plus").removeClass("plus-active").siblings(".sub-menu").slideUp())
            }, 290)
        }), e(".open-menu-mobile").on("click", function() {
            e("#page-wrap, .header").toggleClass("toggle-translate"), e(this).toggleClass("open-menu-active"), e(".menu-mobile").toggleClass("fixSfr"), setTimeout(function() {
                i >= s && (e("html, body").toggleClass("overflow-hidden"), e(".menu-mobile").toggleClass("overflow-auto"), r.children(".plus").removeClass("plus-active").siblings(".sub-menu").slideUp())
            }, 290)
        }), e(".navigation, .open-menu-mobile").on("click", function(e) {
            e.stopPropagation()
        }), r.prepend('<span class="plus"><span>+</span></span>'), r.on("click", "> .plus", function() {
            0 == e(this).hasClass("plus-active") && e(this).parent().siblings().children(".plus").removeClass("plus-active").siblings(".sub-menu").slideUp(300), e(this).toggleClass("plus-active").siblings(".sub-menu").slideToggle(300)
        }), e(".onepage").find(".nav > li").on("click", "> a", function(a) {
            var t = e(this);
            e("html, body").stop().animate({
                scrollTop: e(t.attr("href")).offset().top
            }, 800, "easeInOutExpo"), setTimeout(function() {
                e("#page-wrap, .header").removeClass("toggle-translate"), e(".open-menu-mobile").removeClass("open-menu-active"), e(".menu-mobile").removeClass("fixSfr"), setTimeout(function() {
                    e("html, body").removeClass("overflow-hidden"), e(".menu-mobile").removeClass("overflow-auto"), e(".menu-mobile .nav .menu-item-has-children").children(".plus").removeClass("plus-active").siblings(".sub-menu").slideUp()
                }, 290)
            }, 700), a.preventDefault()
        })
    }

    function i() {
        var a = e(window).height(),
            t = e("header.header").height(),
            i = a - t,
            s = e(".home-fixheight").height();
        e(".home-fullscreen, .home-fullscreen .image-wrap, .home-fullscreen .home-slider").height(i), e(".onepage .home-fullscreen, .onepage .home-fullscreen .image-wrap, .onepage .home-fullscreen .home-slider").height(a), e(".home-fixheight .image-wrap, .home-fixheight .home-slider").height(s)
    }

    function s() {
        if (e("#map").length) {
            var a, t = e("#map"),
                i = t.data("map-zoom"),
                s = t.data("map-latlng").split(",")[0],
                l = t.data("map-latlng").split(",")[1],
                n = t.data("map-marker"),
                r = parseInt(t.data("map-marker-size").split("*")[0]),
                o = parseInt(t.data("map-marker-size").split("*")[1]),
                m = [{
                    featureType: "all",
                    stylers: [{
                        saturation: -100
                    }, {
                        gamma: .5
                    }]
                }],
                d = [{
                    featureType: "all",
                    stylers: [{
                        hue: "#0000b0"
                    }, {
                        invert_lightness: "true"
                    }, {
                        saturation: -30
                    }]
                }],
                g = [{
                    featureType: "all",
                    stylers: [{
                        hue: "#ff1a00"
                    }, {
                        invert_lightness: !0
                    }, {
                        saturation: -100
                    }, {
                        lightness: 33
                    }, {
                        gamma: .5
                    }]
                }],
                c = [{
                    stylers: [{
                        hue: "#ff61a6"
                    }, {
                        visibility: "on"
                    }, {
                        invert_lightness: !0
                    }, {
                        saturation: 40
                    }, {
                        lightness: 10
                    }]
                }],
                u = [{
                    featureType: "water",
                    elementType: "all",
                    stylers: [{
                        hue: "#e9ebed"
                    }, {
                        saturation: -78
                    }, {
                        lightness: 67
                    }, {
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "landscape",
                    elementType: "all",
                    stylers: [{
                        hue: "#ffffff"
                    }, {
                        saturation: -100
                    }, {
                        lightness: 100
                    }, {
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "road",
                    elementType: "geometry",
                    stylers: [{
                        hue: "#bbc0c4"
                    }, {
                        saturation: -93
                    }, {
                        lightness: 31
                    }, {
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "poi",
                    elementType: "all",
                    stylers: [{
                        hue: "#ffffff"
                    }, {
                        saturation: -100
                    }, {
                        lightness: 100
                    }, {
                        visibility: "off"
                    }]
                }, {
                    featureType: "road.local",
                    elementType: "geometry",
                    stylers: [{
                        hue: "#e9ebed"
                    }, {
                        saturation: -90
                    }, {
                        lightness: -8
                    }, {
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "transit",
                    elementType: "all",
                    stylers: [{
                        hue: "#e9ebed"
                    }, {
                        saturation: 10
                    }, {
                        lightness: 69
                    }, {
                        visibility: "on"
                    }]
                }, {
                    featureType: "administrative.locality",
                    elementType: "all",
                    stylers: [{
                        hue: "#2c2e33"
                    }, {
                        saturation: 7
                    }, {
                        lightness: 19
                    }, {
                        visibility: "on"
                    }]
                }, {
                    featureType: "road",
                    elementType: "labels",
                    stylers: [{
                        hue: "#bbc0c4"
                    }, {
                        saturation: -93
                    }, {
                        lightness: 31
                    }, {
                        visibility: "on"
                    }]
                }, {
                    featureType: "road.arterial",
                    elementType: "labels",
                    stylers: [{
                        hue: "#bbc0c4"
                    }, {
                        saturation: -93
                    }, {
                        lightness: -2
                    }, {
                        visibility: "simplified"
                    }]
                }],
                f = [{
                    featureType: "landscape.natural",
                    elementType: "geometry.fill",
                    stylers: [{
                        visibility: "on"
                    }, {
                        color: "#e0efef"
                    }]
                }, {
                    featureType: "poi",
                    elementType: "geometry.fill",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#1900ff"
                    }, {
                        color: "#c0e8e8"
                    }]
                }, {
                    featureType: "landscape.man_made",
                    elementType: "geometry.fill"
                }, {
                    featureType: "road",
                    elementType: "geometry",
                    stylers: [{
                        lightness: 100
                    }, {
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "road",
                    elementType: "labels",
                    stylers: [{
                        visibility: "off"
                    }]
                }, {
                    featureType: "water",
                    stylers: [{
                        color: "#7dcdcd"
                    }]
                }, {
                    featureType: "transit.line",
                    elementType: "geometry",
                    stylers: [{
                        visibility: "on"
                    }, {
                        lightness: 700
                    }]
                }],
                h = [{
                    featureType: "landscape",
                    stylers: [{
                        hue: "#F1FF00"
                    }, {
                        saturation: -27.4
                    }, {
                        lightness: 9.4
                    }, {
                        gamma: 1
                    }]
                }, {
                    featureType: "road.highway",
                    stylers: [{
                        hue: "#0099FF"
                    }, {
                        saturation: -20
                    }, {
                        lightness: 36.4
                    }, {
                        gamma: 1
                    }]
                }, {
                    featureType: "road.arterial",
                    stylers: [{
                        hue: "#00FF4F"
                    }, {
                        saturation: 0
                    }, {
                        lightness: 0
                    }, {
                        gamma: 1
                    }]
                }, {
                    featureType: "road.local",
                    stylers: [{
                        hue: "#FFB300"
                    }, {
                        saturation: -38
                    }, {
                        lightness: 11.2
                    }, {
                        gamma: 1
                    }]
                }, {
                    featureType: "water",
                    stylers: [{
                        hue: "#00B6FF"
                    }, {
                        saturation: 4.2
                    }, {
                        lightness: -63.4
                    }, {
                        gamma: 1
                    }]
                }, {
                    featureType: "poi",
                    stylers: [{
                        hue: "#9FFF00"
                    }, {
                        saturation: 0
                    }, {
                        lightness: 0
                    }, {
                        gamma: 1
                    }]
                }],
                y = [{
                    featureType: "administrative",
                    stylers: [{
                        visibility: "off"
                    }]
                }, {
                    featureType: "poi",
                    stylers: [{
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "road",
                    elementType: "labels",
                    stylers: [{
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "water",
                    stylers: [{
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "transit",
                    stylers: [{
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "landscape",
                    stylers: [{
                        visibility: "simplified"
                    }]
                }, {
                    featureType: "road.highway",
                    stylers: [{
                        visibility: "off"
                    }]
                }, {
                    featureType: "road.local",
                    stylers: [{
                        visibility: "on"
                    }]
                }, {
                    featureType: "road.highway",
                    elementType: "geometry",
                    stylers: [{
                        visibility: "on"
                    }]
                }, {
                    featureType: "water",
                    stylers: [{
                        color: "#84afa3"
                    }, {
                        lightness: 52
                    }]
                }, {
                    stylers: [{
                        saturation: -17
                    }, {
                        gamma: .36
                    }]
                }, {
                    featureType: "transit.line",
                    elementType: "geometry",
                    stylers: [{
                        color: "#3f518c"
                    }]
                }],
                v = [{
                    featureType: "all",
                    elementType: "all",
                    stylers: [{
                        invert_lightness: !0
                    }, {
                        saturation: 10
                    }, {
                        lightness: 30
                    }, {
                        gamma: .5
                    }, {
                        hue: "#435158"
                    }]
                }],
                b = [{
                    stylers: [{
                        hue: "#ff8800"
                    }, {
                        gamma: .4
                    }]
                }];
            switch (t.data("snazzy-map-theme")) {
                case "grayscale":
                    a = m;
                    break;
                case "blue":
                    a = d;
                    break;
                case "dark":
                    a = g;
                    break;
                case "pink":
                    a = c;
                    break;
                case "light":
                    a = u;
                    break;
                case "blue-essence":
                    a = f;
                    break;
                case "bentley":
                    a = h;
                    break;
                case "retro":
                    a = y;
                    break;
                case "cobalt":
                    a = v;
                    break;
                case "brownie":
                    a = b;
                    break;
                default:
                    a = m
            }
            if (p.any()) var w = !1;
            else var w = !0;
            var T = "custom_style",
                x = a,
                C = new google.maps.LatLng(s, l),
                k = {
                    zoom: i,
                    center: C,
                    mapTypeControlOptions: {
                        mapTypeIds: [google.maps.MapTypeId.ROADMAP, T]
                    },
                    mapTypeControl: !1,
                    mapTypeId: T,
                    scrollwheel: !1,
                    draggable: w
                }
                // S = new google.maps.Map(document.getElementById("map"), k),
                // P = {
                //     name: "Custom Style"
                // },
            //     I = new google.maps.StyledMapType(x, P);
            // S.mapTypes.set(T, I), google.maps.event.addDomListener(window, "resize", function() {
            //     var e = S.getCenter();
            //     google.maps.event.trigger(S, "resize"), S.setCenter(e)
            // });
            // {
                // var z = new google.maps.MarkerImage(n, new google.maps.Size(r, o), new google.maps.Point(0, 0)),
                //     A = new google.maps.LatLng(s, l);
                // new google.maps.Marker({
                //     position: A,
                //     map: S,
                //     icon: z,
                //     title: "Road",
                //     zIndex: 3
                // })
            // }
        }
    }

    function l() {
        e(".blog-grid").length && e(".blog-grid").masonry({
            columnWidth: ".grid-sizer",
            itemSelector: ".post"
        })
    }

    function n() {
        e.each(e(".awe-btn"), function() {
            var a = e(this).attr("class");
            e(this).wrap('<div class="' + a + '"></div>').removeClass()
        })
    }

    function r() {
        var a = e(".event-pager-scroll").width() / 4;
        if (window.innerWidth <= 480) var a = e(".event-pager-scroll").width() / 2;
        var t = e(".event-pager a"),
            i = t.length,
            s = i * a;
        t.css("width", a), e(".event-pager").css({
            width: s
        })
    }

    function o() {
        e.each(e(".divider"), function() {
            var a = e(this).css("color"),
                t = a,
                i = '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="16px" height="8 px" viewBox="0 0 96.166 48.083" enable-background="new 0 0 96.166 48.083" xml:space="preserve"><polyline fill="' + t + '" points="0,48.083 48.083,0 96.166,48.083 "/></svg>',
                s = window.btoa(i);
            e(this).css({
                "background-image": "url(data:image/svg+xml;base64," + s + ")"
            })
        })
    }

    function m() {
        e(".awe-parallax").length && (p.any() || (e(".home-media .awe-parallax").parallax("50%", .1), e(".our-story .awe-parallax").parallax("50%", .1), e(".the-menu .awe-parallax").parallax("50%", .1), e(".the-staff .awe-parallax").parallax("50%", .1), e(".events .awe-parallax").parallax("50%", .1), e(".testimonial .awe-parallax").parallax("50%", .1), e(".sub-banner .awe-parallax").parallax("50%", .1)))
    }
    var p = {
            Android: function() {
                return navigator.userAgent.match(/Android/i)
            },
            BlackBerry: function() {
                return navigator.userAgent.match(/BlackBerry/i)
            },
            iOS: function() {
                return navigator.userAgent.match(/iPhone|iPad|iPod/i)
            },
            Opera: function() {
                return navigator.userAgent.match(/Opera Mini/i)
            },
            Windows: function() {
                return navigator.userAgent.match(/IEMobile/i)
            },
            any: function() {
                return p.Android() || p.BlackBerry() || p.iOS() || p.Opera() || p.Windows()
            }
        },
        d = function() {
            for (var e, a = 3, t = document.createElement("div"), i = t.getElementsByTagName("i"); t.innerHTML = "<!--[if gt IE " + ++a + "]><i></i><![endif]-->", i[0];);
            var s = a > 4 ? a : e;
            return s ? s > 9 && o() : o(), a > 4 ? a : e
        };
    e(document).ready(function() {
        a();
        d();

        $(document).ready(function() {
            console.log('doc loaded');
            // e('.preloader').addClass("load-anim");
            n(), l(), i(), m(), e(".preloader").addClass("load-anim");
            var a = e(".event-pager-scroll").outerHeight();
            e(".event-pager-scroll").css("margin-top", -a + 50)
        }), e(window).on("resize", function() {
            i(), r()
        })
    })
}(jQuery);

console.log('sk');