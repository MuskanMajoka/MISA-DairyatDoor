// status.js

$(document).ready(function() {
    // Initially hide all order containers
    $(".order-container").hide();

    // Show requests with statuses other than 'Delivered'
    $(".order-container:not(.status-delivered)").show();

    $(".status-tab").on("click", function() {
        var status = $(this).data("status");
        $(".order-container").hide();

        if (status === "requests") {
            $(".order-container:not(.status-delivered)").show();
        } else {
            $(".order-container.status-" + status).show();
        }
    });

    $(".details-button").on("click", function() {
        $(this).siblings(".order-details").toggle();
    });
});
