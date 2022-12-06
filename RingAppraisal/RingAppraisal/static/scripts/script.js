$(document).ready(function () {
    fetch("./static/data/data.json").then(data => {
        return data.json()
    }).then(data => {
        // hide primary dropdowns
        $(".primary-property-radio").hide()

        // hide secondary dropdowns
        $(".secondary-property-checkbox").hide();
    });

    $('form').bind('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch('/data', {
            method: 'POST',
            body: formData,
        }).then((data) => data.json())
            .then((jsonData) => $('#price').html('&nbsp;$' + jsonData.price));
    })
})

function ChangePrimaryDropdowns(tag) {
    $(".primary-property-radio").hide()
    $(".primary-property-" + tag.value + "-radio").show()
}

function ChangeSecondaryDropdowns(tag) {
    if ($(tag).is(":checked")) {
        $(".secondary-property-" + tag.value + "-checkbox").show()
    }
    else {
        $(".secondary-property-" + tag.value + "-checkbox").hide()
    }
}

