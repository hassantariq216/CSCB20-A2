//api source: https://jqueryui.com/accordion/
$(function () {
    $(".table_grid")
        .accordion({
            header: "> .table_item_wide"
        })
        .sortable({
            axis: "y",
            handle: ".table_item_wide",
            stop: function (event, ui) {
                // IE doesn't register the blur when sorting
                // so trigger focusout handlers to remove .ui-state-focus
                ui.item.children(".table_item_wide").triggerHandler("focusout");

                // Refresh accordion to handle new order
                $(this).accordion("refresh");
            }
        });
});