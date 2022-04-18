$(document).ready(function () {
    d3.json("./static/scripts/constants.json").then((data) => {
        data = data[0]

        $(".primary-property-radio").hide()
        for (const val in data.primary_stone) {
            const valDict = data.primary_stone[val];
            $("#primary-" + val + "-radio").change(function () {
                $(".primary-property-radio").hide()
                if ($(this).is(":checked")) {
                    if (Object.keys(valDict).length !== 0) {
                        for (const prop in valDict) {
                            $("#primary-" + val + "-" + prop + "-dropdown").show();
                        }
                    }
                }
            })
        }

        $(".secondary-property-checkbox").hide();
        for (const val in data.secondary_stones) {
            const valDict = data.secondary_stones[val];
            if (Object.keys(valDict).length !== 0) {
                const idVal = val.replaceAll(" ", "-")
                for (const prop in valDict) {
                    $("#secondary-" + idVal + "-checkbox").change(function () {
                        if ($(this).is(":checked")) {
                            $("#secondary-" + idVal + "-" + prop + "-dropdown").show();
                        } else {
                            $("#secondary-" + idVal + "-" + prop + "-dropdown").hide();
                        }
                    })
                }
            }
        }
    });
})
