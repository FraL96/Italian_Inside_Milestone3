$(document).ready(function () {
    //sidenav
    $('.sidenav').sidenav({
        edge: "right"
    });
    //collapsible
    $('.collapsible').collapsible();
    //tooltip  - all recipes
    $('.tooltipped').tooltip();
    //dropdown options - add/edit recipes
    $('select').formSelect();
    //modal
    $('.modal').modal();
    //code copied from Mini Project - Task Manager from Code Institute - used to modify a Materialize class
    validateMaterializeSelect();

    function validateMaterializeSelect() {
        let classValid = {
            "border-bottom": "1px solid #4caf50",
            "box-shadow": "0 1px 0 0 #4caf50"
        };
        let classInvalid = {
            "border-bottom": "1px solid #f44336",
            "box-shadow": "0 1px 0 0 #f44336"
        };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({
                "display": "block",
                "height": "0",
                "padding": "0",
                "width": "0",
                "position": "absolute"
            });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
    //tooltips - Italy map
    var tooltipsmall = ['#Valle-d-Aosta', '#Molise', '#Liguria', '#Piemonte', '#Lombardia', '#Trentino-Alto-Adige', '#Veneto',
        '#Umbria', '#Lazio', '#Sicilia', '#Sardegna', '#Calabria', '#Campania', '#Basilicata', '#Toscana', '#Abruzzo', '#Friuli-Venezia-Giulia', '#Marche', '#Emilia-Romagna', '#Puglia'
    ];

    $(tooltipsmall).qtip({
        content: function () {
            return $(this).data('tooltip'); //store data in data-tooltip
        },
        position: {
            my: 'bottom center', // Position my top left...
            at: 'top center', // at the bottom right of...
            adjust: {
                y: 10
            }
        },
        style: {
            tip: {
                corner: true,
                border: 1,
                width: 15,
                height: 7
            }
        }
    });
});